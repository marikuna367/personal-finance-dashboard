from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .. import db, models, schemas
from datetime import datetime
from ..bank_client import get_transactions, get_account_info, create_transaction as provider_create_transaction

router = APIRouter(prefix="/finances", tags=["finances"])

@router.get("/linked-accounts")
def list_linked_accounts(user_id: int = 1):
    with Session(db.engine) as session:
        accounts = session.exec(
            select(models.BankAccount).where(models.BankAccount.owner_id == user_id)
        ).all()
        return accounts

@router.post('/link-account')
async def link_account(payload: schemas.BankAccountLink, user_id: int = 1):
    with Session(db.engine) as session:
        account = models.BankAccount(
            owner_id=user_id,
            provider_account_id=str(payload.provider_account_id),
            name=payload.name or "Linked Account"
        )
        try:
            info = await get_account_info(payload.provider_account_id)
            account.balance = info.get('balance', 0)
        except Exception:
            account.balance = 0

        session.add(account)
        session.commit()
        session.refresh(account)
        return account

@router.post('/sync/{account_id}')
async def sync_account(account_id: int, user_id: int = 1):
    with Session(db.engine) as session:
        account = session.get(models.BankAccount, account_id)
        if not account:
            raise HTTPException(status_code=404, detail='Account not found')
        try:
            provider_txns = await get_transactions(account.provider_account_id)
        except Exception:
            raise HTTPException(status_code=502, detail='Failed to fetch from provider')
        added = 0
        for t in provider_txns:
            provider_id = t.get('id')
            exists = session.exec(
                select(models.Transaction).where(models.Transaction.provider_txn_id == provider_id)
            ).first()
            if exists:
                continue

            date_str = t.get('date') or t.get('timestamp') or t.get('created_at') or None
            if date_str:
                try:
                    txn_date = datetime.fromisoformat(date_str)
                except Exception:
                    try:
                        txn_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    except Exception:
                        txn_date = datetime.utcnow()
            else:
                txn_date = datetime.utcnow()
            txn = models.Transaction(
                account_id=account.id,
                provider_txn_id=provider_id,
                amount=t.get('amount', 0),
                date=txn_date,
                description=t.get('description'),
                category=t.get('category') or None
            )
            session.add(txn)
            added += 1

        session.commit()
        return {"synced": added}

@router.get('/transactions/{account_id}')
def list_txns(account_id: int):
    with Session(db.engine) as session:
        txns = session.exec(
            select(models.Transaction)
            .where(models.Transaction.account_id == account_id)
            .order_by(models.Transaction.date.desc())
        ).all()
        return txns

@router.post('/transactions/{account_id}')
def create_txn(account_id: int, txn_in: schemas.TransactionIn):
    with Session(db.engine) as session:
        txn = models.Transaction(
            account_id=account_id,
            amount=txn_in.amount,
            date=txn_in.date or datetime.utcnow(),
            description=txn_in.description,
            category=txn_in.category
        )
        session.add(txn)
        session.commit()
        session.refresh(txn)
    return txn

@router.post('/transactions')
async def create_txn_body(txn: schemas.TransactionIn):
    with Session(db.engine) as session:
        new_txn = models.Transaction(
            account_id=getattr(txn, "account_id", None),
            amount=txn.amount,
            date=txn.date or datetime.utcnow(),
            description=txn.description,
            category=txn.category
        )
        session.add(new_txn)
        session.commit()
        session.refresh(new_txn)
        try:
            await provider_create_transaction(new_txn.account_id, new_txn.amount, new_txn.category or "", new_txn.description or "")
        except Exception:
            pass
        return new_txn
