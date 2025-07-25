#!/usr/bin/env python3
"""
Продвинутый детектор подарков в Telegram
Использует несколько методов обнаружения для максимальной надежности
"""

import logging
import json
from typing import Dict, Any, Optional, List
from pyrogram.types import Message

logger = logging.getLogger(__name__)

class AdvancedGiftDetector:
    """Продвинутый детектор подарков с множественными методами обнаружения"""
    
    def __init__(self):
        # Ключевые слова для поиска подарков
        self.gift_keywords = [
            'gift', 'подарок', 'present', '🎁', 'дарю', 'подарил', 
            'получил подарок', 'вручение', 'награда', 'приз'
        ]
        
        # Паттерны для service сообщений
        self.service_patterns = [
            'gift', 'present', 'award', 'prize'
        ]
        
    async def detect_gift(self, message: Message) -> Dict[str, Any]:
        """
        Комплексное обнаружение подарков в сообщении
        
        Args:
            message: Сообщение для анализа
            
        Returns:
            Словарь с результатами обнаружения
        """
        detection_result = {
            "is_gift": False,
            "confidence": 0.0,
            "detection_method": None,
            "gift_info": {},
            "raw_data": {}
        }
        
        try:
            # Метод 1: Проверка service сообщений
            service_result = await self._check_service_message(message)
            if service_result["detected"]:
                detection_result.update({
                    "is_gift": True,
                    "confidence": service_result["confidence"],
                    "detection_method": "service_message",
                    "gift_info": service_result["info"]
                })
                return detection_result
            
            # Метод 2: Проверка текста сообщения
            text_result = await self._check_text_content(message)
            if text_result["detected"]:
                detection_result.update({
                    "is_gift": True,
                    "confidence": text_result["confidence"],
                    "detection_method": "text_analysis",
                    "gift_info": text_result["info"]
                })
                return detection_result
            
            # Метод 3: Проверка медиа контента
            media_result = await self._check_media_content(message)
            if media_result["detected"]:
                detection_result.update({
                    "is_gift": True,
                    "confidence": media_result["confidence"],
                    "detection_method": "media_analysis",
                    "gift_info": media_result["info"]
                })
                return detection_result
            
            # Метод 4: Проверка raw данных
            raw_result = await self._check_raw_data(message)
            if raw_result["detected"]:
                detection_result.update({
                    "is_gift": True,
                    "confidence": raw_result["confidence"],
                    "detection_method": "raw_data",
                    "gift_info": raw_result["info"]
                })
                return detection_result
            
            logger.debug("Подарок не обнаружен во входящем сообщении")
            
        except Exception as e:
            logger.error(f"Ошибка при обнаружении подарка: {e}")
        
        return detection_result
    
    async def _check_service_message(self, message: Message) -> Dict[str, Any]:
        """Проверка service сообщений на наличие подарков"""
        result = {"detected": False, "confidence": 0.0, "info": {}}
        
        try:
            if not message.service:
                return result
            
            service_str = str(message.service).lower()
            logger.debug(f"Анализ service сообщения: {service_str}")
            
            # Проверяем паттерны
            for pattern in self.service_patterns:
                if pattern in service_str:
                    result.update({
                        "detected": True,
                        "confidence": 0.9,
                        "info": {
                            "service_type": str(message.service),
                            "pattern_matched": pattern,
                            "method": "service_pattern_match"
                        }
                    })
                    logger.info(f"🎁 Подарок обнаружен через service паттерн: {pattern}")
                    break
            
        except Exception as e:
            logger.error(f"Ошибка при проверке service сообщения: {e}")
        
        return result
    
    async def _check_text_content(self, message: Message) -> Dict[str, Any]:
        """Проверка текстового содержимого на наличие подарков"""
        result = {"detected": False, "confidence": 0.0, "info": {}}
        
        try:
            if not message.text:
                return result
            
            text_lower = message.text.lower()
            matched_keywords = []
            
            # Ищем ключевые слова
            for keyword in self.gift_keywords:
                if keyword in text_lower:
                    matched_keywords.append(keyword)
            
            if matched_keywords:
                confidence = min(0.8, len(matched_keywords) * 0.3)
                result.update({
                    "detected": True,
                    "confidence": confidence,
                    "info": {
                        "matched_keywords": matched_keywords,
                        "text_preview": message.text[:100],
                        "method": "text_keyword_match"
                    }
                })
                logger.info(f"🎁 Подарок обнаружен через текст: {matched_keywords}")
            
        except Exception as e:
            logger.error(f"Ошибка при проверке текста: {e}")
        
        return result
    
    async def _check_media_content(self, message: Message) -> Dict[str, Any]:
        """Проверка медиа контента на наличие подарков"""
        result = {"detected": False, "confidence": 0.0, "info": {}}
        
        try:
            if not message.media:
                return result
            
            media_str = str(message.media).lower()
            
            # Проверяем медиа на наличие gift-паттернов
            if any(pattern in media_str for pattern in self.service_patterns):
                result.update({
                    "detected": True,
                    "confidence": 0.7,
                    "info": {
                        "media_type": str(type(message.media)),
                        "media_info": media_str[:200],
                        "method": "media_pattern_match"
                    }
                })
                logger.info(f"🎁 Подарок обнаружен через медиа контент")
            
        except Exception as e:
            logger.error(f"Ошибка при проверке медиа: {e}")
        
        return result
    
    async def _check_raw_data(self, message: Message) -> Dict[str, Any]:
        """Проверка raw данных сообщения"""
        result = {"detected": False, "confidence": 0.0, "info": {}}
        
        try:
            # Проверяем различные атрибуты сообщения
            attributes_to_check = ['raw', '__dict__', '__str__']
            
            for attr_name in attributes_to_check:
                if hasattr(message, attr_name):
                    try:
                        if attr_name == '__dict__':
                            attr_value = str(message.__dict__)
                        elif attr_name == '__str__':
                            attr_value = str(message)
                        else:
                            attr_value = str(getattr(message, attr_name))
                        
                        attr_lower = attr_value.lower()
                        
                        # Ищем gift-паттерны в атрибутах
                        for pattern in self.service_patterns:
                            if pattern in attr_lower:
                                result.update({
                                    "detected": True,
                                    "confidence": 0.6,
                                    "info": {
                                        "attribute": attr_name,
                                        "pattern_matched": pattern,
                                        "data_preview": attr_value[:200],
                                        "method": "raw_data_pattern_match"
                                    }
                                })
                                logger.info(f"🎁 Подарок обнаружен через {attr_name}")
                                return result
                                
                    except Exception as attr_error:
                        logger.debug(f"Ошибка при проверке атрибута {attr_name}: {attr_error}")
            
        except Exception as e:
            logger.error(f"Ошибка при проверке raw данных: {e}")
        
        return result
    
    def get_detection_stats(self) -> Dict[str, Any]:
        """Получение статистики обнаружения"""
        return {
            "total_keywords": len(self.gift_keywords),
            "total_patterns": len(self.service_patterns),
            "detection_methods": [
                "service_message",
                "text_analysis", 
                "media_analysis",
                "raw_data"
            ]
        }