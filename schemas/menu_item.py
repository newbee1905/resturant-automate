from pydantic import BaseModel

class MenuItemForm(BaseModel):
	name: str
	price: float

class MenuItem(MenuItemForm):
	id: int

	class Config:
		orm_mode = True
