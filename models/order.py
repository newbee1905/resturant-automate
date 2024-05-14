from dataclasses import dataclass, field
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, Mapped

from db import Base

from .user import RegularUser
from .menu_item import MenuItem

from dataclasses import dataclass

@dataclass
class OrderItem(Base):
	__tablename__ = "order_items"
	__allow_unmapped__ = True

	id: int = Column(Integer, primary_key=True)
	order_id: int = Column(Integer, ForeignKey("orders.id"))

	item_id: int = Column(Integer, ForeignKey("menu_items.id"))
	item: Mapped = relationship("MenuItem", foreign_keys=[item_id])

@dataclass
class Order(Base):
	__tablename__ = "orders"
	__allow_unmapped__ = True

	id: int = Column(Integer, primary_key=True)
	customer_id: int = Column(Integer, ForeignKey("users.id"))
	customer: Mapped = relationship("RegularUser", foreign_keys=[customer_id])
	items: List[Mapped] = relationship("OrderItem", backref="order")

# if __name__ == "__main__":
# 	menu_items = ["pizza", "burger"]
# 	f = OrderFactory()
# 	print(f.create_order(menu_items))

if __name__ == "__main__":
	# Create an in-memory SQLite database
	engine = create_engine('sqlite:///:memory:', echo=True)

	# Create the table schema
	Base.metadata.create_all(engine)
