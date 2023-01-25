# -*- coding: UTF-8 -*-
import telebot # Telegram API
import config # Telegram API
import requests # IP identity
import qrcode # QR-code
import os # delete QR-code
from telebot import types # Telegram API
from PIL import Image # QR-code

developer = 'https://github.com/kup1o'

ip = requests.get("https://api.ipify.org/?format=json").json()['ip']
bot = telebot.TeleBot(config.TOKEN)
groupID = '' # group id where bot is allowed to work

date_version = "2021.10.24"
version = "21w44"

first_date_version = "2021.09.30"
first_version = "21w40"

# phrases
Monly_group = f"🇬🇧 [EN]\nI'm sorry, but you can only talk with me in {groupID}.\nIf you want to join the group, you can contact my developer @kup1o\n\n🇰🇷 [KR]\n죄송하지만 저와 소통은 {groupID}의 그룹에서만 가능합니다.\n당신이 이 그룹에 입장 요청 받하고 싶다면 저의 개발자 @kup1o에게 연락할 수 있습니다\n\nv. " + version
Mwelcome = "Welcome, {0.first_name}!\nI am {1.first_name}, the helper in this group.\nI'm listening to you!\nYou can check out available commands using /help"
Mhelp = "Available commands:\n/ip - Show me an IP address\n/help - Show me available commands\n/version - Show me the current version\n/qr - Generate a QR"
Mversion = "Current version: "
Mfirstversion = "First version: "
qrlink = ""

def cleanURL(string):
  ret = ''
  skip1c = 0
  skip2c = 0
  for i in string:
    if i == '[':
      skip1c += 1
    elif i == '(':
      skip2c += 1
    elif i == ']' and skip1c > 0:
      skip1c -= 1
    elif i == ')'and skip2c > 0:
      skip2c -= 1
    elif skip1c == 0 and skip2c == 0:
      ret += i
  return ret

@bot.message_handler(commands=['start'])
def welcome(message):
  if message.chat.type == 'group':
    bot.send_message(message.chat.id, Mwelcome.format(message.from_user, bot.get_me()))
  else:
    bot.send_message(message.chat.id, Monly_group.format(message.from_user, bot.get_me()))

@bot.message_handler(commands=['help'])
def commands_help(message):
  if message.chat.type == 'group':
    bot.send_message(message.chat.id, Mhelp)
  else:
    bot.send_message(message.chat.id, Monly_group.format(message.from_user, bot.get_me()))

@bot.message_handler(commands=['ip'])
def commands_ip(message):
  if message.chat.type == 'group':
    bot.send_message(message.chat.id, ip)
  else:
    bot.send_message(message.chat.id, Monly_group.format(message.from_user, bot.get_me()))

@bot.message_handler(commands=['version'])
def commands_version(message):
  if message.chat.type == 'group':
    bot.send_message(message.chat.id, Mversion + version + '(' + date_version + ')\n' + Mfirstversion + first_version + '(' + first_date_version + ')' + "\n\nDeveloper's website: " + developer)
  else:
    bot.send_message(message.chat.id, Monly_group.format(message.from_user, bot.get_me()))

def extract_arg(arg):
  return arg.split()[1:]

@bot.message_handler(commands=['qr'])
def commands_qr(message):
  if message.chat.type == 'group':
    status = extract_arg(message.text)
    status = cleanURL(status) # ['google.com'] => google.com
    qr = qrcode.make(status)
    qr.save('QR.png')
    img = open('QR.png', 'rb')
    bot.send_photo(message.chat.id, photo=img)
    os.remove('QR.png')
  else:
    bot.send_message(message.chat.id, Monly_group.format(message.from_user, bot.get_me()))

bot.polling(none_stop=True)
