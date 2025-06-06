# Руководство по диагностике и устранению проблем с деплоем Telegram бота на Railway

Данное руководство поможет вам диагностировать и устранить распространенные проблемы при деплое Telegram бота на платформе Railway.

## Основные проблемы и их решения

### 1. Бот не отвечает на команды

Если бот запущен на Railway, но не отвечает на команды, возможны следующие проблемы:

1. **Неправильная настройка webhook**
   - Webhook может быть установлен на неправильный URL (например, healthcheck.railway.app)
   - Webhook может быть не настроен вообще
   - Могут быть ошибки в обработке webhook-запросов

2. **Сервис на Railway не запущен или падает**
   - Проверьте логи деплоя в Railway
   - Убедитесь, что healthcheck проходит успешно
   - Проверьте, что порт задан правильно

3. **Конфликт между polling и webhook режимами**
   - Бот не может одновременно работать в режимах polling и webhook
   - Если вы используете webhook, убедитесь, что бот не запущен в режиме polling

## Диагностические инструменты

В этом репозитории есть несколько скриптов для диагностики и исправления проблем:

### `check_railway_service.py` - проверка состояния сервиса

Этот скрипт проверяет доступность сервиса на Railway, настройки webhook и способность бота отправлять сообщения.

```bash
# Базовая проверка
python check_railway_service.py

# Проверка с генерацией отчета
python check_railway_service.py --report

# Проверка с отправкой тестового сообщения
python check_railway_service.py --test --chat-id YOUR_CHAT_ID

# Проверка и исправление проблем с webhook
python check_railway_service.py --fix
```

### `railway_fix.py` - исправление проблем с webhook

Этот скрипт автоматически исправляет проблемы с webhook:

```bash
python railway_fix.py
```

### `start_polling.py` - запуск бота в режиме long polling

Если webhook не работает, вы можете временно запустить бота в режиме long polling:

```bash
python start_polling.py
```

## Типичные ошибки и их решения

### TelegramConflictError: terminated by other getUpdates request

Эта ошибка возникает, когда несколько экземпляров бота пытаются использовать polling одновременно, или когда webhook и polling режимы используются одновременно.

**Решение:**
1. Убедитесь, что запущен только один экземпляр бота
2. Отключите webhook перед использованием polling:
   ```python
   await bot.delete_webhook(drop_pending_updates=True)
   ```
3. Убедитесь, что вы не запускаете polling, если используете webhook

### Webhook установлен на healthcheck.railway.app

Railway использует healthcheck.railway.app для проверки работоспособности приложения, но этот домен не должен использоваться для webhook.

**Решение:**
1. Используйте скрипт `railway_fix.py` для исправления webhook
2. Вручную установите правильный URL для webhook:
   ```python
   railway_service_id = os.environ.get('RAILWAY_SERVICE_ID')
   webhook_url = f"https://{railway_service_id}.up.railway.app/webhook/{BOT_TOKEN}"
   ```

### Healthcheck не проходит

Railway требует, чтобы ваше приложение отвечало на HTTP запросы для подтверждения работоспособности.

**Решение:**
1. Убедитесь, что ваш сервер отвечает на запросы к корневому URL или /health
2. Используйте простой HTTP сервер вместе с вашим ботом:
   ```python
   # Пример с aiohttp
   from aiohttp import web
   
   async def health_check(request):
       return web.Response(text='OK')
   
   app = web.Application()
   app.router.add_get('/', health_check)
   app.router.add_get('/health', health_check)
   ```

## Проверка и настройка переменных окружения

Для правильной работы бота на Railway необходимы следующие переменные окружения:

- `BOT_TOKEN` - токен вашего Telegram бота
- `PORT` - порт для HTTP сервера (обычно устанавливается автоматически на Railway)
- `ADMIN_CHAT_ID` - ID чата администратора (для отправки тестовых сообщений)

Дополнительные переменные для диагностики:
- `WEBHOOK_URL` - полный URL для webhook (можно задать вручную)
- `WEBHOOK_HOST` - хост для webhook (можно задать вручную)
- `WEBHOOK_PATH` - путь для webhook (по умолчанию /webhook/{BOT_TOKEN})

## Рекомендуемая архитектура для Railway

Для стабильной работы бота на Railway рекомендуется:

1. Использовать единый сервер, который обрабатывает и webhook, и healthcheck запросы
2. Автоматически определять правильный URL для webhook на основе переменных окружения Railway
3. Реализовать механизм перезапуска webhook в случае ошибок
4. Добавить подробное логирование для диагностики проблем

Пример такой архитектуры реализован в скрипте `simple_server.py`.

## Дополнительные ресурсы

- [Документация по webhook в Telegram Bot API](https://core.telegram.org/bots/api#setwebhook)
- [Документация Railway](https://docs.railway.app/)
- [Документация aiogram](https://docs.aiogram.dev/)

## Устранение неполадок для конкретных ошибок

### Bad Request: message text is empty

Эта ошибка возникает при попытке отправить пустое сообщение.

**Решение:**
Убедитесь, что текст сообщения не пуст:
```python
if not message_text.strip():
    message_text = "Пустое сообщение не может быть отправлено"
```

### Webhook недоступен по URL

Если Telegram не может получить доступ к вашему webhook URL, проверьте:

1. Доступен ли ваш сервис по указанному URL (можно проверить через браузер или curl)
2. Правильно ли настроен маршрут для обработки webhook запросов
3. Не блокирует ли файрвол или промежуточное ПО запросы от Telegram серверов

### Сервис часто перезапускается на Railway

Если ваш сервис часто перезапускается на Railway:

1. Проверьте логи на наличие ошибок
2. Убедитесь, что healthcheck проходит успешно
3. Исправьте все необработанные исключения в коде
4. Добавьте обработку ошибок и механизмы восстановления

## Процедура полного сброса и переустановки

Если вы столкнулись с серьезными проблемами, которые не удается решить другими способами, выполните полный сброс:

1. Удалите webhook:
```bash
curl "https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true"
```

2. Перезапустите сервис на Railway

3. Установите webhook заново:
```bash
python railway_fix.py
```

4. Проверьте состояние webhook:
```bash
python check_railway_service.py --report
```

## Контакты для поддержки

Если у вас возникли проблемы, которые не удается решить с помощью этого руководства, вы можете обратиться за помощью: 