import telebot
from manager import ShopManager, CartManager, API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
shop = ShopManager()
cart = CartManager()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    shop.send_welcome(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    shop.send_help(message)


@bot.message_handler(commands=['catalog'])
def catalog(message):
    shop.catalog(message)


@bot.message_handler(commands=['cart'])
def show_cart(message):
    cart.show_cart(message)


@bot.message_handler(commands=['clear'])
def clear(message):
    cart.clear(message)


@bot.message_handler(commands=['checkout'])
def checkout(message):
    cart.checkout(message)


@bot.message_handler(func=lambda message: True)
def add_to_cart(message):
    shop.add_to_cart(message)


bot.infinity_polling()