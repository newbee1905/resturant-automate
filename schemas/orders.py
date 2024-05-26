from pydantic import BaseModel
from typing import List
from datetime import datetime

from .menu_items import MenuItem

class OrderForm(BaseModel):
	customer_id: int
	items: List[int]
	notes: List[str]

class OrderItem(BaseModel):
	order_id: int
	state: int
	item_id: int
	item: MenuItem

class Order(BaseModel):
	customer_id: int
	items: List[OrderItem]
	created_at: datetime
