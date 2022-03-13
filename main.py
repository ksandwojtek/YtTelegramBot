from dotenv import load_dotenv
import datetime
import json
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
from youtube import get_yt_video, get_yt_sound
import requests

from colorama import init, Fore
init(autoreset=True)

load_dotenv("config.env")

sys.path.append("./libs")

api_key = os.getenv('TOKEN')
admin = os.getenv('ADMIN')
print(Fore.GREEN + "[+] Bot is starting...")
bot = telebot.TeleBot(api_key, parse_mode=None)

def statsUpdate(link_count=False, user_count=False):
    with open('data.json', 'r') as f:
        data = json.load(f)

    if user_count:
        data["users"] += 1
    if link_count:
        data["link"] += 1

    with open('data.json', 'w') as f:
        try:
            json.dump(data, f)
        except Exception as e:
            print(e)

    return


def getStats(link_count=False, user_count=False):
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()

    if user_count:
        return data["users"]
    if link_count:
        return data["link"]

    return


def db_check(msg):
    with open('user_data.json', 'r+') as f:
        data = json.load(f)
        if str(msg.from_user.id) not in data["userdata"]:
            data["userdata"][msg.from_user.id] = {
                "username": msg.from_user.username,
                "first_name": msg.from_user.first_name,
                "last_name": msg.from_user.last_name,
                "id": msg.from_user.id
            }
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        else:
            pass

@bot.message_handler(commands=['start'])
def start(message):
    db_check(message)
    statsUpdate(user_count=True)


@bot.message_handler(commands=['help'])
def help(message):
    db_check(message)
    bot.send_message(
        message.chat.id, "Send link to download a video or use /stats to see stats")

@bot.message_handler(commands=['stats'])
def stats(message):
    db_check(message)
    users = getStats(user_count=True)
    link_sent = getStats(link_count=True)
    bot.send_message(message.chat.id, f"Users: {users}")
    bot.send_message(message.chat.id, f"Generated videos: {link_sent}")

def extract_arg(arg):
    return arg.split()[1:]


def dict_to_list(dictionary: dict):
    return dict.keys()


@bot.message_handler(commands=['announce'])
def announce(message):
    db_check(message)
    if message.from_user.id == int(admin):
        arg_list = extract_arg(message.text)
        msg = ' '.join([str(elem) for elem in arg_list])
        with open("user_data.json", "r") as f:
            data = json.load(f)
            for user in data["userdata"]:
                try:
                    bot.send_message(user, f"Announcement:\n{msg}")
                except Exception:
                    pass

@bot.message_handler(commands=['debug'])
def debug(message):
    db_check(message)
    if message.from_user.id == int(admin):
        switch = extract_arg(message.text)
        if switch[0] == "on":
            with open("debug.json", "r+") as f:
                data = json.load(f)
                status = data["status"]
                data["chat_id"] = message.chat.id
                if status is True:
                    bot.send_message(
                        message.chat.id, "Debug mode is already on")
                    return
                if status is False:
                    data["status"] = True
                    bot.send_message(message.chat.id, "Debug mode turned on")
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        elif switch[0] == "off":
            with open("debug.json", "r+") as f:
                data = json.load(f)
                status = data["status"]
                data["chat_id"] = message.chat.id
                if status is False:
                    bot.send_message(
                        message.chat.id, "Debug mode is already off")
                    return
                if status is True:
                    data["status"] = False
                    bot.send_message(message.chat.id, "Debug mode turned off")
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            return


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "video":
        try:
            try:
                bot.send_message(
                    text=f"Starting downloading the video.", chat_id=chat_id)
                video = get_yt_video(Url)
            except Exception as e:
                bot.send_message(
                    text=f"Something went wrong, please try again.\n{e}", chat_id=chat_id)
                return
            size = video[1]
            bot.send_message(
                text=f"Requested video will be sent in few minutes!\n{size}", chat_id=chat_id)
            bot.send_video(video=video[0], chat_id=chat_id,
                           supports_streaming=True, timeout=2 * 3600)
            with open("debug.json", "r+") as f:
                data = json.load(f)
                status = data["status"]
                if status is True:
                    bot.send_message(
                        text=f"(Debug)\n{Url}", chat_id=data["chat_id"])

                    dt = datetime.datetime.fromtimestamp(original_msg.date)
                    dt = dt.strftime("%d-%m-%Y %H:%M:%S")

                    debug_link = {str(original_msg.from_user.id) + "/" + str(original_msg.date): {"url": Url, "user_id": original_msg.from_user.id, "chat_id": original_msg.chat.id, "username": original_msg.from_user.username,
                                                                                        "first_name": original_msg.from_user.first_name, "last_name": original_msg.from_user.last_name, "date": dt}}
                    data["links"].update(debug_link)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
        except Exception as e:
            bot.send_message(
                chat_id=chat_id, text="Requested video is too large or something went wrong! Please try again.")
            return
    elif call.data == "sound":
        try:
            try:
                bot.send_message(
                    text=f"Starting downloading sound.", chat_id=chat_id)
                sound = get_yt_sound(Url)
            except Exception as e:
                bot.send_message(
                    chat_id=chat_id, text=f"Something went wrong, please try again.\n{e}")
                return
            size = sound[1]
            bot.send_message(
                chat_id=chat_id, text=f"Requested sound will be sent in few minutes!\n{size}")
            bot.send_audio(audio=sound[0], chat_id=chat_id, timeout=2 * 3600)
            with open("debug.json", "r+") as f:
                data = json.load(f)
                status = data["status"]
                if status is True:
                    bot.send_message(
                        text=f"(Debug)\n{Url}", chat_id=data["chat_id"])

                    dt = datetime.datetime.fromtimestamp(original_msg.date)
                    dt = dt.strftime("%d-%m-%Y %H:%M:%S")

                    debug_link = {str(original_msg.from_user.id) + "/" + str(original_msg.date): {"url": Url, "user_id": original_msg.from_user.id, "chat_id": original_msg.chat.id, "username": original_msg.from_user.username,
                                                                                        "first_name": original_msg.from_user.first_name, "last_name": original_msg.from_user.last_name, "date": dt}}
                    data["links"].update(debug_link)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
        except Exception as e:
            print(e)
            bot.send_message(
                chat_id=chat_id, text="Requested sound is too large or something went wrong! Please try again.")
            return

    statsUpdate(link_count=True)


@bot.message_handler(func=lambda message: True)
def on_message(message):
    chat_id = message.chat.id
    global original_msg
    global Url
    original_msg = message
    Url = str(message.text)

    if Url.find("http") == -1:
        return

    def gen_markup():
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Mp4", callback_data="video"),
                   InlineKeyboardButton("Mp3", callback_data="sound"))
        return markup

    flag = False
    for link in ["https://www.youtube.com/watch", "https://youtu.be/"]:
        if link in Url:
            flag = True
            break

    if flag:
        bot.reply_to(message, "Choose file format:",
                     reply_markup=gen_markup())


if __name__ == '__main__':
    bot.polling(timeout=10, long_polling_timeout=10)
