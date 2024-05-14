from dataclasses import dataclass, field
from typing import List

from order_context import Queueing, OrderItemContext
from models.order import Order, OrderItem
from models.menu_item import MenuItem

from sqlalchemy.orm import Session

@dataclass
class OrderFactory():
	_instance = None

	session: Session

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)

		return cls._instance


	def create_order(self, customer_id: int, item_ids: List[int]) -> List[OrderItemContext]:
		# return [OrderItemContext(self.default_state(), item) for item in items]	
		order = Order(customer_id=customer_id)
		self.session.add(order)
		self.session.commit()

		order_items = []
		for item_id in item_ids:
			order_item = OrderItem(order_id=order.id,  item_id=item_id)
			self.session.add(order_item)
			order_items.append(order_item)

		self.session.commit()
		
		return order_items
