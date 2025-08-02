import os
import json
import random
import urllib.request
import asyncio
from dotenv import load_dotenv
from telegram import Bot


def get_latest_comic_num() -> int:
    with urllib.request.urlopen("https://xkcd.com/info.0.json") as response:
        data = json.load(response)
        return data['num']


def download_xkcd_comic(num: int):
    try:
        with urllib.request.urlopen(f"https://xkcd.com/{num}/info.0.json") as response:
            data = json.load(response)
            title = data['title']
            alt_text = data.get('alt', '')
            img_url = data['img']
            filename = f"xkcd_{num}_{title.replace(' ', '_')}.png"
            urllib.request.urlretrieve(img_url, filename)
            return filename, f"{title}\n\n{alt_text}"
    except Exception:
        return None, None


async def send_to_telegram(token: str, chat_id: str, filename: str, caption: str):
    try:
        bot = Bot(token=token)
        with open(filename, 'rb') as image_file:
            await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")


def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not token or not chat_id:
        print("Ошибка: TELEGRAM_TOKEN или CHAT_ID не заданы в .env")
        return

    latest_num = get_latest_comic_num()
    random_num = random.randint(1, latest_num)
    filename, caption = download_xkcd_comic(random_num)

    if filename:
        asyncio.run(send_to_telegram(token, chat_id, filename, caption))
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Ошибка удаления файла: {e}")


if __name__ == "__main__":
    main()