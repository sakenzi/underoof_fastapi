import requests
import os
from dotenv import load_dotenv


load_dotenv()

P1SMS_API_KEY = os.getenv("P1SMS_API_KEY")

def send_sms(to_number: str, message: str) -> bool:
    url = "https://admin.p1sms.kz/apiSms/create"
    headers = {"Content-Type": "application/json"}

    # phone = to_number.replace("+", "")
    # if phone.startswith("8"):
    #     phone = "7" + phone[1:]

    payload = {
        "apiKey": P1SMS_API_KEY,
        "sms": [
            {
                "channel": "digit",
                "text": message,
                "phone": to_number,
                "plannedAt": 0  
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        print("P1SMS response:", result)  
        return result.get("status") == "success"
    except Exception as e:
        print("Ошибка при отправке SMS:", e)
        return False