#!/usr/bin/env python3
import time
import asyncio
import datetime

# ─── 1) MONKEY‑PATCH для корректного распознавания всех Peer ID ─────────────
import pyrofork.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

# ─── 2) Асинхендлер, чтобы проглатывать Peer id invalid и не падать ─────────
def setup_asyncio_exception_handler():
    loop = asyncio.get_event_loop()
    def handle_exc(loop, context):
        exc = context.get("exception")
        if isinstance(exc, ValueError) and "Peer id invalid" in str(exc):
            return  # игнорируем некорректные peer_id
        loop.default_exception_handler(context)
    loop.set_exception_handler(handle_exc)

# ─── 3) Heartbeat: выводит в консоль сигнал «жив» каждые 5 минут ────────────
async def heartbeat():
    await asyncio.sleep(5)
    while True:
        print(f"💓 Alive at {datetime.datetime.now().isoformat()}")
        await asyncio.sleep(300)

# ─── 4) Импортируем Client и filters из pyrofork ─────────────────────────────
from pyrofork import Client, filters

def start():
    setup_asyncio_exception_handler()

    app = Client(
        "userbot_session",
        api_id=27613166,
        api_hash="f8db5c0f8345c59926194dd36a07062b",
        phone_number="+79301221411"
    )

    @app.on_message(filters.private)
    async def handle_gift(client, message):
        gift = getattr(message, "gift", None)
        if not gift:
            return

        report_lines = [
            f"🎁 Подарок: {getattr(gift, 'name', None) or getattr(gift, 'title', None)}",
            f"ID подарка: {getattr(gift, 'id', None)}",
            f"Цена (stars): {getattr(gift, 'price', None)}",
            f"Дата: {getattr(gift, 'date', None)}",
            f"Ссылка: {getattr(gift, 'link', None)}",
        ]

        attrs = getattr(gift, "attributes", None)
        if attrs:
            for idx, attr in enumerate(attrs, 1):
                report_lines.extend([
                    f"Атрибут {idx}:",
                    f"  type: {getattr(attr, 'type', None)}",
                    f"  name: {getattr(attr, 'name', None)}",
                    f"  rarity: {getattr(attr, 'rarity', None)}",
                    f"  date: {getattr(attr, 'date', None)}",
                    f"  caption: {getattr(attr, 'caption', None)}",
                    f"  from_user: {getattr(getattr(attr, 'from_user', None), 'id', None)}",
                    f"  to_user: {getattr(getattr(attr, 'to_user', None), 'id', None)}",
                    f"  center_color: {getattr(attr, 'center_color', None)}",
                    f"  edge_color: {getattr(attr, 'edge_color', None)}",
                    f"  pattern_color: {getattr(attr, 'pattern_color', None)}",
                    f"  text_color: {getattr(attr, 'text_color', None)}",
                    f"  sticker: {getattr(attr, 'sticker', None)}",
                ])
        else:
            report_lines.append("Атрибуты отсутствуют.")

        await client.send_message(gift.from_user.id, "\n".join(report_lines))

    # Запускаем heartbeat параллельно
    app.add_task(heartbeat())

    print("🚀 Бот запущен. Ожидаю подарки в личных сообщениях…")
    app.run()

# ─── 5) WATCHDOG: перезапускаем при падении через 5 секунд ──────────────────
if __name__ == "__main__":
    while True:
        try:
            start()
        except Exception as e:
            print(f"‼️ Бот упал с ошибкой: {e!r}. Перезапуск через 5 сек.")
            time.sleep(5)
        else:
            print("🔄 Бот остановлен. Перезапуск через 5 сек.")
            time.sleep(5)
