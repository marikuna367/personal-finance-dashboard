import os
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import uuid

load_dotenv()

# External bank provider URL (e.g., Plaid, a mock bank service, etc.)
# If not set or set to own backend, use local mock data
EXTERNAL_BANK_URL = os.getenv("EXTERNAL_BANK_URL", "").rstrip("/")


def _generate_mock_transactions(provider_account_id: str) -> List[Dict[str, Any]]:
    """Generate mock transactions for local development when no external provider is available"""
    categories = [
        "Groceries",
        "Dining",
        "Transportation",
        "Entertainment",
        "Utilities",
        "Shopping",
        "Income",
    ]
    descriptions = {
        "Groceries": ["Whole Foods", "Trader Joe's", "Costco", "Safeway"],
        "Dining": ["Starbucks", "Chipotle", "Local Restaurant", "Pizza Hut"],
        "Transportation": ["Uber", "Gas Station", "Parking", "Metro Card"],
        "Entertainment": ["Netflix", "Spotify", "Movie Theater", "Concert Tickets"],
        "Utilities": ["Electric Bill", "Water Bill", "Internet", "Phone Bill"],
        "Shopping": ["Amazon", "Target", "Best Buy", "Nike"],
        "Income": ["Paycheck", "Freelance Payment", "Refund", "Transfer In"],
    }

    transactions = []
    base_date = datetime.utcnow()

    for i in range(5):
        cat = random.choice(categories)
        is_income = cat == "Income"
        amount = round(
            random.uniform(100, 2000) if is_income else -random.uniform(10, 200), 2
        )

        transactions.append(
            {
                "id": f"mock_{provider_account_id}_{uuid.uuid4().hex[:8]}",
                "account_id": provider_account_id,
                "amount": amount,
                "category": cat,
                "description": random.choice(descriptions[cat]),
                "date": (base_date - timedelta(days=random.randint(1, 30))).isoformat(),
            }
        )

    return transactions


async def get_account_info(provider_account_id: str) -> Dict[str, Any]:
    if not EXTERNAL_BANK_URL:
        # Return mock data for local development
        return {
            "id": provider_account_id,
            "name": f"Account {provider_account_id}",
            "balance": round(random.uniform(1000, 10000), 2),
        }

    async with httpx.AsyncClient(base_url=EXTERNAL_BANK_URL, timeout=10.0) as client:
        r = await client.get(f"/accounts/{provider_account_id}")
        r.raise_for_status()
        return r.json()


async def get_transactions(
    provider_account_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    if not EXTERNAL_BANK_URL:
        # Return mock transactions for local development
        return _generate_mock_transactions(provider_account_id or "1")

    params = {}
    if provider_account_id is not None:
        params["account_id"] = provider_account_id
    async with httpx.AsyncClient(base_url=EXTERNAL_BANK_URL, timeout=10.0) as client:
        r = await client.get("/transactions", params=params)
        r.raise_for_status()
        return r.json()


async def list_accounts() -> List[Dict[str, Any]]:
    if not EXTERNAL_BANK_URL:
        # Return mock accounts for local development
        return [
            {"id": "1", "name": "Mock Checking", "balance": 5432.10},
            {"id": "2", "name": "Mock Savings", "balance": 12500.00},
        ]

    async with httpx.AsyncClient(base_url=EXTERNAL_BANK_URL, timeout=10.0) as client:
        r = await client.get("/accounts")
        r.raise_for_status()
        return r.json()


async def create_transaction(
    account_id: int, amount: float, category: str, description: str
) -> Dict[str, Any]:
    if not EXTERNAL_BANK_URL:
        # Return mock response for local development
        return {
            "id": f"mock_{uuid.uuid4().hex[:8]}",
            "account_id": account_id,
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.utcnow().isoformat(),
        }

    payload = {
        "account_id": account_id,
        "amount": amount,
        "category": category,
        "description": description,
    }
    async with httpx.AsyncClient(base_url=EXTERNAL_BANK_URL, timeout=10.0) as client:
        r = await client.post("/transactions", json=payload)
        r.raise_for_status()
        return r.json()
