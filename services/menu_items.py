from sqlalchemy.orm import Session

# from . import models, schemas

from models.menu_items import MenuItem
from schemas import menu_items as schemas 

import utils

def get_menu_item_by_id(db: Session, id: int):
	return db.query(MenuItem).filter(MenuItem.id == id).first()

def get_menu_item_by_name(db: Session, name: str):
	return db.query(MenuItem).filter(MenuItem.name == name).first()

def get_menu_items(db: Session, skip, limit):
	query = db.query(MenuItem)

	return query.limit(limit).offset(skip).all()

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
