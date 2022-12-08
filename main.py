import requests
import json
from aiogram import *
from aiogram.types import *

TOKEN = "5852982948:AAE7BVeBPYHwDf4uGjqAl1dJxkbceybyLWA"
bot =  Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

def downloader(link):
    url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

    querystring = {"url":link}

    headers = {
        "X-RapidAPI-Key": "5af05fa5fdmsh92e2f2c2d0849bdp1f99ccjsn2f4010a76d64",
        "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    rest = json.loads(response.text)

    dict = {}
    if 'error' in rest:
        return 0
    else:
        if rest['Type'] == 'Post-Image':
            dict['Type'] = 'image'
            dict['media'] = rest['media']
        elif rest['Type'] == 'Carousel':
            dict['Type'] = 'carousel'
            dict['media'] = rest['media']
        elif rest['Type'] == 'Post-Video':
            dict['Type'] = 'video'
            dict['media'] = rest['media']
        elif rest['Type'] == 'Story-Video':
            dict['Type'] = 'story'
            dict['media'] = rest['media']
        else:
            return 0
    return dict

statistic = 0

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global statistic
    statistic += 1
    await message.reply(f'👋Assalomu aleykum *{message.from_user.first_name}.* Ushbu bot orqali siz *Instagram*dan **post** yoki **story**larni yuklab olishingiz mumkin! Marhamat menga link yuboring!', parse_mode='Markdown')

@dp.message_handler()
async def get_url(message: types.Message):
    msg = message.text
    if 'instagram.com' in msg:
        response = downloader(msg)
        if response == 0:
            await message.answer('Yuborgan Link da xatolik bor! Iltimos linkni tekshirib qayta yuboring!')
        else:
            if response['Type'] == 'image':
                await bot.send_photo(chat_id=message.chat.id, photo=response['media'])
            elif response['Type'] == 'carousel':
                for i in response['media']:
                    await bot.send_photo(chat_id=message.chat.id, photo=i)
            elif response['Type'] == 'video':
                await bot.send_video(chat_id=message.chat.id, video=response['media'])
            elif response['Type'] == 'story':
                await bot.send_video(chat_id=message.chat.id, video=response['media'])



if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)