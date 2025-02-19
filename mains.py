from email.mime.image import MIMEImage
import os
import aiosmtplib
import json
import asyncio
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import time
from matplotlib import pyplot as plt
import matplotlib
from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from fake_useragent import UserAgent
import telebot
import aiohttp
import random
from fake_useragent import UserAgent
from telebot.async_telebot import AsyncTeleBot
import re
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import logging
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime, timedelta
from pyCryptoPayAPI import pyCryptoPayAPI
import json
import time
from datetime import datetime, timedelta
import requests
from requests.exceptions import RequestException



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='bot_logs.log', filemode='a')

data_file = 'data.json'
last_links = {}
user_states = {}
subscribers = {} 
crypto = pyCryptoPayAPI(api_token="278031:AA5MEsL3uPl9tDtsLpcg9GKTYkj1O584AHz")
bot = AsyncTeleBot('7713705544:AAFH89lmCbFcc1c00GR-M7Wq5mzcOljKFQU')
owner_id = 7400105708
admins = [1111111111]
report_theme = None
report_text = None

user_states = {}


async def send_long_message(bot: Bot, chat_id: int, text: str, chunk_size=4096):
    for i in range(0, len(text), chunk_size):
        await bot.send_message(chat_id, text[i:i + chunk_size])
async def handle_report_mode(chat_id, user_id, recipient, subject, text):
    global sent_messages, failed_messages
    
async def get_user_state(user_id):
    return user_states.get(user_id, {})

async def set_user_state(user_id, state):
    user_states[user_id] = state

def load_users():
    try:
        with open('users.txt', 'r') as file:
            return [int(line.strip()) for line in file]
    except FileNotFoundError:
        return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open('users.txt', 'w') as file:
            file.write('\n'.join(str(user) for user in users))


@bot.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    if message.text == '/start':
        save_user(user_id)
    is_subscribed = False
    curr_time = datetime.now()
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            sub = data['users'][f"{user_id}"]['subscribe']
            sub_date = datetime.strptime(sub, '%Y-%m-%d %H:%M:%S.%f')
            if sub_date > curr_time:
                is_subscribed = True
    except:
        pass

    if is_subscribed:
        user_username = message.from_user.username
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            user_id_str = str(user_id)
            data['users'][user_id_str]['username'] = user_username
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        mode_send = data['users'][f'{user_id}']['mode']
        photo_path = 'net.jpg'
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn_account = telebot.types.InlineKeyboardButton(callback_data='account', text='Профиль📋')
        btn_report = telebot.types.InlineKeyboardButton(callback_data='reportt', text='SMPT SNOS⛔️')
        btn_reportt = telebot.types.InlineKeyboardButton(callback_data='reporttt', text='WEB SNOS🕸')
        btn_mail = telebot.types.InlineKeyboardButton(callback_data='mail', text='Почты📩')
        btn_pomoch = telebot.types.InlineKeyboardButton(callback_data='pomoch', text='Руководство🛠', url="https://telegra.ph/Rukovodstvo-dlya-snosera-GooseSnoser-11-13")
        btn_tgk = telebot.types.InlineKeyboardButton(call_data='tgk', text='Тгк сносера🍭', url="https://t.me/GooseSnosTGK")

        markup.row(btn_account)
        markup.row(btn_report, btn_reportt)
        markup.row(btn_mail, btn_pomoch)
        markup.row(btn_tgk)
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(message.chat.id, photo,
                           caption=f'''`👋 Привет! Я Goose Snos, твой помощник в удалении аккаунтов Telegram 💀

👁️ Нашёл нарушение? Отправь ссылку — помогу разобраться! 🚨

👥 Активных пользователей: {len(load_users())}
`''',
                           reply_markup=markup, parse_mode="Markdown")
    else:
        invoice = crypto.create_invoice(asset='USDT', amount=3)
        pay_url = invoice['pay_url']
        invoice_id = invoice['invoice_id']
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Преобрести Подписку за (3$)", url=pay_url))
        keyboard.add(types.InlineKeyboardButton("Проверить оплату", callback_data=f"check_status_{invoice_id}"))

        photo_path = 'net1.png'
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(message.chat.id, photo,
                           caption=f"Привествую в GooseSnos! \nЦена подписки  - 3$\nЧтобы купить подписку, нажмите Купить Подписку\nКупить через карту можно у @fucking_goose and @pplmaycry ",
                           reply_markup=keyboard),
async def handle_docs_photo(message):
    user_id = message.from_user.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'{user_id}.txt', 'wb') as new_file:
        new_file.write(downloaded_file)
    out = []
    time.sleep(1)
    with open(f'{user_id}.txt', 'r') as file:
        emails = [line.strip() for line in file if line.strip()]
        for x in emails:
            with open('data.json', 'r') as json_file:
                    data = json.load(json_file)
                    data["users"][f"{user_id}"]["sensers"].append(x)
            with open('data.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
    bot.reply_to(message, f"✅ Почты добавленны {len(emails)} шт!")
    time.sleep(1)
    os.remove(f'{user_id}.txt')
async def handle_add_mail(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_message = message.text
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    if str(user_id) in data["users"]:
     if isinstance(data["users"][f"{user_id}"]["sensers"], list):              data["users"][f"{user_id}"]["sensers"].append(user_message)
    bot.send_message(chat_id, f"Почта добавлена: {user_message}")

    with open('data.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                    
    if str(user_id) in data["users"]:
        if isinstance(data["users"][f"{user_id}"]["sensers"], list):              data["users"][f"{user_id}"]["sensers"].append(user_message)
        bot.send_message(chat_id, f"Почта добавлена: {user_message}")

        with open('data.json', 'w') as json_file:
          json.dump(data, json_file, indent=4)
    else:
        bot.send_message(chat_id, "📞Ошибка в получение списка почт напишите в поддержку.")




@bot.callback_query_handler(func=lambda call: call.data == "mail")
async def listmail(call):
    markup = types.InlineKeyboardMarkup()
    btn_list_mail = types.InlineKeyboardButton(callback_data='listmail', text='Мои почты📨')
    btn_clear_mail = types.InlineKeyboardButton(callback_data='clearmail', text='Удалить все почты🚽')
    btn_add_mail = types.InlineKeyboardButton(callback_data='setupemail', text='Добавить почту➕')
    btn_add_back = types.InlineKeyboardButton(callback_data='back', text='Назад🔙')

    markup.add(btn_add_mail, btn_clear_mail)
    markup.add(btn_list_mail, btn_add_back)

    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                         message_id=call.message.message_id, 
                                         reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data == 'back')
async def handle_back(call):
    user_id = call.from_user.id
    user_username = call.from_user.username


    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        user_id_str = str(user_id)
        data['users'][user_id_str]['username'] = user_username


    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    mode_send = data['users'][user_id_str]['mode']
    photo_path = 'net.jpg'


    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_account = telebot.types.InlineKeyboardButton(callback_data='account', text='Профиль📋')
    btn_report = telebot.types.InlineKeyboardButton(callback_data='reportt', text='SMPT SNOS⛔️')
    btn_reportt = telebot.types.InlineKeyboardButton(callback_data='reporttt', text='WEB SNOS🕸')
    btn_mail = telebot.types.InlineKeyboardButton(callback_data='mail', text='Почты📩')
    btn_pomoch = telebot.types.InlineKeyboardButton(callback_data='pomoch', text='Руководство🛠', url="https://telegra.ph/Rukovodstvo-dlya-snosera-GooseSnoser-11-13")
    btn_tgk = telebot.types.InlineKeyboardButton(call_data='tgk', text='Тгк сносера🍭', url="https://t.me/GooseSnosTGK")

    markup.row(btn_account)
    markup.row(btn_report, btn_reportt)
    markup.row(btn_mail, btn_pomoch)
    markup.row(btn_tgk)

    with open(photo_path, 'rb') as photo:
        await bot.send_photo(
            call.message.chat.id,
            photo,
            caption=f'''`👋 Привет! Я Goose Snos, твой помощник в удалении аккаунтов Telegram 💀

👁️ Нашёл нарушение? Отправь ссылку — помогу разобраться! 🚨

👥 Активных пользователей: {len(load_users())}
`''',
            reply_markup=markup,
            parse_mode="Markdown"
        )
            

@bot.callback_query_handler(func=lambda call: call.data == 'clearmail')
async def clear_mail(call):
  
    await bot.send_message(call.message.chat.id, "Все почты удалены!")

@bot.callback_query_handler(func=lambda call: call.data == 'listmail')
async def support(call):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    user_id = call.from_user.id
    sensors = data["users"].get(f"{user_id}", {}).get("sensers", [])
    mails = "\n".join(sensors[:200])
    count_sensers = len(sensors)

    if count_sensers >= 200:
        await bot.send_message(call.message.chat.id, f"Ваши добавленные почты: {count_sensers}\n\n<code>Выше лимита для вывода >150</code>", parse_mode='HTML')
    else:
        await bot.send_message(call.message.chat.id, f"Ваши добавленные почты: {count_sensers}\nПоказаны первые 150 шт.\n\n<code>{mails}</code>", parse_mode='HTML')
    
    await bot.send_message(call.message.chat.id, "Список почт:")

@bot.callback_query_handler(func=lambda call: call.data == 'setupemail')
async def setup_email(call):
    keyboard = types.InlineKeyboardMarkup()
    btn_handle_docs_photo = types.InlineKeyboardButton(callback_data='handle_docs', text='TXT файл')
    btn_addmail = types.InlineKeyboardButton(callback_data='addmail', text='Вручную')
    btn_back = types.InlineKeyboardButton(callback_data='back', text='Назад')

    keyboard.row(btn_handle_docs_photo, btn_addmail)
    await bot.send_message(call.message.chat.id, "<b>Выберите тип добавления</b>", parse_mode='HTML', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "handle_docs")
async def handle_docs(call):
    await bot.send_message(call.message.chat.id, "<b>Пришлите файл с почтами\nПочты должны быть каждая с новой строки, и в формате <code>почта:пароль</code>!</b>", parse_mode='HTML')
    user_states[call.from_user.id] = 'waiting_for_docs'  
@bot.message_handler(content_types=['document'])
async def handle_docs_photo(message):
    user_id = message.from_user.id

    # Проверяем, находится ли пользователь в процессе загрузки почт
    if user_states.get(user_id) != 'waiting_for_docs':
        return 
    
    try:
        MAX_EMAILS = 200  # Максимальное количество почт за одну загрузку
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Сохраняем файл временно на диск
        with open("emails.txt", 'wb') as new_file:
            new_file.write(downloaded_file)

        # Читаем почты из файла
        with open("emails.txt", "r", encoding="utf-8") as f:
            emails = f.readlines()

        # Проверяем, что количество почт в файле не превышает MAX_EMAILS
        if len(emails) > MAX_EMAILS:
            await bot.send_message(message.chat.id, f"<b>АЙ АЙ АЙ нельзя за раз столько добавлять, уменьшите количество почт до ({MAX_EMAILS}) удачи пупсек 😘.</b>", parse_mode='HTML')
            return

        # Проверяем, что все почты в правильном формате
        for email in emails:
            if ":" not in email:
                await bot.send_message(message.chat.id, "<b>Неправильный формат почты. Пожалуйста, убедитесь, что почты находятся в формате <code>почта:пароль</code>.</b>", parse_mode='HTML')
                return

        # Загружаем данные из JSON файла
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)

        # Если данных о пользователе нет, создаём пустую структуру
        if "users" not in data:
            data["users"] = {}
        if f"{user_id}" not in data["users"]:
            data["users"][f"{user_id}"] = {"sensers": []}
        
        # Получаем список уже сохранённых почт
        current_sensers = data["users"][f"{user_id}"]["sensers"]

        # Добавляем новые почты к уже сохранённым, без ограничений
        data["users"][f"{user_id}"]["sensers"].extend(email.strip() for email in emails)

        # Сохраняем обновлённые данные в файл
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        # Сообщаем пользователю, что почты успешно добавлены
        await bot.send_message(message.chat.id, "<b>Почты успешно добавлены!</b>", parse_mode='HTML')

    except Exception as e:
        # В случае ошибки отправляем сообщение с описанием
        await bot.send_message(message.chat.id, f"<b>Ошибка: {e}</b>")

@bot.callback_query_handler(func=lambda call: call.data == "addmail")
async def addmail(call):
    await bot.send_message(call.message.chat.id, "Введите почту в формате <b><code>почта:пароль</code></b>", parse_mode='HTML')
    user_states[call.from_user.id] = 'waiting_for_add_mail'  


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_add_mail')
async def handle_add_mail(message):
    user_id = message.from_user.id
    email = message.text

    if ":" not in email:
        await bot.send_message(message.chat.id, "<b>Неправильный формат. Пожалуйста, убедитесь, что почта в формате <code>почта:пароль</code>.</b>", parse_mode='HTML')
        return

    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    if "users" not in data:
        data["users"] = {}
    if f"{user_id}" not in data["users"]:
        data["users"][f"{user_id}"] = {"sensers": []}

    data["users"][f"{user_id}"]["sensers"].append(email.strip())

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    await bot.send_message(message.chat.id, "<b>Почта добавлена!</b>", parse_mode='HTML')



async def get_day_word(day):
    if day % 10 == 1 and day % 100 != 11:
        return "день"
    elif day % 10 in [2, 3, 4] and day % 100 not in [12, 13, 14]:
        return "дня"
    else:
        return "дней"

@bot.callback_query_handler(func=lambda c: c.data.startswith('check_status'))
async def check_status(callback_query):
    invoice_id = callback_query.data.split('_')[2]
    old_invoice = crypto.get_invoices(invoice_ids=invoice_id)
    status_old_invoice = old_invoice['items'][0]['status']
    user_id = callback_query.from_user.id

    if status_old_invoice == "paid":
        user_username = callback_query.from_user.username
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.send_message(user_id, "Спасибо за оплату!")
        
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        
        new_user_data = {
            "sensers": [],
            "mode": 'free',
            "subscribe": "",
            "user_name": user_username
        }
        data['users'][str(user_id)] = new_user_data
        
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        await update_subscription(user_id, 30)
        await bot.send_message(user_id, "Подписка успешно активирована!")
    elif status_old_invoice == "active":
        await bot.send_message(user_id, f"Вы не оплатили счет №{invoice_id}!")
    else:
        await bot.send_message(user_id, f"Счет №{invoice_id} не найден.")

@bot.callback_query_handler(func=lambda call: call.data == "info")
async def info(call):
    message_text = "GooseSnos * - `это бот сносер в телеграмме через которого вы можете сносить каналы и своих недоброжелателей.`"
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Канал", callback_data='channel'),
        types.InlineKeyboardButton("Поддержка", callback_data='support'),
        types.InlineKeyboardButton("FAQ ?", callback_data='setup_mode'),
        types.InlineKeyboardButton("Назад", callback_data='back')
    )
    await bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "reporttt")
async def support(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Ожидайте следующего обновление...")
    

    await asyncio.sleep(2) 

@bot.callback_query_handler(func=lambda call: call.data == "account")
async def account(call):
    user_id = call.from_user.id
    user_username = call.from_user.username
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    
    subscribe = data['users'][str(user_id)]['subscribe']
    subscribe_date = datetime.strptime(subscribe, "%Y-%m-%d %H:%M:%S.%f")
    days_left = subscribe_date - datetime.now()

    if subscribe_date > datetime.now():
        mode_send = data['users'][str(user_id)]['mode']
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Cвои почты", callback_data='own_mails'),
            types.InlineKeyboardButton("Фри почты", callback_data='free_mails')
            
        )
        message = (
            f"📋Профиль:\n"
            f"📱Данные: `{user_id} | @{user_username}`\n"
            f"📬Режим почт: {mode_send}\n"
            f"🕰дни подписки: `{str(days_left).split('.')[0]}`\n"
            f"🕕Подписка до: `{str(subscribe).split('.')[0]}`"
        )
        await bot.send_message(call.message.chat.id, message, parse_mode="Markdown", reply_markup=markup)
    else:
        invoice = crypto.create_invoice(asset='USDT', amount=3)
        pay_url = invoice['pay_url']
        invoice_id = invoice['invoice_id']
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Преобрести Подписку за (3$)", url=pay_url),
            types.InlineKeyboardButton("Проверить оплату", callback_data=f"check_status_{invoice_id}")
        )
        await bot.send_message(call.message.chat.id, "Извините, но у вас нет активной подписки.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ["own_mails", "free_mails"])
async def set_mail_mode(call):
    user_id_str = str(call.from_user.id)
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    data['users'][user_id_str]['mode'] = "own" if call.data == "own_mails" else "free"

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    await bot.send_message(call.message.chat.id, f"Режим почты выбран: {'own (ваши почты)' if call.data == 'own_mails' else 'premuim (почты от владельца)'}", parse_mode='HTML')

async def update_subscription(user_id, days):
    new_expiration_date = datetime.now() + timedelta(days=days)
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    data['users'][str(user_id)]['subscribe'] = f"{new_expiration_date}"
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

async def add_subscribes_days(user_id, days):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    subscribe_date = datetime.strptime(data['users'][str(user_id)]['subscribe'], "%Y-%m-%d %H:%M:%S.%f")
    new_expiration_date = subscribe_date + timedelta(days=days)
    data['users'][str(user_id)]['subscribe'] = f"{new_expiration_date}"
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


@bot.message_handler(commands=['admin'])
async def admin_command(message: types.Message):
    user_id = message.from_user.id
    if user_id in admins:
        data = load_users()
        count_users = len(data)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton('Рассылка📡', callback_data='mailing_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Регистрацияℹ️', callback_data='register_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Выдать сабку✅', callback_data='giving_sub_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Продлить сабку', callback_data='extaccess_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Забрать сабку⛔️', callback_data='remove_subscribe'))
        keyboard.add(types.InlineKeyboardButton('Доб. фри почты', callback_data='add_free_mail'))
        keyboard.add(types.InlineKeyboardButton('Юзеры👨‍👩‍👦‍👦', callback_data='user_bot_subscribers'))
        
        await bot.send_message(user_id,
                               f"☀️ <b>Добро пожаловать в админ панель!</b>\n\n"
                               f"👤 Всего пользователей: <code>{count_users}</code>\n"
                               f"Премиум пользователей: <code>{count_users}</code>\n"
                               f"Администраторов пользователей: <code>{len(admins)}</code>",
                               parse_mode='HTML', reply_markup=keyboard)
    else:
        await bot.send_message(user_id, "❌ Вы не администратор!")
        
def load_users():
    try:
        with open('users.txt', 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []
bot.callback_query_handler(lambda call: call.data == 'register_adminpanel')
async def handle_register_callback(call: types.CallbackQuery):
    await register_user(call.message, call.from_user.id)


async def register_user(message: types.Message, user_id: int):
    if user_id in admins:
        try:
            # Чтение данных из JSON
            with open(data_file, 'r') as json_file:
                data = json.load(json_file)

            # Новые данные пользователя
            new_user_data = {
                "sensers": [],
                "mode": "free",
                "subscribe": "",
                "username": message.from_user.username or "example"
            }
            user_id_str = str(user_id)
            data['users'][user_id_str] = new_user_data

            # Запись обновленных данных в JSON
            with open(data_file, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            # Подтверждение администратору и пользователю
            await bot.send_message(message.chat.id, f"Пользователь с ID {user_id_str} добавлен в БД.")
            await bot.send_message(user_id, "Вам зарегистрирован аккаунт!")
        except Exception as e:
            await bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
    else:
        await bot.send_message(message.chat.id, "У вас нет разрешения для выполнения этой команды!")

@bot.callback_query_handler(lambda call: call.data == 'giving_sub_adminpanel')
async def handle_grant_subscription_callback(call: types.CallbackQuery):
    await grant_subscription(call.message, call.from_user)

# Обновление функции grant_subscription для принятия нужных аргументов
async def grant_subscription(message: types.Message, user):
    if user.id in admins:  # Проверка, является ли пользователь админом
        try:
            # Разделение текста на части, если он содержит user_id и количество дней
            command_parts = message.text.split()
            if len(command_parts) >= 3:  
                user_id = int(command_parts[1])  
                days = int(command_parts[2]) 

                # Вызов функции для обновления подписки
                await update_subscription(user_id, days)
                
                # Подтверждение для администратора и уведомление пользователя
                await bot.send_message(message.chat.id, f"Пользователю с ID {user_id} предоставлена подписка на {days} дней!")
                await bot.send_message(user_id, f"🌟 | Вам выдали подписку на {days} дней!")

            else:
                await bot.send_message(message.chat.id, "Неправильный формат команды. Используйте команду: user_id days")
        except Exception as e:
            await bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
    else:
        await bot.send_message(message.chat.id, "У вас нет разрешения для выполнения этой команды!")


# Функция обновления подписки
async def update_subscription(user_id: int, days: int):
    with open(data_file, 'r') as json_file:
        data = json.load(json_file)

    # Обновление подписки пользователя
    user_id_str = str(user_id)
    if user_id_str in data['users']:
        expiration_date = datetime.now() + timedelta(days=days)
        data['users'][user_id_str]['subscribe'] = expiration_date.strftime('%Y-%m-%d %H:%M:%S.%f')

        # Запись обновленных данных
        with open(data_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    else:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")

@bot.callback_query_handler(lambda call: call.data == 'extaccess_adminpanel')
async def handle_extend_subscription_callback(call: types.CallbackQuery):
    await extend_subscription(call.message, call.from_user.id)

# Функция продления подписки
async def extend_subscription(message: types.Message, admin_id: int):
    if admin_id == owner_id:  
        try:
            command_parts = message.text.split()
            if len(command_parts) == 3:
                user_id = int(command_parts[1])
                days = int(command_parts[2])

                # Продление подписки пользователя
                add_subscribes_days(user_id, days)
                
                # Уведомление администратора и пользователя
                await bot.send_message(message.chat.id, f"Пользователю с ID {user_id} добавлено {days} дней к подписке!")
                await bot.send_message(user_id, f"🌟 | Вам продлили подписку на {days} дней!")

            else:
                await bot.send_message(message.chat.id, "Неправильный формат команды. Используйте команду: user_id days")
        except Exception as e:
            await bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
    else:
        await bot.send_message(message.chat.id, "У вас нет разрешения для выполнения этой команды!")

# Функция добавления дней к подписке
def add_subscribes_days(user_id: int, days: int):
    with open(data_file, 'r') as json_file:
        data = json.load(json_file)

    user_id_str = str(user_id)
    if user_id_str in data['users']:
        current_date = datetime.now()
        user_sub_date = data['users'][user_id_str].get("subscribe")
        
        if user_sub_date:
            expiration_date = datetime.strptime(user_sub_date, '%Y-%m-%d %H:%M:%S.%f')
        else:
            expiration_date = current_date

        # Продление на указанное количество дней
        new_expiration_date = expiration_date + timedelta(days=days)
        data['users'][user_id_str]['subscribe'] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S.%f')

        # Запись обновленных данных
        with open(data_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    else:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")


@bot.message_handler(commands=['rasul'])
async def start_mailing(message: types.Message):
    user_id = message.from_user.id

    if user_id not in admins:
        await bot.send_message(user_id, "❌ У вас нет прав для выполнения этой команды!")
        return

  
    text = message.text[len("/rasul "):].strip()
    if not text:
        await bot.send_message(user_id, "❌ Введите текст для рассылки вместе с командой. Пример: /rasul <текст>")
        return

   
    if "http" in text and not re.search(r"https://t\.me/", text):
        await bot.send_message(
            message.chat.id, 
            "❌ Неправильная ссылка: если вы включаете ссылку, она должна начинаться с https://t.me/"
        )
        return


    users = load_users()
    for user in users:
        try:
            await bot.send_message(user, text)
        except Exception:

            continue


@bot.message_handler(commands=['extaccess'])
async def grant_subscription(message: types.Message):
    if message.from_user.id == owner_id:
        try:
            command_parts = message.text.split()
            if len(command_parts) == 3:
                user_id = int(command_parts[1])
                days = int(command_parts[2])

                add_subscribes_days(user_id, days)
                await bot.reply_to(message, f"Пользователю с ID {user_id} добавлено {days} дней к подписке!")
                await bot.send_message(user_id, f"  | Вам продлили подписку на {days} дней!")

            else:
                await bot.reply_to(message, "Неправильный формат команды. Используйте /extaccess user_id days")
        except Exception as e:
            await bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        await bot.reply_to(message, "У вас нет разрешения для выполнения этой команды!")


@bot.message_handler(commands=['givesub'])
async def grant_subscription(message: types.Message):
    if message.from_user.id in admins:  
        try:
            command_parts = message.text.split()
            if len(command_parts) >= 3:  
                user_id = int(command_parts[1])  
                days = int(command_parts[2]) 

                await update_subscription(user_id, days)  
                await bot.reply_to(message, f"Пользователю с ID {user_id} предоставлена подписка на {days} дней!")
                await bot.send_message(user_id, f" 🌟 | Вам выдали подписку на {days} дней!")

            else:
                await bot.reply_to(message, "Неправильный формат команды. Используйте /givesub user_id days")
        except Exception as e:
            await bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        await bot.reply_to(message, "У вас нет разрешения для выполнения этой команды!")

@bot.message_handler(commands=['unsub'])
async def handle_messages(message: Message):
    # Обработка команды /unsub
    if message.text.startswith('/unsub'):
        user_id = message.from_user.id
        # Проверка на администратора
        if user_id not in admins:
            await bot.send_message(message.chat.id, "❌ У вас нет прав для выполнения этой команды!")
            return

        # Получение ID пользователя для отписки
        try:
            user_id_to_unsub = int(message.text.split()[1])
        except (IndexError, ValueError):
            await bot.send_message(message.chat.id, "Пожалуйста, укажите корректный ID пользователя после команды.")
            return

        # Чтение данных из JSON
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)

            # Проверка, существует ли пользователь в данных
            user_id_str = str(user_id_to_unsub)
            if user_id_str not in data['users']:
                await bot.send_message(message.chat.id, "Пользователь не найден в базе данных.")
                return

            # Обновление подписки пользователя
            data['users'][user_id_str]['subscribe'] = f"{datetime.now()}"

            # Сохранение данных обратно в JSON
            with open('data.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            # Уведомление об успешной отписке
            await bot.send_message(message.chat.id, f"Подписка у пользователя {user_id_to_unsub} была успешно забрана.")
            await bot.send_message(user_id_to_unsub,
                                   "❌ | У вас была забрана подписка!\nЕсли не согласны с решением, свяжитесь: @fucking_goose")
        except Exception as e:
            await bot.send_message(message.chat.id, "Произошла ошибка при выполнении команды.")
            print(f"Ошибка: {e}")
            

@bot.message_handler(commands=['register'])
async def register_user(message: types.Message):
    if message.from_user.id in admins:
        try:
            command_parts = message.text.split()
            if len(command_parts) == 2:  
                user_id = int(command_parts[1])
                with open('data.json', 'r') as json_file:
                    data = json.load(json_file)

                new_user_data = {
                    "sensers": [],
                    "mode": "free",
                    "subscribe": "",
                    "username": message.from_user.username or "example"
                }
                user_id_str = str(user_id)
                data['users'][user_id_str] = new_user_data

                with open('data.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                await bot.reply_to(message, f"Пользователь с ID {user_id_str} добавлен в БД.")
                await bot.send_message(user_id, "  | Вам зарегистрирован аккаунт!")
            else:
                await bot.reply_to(message, "Неправильный формат команды. Используйте /register user_id")
        except Exception as e:
            await bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        await bot.reply_to(message, "У вас нет разрешения для выполнения этой команды!")





sent_messages = 0
failed_messages = 0

@bot.callback_query_handler(func=lambda call: call.data == "reportt")
async def report_type_selection(call):
    user_id = call.from_user.id

    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    subscribe = data['users'][f'{user_id}']['subscribe']
    subscribe_date = datetime.strptime(subscribe, "%Y-%m-%d %H:%M:%S.%f")

    if subscribe_date > datetime.now():
        markup = telebot.types.InlineKeyboardMarkup()
        for i, subject in enumerate(subjects):
            btn_report_type = telebot.types.InlineKeyboardButton(callback_data=f'report_type_{i}', text=subject)
            markup.add(btn_report_type)

        await bot.send_message(call.message.chat.id, "Выберите тип жалобы:", reply_markup=markup, parse_mode='HTML')
    else:
        invoice = crypto.create_invoice(asset='USDT', amount=2)
        pay_url = invoice['pay_url']
        invoice_id = invoice['invoice_id']
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Преобрести Подписку за (2$)", url=pay_url))
        keyboard.add(telebot.types.InlineKeyboardButton("Проверить оплату", callback_data=f"check_status_{invoice_id}"))
        await bot.send_message(call.message.chat.id, "Извините, но у вас нет активной подписки.", reply_markup=keyboard)
        

@bot.callback_query_handler(func=lambda call: call.data.startswith("report_type"))
async def report_type_selected(call):
    user_id = call.from_user.id
    
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        
    subscribe = data['users'][f'{user_id}']['subscribe']
    subscribe_date = datetime.strptime(subscribe, "%Y-%m-%d %H:%M:%S.%f")
    
    if subscribe_date > datetime.now():
        try:
            report_type_index = int(call.data.split("_")[2])
            report_type = subjects[report_type_index]
            
            await bot.send_message(call.message.chat.id, f"Вы выбрали тип жалобы: {report_type}")

   
            logging.info(f"User {user_id} выбрал тип жалобы: {report_type}")

 
            if user_id not in user_states or "link_sent" not in user_states[user_id]:
                await bot.send_message(call.message.chat.id,
                                       "Теперь отправьте ссылку на нарушение из публичного чата:\nЕсли вы не отправите ссылку на нарушение в формате https://t.me/\nТо бот не отправит сообщения на почту")
                user_states[user_id] = {"report_type": report_type, "link_sent": True}  
            else:
                user_states[user_id]["report_type"] = report_type 
        
        except (IndexError, ValueError):
            await bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, выберите тип жалобы снова.")

    else:
        invoice = crypto.create_invoice(asset='USDT', amount=2)
        pay_url = invoice['pay_url']
        invoice_id = invoice['invoice_id']
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Преобрести Подписку за (2$)", url=pay_url))
        keyboard.add(telebot.types.InlineKeyboardButton("Проверить оплату", callback_data=f"check_status_{invoice_id}"))
        await bot.send_message(call.message.chat.id, "Извините, но у вас нет активной подписки.", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.from_user.id in user_states)
async def handle_report_link(message):
    sent_messages = 0 
    failed_messages = 0  
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        sub = data['users'][f"{user_id}"]['subscribe']
        sub_date = datetime.strptime(sub, '%Y-%m-%d %H:%M:%S.%f')
        curr_time = datetime.now()

        if sub_date > curr_time:
            link = message.text
            if link.startswith("https://t.me/"):
                if last_links.get(user_id) == link:
                    return  
                last_links[user_id] = link


                report_type = user_states[user_id].get("report_type")
                

                if report_type == "first_reason" and "victim" not in user_states[user_id]:
                    await message.reply("Введите имя жертвы:")
                    return

                elif report_type == "second_reason":

                    user_states[user_id]["victim"] = None
                    

                    await message.reply("Пожалуйста, введите дополнительные сведения для второй причины:")
                    return
                

                logging.info(f"User {user_id} отправил ссылку на канал: {link} для типа жалобы: {report_type}")
                print(f"User {user_id} отправил ссылку на канал: {link} для типа жалобы: {report_type}")


                report_texts = {
                    'СПАМ': f"Здравствуйте, уважаемая служба поддержки!\nНа вашей платформе обнаружил(-а) пользователя, который активно распространяет нежелательные сообщения (спам). \nЭто нарушает комфорт общения и, возможно, правила Telegram.\nСсылка на нарушение:\n{link}\nПрошу рассмотреть мое обращение и принять необходимые меры. \nЗаранее благодарю за вашу оперативную помощь. С уважением ",
                    'ДЕСКОЕ ПОРНО': f"Здравствуйте, уважаемая служба поддержки Telegram.\nНа вашей платформе я обнаружил материал, содержащий неприемлемый и незаконный контент, связанный с детской эксплуатацией. \nЭто грубое нарушение закона и представляет серьёзную опасность.\nСсылка на материал:\n{link}\nПрошу вас немедленно рассмотреть данное сообщение и принять соответствующие меры для удаления данного контента и предотвращения его распространения.\nЗаранее благодарю за вашу оперативность и внимание к данной ситуации. С уважением.",
                    'ПОРНО': f"Здравствуйте, уважаемая служба поддержки Telegram.\nНа вашей платформе я обнаружил неподобающий контент, связанный с порнографией, который нарушает правила использования и создает дискомфорт для пользователей.\nСсылка на материал:\n{link}\nПрошу вас рассмотреть данное сообщение и принять меры для удаления этого контента.\nЗаранее благодарю за вашу помощь. С уважением.",
                    'НАРКОТА': f"Здравствуйте, уважаемая служба поддержки Telegram.\nНа платформе обнаружен пользователь, распространяющий материалы, связанные с незаконными веществами (наркотиками). \nЭто не только нарушает правила использования Telegram, но и противоречит законодательству.\nСсылка на профиль/контент:\n{link}\nПрошу вас принять меры для блокировки данного пользователя и удаления этого опасного контента.\nЗаранее благодарю за вашу оперативную помощь. С уважением.",
                    'НАСИЛИЕ': f"Здравствуйте, уважаемая служба поддержки Telegram.\nНа вашей платформе я обнаружил(-а) пользователя, который распространяет материалы, содержащие сцены насилия. \nЭтот контент не только нарушает правила использования Telegram, но и может причинить вред пользователям.\nСсылка на профиль/контент:\n{link}\nПрошу вас принять меры для блокировки данного пользователя и удаления опасного контента.\nЗаранее благодарю за вашу оперативную помощь. С уважением.",
                    'ЛИЧНЫЕ ДАННЫЕ': f"Здравствуйте, уважаемая служба поддержки Telegram.\nНа вашей платформе я обнаружил(-а) пользователя, который распространяет личные данные других людей без их согласия.\n Это нарушает правила конфиденциальности и может причинить вред пострадавшим.\nСсылка на профиль/контент:\n{link}\nПрошу вас принять меры для блокировки данного пользователя и удаления этого контента.\nЗаранее благодарю за вашу оперативность и внимание к вопросу. С уважением.",
                    'ЖИВОДЕРСТВО': f"Здравствуйте, уважаемая служба поддержки Telegram.\nНа платформе я обнаружил(-а) пользователя, который публикует контент, связанный с жестоким обращением с животными (живодёрством). \nЭтот материал вызывает шок и нарушает нормы сообщества, создавая вредную и опасную среду для пользователей.\nСсылка на профиль/контент:\n{link}\nПрошу вас незамедлительно принять меры для блокировки данного пользователя и удаления подобного контента.\nЗаранее благодарю за вашу помощь и внимание к данной проблеме. С уважением."

                }
                text = report_texts.get(report_type, f"Неизвестный тип жалобы: {link}")

                recipient = ['stopca@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org', 'sticker@telegram.org', 'support@telegram.org', 'security@telegram.org', 'sms@telegram.org']
                subject = report_type

                mode_send = data['users'][str(user_id)]['mode']
                sensers = []
                count_sensers = 0
    
                if mode_send == 'own':
                    sensers = data["users"][str(user_id)]["sensers"]
                    count_sensers = len(sensers)
                    await bot.send_message(chat_id, f"Старт!✅\nКол-во своих почт: {count_sensers}")

                    for email in sensers:
                        for receiver in recipient:
                        
                         if ":" in email:    
                            domain_email, password = email.split(":")
                            try:
                                await send_email(receiver, domain_email, password, subject, text, user_id, chat_id)
                                sent_messages += 1
                                
                            except Exception as e:
                                failed_messages += 1
                                
                    await bot.send_message(chat_id, f"Успешно Репортов: {sent_messages} шт. ✅\nНе успешно: {failed_messages} репортов. ❌")
                    sent_messages = 0
                    failed_messages = 0
                    
                elif mode_send == 'free':
                    with open('freesenders.json', 'r') as js_file:
                        freemail = json.load(js_file)
                        sensers = freemail["sensers"]
                        count_sensers = len(sensers)
                        await bot.send_message(chat_id, f"Старт!✅\nКол-во премиум почт от гуся: {count_sensers}")

                        for email in sensers:
                            for receiver in recipient:
                                
                             if ":" in email:
                                domain_email, password = email.split(":")
                                try:
                                    await send_email(receiver, domain_email, password, subject, text, user_id, chat_id)
                                    sent_messages += 1
                                    
                                except Exception as e:
                                    failed_messages += 1
                                    
                    await bot.send_message(chat_id, f"Успешно Репортов: {sent_messages} шт. ✅\nНе успешно: {failed_messages} репортов. ❌")
                    sent_messages = 0
                    failed_messages = 0

            else:
                await bot.send_message(chat_id, "Неправильная ссылка: должна начинаться с https://t.me/", parse_mode='HTML')
   
            
        else:
            invoice = crypto.create_invoice(asset='USDT', amount=3)
            pay_url = invoice['pay_url']
            invoice_id = invoice['invoice_id']
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("Купить Подписку (3$ 30days)", url=pay_url))
            keyboard.add(types.InlineKeyboardButton("Проверить оплату", callback_data=f"check_status_{invoice_id}"))
            await bot.send_message(chat_id, "Подписка истекла. ❌", reply_markup=keyboard)
            
async def remove_email(user_id, email_to_remove):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    sensers = data["users"][str(user_id)]["sensers"]
    if email_to_remove in sensers:
        sensers.remove(email_to_remove)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


async def send_email(receiver, sender, password, subject, body, user_id, chat_id):
    service = None
    smtp_server = ''
    smtp_port = 587

    if '@gmail.com' in sender:
        service = 'gmail'
        smtp_server = 'smtp.gmail.com'
    elif '@outlook.com' in sender or '@hotmail.com' in sender or '@live.com' in sender:
        service = 'hotmail'
        smtp_server = 'smtp-mail.outlook.com'
    elif '@mail.ru' in sender:
        service = 'mail'
        smtp_server = 'smtp.mail.ru'
    elif '@rambler.ru' in sender:
        service = 'rambler'
        smtp_server = 'smtp.rambler.ru'

    if service is None:
        await remove_email(user_id, f'{sender}:{password}')
        await bot.send_message(chat_id, f"Неподдерживаемая почта: {sender}")
        return

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(body))

    try:
        await aiosmtplib.send(
            msg,
            hostname=smtp_server,
            port=smtp_port,
            username=sender,
            password=password,
            start_tls=True
        )
    except aiosmtplib.SMTPException:

        await remove_email(user_id, f'{sender}:{password}')
        return  



subjects = [
    'СПАМ',
    'ДЕСКОЕ ПОРНО',
    'ПОРНО',
    'НАРКОТА',
    'НАСИЛИЕ',
    'ЛИЧНЫЕ ДАННЫЕ',
    'ЖИВОДЕРСТВО'
]

if __name__ == '__main__':
    sent_messages = 0
    failed_messages = 0

    async def main_loop():
        while True:
            try:
                await bot.polling(non_stop=True)
            except Exception as e:
                print(f"Ошибка: {e}")
                await asyncio.sleep(10)

    asyncio.run(main_loop())