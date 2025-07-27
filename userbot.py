#!/usr/bin/env python3
import time
import asyncio
import datetime

# ─── 1) MONKEY‑PATCH: расширяем границы ID, чтобы не ловить Peer id invalid ───
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

# ─── 2) Exception‑handler: проглатываем ValueError("Peer id invalid") ─────────
def setup_asyncio_exception_handler():
    loop = asyncio.get_event_loop()
    def handle_exc(loop, context):
        exc = context.get("exception")
        if isinstance(exc, ValueError) and "Peer id invalid" in str(exc):
            return
        loop.default_exception_handler(context)
    loop.set_exception_handler(handle_exc)

# ─── 3) Основная корутина ─────────────────────────────────────────────────────
async def main():
    setup_asyncio_exception_handler()

    # импортируем внутри функции, чтобы utils уже патчен был
    from pyrogram import Client, filters, idle

    # Client инициализируется только с именем сессии
    app = Client("userbot_session")

    @app.on_message(filters.private)
    async def handle_gift(client, message):
        gift = getattr(message, "gift", None)
        if not gift:
            return

        report = [
            f"🎁 Подарок: {gift.name or gift.title}",
            f"ID подарка: {gift.id}",
            f"Цена (stars): {gift.price}",
            f"Дата: {gift.date}",
            f"Ссылка: {gift.link}",
        ]

        attrs = gift.attributes or []
        for idx, attr in enumerate(attrs, 1):
            report.extend([
                f"Атрибут {idx}:",
                f"  type: {attr.type}",
                f"  name: {attr.name}",
                f"  rarity: {attr.rarity}",
                f"  date: {attr.date}",
                f"  caption: {attr.caption}",
                f"  from_user: {attr.from_user.id if attr.from_user else None}",
                f"  to_user: {attr.to_user.id if attr.to_user else None}",
                f"  center_color: {attr.center_color}",
                f"  edge_color: {attr.edge_color}",
                f"  pattern_color: {attr.pattern_color}",
                f"  text_color: {attr.text_color}",
                f"  sticker: {attr.sticker}",
            ])

        await client.send_message(gift.from_user.id, "\n".join(report))

    # 3.1) Запуск клиента
    await app.start()
    print("🚀 Бот запущен по session‑файлу. Ожидаю подарки в ЛС…")

    # 3.2) Heartbeat
    async def heartbeat():
        await asyncio.sleep(5)
        while True:
            print(f"💓 Alive at {datetime.datetime.now().isoformat()}")
            await asyncio.sleep(300)
    asyncio.create_task(heartbeat())

    # 3.3) Ждём обновлений и Ctrl+C
    await idle()

    # 3.4) Останов
    await app.stop()
    print("🔄 Бот остановлен.")

# ─── 4) WATCHDOG: перезапускаем main() при любой ошибке ───────────────────────
if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"‼️ Ошибка: {e!r}. Перезапуск через 5 сек.")
            time.sleep(5)
        else:
            print("🔄 main() завершился нормально. Перезапуск через 5 сек.")
            time.sleep(5)
