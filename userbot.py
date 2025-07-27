#!/usr/bin/env python3
import os
import time
import asyncio
import datetime

# ─── 0) Абсолютный путь к директории скрипта ────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── 1) MONKEY‑PATCH: расширяем границы для Peer id ─────────────────────────
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

# ─── 2) Exception‑handler: «глотаем» Peer id invalid ────────────────────────
def setup_asyncio_exception_handler():
    loop = asyncio.get_event_loop()
    def handler(loop, ctx):
        exc = ctx.get("exception")
        if isinstance(exc, ValueError) and "Peer id invalid" in str(exc):
            return
        loop.default_exception_handler(ctx)
    loop.set_exception_handler(handler)

# ─── 3) Основная корутина ────────────────────────────────────────────────────
async def main():
    setup_asyncio_exception_handler()

    from pyrogram import Client, filters, idle

    # ─── 3.1) Собираем имя сессии (без .session — Pyrogram сам подставит расширение)
    session_base = os.path.join(BASE_DIR, "userbot_session")

    # ─── 3.2) Инициализируем Client позиционно: (session_name, api_id, api_hash)
    app = Client(
        session_base,
        api_id=27613166,
        api_hash="f8db5c0f8345c59926194dd36a07062b"
    )

    @app.on_message(filters.private)
    async def handle_gift(client, message):
        gift = getattr(message, "gift", None)
        if not gift:
            return

        report = [
            f"🎁 Подарок: {gift.name or gift.title}",
            f"ID: {gift.id}",
            f"Цена: {gift.price}",
            f"Дата: {gift.date}",
            f"Ссылка: {gift.link}",
        ]

        for idx, attr in enumerate(gift.attributes or [], 1):
            report.extend([
                f"Атрибут {idx}:",
                f"  type: {attr.type}",
                f"  name: {attr.name}",
                f"  rarity: {attr.rarity}",
                f"  date: {attr.date}",
                f"  caption: {attr.caption}",
                f"  from_user: {attr.from_user.id if attr.from_user else None}",
                f"  to_user:   {attr.to_user.id   if attr.to_user   else None}",
                f"  center_color:  {attr.center_color}",
                f"  edge_color:    {attr.edge_color}",
                f"  pattern_color: {attr.pattern_color}",
                f"  text_color:    {attr.text_color}",
                f"  sticker:       {attr.sticker}",
            ])

        await client.send_message(gift.from_user.id, "\n".join(report))

    # ─── 3.3) Запуск
    await app.start()
    print("🚀 Бот запущен. Ожидаю подарки в ЛС…")

    # ─── 3.4) Heartbeat
    async def heartbeat():
        await asyncio.sleep(5)
        while True:
            print("💓 Alive at", datetime.datetime.now().isoformat())
            await asyncio.sleep(300)
    asyncio.create_task(heartbeat())

    # ─── 3.5) Ждём обновлений и Ctrl+C
    await idle()

    # ─── 3.6) Остановка
    await app.stop()
    print("🔄 Бот корректно остановлен.")

# ─── 4) WATCHDOG: перезапускаем main() при падении ───────────────────────────
if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"‼️ Ошибка: {e!r}. Перезапуск через 5 сек.")
            time.sleep(5)
        else:
            print("🔄 main() завершился удачно. Перезапуск через 5 сек.")
            time.sleep(5)
