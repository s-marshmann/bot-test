from db.base import CartItem, create_session
from sqlalchemy.orm import joinedload


class CartStorage:
    def get_all(self, user: str):
        with create_session() as session:
            cart_items = session.query(CartItem).options(joinedload(CartItem.item)).filter_by(user=user).all()
            return cart_items
        
    def get_item(self, user: str, item_id: int):
        with create_session() as session:
            cart_item = session.query(CartItem).filter_by(user=user, item_id=item_id).first()
            return cart_item
        
    def add(self, user: str, item_id: int) -> None:
        cart_item = CartItem(user=user, item_id=item_id, quantity=1)
        with create_session() as session:
            session.add(cart_item)
            session.commit()
    
    def increment(self, user: str, item_id: int) -> None:
        with create_session() as session:
            cart_item = session.query(CartItem).filter_by(user=user, item_id=item_id).first()
            cart_item.quantity += 1
            session.commit()
        
    def delete(self, user: str) -> None:
        with create_session() as session:
            session.query(CartItem).filter_by(user=user).delete()
            session.commit()