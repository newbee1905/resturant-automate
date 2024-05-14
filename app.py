from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Cookie
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse

from db import SessionLocal

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

@app.post("/users/register", response_model=UserSchema.User)
def register(user: UserSchema.UserForm, db: Session = Depends(get_db)):
	db_user = UserService.get_user_by_email(db, email=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	return UserService.create_user(db=db, user=user)

@app.post("/users/login", response_model=UserSchema.User)
def login(user: UserSchema.UserForm, db: Session = Depends(get_db)):
	db_user = UserService.get_user_by_email(db, email=user.email)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	try:
		utils.ph.verify(db_user.password, user.password)
	except:
		raise HTTPException(status_code=401, detail="Wrong password")
	payload = {
		"email": db_user.email,
		"id": db_user.id,
		"name": db_user.name,
		"type": db_user.type,
	}
	response = JSONResponse(content=payload)
	token = utils.jwt_encode(payload)
	response.set_cookie(key="access_token", value=token, httponly=True)
	return response

@app.get("/users/auth", response_model=UserSchema.User)
def auth(access_token: Annotated[str | None, Cookie()] = None):
	try:
		user = utils.jwt_decode(access_token)
	except:
		raise HTTPException(status_code=401, detail="Invalid Token")

	exp = user["exp"]
	user.pop("exp")
	response = JSONResponse(content=user)

	if exp - datetime.now(tz=timezone.utc).timestamp() < 5 * 24 * 60 * 60:
		token = utils.jwt_encode(user)
		response.set_cookie(key="access_token", value=token, httponly=True)

	return response

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
