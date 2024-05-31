from dataclasses import dataclass, field
from typing import List

from order_context import Queueing, OrderItemContext
from models.orders import Order, OrderItem
from models.menu_items import MenuItem

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OrderFactory():
	_instance = None

	session: Session

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)

		return cls._instance


	def create_order(self, customer_id: int, item_ids: List[int]) -> Order:
		"""
		Creates an order for a customer with specified items.

		Args:
			customer_id (int): The ID of the customer placing the order.
			item_ids (List[int]): List of menu item IDs to include in the order.

		Returns:
			Order: The created order with associated order items.

		Raises:
			SQLAlchemyError: If there is an issue with database operations.
			ValueError: If any item_id does not exist.
		"""
		try:
			valid_item_ids = {item.id for item in self.session.query(MenuItem).filter(MenuItem.id.in_(item_ids)).all()}
			for item_id in item_ids:
				if item_id not in valid_item_ids:
					raise ValueError(f"Menu item with ID {item_id} does not exist.")

			order = Order(customer_id=customer_id)
			self.session.add(order)
			self.session.commit()

			order_items = [
				OrderItem(order_id=order.id, item_id=item_id)
				for i, item_id in enumerate(item_ids)
			]
			self.session.add_all(order_items)
			self.session.commit()

			self.session.refresh(order)	
			return order

		except (SQLAlchemyError, ValueError) as e:
			self.session.rollback()
			logger.error(f"Error creating order: {e}")
			raise
