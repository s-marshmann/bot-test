from bot import bot
from managers.shop import ShopManager
from managers.cart import CartManager
from storage.shop import ShopStorage
from storage.cart import CartStorage

shop = ShopManager(shop_storage=ShopStorage(), cart_storage=CartStorage())
cart = CartManager(cart_storage=CartStorage())


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
def get(message):
    cart.get(message)


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