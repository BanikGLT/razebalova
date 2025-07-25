#!/usr/bin/env python3
"""
Telegram UserBot для обработки подарков
Использует pyrofork для работы с Telegram API
"""

import asyncio
import logging
import sys
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageServiceType

from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME, DEBUG
from gift_handler import GiftHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('userbot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TelegramGiftBot:
    """Основной класс userbot для обработки подарков"""
    
    def __init__(self):
        """Инициализация бота"""
        self.client = None
        self.gift_handler = None
        self.is_running = False
        
    async def initialize(self):
        """Инициализация клиента и обработчиков"""
        try:
            # Проверяем наличие необходимых данных
            if not API_ID or not API_HASH:
                logger.error("API_ID и API_HASH должны быть установлены в .env файле")
                return False
            
            # Создаем клиент Pyrogram
            self.client = Client(
                SESSION_NAME,
                api_id=API_ID,
                api_hash=API_HASH,
                phone_number=PHONE_NUMBER
            )
            
            # Инициализируем обработчик подарков
            self.gift_handler = GiftHandler(self.client)
            
            logger.info("UserBot инициализирован успешно")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации: {e}")
            return False
    
    async def start(self):
        """Запуск userbot"""
        try:
            if not await self.initialize():
                logger.error("Не удалось инициализировать бота")
                return
            
            # Запускаем клиент
            await self.client.start()
            self.is_running = True
            
            # Получаем информацию о текущем пользователе
            me = await self.client.get_me()
            logger.info(f"UserBot запущен для пользователя: {me.first_name} (@{me.username})")
            
            # Регистрируем обработчики сообщений
            self.register_handlers()
            
            logger.info("🎁 UserBot готов к обработке подарков!")
            logger.info("Бот работает в режиме 24/7. Нажмите Ctrl+C для остановки.")
            
            # Основной цикл
            await self.run_forever()
            
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
        finally:
            await self.stop()
    
    def register_handlers(self):
        """Регистрация обработчиков сообщений"""
        
        @self.client.on_message(filters.service)
        async def handle_service_message(client: Client, message: Message):
            """Обработчик служебных сообщений (включая подарки)"""
            try:
                # Проверяем, является ли это подарком
                if message.service == MessageServiceType.GIFT:
                    logger.info(f"🎁 Обнаружен подарок в сообщении ID: {message.id}")
                    
                    # Обрабатываем подарок асинхронно для максимальной скорости
                    asyncio.create_task(self.gift_handler.process_gift(message))
                    
                elif DEBUG:
                    # В режиме отладки логируем все служебные сообщения
                    logger.debug(f"Служебное сообщение: {message.service}")
                    
            except Exception as e:
                logger.error(f"Ошибка в обработчике служебных сообщений: {e}")
        
        @self.client.on_message(filters.private & filters.text)
        async def handle_private_message(client: Client, message: Message):
            """Обработчик личных сообщений (для дополнительной проверки подарков)"""
            try:
                # Дополнительная проверка на подарки в текстовых сообщениях
                if message.text and any(keyword in message.text.lower() for keyword in ['подарок', 'gift', '🎁']):
                    if DEBUG:
                        logger.debug(f"Возможный подарок в текстовом сообщении: {message.text[:50]}...")
                        
            except Exception as e:
                logger.error(f"Ошибка в обработчике личных сообщений: {e}")
        
        logger.info("Обработчики сообщений зарегистрированы")
    
    async def run_forever(self):
        """Основной цикл работы бота"""
        try:
            # Ждем до получения сигнала остановки
            while self.is_running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки (Ctrl+C)")
        except Exception as e:
            logger.error(f"Ошибка в основном цикле: {e}")
    
    async def stop(self):
        """Остановка userbot"""
        try:
            self.is_running = False
            
            if self.client:
                await self.client.stop()
                logger.info("UserBot остановлен")
                
        except Exception as e:
            logger.error(f"Ошибка при остановке бота: {e}")

async def main():
    """Главная функция"""
    bot = TelegramGiftBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Программа прервана пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        logger.info("Завершение работы...")

if __name__ == "__main__":
    # Запускаем бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)