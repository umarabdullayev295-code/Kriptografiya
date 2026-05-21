# Kriptografik Kalitlar Menedjer

Kriptografik kalitlarni xavfsiz saqlash va boshqarish uchun Python-da yozilgan professional kalitlar menedjer.

## Xususiyatlari

- 🔐 **Xavfsiz Shifrlash**: Fernet (AES-128) shifrlashdan foydalanadi
- 🔑 **Master Parol**: PBKDF2 algoritmi bilan master paroldan kalit yaratish
- 💾 **JSON Saqlash**: Kalitlarni JSON formatida saqlash
- 📝 **Metadata**: Har bir kalit uchun qo'shimcha ma'lumot saqlash
- 🔄 **Yangilash**: Mavjud kalitlarni yangilash imkoniyati
- 📤 **Eksport**: Barcha kalitlarni eksport qilish
- 🗑️ **O'chirish**: Kalitlarni xavfsiz o'chirish

## O'rnatish

```bash
pip install -r requirements.txt
```

## Foydalanish

### Asosiy Misol

```python
import os
from key_manager import KeyManager

# Master parolni o'rnating
os.environ["MASTER_PASSWORD"] = "your_secure_password"

# KeyManager-ni yaratish
manager = KeyManager()

# Kalitni saqlash
manager.save_key("api_key", "sk_live_abc123", {"service": "stripe"})

# Kalitni olish
api_key = manager.get_key("api_key")
print(api_key)  # sk_live_abc123

# Barcha kalitlarni ko'rish
keys = manager.list_keys()
for key in keys:
    print(f"- {key['name']}")

# Kalitni yangilash
manager.update_key("api_key", "sk_live_new_key")

# Kalitni o'chirish
manager.delete_key("api_key")

# Kalitlarni eksport qilish
manager.export_keys("backup.json")
```

## API Dokumentatsiyasi

### KeyManager Sinfi

#### `__init__(storage_path=".keys", master_password=None)`
KeyManager-ni ishga tushirish.

**Parametrlar:**
- `storage_path` (str): Kalitlarni saqlash uchun papka yo'li
- `master_password` (str): Asosiy parol (agar None bo'lsa, MASTER_PASSWORD muhit o'zgaruvchisidan olinadi)

#### `save_key(key_name, key_value, metadata=None)`
Kalitni xavfsiz saqlash.

**Parametrlar:**
- `key_name` (str): Kalitning nomi
- `key_value` (str): Kalitning qiymati
- `metadata` (dict): Qo'shimcha ma'lumot (ixtiyoriy)

**Qaytaradi:** bool - Muvaffaqiyat holati

#### `get_key(key_name)`
Kalitni olish va shifrlashni ochish.

**Parametrlar:**
- `key_name` (str): Kalitning nomi

**Qaytaradi:** str yoki None - Kalitning qiymati yoki None

#### `delete_key(key_name)`
Kalitni o'chirish.

**Parametrlar:**
- `key_name` (str): Kalitning nomi

**Qaytaradi:** bool - Muvaffaqiyat holati

#### `list_keys()`
Barcha saqlangan kalitlarning nomlarini olish.

**Qaytaradi:** list - Kalitlar ro'yxati

#### `update_key(key_name, new_value)`
Mavjud kalitni yangilash.

**Parametrlar:**
- `key_name` (str): Kalitning nomi
- `new_value` (str): Yangi qiymat

**Qaytaradi:** bool - Muvaffaqiyat holati

#### `export_keys(export_path)`
Barcha kalitlarni eksport qilish (shifrlangan holda).

**Parametrlar:**
- `export_path` (str): Eksport fayli yo'li

**Qaytaradi:** bool - Muvaffaqiyat holati

## Xavfsizlik Tavsiyalari

1. **Master Parol**: Kuchli master parol ishlating (kamida 16 ta belgi)
2. **Muhit O'zgaruvchisi**: Master parolni kod ichida yozmayin, muhit o'zgaruvchisidan foydalaning
3. **Fayl Ruxsatlari**: `.keys` papkasining ruxsatlarini cheklang
4. **Backup**: Kalitlarni xavfsiz joyda zaxiralang
5. **Parol Boshqarish**: Master parolni doimiy o'zgartiring

## Testlar

Testlarni ishga tushirish:

```bash
python -m pytest test_key_manager.py -v
```

yoki

```bash
python test_key_manager.py
```

## Litsenziya

MIT License

## Muallif

Kriptografik Kalitlar Menedjer - 2024
