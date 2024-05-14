from sqlalchemy.orm import Session

# from . import models, schemas

from models.menu_item import MenuItem
from schemas import menu_item as schemas 

import utils

def get_menu_item_by_id(db: Session, id: int):
	return db.query(MenuItem).filter(MenuItem.id == id).first()

def get_menu_item_by_name(db: Session, name: str):
	return db.query(MenuItem).filter(MenuItem.name == name).first()

def get_menu_items(db: Session, limit_value = 100, offset_value = 0):
	return db.query(MenuItem).limit(limit_value).offset(offset_value).all()

def create_menu_item(db: Session, menu_item: schemas.MenuItemForm):
	try:
		db_menu_item = MenuItem(name=menu_item.name, price=menu_item.price)
		db.add(db_menu_item)
		db.commit()
		db.refresh(db_menu_item)
	except:
		db.rollback()
		raise
	return db_menu_item
