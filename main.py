from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import openai
import logging

TOKEN_API='5826526647:AAHVt1ApTn49PJITb_ptYsxrIH-GQq-YNY4'
chat_api='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'
BOT_PERSONALITY ='Friendly'

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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
