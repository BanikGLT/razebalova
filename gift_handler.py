import asyncio
import logging
from typing import Dict, Any
from pyrogram import Client
from pyrogram.types import Message

logger = logging.getLogger(__name__)

class GiftHandler:
    """Класс для обработки подарков в Telegram"""
    
    def __init__(self, client: Client):
        self.client = client
    
    async def get_gift_info(self, message: Message) -> Dict[str, Any]:
        """
        Извлекает информацию о подарке из сообщения
        
        Args:
            message: Сообщение с подарком
            
        Returns:
            Словарь с информацию о подарке
        """
        gift_info = {
            "sender": None,
            "sender_id": None,
            "gift_type": "Unknown",
            "gift_description": "Подарок получен",
            "timestamp": message.date,
            "message_id": message.id
        }
        
        # Получаем информацию об отправителе
        if message.from_user:
            gift_info["sender"] = message.from_user.first_name
            if message.from_user.last_name:
                gift_info["sender"] += f" {message.from_user.last_name}"
            gift_info["sender_id"] = message.from_user.id
            
            # Добавляем username если есть
            if message.from_user.username:
                gift_info["sender_username"] = message.from_user.username
        
        # Анализируем тип подарка
        if message.service:
            if message.service == MessageServiceType.GIFT:
                gift_info["gift_type"] = "Telegram Gift"
                gift_info["gift_description"] = "Получен подарок в Telegram"
        
        # Дополнительная информация из текста сообщения
        if message.text:
            gift_info["message_text"] = message.text
        
        return gift_info
    
    async def format_gift_response(self, gift_info: Dict[str, Any]) -> str:
        """
        Форматирует ответ с информацией о подарке
        
        Args:
            gift_info: Информация о подарке
            
        Returns:
            Отформатированное сообщение
        """
        sender_name = gift_info.get("sender", "Неизвестный")
        gift_type = gift_info.get("gift_type", "Unknown")
        timestamp = gift_info.get("timestamp")
        
        # Форматируем время
        time_str = timestamp.strftime("%H:%M:%S %d.%m.%Y") if timestamp else "Неизвестно"
        
        response = f"🎁 **Получен подарок!**\n\n"
        response += f"👤 **От:** {sender_name}\n"
        
        if gift_info.get("sender_username"):
            response += f"📱 **Username:** @{gift_info['sender_username']}\n"
        
        response += f"🎭 **Тип подарка:** {gift_type}\n"
        response += f"⏰ **Время:** {time_str}\n"
        
        if gift_info.get("message_text"):
            response += f"💬 **Сообщение:** {gift_info['message_text']}\n"
        
        response += f"\n✅ **Статус:** Подарок успешно получен и обработан!"
        
        return response
    
    async def send_gift_response(self, message: Message, gift_info: Dict[str, Any]) -> bool:
        """
        Отправляет ответ отправителю подарка
        
        Args:
            message: Исходное сообщение с подарком
            gift_info: Информация о подарке
            
        Returns:
            True если сообщение отправлено успешно
        """
        try:
            response_text = await self.format_gift_response(gift_info)
            
            # Отправляем ответ отправителю
            if message.from_user:
                await self.client.send_message(
                    chat_id=message.from_user.id,
                    text=response_text
                )
                logger.info(f"Отправлен ответ пользователю {gift_info.get('sender')} (ID: {gift_info.get('sender_id')})")
                return True
            else:
                logger.warning("Не удалось определить отправителя подарка")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка при отправке ответа: {e}")
            return False
    
    async def process_gift(self, message: Message) -> bool:
        """
        Основная функция обработки подарка
        
        Args:
            message: Сообщение с подарком
            
        Returns:
            True если подарок обработан успешно
        """
        try:
            logger.info(f"Обрабатываем подарок от сообщения ID: {message.id}")
            
            # Получаем информацию о подарке
            gift_info = await self.get_gift_info(message)
            
            # Логируем информацию о подарке
            logger.info(f"Получен подарок от {gift_info.get('sender')} (ID: {gift_info.get('sender_id')})")
            
            # Отправляем ответ
            success = await self.send_gift_response(message, gift_info)
            
            if success:
                logger.info("Подарок успешно обработан")
            else:
                logger.warning("Не удалось отправить ответ на подарок")
            
            return success
            
        except Exception as e:
            logger.error(f"Ошибка при обработке подарка: {e}")
            return False