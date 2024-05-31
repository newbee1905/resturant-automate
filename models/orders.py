from dataclasses import dataclass, field
from typing import List
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Enum, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped

from db import Base

from .users import RegularUser
from .menu_items import MenuItem

from dataclasses import dataclass
from datetime import datetime

class OrderItemState(enum.IntEnum):
	Queueing = 1
	Cooking = 2
	Cooked = 3
	Served = 4

OrderItemStates = list(OrderItemState)

class OrderState(enum.IntEnum):
	Reserving = 1
	Paid = 2
	Serving = 3
	Served = 4

OrderStates = list(OrderState)

@dataclass
class OrderItem(Base):
	__tablename__ = "order_items"
	__allow_unmapped__ = True

	id: int = Column(Integer, primary_key=True)
	order_id: int = Column(Integer, ForeignKey("orders.id"))
	state: OrderItemState = Column(Enum(OrderItemState), default=OrderItemState.Queueing)
	item_id: int = Column(Integer, ForeignKey("menu_items.id"))
	item: Mapped = relationship("MenuItem", foreign_keys=[item_id])

@dataclass
class Order(Base):
	__tablename__ = "orders"
	__allow_unmapped__ = True

	id: int = Column(Integer, primary_key=True)
	state: OrderState = Column(Enum(OrderState), default=OrderState.Paid)

	customer_id: int = Column(Integer, ForeignKey("users.id"))
	customer: Mapped = relationship("RegularUser", foreign_keys=[customer_id])
	items: List[Mapped] = relationship("OrderItem", backref="order")
	created_at = Column(DateTime, default=datetime.utcnow, index=True)
