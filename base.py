from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    quantity = Column(Integer, default=1)
    item = relationship("Item")

# Base.metadata.create_all(engine)


# new_item = Item(name="iPhone 16 Pro Max", price=1499.00)
# session.add(new_item)
# new_item = Item(name="iPhone 15 Pro", price=999.00)
# session.add(new_item)
# new_item = Item(name="iPhone 14 Plus", price=799.00)
# session.add(new_item)
# new_item = Item(name="Macbook Pro 16 2024", price=1999.00)
# session.add(new_item)
# new_item = Item(name="iMac 2023", price=1399.00)
# session.add(new_item)
# session.commit()
# item = session.query(Item).filter_by(name="iMac 2023").first()
# print(item.item_id, item.name, item.price)