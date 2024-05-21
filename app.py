from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Cookie
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse

from db import SessionLocal
from routers import users

from schemas import user as UserSchema
from services import user as UserService

from schemas import menu_item as MenuItemSchema
from services import menu_item as MenuItemService

from datetime import datetime, timezone

import utils

app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
	return response

app.include_router(users.router)


@app.get("/menu/{id}", response_model=MenuItemSchema.MenuItem)
def get_menu_item(id: int, db: Session = Depends(get_db)):
	db_menu_item = MenuItemService.get_menu_item_by_id(db, id)
	if db_menu_item is None:
		raise HTTPException(status_code=404, detail="Menu Item not found")
	return db_menu_item

@app.get("/menu/", response_model=list[MenuItemSchema.MenuItem])
def get_menu_items(db: Session = Depends(get_db)):
	return MenuItemService.get_menu_items(db)

@app.post("/menu/", response_model=MenuItemSchema.MenuItem)
def create_menu_item(menu_item: MenuItemSchema.MenuItemForm, db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
	try:
		user = utils.jwt_decode(access_token)
	except:
		raise HTTPException(status_code=401, detail="Unauthorized to create menu item")
	
	if user["type"] != "manager":
		raise HTTPException(status_code=401, detail="Unauthorized to create menu item")

	db_menu_item = MenuItemService.get_menu_item_by_name(db, name=menu_item.name)
	if db_menu_item:
		raise HTTPException(status_code=400, detail="Menu Item already registered")

	return MenuItemService.create_menu_item(db=db, menu_item=menu_item)

@app.put("/menu/", response_model=MenuItemSchema.MenuItem)
def create_menu_item(menu_item: MenuItemSchema.MenuItemUpdate, db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
	try:
		user = utils.jwt_decode(access_token)
	except:
		raise HTTPException(status_code=401, detail="Unauthorized to edit menu item")
	
	if user["type"] != "manager":
		raise HTTPException(status_code=401, detail="Unauthorized to edit menu item")

	db_menu_item = MenuItemService.get_menu_item_by_id(db, id=menu_item.id)
	if db_menu_item is None:
		raise HTTPException(status_code=400, detail="Menu Item not found")

	return MenuItemService.edit_menu_item(db=db, menu_item=menu_item)

