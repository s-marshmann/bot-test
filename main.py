import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from base import Item, CartItem

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

bot = telebot.TeleBot(API_TOKEN)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, добро пожаловать в наш магазин! Введите /help для просмотра доступных команд или /catalog для просмотра товаров.")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это меню помощи\n"
        "/catalog - Показать каталог товаров\n"
        "/cart - Показать содержимое вашей корзины\n"
        "/clear - Очистить содержимое вашей корзины\n"
        "Просто отправьте название товара, чтобы добавить его в корзину.")


@bot.message_handler(commands=['catalog'])
def catalog(message):
    items = session.query(Item).all()
    if items:
        catalog = "Каталог товаров:\n"
        for item in items:
            catalog += f"{item.name} - {item.price:.2f}$\n"
        catalog += "\nВведите название товара, чтобы добавить его в корзину."
    else:
        catalog = "Каталог пуст."
    bot.send_message(message.chat.id, catalog)


@bot.message_handler(commands=['cart'])
def cart(message):
    cart_items = session.query(CartItem).filter_by(user=message.from_user.username).all()
    if cart_items:
        cart = "Ваша корзина:\n"
        total = 0
        for cart_item in cart_items:
            item_total = cart_item.quantity * cart_item.item.price
            cart += f"{cart_item.item.name} - {cart_item.quantity} шт. - {item_total:.2f}$\n"
            total += item_total
        cart += f"\nИтого: {total:.2f}$"
        cart += "\nВведите /checkout для оформления заказа."
    else:
        cart = "Ваша корзина пуста."
    bot.send_message(message.chat.id, cart)


@bot.message_handler(commands=['clear'])
def clear(message):
    session.query(CartItem).filter_by(user=message.from_user.username).delete()
    session.commit()
    bot.send_message(message.chat.id, 'Ваша корзина очищена.')


@bot.message_handler(commands=['checkout'])
def checkout(message):
    cart_items = session.query(CartItem).filter_by(user=message.from_user.username).all()
    if cart_items:
        session.query(CartItem).filter_by(user=message.from_user.username).delete()
        session.commit()
        checkout = "Спасибо, что оформили заказ!\nОжидайте звонка от нашего менеджера."
    else:
        checkout = "Ваша корзина пуста.\nВведите название товара, чтобы добавить его в корзину."
    bot.send_message(message.chat.id, checkout)


@bot.message_handler(func=lambda message: True)
def add_to_cart(message):
    item_name = message.text.strip()
    item = session.query(Item).filter_by(name=item_name).first()
    if item:
        cart_item = session.query(CartItem).filter_by(user=message.from_user.username, item_id=item.item_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user=message.from_user.username, item_id=item.item_id, quantity=1)
            session.add(cart_item)
        session.commit()
        bot.send_message(message.chat.id, f'Товар "{item_name}" добавлен в корзину.')
    else:
        bot.send_message(message.chat.id, 'Товар не найден. Пожалуйста, введите корректное название товара.')


bot.infinity_polling()