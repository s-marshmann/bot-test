from db.base import Item, create_read_only_session


class ShopStorage:
    def get_all(self):
        with create_read_only_session() as session:
            shop_items = session.query(Item).all()
            return shop_items
        
    def get_item(self, name: str):
        with create_read_only_session() as session:
            shop_item = session.query(Item).filter_by(name=name).first()
            return shop_item