import requests as r
import datetime
import time
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)
CHANNEL_NAME = '@lerabonk'



@dp.message_handler(commands=["start"])
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    cur_weather_check = 0
    humidity_check = 0
    speed_check = 0
    emergency_brake = True
    while emergency_brake:
        try:
            pogoda = r.get(f'https://api.openweathermap.org/data/2.5/weather?lat=56.50&lon=60.35&appid={open_weather_token}&units=metric')
            data = pogoda.json()
            #print(data)

            cur_weather = data['main']['temp']
            humidity = data['main']['humidity']
            speed = data['wind']['speed']


            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]


            message = (f'*** Сегодня {datetime.datetime.now().strftime("%d.%m.%Y")} ***\n'
                    f'В Екатеринбурге: {cur_weather}°, {wd}\n'
                    f'Влажность в штанах: {humidity}%\n'
                    f'Скорость вiтра тобi у сраку: {round((speed * 3.6), 1)} км/ч')

            #print(message)
            await bot.send_message(CHANNEL_NAME, message)

        except Exception as ex:
            #print('Ошибка', ex)
            await bot.send_message(CHANNEL_NAME, 'Вы абсолютно дэбильны\nПроверь свой код, айтишник мамкин')
            break

        if cur_weather == cur_weather_check and humidity == humidity_check and speed == speed_check:
            await bot.send_message(CHANNEL_NAME, 'Токен протух, а ты - петух')
            emergency_brake = False
            break


        cur_weather_check = cur_weather
        humidity_check = humidity
        speed_check = speed

        time.sleep(86400)



if __name__ == '__main__':
    executor.start_polling(dp)

