#!/usr/bin/env python3
import os
import time
import asyncio
import datetime

# ─── 0) Определяем абсолютный путь до папки со скриптом ─────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── 1) MONKEY‑PATCH: расширяем границы ID ─────────────────────────────────
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

# ─── 2) Exception‑handler: «глотаем» ValueError("Peer id invalid") ──────────
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

    # ─── 3.1) Создаём Client, указывая полный путь до файла сессии
    session_path = os.path.join(BASE_DIR, "userbot_session.session")
    app = Client(session_name=session_path)

    # ─── 3.2) Регистрируем хэндлер подарков
    @app.on_message(filters.private)
    async def handle_gift(client, message):
        gift = getattr(message, "gift", None)
        if not gift:
            return

        lines = [
            f"🎁 Подарок: {gift.name or gift.title}",
            f"ID: {gift.id}",
            f"Цена: {gift.price}",
            f"Дата: {gift.date}",
            f"Ссылка: {gift.link}",
        ]
        for idx, attr in enumerate(gift.attributes or [], 1):
            lines.extend([
                f"Атрибут {idx}:",
                f"  type: {attr.type}",
                f"  name: {attr.name}",
                f"  rarity: {attr.rarity}",
                f"  date: {attr.date}",
                f"  caption: {attr.caption}",
                f"  from_user: {getattr(attr.from_user, 'id', None)}",
                f"  to_user:   {getattr(attr.to_user,   'id', None)}",
                f"  center_color: {attr.center_color}",
                f"  edge_color:   {attr.edge_color}",
                f"  pattern_color:{attr.pattern_color}",
                f"  text_color:   {attr.text_color}",
                f"  sticker:      {attr.sticker}",
            ])

        await client.send_message(gift.from_user.id, "\n".join(lines))

    # ─── 3.3) Запускаем клиента
    await app.start()
    print("🚀 Бот запущен. Ожидаю подарки в ЛС…")

    # ─── 3.4) Heartbeat‑таск
    async def heartbeat():
        await asyncio.sleep(5)
        while True:
            print(f"💓 Alive at {datetime.datetime.now().isoformat()}")
            await asyncio.sleep(300)
    asyncio.create_task(heartbeat())

    # ─── 3.5) Ждём обновлений
    await idle()

    # ─── 3.6) Останавливаем
    await app.stop()
    print("🔄 Бот корректно завершён.")

# ─── 4) WATCHDOG: перезапуск при падении ─────────────────────────────────────
if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"‼️ Ошибка: {e!r}. Перезапуск через 5 сек.")
            time.sleep(5)
        else:
            print("🔄 main() завершился без ошибок. Перезапуск через 5 сек.")
            time.sleep(5)
