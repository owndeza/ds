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
import telebot
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

last_links = {}
user_states = {}
subscribers = {} 
crypto = pyCryptoPayAPI(api_token="283898:AAM42CGREiemjNaKr0d6P0em8bARI6RLZqv")
bot = AsyncTeleBot('7611702907:AAGz0JVHWKbVAtQIhgwPxNRQIFnunkKwrV4')
owner_id = 5127026939
admins = [7494399049, 5127026939, 6423574058]
report_theme = None
report_text = None

user_states = {}

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
        btn_mail = telebot.types.InlineKeyboardButton(callback_data='mail', text='Почты📩')
        btn_pomoch = telebot.types.InlineKeyboardButton(callback_data='pomoch', text='Помощь в сносере🛠')
  
        markup.row(btn_account, btn_report)
        markup.row(btn_mail, btn_pomoch)

        with open(photo_path, 'rb') as photo:
            await bot.send_photo(message.chat.id, photo,
                           caption=f'''`👋 Привет! Я бот Goose Snos, твой помощник в удалении аккаунтов Telegram 💀

━━━━━━━━━━━━━━━ 👁️ Если заметишь нарушение — отправь ссылку, и я помогу разобраться с нарушителем! 🚨

━━━━━━━━━━━━━━━ 💡 Нужна инструкция? Нажми на кнопку «Помощь в сносере» 🔧, чтобы узнать, как действовать. ━━━━━━━━━━━━━━━

👥 Активных пользователей: {len(load_users())} 💼
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
                           caption=f"Привествую в GooseSnos! \nЦена подписки  - 3$\nЧтобы купить подписку, нажмите Купить Подписку",
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

    # Чтение данных асинхронно
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        user_id_str = str(user_id)
        data['users'][user_id_str]['username'] = user_username

    # Запись данных асинхронно
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    mode_send = data['users'][user_id_str]['mode']
    photo_path = 'net.jpg'

    # Создание кнопок меню
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_account = telebot.types.InlineKeyboardButton(callback_data='account', text='Профиль📋')
    btn_report = telebot.types.InlineKeyboardButton(callback_data='reportt', text='SMPT SNOS⛔️')
    btn_mail = telebot.types.InlineKeyboardButton(callback_data='mail', text='Почты📩')
    btn_pomoch = telebot.types.InlineKeyboardButton(callback_data='pomoch', text='Помощь в сносере🛠')

    markup.row(btn_account, btn_report)
    markup.row(btn_mail, btn_pomoch)

    # Отправка фото и сообщения с кнопками
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(
            call.message.chat.id,
            photo,
            caption=f'''`Привет!

Я бот Goose Snos, созданный для помощи в удалении аккаунтов в Telegram.☠️
➖➖➖➖➖➖➖➖➖
Если ты заметил нарушения в сообщениях или действиях пользователей, просто напиши мне сообщение ссылкой, и я помогу с дальнейшими шагами по их устранению.💤
➖➖➖➖➖➖➖➖➖
Также я могу предоставить инструкции по их удалению. Для этого нажми на кнопку "Помощь в сносере"
👨‍👦Кол-во активных юзеров: {len(load_users())}
`''',
            reply_markup=markup,
            parse_mode="Markdown"
        )
            

@bot.callback_query_handler(func=lambda call: call.data == 'clearmail')
async def clear_mail(call):
    # Здесь можно добавить логику для удаления почт
    await bot.send_message(call.message.chat.id, "Все почты удалены!")

@bot.callback_query_handler(func=lambda call: call.data == 'listmail')
async def support(call):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    user_id = call.from_user.id
    sensors = data["users"].get(f"{user_id}", {}).get("sensers", [])
    mails = "\n".join(sensors[:150])
    count_sensers = len(sensors)

    if count_sensers >= 150:
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
    user_states[call.from_user.id] = 'waiting_for_docs'  # Устанавливаем состояние

@bot.message_handler(content_types=['document'])
async def handle_docs_photo(message):
    user_id = message.from_user.id

    if user_states.get(user_id) != 'waiting_for_docs':
        return  # Если не ожидается файл, игнорируем

    try:
        MAX_EMAILS = 150
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        with open("emails.txt", 'wb') as new_file:
            new_file.write(downloaded_file)

        with open("emails.txt", "r", encoding="utf-8") as f:
            emails = f.readlines()

        if len(emails) > MAX_EMAILS:
            await bot.send_message(message.chat.id, f"<b>АЙ АЙ АЙ нельзя за раз столько добавлять, уменьшите количество почт до ({MAX_EMAILS}) удачи пупсек 😘.</b>", parse_mode='HTML')
            return

        for email in emails:
            if ":" not in email:
                await bot.send_message(message.chat.id, "<b>Неправильный формат почты. Пожалуйста, убедитесь, что почты находятся в формате <code>почта:пароль</code>.</b>", parse_mode='HTML')
                return

        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        if "users" not in data:
            data["users"] = {}
        if f"{user_id}" not in data["users"]:
            data["users"][f"{user_id}"] = {"sensers": []}
        
        current_count = len(data["users"][f"{user_id}"]["sensers"])
        if current_count + len(emails) > MAX_EMAILS:
            await bot.send_message(message.chat.id, f"<b>Превышено максимальное количество почт ({MAX_EMAILS}). Пожалуйста, добавьте меньше почт.</b>", parse_mode='HTML')
            return
        
        data["users"][f"{user_id}"]["sensers"].extend(email.strip() for email in emails)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        
        await bot.send_message(message.chat.id, "<b>Почты успешно добавлены!</b>", parse_mode='HTML')

    except Exception as e:
        await bot.send_message(message.chat.id, f"<b>Ошибка: {e}</b>")

@bot.callback_query_handler(func=lambda call: call.data == "addmail")
async def addmail(call):
    await bot.send_message(call.message.chat.id, "Введите почту в формате <b><code>почта:пароль</code></b>", parse_mode='HTML')
    user_states[call.from_user.id] = 'waiting_for_add_mail'  # Устанавливаем состояние

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
        keyboard.add(types.InlineKeyboardButton('Рассылка', callback_data='mailing_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Выдать сабку', callback_data='giving_sub_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Продлить сабку', callback_data='extaccess_adminpanel'))
        keyboard.add(types.InlineKeyboardButton('Забрать сабку', callback_data='remove_subscribe'))
        keyboard.add(types.InlineKeyboardButton('Доб. фри почты', callback_data='add_free_mail'))
        keyboard.add(types.InlineKeyboardButton('Юзеры', callback_data='user_bot_subscribers'))
        
        await bot.send_message(user_id,
                               f"☀️ <b>Добро пожаловать в админ панель!</b>\n\n"
                               f"👤 Всего пользователей: <code>{count_users}</code>\n"
                               f"Премиум пользователей: <code>{count_users}</code>\n"
                               f"Администраторов пользователей: <code>{len(admins)}</code>",
                               parse_mode='HTML', reply_markup=keyboard)
    else:
        await bot.send_message(user_id, "❌ Вы не администратор!")
        
@bot.callback_query_handler(func=lambda call: call.data == "pomoch")
async def support(call):

    support_text = """
    Вот инструкция для платформы Goose Snos:

    **Правила использования Goose Snos**

    1. **Цель платформы**
       Goose Snos предназначен для выявления и сообщения о нарушениях в Telegram. Используйте его ответственно и в соответствии с законодательством.

    2. **Допустимые причины для сноса**
       Аккаунты могут быть удалены по следующим причинам:
       - Распространение спама
       - Угрозы, запугивание или домогательства
       - Пропаганда насилия или ненависти
       - Размещение незаконного контента (порнография, наркотики и т.д.)
       - Мошенничество и обман

    3. **Процесс подачи сообщения**
       - Укажите конкретные сообщения или действия, которые вы считаете нарушением.
       - Приложите ссылки на соответствующий контент, если это возможно.

    4. **Конфиденциальность и безопасность**
       Все сообщения обрабатываются анонимно. Не делитесь личной информацией других пользователей.

    5. **Ответственность**
       Пользователи, нарушающие эти правила, могут быть заблокированы или исключены из платформы.

    6. **Изменения правил**
       Мы оставляем за собой право вносить изменения в правила в любое время. Обновления будут опубликованы в нашем канале.

    **Часто задаваемые вопросы**

    - **Что за ссылка на нарушение?**
      Данную ссылку вы найдете в публичных чатах, нажимая на сообщения. Там будет кнопка "Копировать ссылку".

    - **За что чаще сносит?**
      За спам, рекламу, живодёрство, порно, дианон и сват.

    - **Какие сносит айдишники или отлеги?**
      Сносер может снести до 3 лет отлеги и айдишники, которые начинаются на 7, 6, 5.

    - **Какие почты лучше всего сносят?**
      Лучше всего сносят gmail, mail.ru, rambler, outlook. Но лучше покупать gmail.

    - **Как правильно добавлять почты?**
      Данный вопрос вы сможете найти в нашем тгк.
    """

    if call.message.text:
        # Редактируем сообщение, если есть текст 
        await bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=support_text, 
            parse_mode="Markdown"
        )
    else:
        # Отправляем новое сообщение, если в исходном нет текста
        await bot.send_message(
            chat_id=call.message.chat.id, 
            text=support_text, 
            parse_mode="Markdown"
        )

           
bot.callback_query_handler(func=lambda call: call.data == "user_bot_subscribers")
async def user_bot_subscribers(call):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    usernames = [user_data.get("username", "Не указано") for user_data in data["users"].values()]
    user_ids = list(data["users"].keys())

    message = "Пользователи с активной подпиской:\n\n"
    for user_id, username in zip(user_ids, usernames):
        message += f"<code>{user_id} @{username}</code>\n"
    await bot.send_message(call.message.chat.id, message, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == "add_free_mail")
async def add_free_mail(call):
    await bot.send_message(call.message.chat.id,
                           "Вы выбрали <b>Добавить почту в фри доступ</b>\nВведите почту в формате <b><code>почта:пароль</code></b>",
                           parse_mode='HTML')
    await bot.register_next_step_handler(call.message, add_free_mail_subproc)


async def add_free_mail_subproc(message):
    user_message = message.text
    with open('freesenders.json', 'r') as json_file:
        data = json.load(json_file)
    data["sensers"].append(user_message)
    with open('freesenders.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    await bot.send_message(message.from_user.id, f"Почта {user_message} добавлена в бесплатный доступ!", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == "remove_subscribe")
async def remove_subscribe(call):
    await bot.send_message(call.message.chat.id,
                           "Вы выбрали <b>забрать сабку</b>\nВведите id пользователя и количество дней пример <b><code>5606138180</code></b>",
                           parse_mode='HTML')
    await bot.register_next_step_handler(call.message, remove_subscribe_subproc)


async def remove_subscribe_subproc(message):
    command_parts = message.text.split()
    if len(command_parts) >= 1:
        try:
            user_id_to_demote = int(command_parts[0])
        except (IndexError, ValueError):
            await bot.send_message(message.chat.id, "Неверный Айди")
            return
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        user_id_str = str(user_id_to_demote)
        data['users'][user_id_str]['subscribe'] = f"{datetime.now()}"
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        await bot.send_message(user_id_to_demote,
                               f" ❌ | У вас Забрали Подписку!\nЕсли не согласны с решением, отпишите: @fucking_goose")
        await bot.send_message(message.from_user.id, f"Вы забрали сабку у пользователя с ID {user_id_to_demote}!", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == "extaccess_adminpanel")
async def extaccess_adminpanel(call):
    await bot.send_message(call.message.chat.id,
                           "Вы выбрали <b>продление</b>\nВведите id пользователя и количество дней пример <b><code>5606138180 1</code></b>",
                           parse_mode='HTML')
    await bot.register_next_step_handler(call.message, extaccess_sub_subproc)


async def extaccess_sub_subproc(message):
    command_parts = message.text.split()
    if len(command_parts) >= 2:
        user_id = int(command_parts[0])
        days = int(command_parts[1])
        try:
            add_subscribes_days(user_id, days)
            await bot.send_message(user_id, f"☀️Вам продлили подписку на {days} {get_day_word(int(days))}!")
            await bot.send_message(message.from_user.id, f"Сабка продлена {user_id} на {days} {get_day_word(int(days))}!", parse_mode='HTML')
        except:
            await bot.send_message(message.from_user.id, f"Сначала выдайте подписку потом продлевайте", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == "giving_sub_adminpanel")
async def giving_sub_adminpanel(call):
    await bot.send_message(call.message.chat.id,
                           "Вы выбрали <b>выдачу сабки</b>\nВведите id пользователя и количество дней пример <b><code>5606138180 1</code></b>",
                           parse_mode='HTML')
    await bot.register_next_step_handler(call.message, giving_sub_subproc)


async def giving_sub_subproc(message):
    command_parts = message.text.split()
    if len(command_parts) >= 2:
        user_id = int(command_parts[0])
        days = int(command_parts[1])
        update_subscription(user_id, days)
        await bot.send_message(user_id, f"☀️Вам выдали подписку на {days} {get_day_word(int(days))}!")
        await bot.send_message(message.from_user.id, f"Сабка выдана {user_id} на {days} {get_day_word(int(days))}!", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'mailing_adminpanel' and call.from_user.id in admins)
async def mailing_callback(call):
    await bot.send_message(call.from_user.id, " | Введите сообщение для рассылки")
    await bot.register_next_step_handler(call.message, mailing_process)


async def mailing_process(message):
    text = message.text
    users = load_users()
    sent_count = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            sent_count += 1
        except:
            pass
    await bot.send_message(message.from_user.id,
                           f" | <b>Рассылка завершена!</b>\n\nМы смогли отправить сообщение {sent_count}/{len(users)} пользователям!",
                           parse_mode='HTML')


@bot.message_handler(commands=['extaccess'])
async def grant_subscription(message):
    if message.from_user.id == owner_id:
        try:
            command_parts = message.text.split()
            if len(command_parts) == 3:
                user_id = int(command_parts[1])
                days = int(command_parts[2])

                add_subscribes_days(user_id, days)
                await bot.reply_to(message, f"Пользователю с ID {user_id} добавлено {days} дней к подписке!")
                await bot.send_message(user_id, f"  | Вам продлили подписку на {days} Дней!")

            else:
                await bot.reply_to(message, "Неправильный формат команды. Используйте /extaccess user_id days")
        except Exception as e:
            await bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        await bot.reply_to(message, "У вас нет разрешения для выполнения этой команды!")


@bot.message_handler(commands=['givesub'])
async def grant_subscription(message: types.Message):
    # Проверяем, является ли пользователь администратором
    if message.from_user.id not in admins:  # Проверяем, есть ли ID пользователя в списке администраторов
        await bot.reply_to(message, "У вас нет разрешения для выполнения этой команды!")
        return

    command_parts = message.text.split()
    if len(command_parts) != 3:  # Убедимся, что есть ровно 3 элемента
        await bot.reply_to(message, "Неправильный формат команды. Используйте /givesub user_id days")
        return

    try:
        user_id = int(command_parts[1])  # Получаем ID пользователя
        days = int(command_parts[2])  # Получаем количество дней

        # Проверка, существует ли пользователь (пример проверки)
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        
        user_id_str = str(user_id)
        if user_id_str not in data.get('users', {}):
            await bot.reply_to(message, f"Пользователь с ID {user_id} не найден в базе данных.")
            return

        # Вызываем асинхронную функцию с await
        await update_subscription(user_id, days)  
        await bot.reply_to(message, f"Пользователю с ID {user_id} предоставлена подписка на {days} дней!")
        await bot.send_message(user_id, f" | Вам выдали подписку на {days} дней!")

    except ValueError:
        await bot.reply_to(message, "ID пользователя и количество дней должны быть целыми числами.")
    except json.JSONDecodeError:
        await bot.reply_to(message, "Ошибка при чтении файла data.json. Проверьте его структуру.")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {e}")





@bot.message_handler(commands=['register'])
async def register_user(message: types.Message):
    if message.from_user.id not in admins:
        await bot.reply_to(message, "У вас нет разрешения для выполнения этой команды!")
        return

    command_parts = message.text.split()
    if len(command_parts) != 2:
        await bot.reply_to(message, "Неправильный формат команды. Используйте /register user_id")
        return

    try:
        user_id = int(command_parts[1])  # Проверка, что ID пользователя — число

        # Проверка, существует ли файл и содержит ли он валидные данные
        if not os.path.exists('data.json'):
            data = {'users': {}}
        else:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)

        # Создание новой записи для пользователя
        new_user_data = {
            "sensers": [],
            "mode": "free",
            "subscribe": "",
            "username": message.from_user.username or "example"
        }
        user_id_str = str(user_id)
        data['users'][user_id_str] = new_user_data

        # Сохранение данных в JSON
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        await bot.reply_to(message, f"Пользователь с ID {user_id_str} добавлен в БД.")
        
        try:
            await bot.send_message(user_id, " | Вам зарегистрирован аккаунт!")
        except Exception as e:
            await bot.reply_to(message, f"Ошибка при отправке сообщения пользователю: {e}")

    except ValueError:
        await bot.reply_to(message, "Неправильный формат ID. Пожалуйста, введите числовой ID пользователя.")
    except json.JSONDecodeError:
        await bot.reply_to(message, "Ошибка при чтении файла data.json. Проверьте его структуру.")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {e}")


@bot.message_handler(commands=['demote'])
async def demote_user(message: types.Message):
    user_id = message.from_user.id
    if user_id in admins:
        try:
            command_parts = message.text.split()
            user_id_to_demote = int(command_parts[1])
        except (IndexError, ValueError):
            await bot.send_message(message.chat.id, "Неверный Айди")
            return
        
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        
        user_id_str = str(user_id_to_demote)
        data['users'][user_id_str]['subscribe'] = f"{datetime.now()}"
        
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        await bot.send_message(message.chat.id, f"Подписка у {user_id_to_demote} забрана.")
        await bot.send_message(user_id_to_demote, " ❌ | У вас Забрали Подписку!\nЕсли не согласны с решением, отпишите: @fucking_goose")
    else:
        await bot.send_message(user_id, "❌ Вы не администратор!")


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
        invoice = crypto.create_invoice(asset='USDT', amount=3)
        pay_url = invoice['pay_url']
        invoice_id = invoice['invoice_id']
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Преобрести Подписку за (3$)", url=pay_url))
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

            # Логируем выбор типа жалобы
            logging.info(f"User {user_id} выбрал тип жалобы: {report_type}")

            # Проверяем, было ли уже отправлено сообщение с просьбой о ссылке
            if user_id not in user_states or "link_sent" not in user_states[user_id]:
                await bot.send_message(call.message.chat.id,
                                       "Теперь отправьте ссылку на нарушающий канал:\nЕсли вы не отправите ссылку на канал в формате https://t.me/\nТо бот не отправит сообщения на почту")
                user_states[user_id] = {"report_type": report_type, "link_sent": True}  
            else:
                user_states[user_id]["report_type"] = report_type 
        
        except (IndexError, ValueError):
            await bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, выберите тип жалобы снова.")

    else:
        invoice = crypto.create_invoice(asset='USDT', amount=3)
        pay_url = invoice['pay_url']
        invoice_id = invoice['invoice_id']
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Преобрести Подписку за (3$)", url=pay_url))
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
                report_type = user_states[user_id]["report_type"]
                

                logging.info(f"User {user_id} отправил ссылку на канал: {link} для типа жалобы: {report_type}")
                print(f"User {user_id} отправил ссылку на канал: {link} для типа жалобы: {report_type}")


                report_texts = {
                    'СПАМ И РЕКЛАМА': f" Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ.Ссылка на нарушение/нарушения - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю.",
                    'ДОКСИНГ': f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. Ссылка на нарушение/нарушения - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                    'ТРОЛИНГ': f"Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. Ссылка на нарушение/нарушения - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                    'ПРОДАЖА НАРКОТЫ': f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает и рекламирует наркотические вещества. Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                    'ПРОДАЖА ЦП': f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает порнографические материалы с участием несовешеннолетних. Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                    'УГНЕТАНИЕ РАСЫ/ВЕРЫ': f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает нацию и религию тем самом разжигает конфликты. Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователб=ю путем блокировки его аккаунта.",
                    'РАСПРОСТРАНЯЕТ РАСЧЛЕНЕНКУ/ЖИВОДЕРКУ': f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирущего контента с убийством людей или животных. Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                    'ПОТАЛКИВАНИЕ К САМОУБИЙСТВУ': f'Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения которые приводят людей к суициду. Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.',
                    'ПОТАЛКИВАНИЕ К ТЕРОРИЗМУ': f' Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения с призывом к террризму.Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.',
                    'УГРОЗЫ СВАТА': f'Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям распростронением личной информации.Ссылка на нарушение - \n{link}. \nПожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.',
                    'СНОС ВИРТ НОМЕРА': f'Добрый день поддержка Telegram! Аккаунт использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться. Ссылка на нарушение/нарушения - \n{link}. \nПрошу разберитесь с этим. Заранее спасибо!',
                    'СНОС ПРЕМКИ': f'Добрый день поддержка Telegram! Аккаунт  приобрёл премиум в вашем мессенджере чтобы рассылать спам-сообщения и обходить ограничения Telegram. Ссылка на нарушение/нарушения - \n{link} . \nПрошу проверить данную жалобу и принять меры!'


                }
                text = report_texts.get(report_type, f"Неизвестный тип жалобы: {link}")

                recipient = ['stopca@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org', 'sticker@telegram.org', 'support@telegram.org']
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
        # Не выводим ошибку в консоль
        await remove_email(user_id, f'{sender}:{password}')
        return  



subjects = [
    'СПАМ И РЕКЛАМА',
    'ДОКСИНГ',
    'ТРОЛИНГ',
    'ПРОДАЖА ЦП',
    'УГНЕТАНИЕ РАСЫ/ВЕРЫ',
    'РАСПРОСТРАНЯЕТ РАСЧЛЕНЕНКУ/ЖИВОДЕРКУ',
    'ПОТАЛКИВАНИЕ К САМОУБИЙСТВУ',
    'ПОТАЛКИВАНИЕ К ТЕРОРИЗМУ',
    'УГРОЗЫ СВАТА',
    'СНОС ВИРТ НОМЕРА',
    'СНОС ПРЕМКИ'
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