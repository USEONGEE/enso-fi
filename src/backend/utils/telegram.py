from hypurrquant.api.async_http import send_request_for_external

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def send_telegram_message(chat_id: str, message: str):
    """
    텔레그램 메시지를 보내는 함수
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    await send_request_for_external("POST", url, data=data)
