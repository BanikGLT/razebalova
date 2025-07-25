#!/usr/bin/env python3
"""
Тестирование детектора подарков
Проверяет различные методы обнаружения без подключения к Telegram
"""

import asyncio
import logging
from typing import Dict, Any

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MockMessage:
    """Мок-объект сообщения для тестирования"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 12345)
        self.text = kwargs.get('text', None)
        self.service = kwargs.get('service', None)
        self.media = kwargs.get('media', None)
        self.raw = kwargs.get('raw', None)
        self.from_user = kwargs.get('from_user', None)
        
    def __str__(self):
        return f"MockMessage(id={self.id}, text='{self.text}', service={self.service})"

async def test_gift_detection():
    """Тестирование различных сценариев обнаружения подарков"""
    
    # Импортируем детектор только при тестировании
    try:
        from gift_detector import AdvancedGiftDetector
        detector = AdvancedGiftDetector()
    except ImportError:
        logger.error("Не удалось импортировать AdvancedGiftDetector")
        return
    
    # Тестовые случаи
    test_cases = [
        {
            "name": "Service сообщение с 'gift'",
            "message": MockMessage(service="MessageServiceType.GIFT", text=None)
        },
        {
            "name": "Текстовое сообщение с подарком",
            "message": MockMessage(text="Привет! Я дарю тебе подарок 🎁", service=None)
        },
        {
            "name": "Английский текст с gift",
            "message": MockMessage(text="Here is your gift from me!", service=None)
        },
        {
            "name": "Обычное сообщение без подарка",
            "message": MockMessage(text="Привет, как дела?", service=None)
        },
        {
            "name": "Service сообщение без подарка",
            "message": MockMessage(service="MessageServiceType.JOIN", text=None)
        },
        {
            "name": "Сообщение с эмодзи подарка",
            "message": MockMessage(text="🎁🎁🎁", service=None)
        }
    ]
    
    print("🧪 Тестирование детектора подарков")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        try:
            result = await detector.detect_gift(test_case['message'])
            
            if result['is_gift']:
                print(f"✅ ПОДАРОК ОБНАРУЖЕН!")
                print(f"   Метод: {result['detection_method']}")
                print(f"   Уверенность: {result['confidence']:.2f}")
                print(f"   Информация: {result['gift_info']}")
            else:
                print(f"❌ Подарок не обнаружен")
                
        except Exception as e:
            print(f"💥 Ошибка при тестировании: {e}")
    
    # Статистика детектора
    print(f"\n📊 Статистика детектора:")
    stats = detector.get_detection_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

async def test_keywords():
    """Тестирование ключевых слов"""
    print(f"\n🔍 Тестирование ключевых слов")
    print("=" * 30)
    
    try:
        from gift_detector import AdvancedGiftDetector
        detector = AdvancedGiftDetector()
        
        print("Ключевые слова для поиска подарков:")
        for i, keyword in enumerate(detector.gift_keywords, 1):
            print(f"  {i}. '{keyword}'")
            
        print(f"\nПаттерны для service сообщений:")
        for i, pattern in enumerate(detector.service_patterns, 1):
            print(f"  {i}. '{pattern}'")
            
    except ImportError:
        print("Детектор недоступен для тестирования")

async def main():
    """Основная функция тестирования"""
    print("🎁 Тестирование системы обнаружения подарков Telegram")
    print("=" * 60)
    
    await test_keywords()
    await test_gift_detection()
    
    print(f"\n✅ Тестирование завершено!")
    print(f"💡 Для реального использования запустите: python3 start.py")

if __name__ == "__main__":
    asyncio.run(main())