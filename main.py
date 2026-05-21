from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
from key_manager import KeyManager

app = FastAPI(title="Key Manager API", description="Render.com da ishlaydigan Key Manager Web Serveri")

# Helper function to get KeyManager instance
def get_key_manager():
    # Render.com will pass environment variables like MASTER_PASSWORD
    master_password = os.getenv("MASTER_PASSWORD", "default_secure_password_for_render_123")
    os.environ["MASTER_PASSWORD"] = master_password
    return KeyManager()

from pydantic import BaseModel, Field

class KeyCreate(BaseModel):
    name: str = Field(..., pattern="^[a-zA-Z0-9_-]+$", description="Faqat harf, raqam, tagchiziq va chiziqcha")
    value: str = Field(..., min_length=1, description="Bo'sh bo'lishi mumkin emas")
    metadata: Optional[Dict[str, Any]] = None

class KeyUpdate(BaseModel):
    value: str = Field(..., min_length=1, description="Bo'sh bo'lishi mumkin emas")

@app.get("/")
def read_root():
    return {"message": "Key Manager API is running on Render.com!"}

@app.post("/keys/")
def save_key(key_data: KeyCreate):
    manager = get_key_manager()
    success = manager.save_key(key_data.name, key_data.value, key_data.metadata)
    if not success:
        raise HTTPException(status_code=500, detail="Kalitni saqlashda xatolik yuz berdi")
    return {"message": f"'{key_data.name}' kaliti muvaffaqiyatli saqlandi"}

@app.get("/keys/{key_name}")
def get_key(key_name: str):
    manager = get_key_manager()
    value = manager.get_key(key_name)
    if value is None:
        raise HTTPException(status_code=404, detail="Kalit topilmadi")
    return {"name": key_name, "value": value}

@app.get("/keys/")
def list_keys():
    manager = get_key_manager()
    return {"keys": manager.list_keys()}

@app.put("/keys/{key_name}")
def update_key(key_name: str, key_data: KeyUpdate):
    manager = get_key_manager()
    success = manager.update_key(key_name, key_data.value)
    if not success:
        raise HTTPException(status_code=404, detail="Kalit topilmadi yoki yangilashda xatolik")
    return {"message": f"'{key_name}' kaliti muvaffaqiyatli yangilandi"}

@app.delete("/keys/{key_name}")
def delete_key(key_name: str):
    manager = get_key_manager()
    success = manager.delete_key(key_name)
    if not success:
        raise HTTPException(status_code=404, detail="Kalit topilmadi yoki o'chirishda xatolik")
    return {"message": f"'{key_name}' kaliti muvaffaqiyatli o'chirildi"}

@app.get("/export/")
def export_keys():
    manager = get_key_manager()
    export_path = "export_backup.json"
    success = manager.export_keys(export_path)
    if not success:
        raise HTTPException(status_code=500, detail="Eksport qilishda xatolik")
    
    import json
    with open(export_path, 'r') as f:
        data = json.load(f)
    os.remove(export_path)
    return {"exported_keys": data}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
