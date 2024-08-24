import random
import string
import re
import os

from shortzy import Shortzy
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread


bot = Client(
    "Link-Gen",
    api_hash="08d78fb05bdb90f1be4a4f1f0fef5f1e",
    api_id=16768772,
    bot_token=os.getenv("TOKEN"),
)

flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is running", 200

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


@bot.on_message(filters.command('start'))
async def start(client: Client, message: Message):
    first = message.from_user.first_name
    await message.reply(f"Hello {first}, You can use me to generate public earn links by sending me links!\n\n\nThis Bot is made by @Aakash1230")


async def get_shortlink(url, api, link):
    shortzy = Shortzy(api_key=api, base_site=url)
    link = await shortzy.convert(link)
    return link

def is_valid_url(url):
    regex = re.compile(
        r'^(https?:\/\/)?'
        r'(\w+\.)?'
        r'([\w-]+)'
        r'(\.[a-z]{2,})'
        r'(\/\S*)?$'
    )
    return re.match(regex, url) is not None

@bot.on_message(filters.text)
async def link_gen(client: Client, message: Message):
    link = message.text
    
    if is_valid_url(link):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        short_url = "publicearn.com"
        short_token = "5fcfd0c999d65c6deaa756e5cb898658ce28f728"
        link = await get_shortlink(short_url, short_token, link)
        await message.reply(f"Your short link is: `{link}`")
    else:
        await message.reply("The message isn't a valid link.")


if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run()
