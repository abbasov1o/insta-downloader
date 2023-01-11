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

@bot.on_message(filters.command(['start']))
async def start(_, message):
    await message.reply_text(
        f"""Salam! {message.from_user.mention}👤\nMən sənin asanlıqla istədiyin video yükləməyə kömək edəcək botam✅\nBotda reklam vermək istəsən sahibimlə əlaqə saxla.\n\nNümunə:\n/musiqi Əlimdə Roza 🎵!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅Qrupa əlavə et", url="https://t.me/song_azbot?startgroup=true")
                ],
                [
                    InlineKeyboardButton(
                        "🛎Rəsmi Qrupumuz", url="https://t.me/zerotteam"),
                    InlineKeyboardButton(
                        "☑️ Rəsmi kanal", url="https://t.me/elisbots")     
                ],[ 
                    InlineKeyboardButton(
                        "🇦🇿PlayList", url="t.me/zenmusiqi"
                        )
                ]
            ]
        ),
        disable_web_page_preview=True,
    )

@bot.on_message()
async def get_url(message: types.Message):
    msg = message.text
    if 'instagram.com' in msg:
        response = downloader(msg)
        if response == 0:
            await message.answer('Göndərdiyiniz linkdə xəta var! Zəhmət olmasa linki yoxlayın və yenidən göndərin!')
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
