from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import openai
import speech_recognition as sr
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
import moviepy.editor as mp
import datetime
import requests
from aiogram.types import ContentType, File, Message
import subprocess
import logging
from pathlib import Path


TOKEN_API='5826526647:AAHVt1ApTn49PJITb_ptYsxrIH-GQq-YNY4'
chat_api='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'
BOT_PERSONALITY ='Friendly'
logfile = str(datetime.date.today()) + '.log'

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

whiteList=[358255347, 1591853871 ]
comands=['Обычный режим', 'Режим для написания кода', '/help']

def createBtn(btns):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for i in btns:
        kb.add(KeyboardButton(i))
    return kb

@dp.message_handler(commands=['start'])
async def star_cmd (message:types.Message):
    print(message.chat.id)
    chek= message["chat"]["type"]
    userId2 = message["from"]["id"]
    userId = message.chat.id
    if userId2   not in whiteList:
        await message.answer(text='В даный момент этот бот Вам не доступен, вступите в паблик @lik11q и запросите доступ у @likvp')
    else:
        if chek != "supergroup" and chek != "group":
            kb = createBtn(comands)
            await message.answer(text='Выберите:', reply_markup=kb)
        else:
            await message.answer(
                text='Что бы использовать бота нужно ввести команду "/gpt" и в той же строчке ввести свой запрос \n Пример: /gpt Напиши код калькулятора на языке python')

@dp.message_handler(commands=['help'])
async def help_cmd(message:types.Message):
    print(message)
    userId2 = message["from"]["id"]
    userId=message.chat.id
    chek = message["chat"]["type"]

    if userId2 not in whiteList:
        await message.answer(text='В даный момент этот бот Вам не доступен')

    if chek!="supergroup" and chek!="group" and userId in whiteList:
        kb= createBtn(comands)
        await message.answer (  text='Что бы использовать бота нужно ввести команду "/start" и выбрать режим.', reply_markup=kb)

    if chek == "supergroup" or chek=="group" and userId2 in whiteList:
        await message.answer ( text='Что бы использовать бота нужно ввести команду "/gpt" и в той же строчке ввести свой запрос \n  Пример: /gpt Напиши код калькулятора на языке python')

@dp.message_handler(commands=['gpt'])
async def gpt_cmd(message:types.Message):
    userId=message["from"]["id"]
    print(whiteList)
    print(message.chat.id)
    if userId not in whiteList:
        await message.answer(text='В даный момент этот бот Вам не доступен, вступите в паблик @lik11q и запросите доступ у @likvp')

    else:
        arg = message.get_args()
        openai.api_key = chat_api
        model_engine = 'text-davinci-003'
        prompt = f'{arg}'
        completation = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        response = completation.choices[0].text
        await message.reply(f'{response}')


@dp.message_handler()
async def main (message:types.Message):


    chek = message["chat"]["type"]
    userText=message.text
    userId= message.chat.id

    if userText=='Обычный режим' and userId in whiteList:
        await message.answer(text='Включен обычный режим. Этот режим подходит для получение ответов на заданые вопросы.')

    elif userText=='Режим для написания кода' and userId in whiteList:
        await message.answer(text='Включен режим для написания кода. Но этот режим не дает 100% гарантии на получения нужного вам ответа. все зависит от запроса.')

    elif chek!="supergroup" and chek!="group" and userText!='Обычный режим' and userText!='Режим для написания кода' and userId in whiteList:
        arg = message.get_args()
        openai.api_key = chat_api
        model_engine = 'text-davinci-003'
        prompt = f'{arg}'
        try:
            completation = openai.Completion.create(
                engine=model_engine,
                prompt=message.text,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5
            )

            response = completation.choices[0].text
            await message.reply(f'{response}')
        except:
            await message.reply(f'токен перегружен или закончился ')


    else:
        pass

    if "forward_from" in message and chek=='private' and (userId==358255347 or userId == 1591853871):
        heckAdd = message["forward_from"]["id"]
        print(heckAdd)
        if heckAdd not in whiteList:
            whiteList.append(heckAdd)
            print(whiteList)
            await message.answer(text='Пользователь был успешно добавлен')

    if userId not in whiteList and chek != "supergroup" and chek != "group":
        await message.answer(text='В даный момент этот бот Вам не доступен')

def audio_to_text(dest_name: str):
# Функция для перевода аудио , в формате ".vaw" в текст
    r = sr.Recognizer() # такое вообще надо комментить?
    # тут мы читаем наш .vaw файл
    print(dest_name)
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU") # здесь можно изменять язык распознавания
    return result


async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

@dp.message_handler(content_types=[ContentType.VOICE])
async def get_audio_messages(message:types.Message):
# Основная функция, принимает голосовуху от пользователя
    chek = message["chat"]["type"]
    userText = message.text
    userId = message.chat.id
    if userId not in whiteList:
        await message.answer(
            text='В даный момент этот бот Вам не доступен, вступите в паблик @lik11q и запросите доступ у @likvp')

    else:
        try:
            print("Started recognition...")
            #print(message)
            # Ниже пытаемся вычленить имя файла, да и вообще берем данные с мессаги
            file_info = await message.voice.get_file()
            fname = f"{file_info.file_path.split('/')[1].split('.')[0]}" # Преобразуем путь в имя файла (например: file_2.oga)

            doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN_API, file_info.file_path))# Получаем и сохраняем присланную голосвуху (Ага, админ может в любой момент отключить удаление айдио файлов и слушать все, что ты там говоришь. А представь, что такую бяку подселят в огромный чат и она будет просто логировать все сообщения [анонимность в телеграмме, ахахаха])
            with open(fname+'.oga', 'wb') as f:
                f.write(doc.content)
            clip = mp.AudioFileClip(fname+'.oga')
            clip.write_audiofile(fname+".wav")
            #process = subprocess.run(['ffmpeg', '-i', os.path.dirname(os.path.abspath(__file__))+fname+'.oga', os.path.dirname(os.path.abspath(__file__))+fname+'.wav'])# здесь используется страшное ПО ffmpeg, для конвертации .oga в .vaw
            result = audio_to_text(fname+'.wav') # Вызов функции для перевода аудио в текст, а заодно передаем имена файлов, для их последующего удаления
            print(result)
            await message.answer (text=f'Расщифровка гс :\n{ format(result)}')
            arg = message.get_args()
            openai.api_key = chat_api
            model_engine = 'text-davinci-003'
            prompt = f'{result}'
            completation = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5
            )
            response = completation.choices[0].text
            await message.reply(f'{response}')
        except sr.UnknownValueError as e:
            await message.answer(text=  "Прошу прощения, но я не разобрал сообщение, или оно поустое...")
            with open(logfile, 'a', encoding='utf-8') as f:
                f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) + ':Message is empty.\n')
        except Exception as e:
            print(e)
            await message.answer(text=  "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
            with open(logfile, 'a', encoding='utf-8') as f:
                f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) +':' + str(e) + '\n')
        finally:
             pass
             #os.remove(fname+'.wav')
             #os.remove(fname+'.oga')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
