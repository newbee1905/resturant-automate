from dataclasses import dataclass, field
from typing import List

from order_context import Queueing, OrderItemContext
from models.orders import Order, OrderItem
from models.menu_items import MenuItem

from sqlalchemy.orm import Session

@dataclass
class OrderFactory():
	_instance = None

	session: Session

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)

		return cls._instance


	def create_order(self, customer_id: int, item_ids: List[int], item_notes: List[str]) -> List[OrderItemContext]:
		# return [OrderItemContext(self.default_state(), item) for item in items]	
		order_item = []
		try:
			order = Order(customer_id=customer_id)
			self.session.add(order)
			self.session.commit()
			self.session.refresh(order)	

			order_items = []
			for i, item_id in enumerate(item_ids):
				order_item = OrderItem(order_id=order.id, item_id=item_id, note=item_notes[i])
				self.session.add(order_item)
				order_items.append(order_item)

			self.session.commit()
			for order_item in order_items:
				self.session.refresh(order_item)	
		except:
			self.session.rollback()
			raise

		return order
