#!/usr/bin/env python3
import os
import asyncio
import logging
from datetime import datetime

# ─── MONKEY‑PATCH: расширяем границы peer_id, чтобы не ловить Peer id invalid ───
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

from pyrogram import Client, filters, idle
from pyrogram.raw.types import MessageActionStarGift

# ─── КОНФИГ ───────────────────────────────────────────────────────────────────
API_ID   = 27613166
API_HASH = "f8db5c0f8345c59926194dd36a07062b"
PHONE    = "+79301221411"
# Базовое имя сессии; будет файл userbot_session.session рядом со скриптом
SESSION  = os.path.join(os.path.dirname(__file__), "userbot_session")

# ─── ЛОГГЕР ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ─── ИНИЦИАЛИЗАЦИЯ CLIENT ────────────────────────────────────────────────────
app = Client(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE
)

# ─── HEARTBEAT: проверка, что бот жив ────────────────────────────────────────
async def heartbeat():
    await asyncio.sleep(5)
    while True:
        logger.info("Heartbeat: bot is alive")
        await asyncio.sleep(300)

# ─── DEBUG‑ХЭНДЛЕР: логируем все входящие личные сообщения ──────────────────
@app.on_message(filters.private)
async def debug_all(client, message):
    logger.debug(f"Incoming private message: {message.raw or message}")

# ─── ОБРАБОТЧИК STAR‑GIFT ──────────────────────────────────────────────────
@app.on_message(filters.private)
async def handle_star_gift(client, message):
    try:
        action = getattr(message.raw, "action", None)
        if not isinstance(action, MessageActionStarGift):
            return

        logger.info(f"StarGift detected in chat {message.chat.id}")

        star = action.gift  # raw StarGift объект

        # Базовая информация о подарке
        lines = [
            f"🎁 Star‑Gift ID:       {star.id}",
            f"    Stars:            {star.stars}",
            f"    Convertible:      {star.convert_stars}",
            f"    Limited:          {bool(star.limited)}",
            f"    Sold out:         {bool(star.sold_out)}",
            f"    First sold:       {star.first_sale_date}",
            f"    Last sold:        {star.last_sale_date}",
            f"    Title:            {star.title or '—'}",
            ""
        ]
        logger.debug(f"StarGift core data: {lines}")

        # Дополнительные атрибуты
        attrs = getattr(star, "attributes", None) or []
        if attrs:
            logger.info(f"StarGift has {len(attrs)} attributes")
            for idx, attr in enumerate(attrs, 1):
                logger.debug(f"Processing attribute #{idx}: {attr}")
                lines.append(f"── Атрибут #{idx} ──")
                for field in [
                    "name", "backdrop_id", "center_color", "edge_color",
                    "pattern_color", "text_color", "rarity_permille",
                    "count", "counter_id"
                ]:
                    value = getattr(attr, field, None)
                    if value is not None:
                        lines.append(f"  {field}: {value}")
                lines.append("")
        else:
            logger.info("No additional attributes in StarGift")
            lines.append("Нет дополнительных атрибутов.\n")

        report = "\n".join(lines)
        logger.info(f"Sending report to chat {message.chat.id}")
        await client.send_message(message.chat.id, report)
        logger.info("Report sent successfully")

    except Exception as e:
        logger.exception(f"Error in handle_star_gift: {e}")

# ─── MAIN: старт, idle и остановка ────────────────────────────────────────────
async def main():
    logger.info("Starting userbot…")
    await app.start()
    logger.info("Userbot started. Waiting for Star‑Gifts in private chats…")
    asyncio.create_task(heartbeat())
    await idle()
    logger.info("Stopping userbot…")
    await app.stop()
    logger.info("Userbot stopped cleanly")

if __name__ == "__main__":
    asyncio.run(main())
