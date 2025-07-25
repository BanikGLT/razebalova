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
# from pyrogram.enums import MessageServiceType  # Закомментировано, так как GIFT может отсутствовать

from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME, DEBUG
from gift_handler import GiftHandler
from gift_detector import AdvancedGiftDetector

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
            
            # Инициализируем обработчик и детектор подарков
            self.gift_handler = GiftHandler(self.client)
            self.gift_detector = AdvancedGiftDetector()
            
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
        
        @self.client.on_message()
        async def universal_message_handler(client: Client, message: Message):
            """Универсальный обработчик для поиска подарков"""
            try:
                # Используем продвинутый детектор подарков
                detection_result = await self.gift_detector.detect_gift(message)
                
                if detection_result["is_gift"]:
                    logger.info(f"🎁 ПОДАРОК ОБНАРУЖЕН! ID: {message.id}")
                    logger.info(f"Метод обнаружения: {detection_result['detection_method']}")
                    logger.info(f"Уверенность: {detection_result['confidence']:.2f}")
                    
                    # Быстрая обработка подарка
                    asyncio.create_task(self.gift_handler.process_gift(message))
                    
                elif DEBUG and message.service:
                    # В режиме отладки логируем служебные сообщения
                    logger.debug(f"Служебное сообщение: {message.service}")
                    
            except Exception as e:
                logger.error(f"Ошибка в универсальном обработчике: {e}")
        
        @self.client.on_message(filters.private & ~filters.service)
        async def handle_private_message(client: Client, message: Message):
            """Обработчик личных сообщений (для дополнительной проверки подарков)"""
            try:
                # Используем детектор для всех личных сообщений
                detection_result = await self.gift_detector.detect_gift(message)
                
                if detection_result["is_gift"]:
                    logger.info(f"🎁 Подарок обнаружен в личном сообщении ID: {message.id}")
                    logger.info(f"Метод: {detection_result['detection_method']}, Уверенность: {detection_result['confidence']:.2f}")
                    
                    # Обрабатываем подарок
                    asyncio.create_task(self.gift_handler.process_gift(message))
                    
                elif DEBUG and message.text:
                    logger.debug(f"Проанализировано личное сообщение: {message.text[:50]}...")
                        
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