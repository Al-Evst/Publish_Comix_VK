import os
import random
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError


def check_response(response):
    if response.status_code in [401, 404, 500]:
        raise HTTPError(f"HTTP error {response.status_code}: {response.reason}")
    response.raise_for_status()


def get_latest_comic_num() -> int:
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url, timeout=10)
    check_response(response)
    comic_info = response.json()
    return comic_info['num']


def download_xkcd_comic(num: int):
    url = f"https://xkcd.com/{num}/info.0.json"
    response = requests.get(url, timeout=10)
    check_response(response)
    comic_info = response.json()

    title = comic_info['title']
    alt_text = comic_info.get('alt', '')
    img_url = comic_info['img']
    filename = f"xkcd_{num}_{title.replace(' ', '_')}.png"

    image_response = requests.get(img_url, timeout=10)
    check_response(image_response)
    with open(filename, 'wb') as f:
        f.write(image_response.content)

    return filename, f"{title}\n\n{alt_text}"


def send_to_telegram(token: str, chat_id: str, filename: str, caption: str):
    bot = Bot(token=token)
    with open(filename, 'rb') as image_file:
        bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption)


def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not token or not chat_id:
        print("Ошибка: TELEGRAM_TOKEN или CHAT_ID не заданы в .env")
        return

    try:
        latest_comic_num = get_latest_comic_num()
    except (HTTPError, Timeout, ConnectionError) as e:
        print(f"Ошибка получения номера последнего комикса: {e}")
        return

    random_comic_num = random.randint(1, latest_comic_num)

    try:
        filename, caption = download_xkcd_comic(random_comic_num)
    except (HTTPError, Timeout, ConnectionError) as e:
        print(f"Ошибка загрузки комикса: {e}")
        return

    try:
        send_to_telegram(token, chat_id, filename, caption)
    except TelegramError as e:
        print(f"Ошибка отправки в Telegram: {e}")

    try:
        os.remove(filename)
    except OSError as e:
        print(f"Ошибка удаления файла: {e}")


if __name__ == "__main__":
    main()