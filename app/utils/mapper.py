# app/utils/mapper.py
# small helper functions (placeholder for future)
def safe_get(d: dict, key: str, default=None):
    return d.get(key, default) if isinstance(d, dict) else default
