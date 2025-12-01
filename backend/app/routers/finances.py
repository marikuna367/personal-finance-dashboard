from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .. import db, models, schemas
from datetime import datetime
from ..bank_client import get_transactions, get_account_info

router = APIRouter(prefix="/finances", tags=["finances"])

# NOTE: in a real app you should require auth and use a dependency to get current user.
# For brevity this example uses a placeholder user_id=1.

@router.post('/link-account')
async def link_account(payload: schemas.BankAccountLink, user_id: int = 1):
    with Session(db.engine) as session:
        account = models.BankAccount(
            owner_id=user_id,
            provider_account_id=payload.provider_account_id,
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
            exists = session.exec(
                select(models.Transaction).where(models.Transaction.provider_txn_id == t.get('id'))
            ).first()
            if exists:
                continue

            txn = models.Transaction(
                account_id=account.id,
                provider_txn_id=t.get('id'),
                amount=t.get('amount', 0),
                date=datetime.fromisoformat(t.get('date')) if 'date' in t else datetime.utcnow(),
                description=t.get('description'),
                category=None
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
            date=txn_in.date,
            description=txn_in.description,
            category=txn_in.category
        )
        session.add(txn)
        session.commit()
        session.refresh(txn)
        return txn
