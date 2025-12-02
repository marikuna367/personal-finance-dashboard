# 
import requests
from typing import List, Dict, Any, Optional

class MockBankClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # Accounts
    def list_accounts(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/accounts"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_account(self, provider_account_id: int) -> Dict[str, Any]:
        url = f"{self.base_url}/accounts/{provider_account_id}"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def create_account(self, name: str, type_: str = "checking", balance: float = 0.0) -> Dict[str, Any]:
        url = f"{self.base_url}/accounts"
        payload = {"name": name, "type": type_, "balance": balance}
        r = requests.post(url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # Transactions
    def list_transactions(self, account_id: Optional[int] = None) -> List[Dict[str, Any]]:
        #
        url = f"{self.base_url}/transactions"
        params = {}
        if account_id is not None:
            params["account_id"] = account_id
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def create_transaction(self, account_id: int, amount: float, category: str, description: str) -> Dict[str, Any]:
        url = f"{self.base_url}/transactions"
        payload = {
            "account_id": account_id,
            "amount": amount,
            "category": category,
            "description": description
        }
        r = requests.post(url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()
