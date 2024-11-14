from bot import bot


class ShopManager:
    def __init__(self, cart_storage, shop_storage) -> None:
        self._cart_storage = cart_storage
        self._shop_storage = shop_storage

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
        items = self._shop_storage.get_all()
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
        item = self._shop_storage.get_item(name = item_name)
        if item:
            cart_item = self._cart_storage.get_item(user=message.from_user.username, item_id=item.item_id)
            if cart_item:
                self._cart_storage.increment(user=message.from_user.username, item_id=item.item_id)
            else:
                self._cart_storage.add(user=message.from_user.username, item_id=item.item_id)
            bot.send_message(message.chat.id, f'Товар "{item_name}" добавлен в корзину.')
        else:
            bot.send_message(message.chat.id, 'Товар не найден. Пожалуйста, введите корректное название товара.')