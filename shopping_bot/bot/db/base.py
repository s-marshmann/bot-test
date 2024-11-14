from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@contextmanager
def create_session(session_maker = Session):
    new_session = session_maker()
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise 
    finally:
        new_session.close()

@contextmanager
def create_read_only_session(session_maker = Session):
    new_session = session_maker()
    try:
        yield new_session 
    finally:
        new_session.close()

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