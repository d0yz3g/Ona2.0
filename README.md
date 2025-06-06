# Ona AI Telegram Bot

Telegram бот с использованием aiogram 3.x и деплоем на Railway.

## Описание

Бот представляет собой интеллектуального ассистента, который помогает пользователям разобраться в своих эмоциях и предоставляет персонализированные ответы и рекомендации.

## Особенности

- Обработка сообщений пользователя с использованием OpenAI
- Профиль пользователя на основе вопросов
- Голосовые медитации с ElevenLabs
- Режимы работы webhook и long polling
- Поддержка различных команд (/start, /help, /profile, /meditate)
- Автоматические напоминания
- Готовность к деплою на Railway

## Быстрый старт

### Требования

- Python 3.10+ 
- Токен Telegram бота от BotFather
- Опционально: API ключи OpenAI и ElevenLabs

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Запустите скрипт для создания файла `.env`:

```bash
python create_env.py
```

Или создайте файл вручную с минимальными настройками:

```
BOT_TOKEN=ваш_токен_бота
WEBHOOK_MODE=false
```

### 3. Запуск бота в режиме polling (для разработки)

```bash
python main.py
```

### 4. Или запуск в режиме webhook (для продакшена)

```bash
python webhook_server.py
```

## Режимы работы

Бот поддерживает два режима работы:

1. **Long polling** - рекомендуется для локальной разработки:
   - Проще в настройке
   - Не требует внешнего доступа
   - Запуск: `python main.py`

2. **Webhook** - рекомендуется для продакшена:
   - Более эффективное использование ресурсов
   - Мгновенная обработка сообщений
   - Требует публичный URL (например, Railway)
   - Запуск: `python webhook_server.py`

## Диагностика и проверка работоспособности

### Автоматическая диагностика

Для полной диагностики и выявления проблем запустите:

```bash
python diagnose.py --full
```

### Проверка здоровья

Для проверки работоспособности бота:

```bash
python test_health.py
```

### Тестирование команд бота

Для тестирования базовых команд (требуется указать ваш chat_id):

```bash
python test_bot.py --admin-chat-id=ваш_chat_id
```

## Деплой на Railway

1. Зарегистрируйтесь на Railway
2. Создайте новый проект и выберите "Deploy from GitHub"
3. Подключите ваш GitHub репозиторий
4. Добавьте переменные окружения:  
   * `BOT_TOKEN` - токен вашего Telegram бота  
   * `WEBHOOK_MODE` - установите в `true`  
   * `RAILWAY_PUBLIC_DOMAIN` - будет установлен автоматически (или настройте `WEBHOOK_URL` вручную)
5. Railway автоматически развернет ваше приложение

### Важно для деплоя на Railway

Railway требует, чтобы приложение отвечало на HTTP-запросы для проверки работоспособности (healthcheck). Для этого:

1. Убедитесь, что в `railway.json` указано:
   ```json
   {
     "deploy": {
       "startCommand": "python webhook_server.py",
       "healthcheckPath": "/health"
     },
     "variables": {
       "WEBHOOK_MODE": "true",
       "RAILWAY": "true"
     }
   }
   ```

2. При использовании webhook на Railway, URL вашего бота будет:
   ```
   https://<your-app-name>.up.railway.app/webhook/<BOT_TOKEN>
   ```
   
3. Если ваш бот не отвечает на сообщения, проверьте:
   * Правильно ли настроен webhook в Telegram (запустите `/webhook` в боте @BotFather)
   * Логи в Railway на наличие ошибок
   * Статус healthcheck в настройках Railway

4. Для локального тестирования webhook можно использовать:
   * ngrok: `ngrok http 8080`
   * Затем установите `WEBHOOK_URL=https://<your-ngrok-url>/webhook/<BOT_TOKEN>`

## Решение распространенных проблем

### Конфликт webhook и polling

Если видите ошибку "Conflict: terminated by other getUpdates request":

```bash
python webhook_server.py --disable-webhook
```

Затем перезапустите бота в нужном режиме.

### Проблемы с портом на Railway

Если health check не проходит:

1. Убедитесь, что бот слушает порт из переменной `PORT`
2. Проверьте наличие файла `railway.json` с правильными настройками
3. Проверьте логи для выявления конкретной ошибки

### Бот запускается, но не отвечает

1. Проверьте валидность токена бота:
   ```bash
   python test_health.py
   ```
2. Убедитесь, что webhook установлен правильно (для webhook-режима)
3. Проверьте, не блокирует ли сеть запросы к api.telegram.org

## Структура проекта

- `main.py` - основной файл для запуска в режиме polling
- `webhook_server.py` - сервер для webhook режима
- `test_health.py` - скрипт для проверки работоспособности
- `diagnose.py` - утилита для диагностики
- `health_check.py` - эндпоинт проверки здоровья для Railway

## Полная документация

- [WEBHOOK_README.md](WEBHOOK_README.md) - подробная информация о работе с webhook
- [DEPLOYMENT_TROUBLESHOOTING.md](DEPLOYMENT_TROUBLESHOOTING.md) - решение проблем с деплоем
- [RECOMMENDATIONS.md](RECOMMENDATIONS.md) - рекомендации по улучшению бота 