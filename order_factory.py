from dataclasses import dataclass, field
from typing import List

from order_context import Queueing, OrderItemContext

@dataclass
class OrderFactory():
	default_state = Queueing

	def create_order(self, items: List[str]) -> List[OrderItemContext]:
		return [OrderItemContext(self.default_state(), item) for item in items]	

if __name__ == "__main__":
	menu_items = ["pizza", "burger"]
	f = OrderFactory()
	print(f.create_order(menu_items))
