#!/bin/bash

echo "🎁 Установка Telegram UserBot для обработки подарков"
echo "=================================================="

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8 или выше"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Проверяем pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip"
    exit 1
fi

echo "✅ pip найден"

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Зависимости установлены успешно"
else
    echo "❌ Ошибка при установке зависимостей"
    exit 1
fi

# Создаем .env файл если его нет
if [ ! -f .env ]; then
    echo "📝 Создаем файл конфигурации..."
    cp .env.example .env
    echo "✅ Файл .env создан"
    echo ""
    echo "🔧 ВАЖНО: Отредактируйте файл .env и заполните:"
    echo "   - API_ID (получить на https://my.telegram.org)"
    echo "   - API_HASH (получить на https://my.telegram.org)"
    echo "   - PHONE_NUMBER (ваш номер телефона)"
    echo ""
    echo "📝 Команда для редактирования: nano .env"
else
    echo "✅ Файл .env уже существует"
fi

# Делаем скрипты исполняемыми
chmod +x start.py
chmod +x userbot.py

echo ""
echo "🎉 Установка завершена!"
echo ""
echo "🚀 Для запуска используйте:"
echo "   python3 start.py"
echo ""
echo "📚 Или напрямую:"
echo "   python3 userbot.py"