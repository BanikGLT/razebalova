# Userbot Telegram Gifts (Pyrofork + FastAPI)

## Описание

- Userbot на Pyrofork для автоматического ответа на подарки в Telegram.
- FastAPI backend для проверки статуса и управления.

## Быстрый старт

### 1. Клонируйте репозиторий
```bash
git clone <ВАШ_РЕПОЗИТОРИЙ>
cd <ВАШ_РЕПОЗИТОРИЙ>/backend
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

### 3. Запустите FastAPI сервер
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Запустите userbot (одновременно или как отдельный процесс)
```bash
python userbot.py
```

- При первом запуске userbot запросит код подтверждения Telegram.
- Сессия сохранится в файл `userbot_session.session`.
- При последующих запусках код не потребуется.

## Переменные и настройки
- `api_id`, `api_hash`, `phone_number` указываются прямо в userbot.py (или через переменные окружения).

## Для деплоя на Timeweb Cloud
- Загрузите папку backend в свой репозиторий.
- Укажите команду запуска FastAPI: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Для запуска userbot используйте отдельный процесс: `python userbot.py`

---

**Вопросы и доработки — пишите в Issues или Telegram!** 