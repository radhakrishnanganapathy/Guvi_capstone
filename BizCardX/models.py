# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text, Date, Interval, func, extract,ARRAY
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy.orm import Session
from db import Base
from db import get_db

# Define the database connection
# secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit/secrets.toml")

class Card(Base):
     __tablename__ = 'carddata'
     id = Column(Integer,primary_key=True)
     name = Column(String(255))
     position = Column(String(255))
     mobile = Column(ARRAY(String))
     email = Column(String(255))
     website = Column(String(255))
     address = Column(String(255))

     def create_card (db:Session,name,position,mobile,email,website,address):
           db_return = Card(
                 name = name,
                 position = position,
                 mobile = mobile,
                 email = email,
                 website = website,
                 address = address,
           )
           db.add(db_return)
           db.commit()
           db.refresh(db_return)
           return db_return
     def get_card(db:Session):
           db_return = db.query(Card).all()
           return db_return

class CardInfo(Base):
      __tablename__ = 'cardinfo'
      id = Column(Integer,primary_key=True)
      card = Column(Text)

      def full_card (db:Session, card):
            db_return = CardInfo(
                  card = card
            )
            db.add(db_return)
            db.commit()
            db.refresh(db_return)
            return db_return
      def full_text(db:Session):
            db_return = db.query(CardInfo).all()
            return db_return
    