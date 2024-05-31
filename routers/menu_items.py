from typing import Annotated, List

from fastapi import APIRouter, Depends, Cookie, HTTPException

from dependencies import get_user_from_access_token, get_db
from sqlalchemy.orm import Session

from schemas import menu_items as MenuItemSchema
from schemas import users as UserSchema
from services import menu_items as MenuItemService

from base64 import b64encode

import utils

router = APIRouter(
	prefix="/menu_items",
	tags=["Menu Items"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=MenuItemSchema.MenuItem)
def get_menu_item(id: int, db: Session = Depends(get_db)):
	try:
		db_menu_item = MenuItemService.get_menu_item_by_id(db, id)
		if db_menu_item is None:
			raise HTTPException(status_code=404, detail="Menu Item not found")
		return db_menu_item
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/", response_model=List[MenuItemSchema.MenuItem])
def get_menu_items(
	skip: int = 0,
	limit: int = 20,
	db: Session = Depends(get_db),
):
	try:
		menu_items = MenuItemService.get_menu_items(db, skip, limit)
		return menu_items
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"{e}")

@router.post("/", response_model=MenuItemSchema.MenuItem)
def create_menu_item(
	menu_item: MenuItemSchema.MenuItemForm,
	user: UserSchema.User = Depends(get_user_from_access_token),
	db: Session = Depends(get_db),
):
	exp = user["exp"]
	user.pop("exp")

	try:
		if user["type"] != "manager":
			raise HTTPException(status_code=401, detail="Unauthorized to create menu item")

		db_menu_item = MenuItemService.get_menu_item_by_name(db, name=menu_item.name)
		if db_menu_item:
			raise HTTPException(status_code=400, detail="Menu Item already registered")

		menu_item = MenuItemService.create_menu_item(db=db, menu_item=menu_item)
		print(menu_item)
		return menu_item
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"{e}")

@router.put("/", response_model=MenuItemSchema.MenuItem)
def update_menu_item(menu_item: MenuItemSchema.MenuItemUpdate, db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
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
