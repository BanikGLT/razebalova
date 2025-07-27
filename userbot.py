#!/usr/bin/env python3
import os
import asyncio
import datetime

# 1) MONKEY‑PATCH для корректного распознавания любых peer_id
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

from pyrogram import Client, filters, idle

API_ID   = 27613166
API_HASH = "f8db5c0f8345c59926194dd36a07062b"
PHONE    = "+79301221411"
SESSION  = os.path.join(os.path.dirname(__file__), "userbot_session")

# 2) Создаём клиент с номером — Pyrogram при первом запуске спросит код,
#    при последующих — подхватит сохранённую сессию и не станет спрашивать снова.
app = Client(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE
)

# 3) Хэндлер star‑gifts
@app.on_message(filters.private)
async def handle_gift(client, message):
    gift = getattr(message, "gift", None)
    if not gift:
        return

    report = [
        f"🎁 Подарок: {gift.name or gift.title}",
        f"ID: {gift.id}",
        f"Цена (stars): {gift.price}",
        f"Дата: {gift.date}",
        f"Ссылка: {gift.link}",
    ]

    for idx, attr in enumerate(gift.attributes or [], 1):
        report.extend([
            f"── Атрибут #{idx} ──",
            f"type: {attr.type}",
            f"name: {attr.name}",
            f"rarity: {attr.rarity}",
            f"date: {attr.date}",
            f"caption: {attr.caption}",
            f"from_user: {getattr(attr.from_user, 'id', None)}",
            f"to_user:   {getattr(attr.to_user,   'id', None)}",
            f"center_color:  {attr.center_color}",
            f"edge_color:    {attr.edge_color}",
            f"pattern_color: {attr.pattern_color}",
            f"text_color:    {attr.text_color}",
            f"sticker:       {attr.sticker}",
        ])

    await client.send_message(gift.from_user.id, "\n".join(report))

# 4) Heartbeat, чтобы видеть, что бот жив
async def heartbeat():
    await asyncio.sleep(5)
    while True:
        print(f"💓 Alive at {datetime.datetime.now().isoformat()}")
        await asyncio.sleep(300)

# 5) Точка входа
async def main():
    await app.start()
    print("🚀 Бот запущен. Ожидаю подарки в ЛС…")
    # Запускаем heartbeat
    asyncio.create_task(heartbeat())
    # Ждём Ctrl+C
    await idle()
    await app.stop()
    print("🔄 Бот остановлен.")

if __name__ == "__main__":
    asyncio.run(main())
