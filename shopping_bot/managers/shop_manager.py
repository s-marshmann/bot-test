import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from db.base import Item, CartItem

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

bot = telebot.TeleBot(API_TOKEN)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ShopManager:
    def send_welcome(self, message: str) -> None:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, добро пожаловать в наш магазин! Введите /help для просмотра доступных команд или /catalog для просмотра товаров.")

    def send_help(self, message: str) -> None:
        bot.send_message(message.chat.id, "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это меню помощи\n"
        "/catalog - Показать каталог товаров\n"
        "/cart - Показать содержимое вашей корзины\n"
        "/clear - Очистить содержимое вашей корзины\n"
        "Просто отправьте название товара, чтобы добавить его в корзину.")
         
    def catalog(self, message: str) -> None:
        items = session.query(Item).all()
        if items:
            catalog = "Каталог товаров:\n"
            for item in items:
                catalog += f"{item.name} - {item.price:.2f}$\n"
            catalog += "\nВведите название товара, чтобы добавить его в корзину."
        else:
            catalog = "Каталог пуст."
        bot.send_message(message.chat.id, catalog)

    def add_to_cart(self, message: str) -> None:
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