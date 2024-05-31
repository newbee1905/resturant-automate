from pydantic import BaseModel
from fastapi import UploadFile, File

class MenuItemForm(BaseModel):
	name: str
	price: float
	thumbnail: str | None = None

class MenuItem(BaseModel):
	id: int
	name: str
	price: float
	thumbnail: str

	class Config:
		orm_mode = True

class MenuItemData(BaseModel):
	id: int
	name: str
	price: float

	class Config:
		orm_mode = True

class MenuItemUpdate(BaseModel):
	id: int
	name: str | None = None
	price: float | None = None
	thumbnail: UploadFile | None = File(None)
