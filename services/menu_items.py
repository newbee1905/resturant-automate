from sqlalchemy.orm import Session

# from . import models, schemas

from models.menu_items import MenuItem
from schemas import menu_items as schemas 
from base64 import b64encode, b64decode

import utils

def get_menu_item_by_id(db: Session, id: int):
	m = db.query(MenuItem).filter(MenuItem.id == id).first()
	return schemas.MenuItem(id=m.id, name=m.name, price=m.price, thumbnaild=b64encode(m.thumbnail).decode('utf-8'))

def get_menu_item_by_name(db: Session, name: str):
	return db.query(MenuItem).filter(MenuItem.name == name).first()

def get_menu_items(db: Session, skip, limit):
	try:
		query = db.query(MenuItem)

		raw_menu_items = query.limit(limit).offset(skip).all()
		menu_items = [schemas.MenuItem(id=m.id, name=m.name, price=m.price, thumbnail=b64encode(m.thumbnail).decode('utf-8')) for m in raw_menu_items]
		return menu_items
	except:
		raise

def create_menu_item(db: Session, menu_item: schemas.MenuItemForm):
	try:
		thumbnail_data = b64decode(menu_item.thumbnail)
		db_menu_item = MenuItem(name=menu_item.name, price=menu_item.price, thumbnail=thumbnail_data)
		db.add(db_menu_item)
		db.commit()
		db.refresh(db_menu_item)
		menu_item = schemas.MenuItem(id=db_menu_item.id, name=db_menu_item.name, price=db_menu_item.price, thumbnail=b64encode(db_menu_item.thumbnail).decode('utf-8'))
		return menu_item
	except Exception as e:
		db.rollback()
		print(e)
		raise
