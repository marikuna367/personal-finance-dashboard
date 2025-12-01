# small HTTP client wrapper to talk to your MockBank API
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

MOCK_BANK_URL = os.getenv("MOCK_BANK_URL", "http://104.248.41.128:8000")

async def get_account_info(provider_account_id: str):
    async with httpx.AsyncClient() as client:
        url = f"{MOCK_BANK_URL}/accounts/{provider_account_id}"
        r = await client.get(url)
        r.raise_for_status()
        return r.json()

async def get_transactions(provider_account_id: str):
    async with httpx.AsyncClient() as client:
        url = f"{MOCK_BANK_URL}/accounts/{provider_account_id}/transactions"
        r = await client.get(url)
        r.raise_for_status()
        return r.json()

async def make_transfer(from_id: str, to_id: str, amount: float):
    async with httpx.AsyncClient() as client:
        url = f"{MOCK_BANK_URL}/transfer"
        payload = {"from": from_id, "to": to_id, "amount": amount}
        r = await client.post(url, json=payload)
        r.raise_for_status()
        return r.json()
