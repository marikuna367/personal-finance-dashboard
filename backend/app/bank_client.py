import os
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

MOCK_BANK_URL = os.getenv("MOCK_BANK_URL", "http://localhost:8001").rstrip("/")

async def _client():
    return httpx.AsyncClient(base_url=MOCK_BANK_URL, timeout=10.0)

async def get_account_info(provider_account_id: str) -> Dict[str, Any]:
    async with httpx.AsyncClient(base_url=MOCK_BANK_URL, timeout=10.0) as client:
        r = await client.get(f"/accounts/{provider_account_id}")
        r.raise_for_status()
        return r.json()

async def get_transactions(provider_account_id: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {}
    if provider_account_id is not None:
        params["account_id"] = provider_account_id
    async with httpx.AsyncClient(base_url=MOCK_BANK_URL, timeout=10.0) as client:
        r = await client.get("/transactions", params=params)
        r.raise_for_status()
        return r.json()

async def list_accounts() -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(base_url=MOCK_BANK_URL, timeout=10.0) as client:
        r = await client.get("/accounts")
        r.raise_for_status()
        return r.json()

async def create_transaction(account_id: int, amount: float, category: str, description: str) -> Dict[str, Any]:
    payload = {
        "account_id": account_id,
        "amount": amount,
        "category": category,
        "description": description,
    }
    async with httpx.AsyncClient(base_url=MOCK_BANK_URL, timeout=10.0) as client:
        r = await client.post("/transactions", json=payload)
        r.raise_for_status()
        return r.json()
