#!/usr/bin/env python3
import os
import asyncio
import datetime

# ─── MONKEY‑PATCH: расширяем границы peer_id, чтобы не ловить Peer id invalid ──
import pyrogram.utils as u
u.MIN_CHANNEL_ID = -1003000000000
u.MIN_CHAT_ID    = -999999999999

from pyrogram import Client, filters, idle
from pyrogram.raw.types import MessageActionStarGift

# ─── КОНФИГ ────────────────────────────────────────────────────────────────
API_ID   = 27613166
API_HASH = "f8db5c0f8345c59926194dd36a07062b"
PHONE    = "+79301221411"
SESSION  = os.path.join(os.path.dirname(__file__), "userbot_session")

# ─── ИНИЦИАЛИЗАЦИЯ CLIENT ──────────────────────────────────────────────────
app = Client(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE
)

# ─── ОБРАБОТЧИК STAR‑GIFT ──────────────────────────────────────────────────
@app.on_message(filters.private)
async def handle_star_gift(client, message):
    action = getattr(message.raw, "action", None)
    if not isinstance(action, MessageActionStarGift):
        return

    star = action.gift  # raw StarGift объект

    # Составляем отчёт
    lines = [
        f"🎁 Star‑Gift ID: {star.id}",
        f"Stars:         {star.stars}",
        f"Convertable:   {star.convert_stars}",
        f"Limited:       {bool(star.limited)}",
        f"Sold out:      {bool(star.sold_out)}",
        f"Date:          {star.first_sale_date or star.last_sale_date or '—'}",
        ""
    ]

    # Атрибуты StarGift (если есть)
    attrs = getattr(star, "attributes", None)
    if attrs:
        for idx, attr in enumerate(attrs, 1):
            lines.extend([
                f"── Атрибут #{idx} ──",
                f"  type:           {getattr(attr, 'type', '—')}",
                f"  name:           {getattr(attr, 'name', '—')}",
                f"  rarity:         {getattr(attr, 'rarity', '—')}",
                f"  date:           {getattr(attr, 'date', '—')}",
                f"  caption:        {getattr(attr, 'caption', '—')}",
                f"  sticker:        {getattr(attr, 'sticker', '—')}",
                f"  colors: center={getattr(attr, 'center_color', '—')}, "
                  f"edge={getattr(attr, 'edge_color', '—')}, "
                  f"pattern={getattr(attr, 'pattern_color', '—')}, "
                  f"text={getattr(attr, 'text_color', '—')}",
                ""
            ])
    else:
        lines.append("Нет дополнительных атрибутов.")

    # Отправляем отчёт обратно в тот же чат
    await client.send_message(message.chat.id, "\n".join(lines))


# ─── HEARTBEAT ─────────────────────────────────────────────────────────────
async def heartbeat():
    await asyncio.sleep(5)
    while True:
        print(f"💓 Alive at {datetime.datetime.now().isoformat()}")
        await asyncio.sleep(300)


# ─── MAIN ─────────────────────────────────────────────────────────────────
async def main():
    await app.start()
    print("🚀 Userbot запущен. Жду MTProto star‑gifts в личке…")
    # Запускаем heartbeat
    asyncio.create_task(heartbeat())
    # Ждём сигнал Ctrl+C и прихода обновлений
    await idle()
    await app.stop()
    print("🔄 Userbot остановлен.")

if __name__ == "__main__":
    asyncio.run(main())
