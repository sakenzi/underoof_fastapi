import re


def normalize_phone(phone: str) -> str:
    import re
    phone = re.sub(r'\D', '', phone)  
    if phone.startswith('8') and len(phone) == 11:
        phone = '7' + phone[1:]  
    if not phone.startswith('7') or len(phone) != 11:
        raise ValueError("Неверный формат номера телефона")
    return phone