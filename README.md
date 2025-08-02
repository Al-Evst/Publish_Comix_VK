# XKCD Publisher Bot

Этот скрипт публикует случайный комикс [xkcd](https://xkcd.com/) в указанный Telegram-чат или канал.

## Возможности

- Получает номер последнего комикса с xkcd API
- Случайным образом выбирает один из существующих комиксов
- Скачивает изображение и отправляет его в Telegram
- Удаляет локальный файл после отправки

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/yourusername/xkcd-publisher.git
   cd xkcd-publisher
   ```

2. Установите зависимости:

```
pip install -r requirements.txt
```
3. Создайте файл .env в корне проекта и укажите:

```
TELEGRAM_TOKEN=ваш_токен_бота
CHAT_ID=@your_channel_or_chat_id
```
## Запуск
Просто запустите скрипт:
```
python main.py
```
