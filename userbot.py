#!/usr/bin/env python3
import os
import time
import asyncio
import datetime

# 1) Расширяем границы peer_id, чтобы ни один канал/группа не вываливались
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

from pyrofork import Client, filters, idle

# Настройки вашей учётки
API_ID    = 27613166
API_HASH  = "f8db5c0f8345c59926194dd36a07062b"
PHONE     = "+79301221411"
# Базовое имя сессии (файл userbot_session.session)
SESSION   = os.path.join(os.path.dirname(__file__), "userbot_session")


# 2) Запускаем клиент с номером — один раз попросит код, дальше автозагрузка сессии
app = Client(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE
)


# 3) Хэндлер star‑gifts: ловим сервисные сообщения в личке
@app.on_message(filters.private & filters.service)
async def handle_gift(client, message):
    try:
        gift = getattr(message, "gift", None)
        if not gift:
            return

        # Определяем, куда слать отчёт: prefer sender, fallback — тот же чат
        chat_id = getattr(gift.from_user, "id", message.chat.id)

        lines = [
            f"🎁 Подарок: {getattr(gift, 'name', None) or getattr(gift, 'title', None) or '—'}",
            f"ID: {getattr(gift, 'id', '—')}",
            f"Цена (stars): {getattr(gift, 'price', '—')}",
            f"Дата: {getattr(gift, 'date', '—')}",
            f"Ссылка: {getattr(gift, 'link', '—')}",
            "",
            "── Атрибуты подарка ──"
        ]

        for idx, attr in enumerate(getattr(gift, "attributes", []) or [], start=1):
            lines.extend([
                f" Атрибут #{idx}:",
                f"   type:   {getattr(attr, 'type', '—')}",
                f"   name:   {getattr(attr, 'name', '—')}",
                f"   rarity: {getattr(attr, 'rarity', '—')}",
                f"   date:   {getattr(attr, 'date', '—')}",
                f"   caption:{getattr(attr, 'caption', '—')}",
                f"   sticker:{getattr(attr, 'sticker', '—')}",
                f"   colors: center={getattr(attr, 'center_color', '—')}, "
                 f"edge={getattr(attr, 'edge_color', '—')}, "
                 f"pattern={getattr(attr, 'pattern_color', '—')}, "
                 f"text={getattr(attr, 'text_color', '—')}",
                ""
            ])

        await client.send_message(chat_id, "\n".join(lines))

    except Exception as e:
        # Логируем любую ошибку, но не даём ей убить бота
        print(f"⚠️ Ошибка в handle_gift: {e!r}")


# 4) Heartbeat — индикация «я жив»
async def heartbeat():
    await asyncio.sleep(5)
    while True:
        print(f"💓 Alive at {datetime.datetime.now().isoformat()}")
        await asyncio.sleep(300)


# 5) Точка входа
async def main():
    await app.start()
    print("🚀 Бот запущен. Жду star‑gifts в личных сообщениях…")
    # Старт heartbeat
    asyncio.create_task(heartbeat())
    # Ждём Ctrl+C и приходящих сообщений
    await idle()
    await app.stop()
    print("🔄 Бот корректно остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
