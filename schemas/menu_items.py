from pydantic import BaseModel

class MenuItemForm(BaseModel):
	name: str
	price: float

class MenuItem(MenuItemForm):
	id: int

	class Config:
		orm_mode = True

class MenuItemUpdate(BaseModel):
	id: int
	name: str | None = None
	price: float | None = None
