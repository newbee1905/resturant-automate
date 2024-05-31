from pydantic import BaseModel
from typing import List
from datetime import datetime

from .menu_items import MenuItemData
from .users import UserData

class OrderForm(BaseModel):
	items: List[int]

class OrderItem(BaseModel):
	order_id: int
	state: int
	item_id: int
	item: MenuItemData

class Order(BaseModel):
	id: int
	customer_id: int
	customer: UserData
	items: List[OrderItem]
	created_at: datetime
