import requests
from typing import Optional, Dict
import json

class AuthClient:
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:8000"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": api_key})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response
    
    def validate_api_key(self) -> bool:
        try:
            response = self._make_request("POST", "/auth/validate")
            return response.status_code == 200
        except Exception:
            return False
    
    def get_account(self, alias: str) -> Optional[Dict[str, str]]:
        try:
            response = self._make_request("GET", f"/accounts/{alias}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to get account '{alias}': {str(e)}")
    
    def create_account(self, alias: str, username: str, password: str) -> Dict:
        try:
            data = {
                "alias": alias,
                "username": username,
                "password": password
            }
            response = self._make_request("POST", "/accounts", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to create account '{alias}': {str(e)}")
    
    def update_account(self, alias: str, username: Optional[str] = None, password: Optional[str] = None) -> Dict:
        try:
            data = {}
            if username:
                data["username"] = username
            if password:
                data["password"] = password
            
            response = self._make_request("PUT", f"/accounts/{alias}", json=data)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise Exception(f"Account '{alias}' not found")
            else:
                response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to update account '{alias}': {str(e)}")
    
    def delete_account(self, alias: str) -> bool:
        try:
            response = self._make_request("DELETE", f"/accounts/{alias}")
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            else:
                response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to delete account '{alias}': {str(e)}")
    
    def list_accounts(self) -> list:
        try:
            response = self._make_request("GET", "/accounts")
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to list accounts: {str(e)}")

class AccountCredentials:
    def __init__(self, alias: str, username: str, password: str):
        self.alias = alias
        self.username = username
        self.password = password
    
    def __str__(self):
        return f"Account(alias={self.alias}, username={self.username})"
    
    def __repr__(self):
        return self.__str__()

class SimpleAuthClient:
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:8000"):
        self.client = AuthClient(api_key, base_url)
    
    def get_credentials(self, alias: str) -> Optional[AccountCredentials]:
        account_data = self.client.get_account(alias)
        if account_data:
            return AccountCredentials(
                alias=account_data['alias'],
                username=account_data['username'],
                password=account_data['password']
            )
        return None
    
    def is_connected(self) -> bool:
        return self.client.validate_api_key()

def create_client(api_key: str, server_url: str = "http://127.0.0.1:8000") -> SimpleAuthClient:
    return SimpleAuthClient(api_key, server_url)

if __name__ == "__main__":
    client = SimpleAuthClient("your-api-key-here")
    
    if client.is_connected():
        print("✓ API 연결 성공")
        
        credentials = client.get_credentials("example")
        if credentials:
            print(f"계정 정보: {credentials.username}")
        else:
            print("계정을 찾을 수 없습니다.")
    else:
        print("✗ API 연결 실패")