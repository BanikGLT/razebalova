from pyrofork import Client, filters

api_id = 27613166
api_hash = "f8db5c0f8345c59926194dd36a07062b"
phone_number = "+79301221411"
session_name = "userbot_session"

app = Client(
    session_name,
    api_id=api_id,
    api_hash=api_hash,
    phone_number=phone_number
)

@app.on_message(filters.private)
async def handle_gift(client, message):
    if getattr(message, "gift", None):
        gift = message.gift
        from_user = gift.from_user
        text = [
            f"🎁 Подарок: {getattr(gift, 'name', None) or getattr(gift, 'title', None)}",
            f"ID подарка: {getattr(gift, 'id', None)}",
            f"Цена: {getattr(gift, 'price', None)}",
            f"Дата: {getattr(gift, 'date', None)}",
            f"Ссылка: {getattr(gift, 'link', None)}",
        ]
        attributes = getattr(gift, "attributes", None)
        if attributes:
            for idx, attr in enumerate(attributes, 1):
                attr_lines = [
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
                ]
                text.extend(attr_lines)
        else:
            text.append("Атрибуты отсутствуют.")

        if from_user:
            await client.send_message(
                from_user.id,
                "\n".join(text)
            )

if __name__ == "__main__":
    app.run()
