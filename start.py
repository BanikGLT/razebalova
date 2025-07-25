#!/usr/bin/env python3
"""
Скрипт для запуска Telegram UserBot
"""

import os
import sys

def check_env_file():
    """Проверяет наличие .env файла с настройками"""
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("📝 Создайте файл .env на основе .env.example и заполните его:")
        print("   cp .env.example .env")
        print("   nano .env")
        print("\n🔑 Получить API_ID и API_HASH можно на https://my.telegram.org")
        return False
    return True

def check_dependencies():
    """Проверяет установленные зависимости"""
    try:
        import pyrogram
        import dotenv
        return True
    except ImportError as e:
        print(f"❌ Не установлены зависимости: {e}")
        print("📦 Установите зависимости командой:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Главная функция запуска"""
    print("🚀 Запуск Telegram UserBot для обработки подарков...")
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Проверяем конфигурацию
    if not check_env_file():
        sys.exit(1)
    
    print("✅ Все проверки пройдены")
    print("🎁 Запускаем UserBot...")
    
    # Импортируем и запускаем основной модуль
    try:
        from userbot import main as run_userbot
        import asyncio
        asyncio.run(run_userbot())
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()