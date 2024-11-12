from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from shopping_bot.db.base import Item

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

new_item = Item(name="test_item", price=0)
session.add(new_item)
session.commit()

def test_connection():
    assert DATABASE_URL == 'sqlite:///shop.db'

def test_base():
    catalog = session.query(Item).filter_by(name="test_item").all()
    assert catalog.price == 0
    
session.query(Item).filter_by(name="test_item").delete()
session.commit()