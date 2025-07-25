#!/usr/bin/env python3
"""
Упрощенное тестирование логики детектора подарков
Без зависимостей от pyrogram
"""

import asyncio

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

class SimpleGiftDetector:
    """Упрощенный детектор для тестирования логики"""
    
    def __init__(self):
        self.gift_keywords = [
            'gift', 'подарок', 'present', '🎁', 'дарю', 'подарил', 
            'получил подарок', 'вручение', 'награда', 'приз'
        ]
        
        self.service_patterns = [
            'gift', 'present', 'award', 'prize'
        ]
    
    async def detect_gift(self, message):
        """Упрощенное обнаружение подарков"""
        result = {
            "is_gift": False,
            "confidence": 0.0,
            "detection_method": None,
            "gift_info": {}
        }
        
        # Проверка service сообщений
        if message.service:
            service_str = str(message.service).lower()
            for pattern in self.service_patterns:
                if pattern in service_str:
                    result.update({
                        "is_gift": True,
                        "confidence": 0.9,
                        "detection_method": "service_message",
                        "gift_info": {"pattern": pattern}
                    })
                    return result
        
        # Проверка текста
        if message.text:
            text_lower = message.text.lower()
            matched_keywords = []
            
            for keyword in self.gift_keywords:
                if keyword in text_lower:
                    matched_keywords.append(keyword)
            
            if matched_keywords:
                confidence = min(0.8, len(matched_keywords) * 0.3)
                result.update({
                    "is_gift": True,
                    "confidence": confidence,
                    "detection_method": "text_analysis",
                    "gift_info": {"keywords": matched_keywords}
                })
                return result
        
        return result

async def test_detection():
    """Тестирование обнаружения подарков"""
    detector = SimpleGiftDetector()
    
    test_cases = [
        {
            "name": "Service сообщение с 'gift'",
            "message": MockMessage(service="MessageServiceType.GIFT")
        },
        {
            "name": "Текст с подарком",
            "message": MockMessage(text="Привет! Я дарю тебе подарок 🎁")
        },
        {
            "name": "English gift",
            "message": MockMessage(text="Here is your gift!")
        },
        {
            "name": "Обычное сообщение",
            "message": MockMessage(text="Привет, как дела?")
        },
        {
            "name": "Только эмодзи",
            "message": MockMessage(text="🎁🎁🎁")
        }
    ]
    
    print("🧪 Тестирование детектора подарков")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        result = await detector.detect_gift(test_case['message'])
        
        if result['is_gift']:
            print(f"✅ ПОДАРОК ОБНАРУЖЕН!")
            print(f"   Метод: {result['detection_method']}")
            print(f"   Уверенность: {result['confidence']:.2f}")
            print(f"   Детали: {result['gift_info']}")
        else:
            print(f"❌ Подарок не обнаружен")

async def main():
    print("🎁 Тестирование логики обнаружения подарков")
    print("=" * 50)
    
    await test_detection()
    
    print(f"\n✅ Тестирование завершено!")
    print(f"📝 Основной бот использует более продвинутые методы обнаружения")

if __name__ == "__main__":
    asyncio.run(main())