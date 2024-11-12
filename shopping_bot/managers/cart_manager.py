import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from db.base import CartItem

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

bot = telebot.TeleBot(API_TOKEN)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class CartManager:
    def get(self, message: str) -> None:
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

    def clear(self, message: str) -> None:
        session.query(CartItem).filter_by(user=message.from_user.username).delete()
        session.commit()
        bot.send_message(message.chat.id, 'Ваша корзина очищена.')

    def checkout(self, message: str) -> None:
        cart_items = session.query(CartItem).filter_by(user=message.from_user.username).all()
        if cart_items:
            session.query(CartItem).filter_by(user=message.from_user.username).delete()
            session.commit()
            checkout = "Спасибо, что оформили заказ!\nОжидайте звонка от нашего менеджера."
        else:
            checkout = "В корзине пока ничего нет.\nВведите название товара, чтобы добавить его в корзину."
        bot.send_message(message.chat.id, checkout)