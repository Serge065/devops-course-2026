def validate_phone(phone: str) -> bool:
    """Валидация российского номера телефона."""
    import re
    pattern = r'^\+?7\d{10}$'
    return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))

def validate_inn(inn: str) -> bool:
    """TODO: валидация ИНН."""
    pass