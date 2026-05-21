import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import base64
import hashlib
from cryptography.fernet import Fernet


class KeyManager:
    
    def __init__(self, storage_path: str = ".keys", master_password: str = None):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        if master_password is None:
            master_password = os.getenv("MASTER_PASSWORD")
            if not master_password:
                raise ValueError("Master parol kerak. MASTER_PASSWORD muhit o'zgaruvchisini o'rnating.")
        
        self.master_password = master_password
        self._cipher = self._create_cipher()
    
    def _create_cipher(self) -> Fernet:
        hash_obj = hashlib.sha256(self.master_password.encode())
        key = base64.urlsafe_b64encode(hash_obj.digest())
        return Fernet(key)
    
    def save_key(self, key_name: str, key_value: str, metadata: Dict[str, Any] = None) -> bool:
        try:
            encrypted_value = self._cipher.encrypt(key_value.encode())
            
            key_data = {
                "name": key_name,
                "encrypted_value": encrypted_value.decode(),
                "created_at": self._get_timestamp(),
                "metadata": metadata or {}
            }
            
            file_path = self.storage_path / f"{key_name}.json"
            with open(file_path, 'w') as f:
                json.dump(key_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Xato: Kalitni saqlashda muammo - {e}")
            return False
    
    def get_key(self, key_name: str) -> Optional[str]:
        try:
            file_path = self.storage_path / f"{key_name}.json"
            
            if not file_path.exists():
                print(f"Xato: '{key_name}' kaliti topilmadi")
                return None
            
            with open(file_path, 'r') as f:
                key_data = json.load(f)
            
            encrypted_value = key_data["encrypted_value"].encode()
            decrypted_value = self._cipher.decrypt(encrypted_value).decode()
            
            return decrypted_value
        except Exception as e:
            print(f"Xato: Kalitni olishda muammo - {e}")
            return None
    
    def delete_key(self, key_name: str) -> bool:
        try:
            file_path = self.storage_path / f"{key_name}.json"
            
            if file_path.exists():
                file_path.unlink()
                return True
            else:
                print(f"Xato: '{key_name}' kaliti topilmadi")
                return False
        except Exception as e:
            print(f"Xato: Kalitni o'chirishda muammo - {e}")
            return False
    
    def list_keys(self) -> list:
        try:
            keys = []
            for file_path in self.storage_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    key_data = json.load(f)
                    keys.append({
                        "name": key_data["name"],
                        "created_at": key_data["created_at"],
                        "metadata": key_data.get("metadata", {})
                    })
            return keys
        except Exception as e:
            print(f"Xato: Kalitlarni ro'yxatini olishda muammo - {e}")
            return []
    
    def update_key(self, key_name: str, new_value: str) -> bool:
        try:
            file_path = self.storage_path / f"{key_name}.json"
            
            if not file_path.exists():
                print(f"Xato: '{key_name}' kaliti topilmadi")
                return False
            
            with open(file_path, 'r') as f:
                key_data = json.load(f)
            
            encrypted_value = self._cipher.encrypt(new_value.encode())
            key_data["encrypted_value"] = encrypted_value.decode()
            key_data["updated_at"] = self._get_timestamp()
            
            with open(file_path, 'w') as f:
                json.dump(key_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Xato: Kalitni yangilashda muammo - {e}")
            return False
    
    def export_keys(self, export_path: str) -> bool:
        try:
            keys_data = []
            for file_path in self.storage_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    keys_data.append(json.load(f))
            
            with open(export_path, 'w') as f:
                json.dump(keys_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Xato: Kalitlarni eksport qilishda muammo - {e}")
            return False
    
    @staticmethod
    def _get_timestamp() -> str:
        return datetime.now().isoformat()


if __name__ == "__main__":
    os.environ["MASTER_PASSWORD"] = "my_secure_master_password_123"
    
    manager = KeyManager()
    
    print("=== Kalitlarni saqlash ===")
    manager.save_key("api_key", "sk_live_abc123xyz", {"service": "stripe"})
    manager.save_key("db_password", "secure_db_pass_456", {"service": "postgresql"})
    manager.save_key("jwt_secret", "jwt_secret_key_789", {"service": "auth"})
    print("Kalitlar saqlandi")
    
    print("\n=== Kalitlarni olish ===")
    api_key = manager.get_key("api_key")
    print(f"API Kaliti: {api_key}")
    
    print("\n=== Barcha kalitlar ===")
    all_keys = manager.list_keys()
    for key_info in all_keys:
        print(f"- {key_info['name']} (Yaratilgan: {key_info['created_at']})")
    
    print("\n=== Kalitni yangilash ===")
    manager.update_key("api_key", "sk_live_new_key_999")
    updated_key = manager.get_key("api_key")
    print(f"Yangilangan API Kaliti: {updated_key}")
    
    print("\n=== Kalitlarni eksport qilish ===")
    manager.export_keys("keys_backup.json")
    print("Kalitlar eksport qilindi")
    
    print("\n=== Kalitni o'chirish ===")
    manager.delete_key("jwt_secret")
    print("Kalit o'chirildi")
