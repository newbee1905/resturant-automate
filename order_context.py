from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from models.order import OrderItem

@dataclass
class OrderItemContext:
	"""
	The Context defines the interface of interest to clients. It also maintains
	a reference to an instance of a State subclass, which represents the current
	state of the Context.
	"""

	_state: ItemState
	"""
	A reference to the current state of the Context
	"""

	order_item: OrderItem
	"""
	Order Item details in Database
	"""

	def __post_init__(self) -> None:
		self._state.context = self

	@property
	def state(self):
		return self._state
	
	@state.setter
	def state(self, state: State):
		"""
		Changing the state at runtime
		"""

		print(f"Context: Transition from {type(self.state).__name__} to {type(state).__name__}")
		self._state = state
		self._state.context = self
	
	def request(self):
		self._state.handle()


@dataclass
class ItemState(ABC):
	"""
	The base State class declares methods that all Concrete State should
	implement and also provides a backreference to the Context object,
	associated with the State. This backreference can be used by States to
	transition the Context to another State.
	"""

	context: Optional[Context] = None

	@abstractmethod
	def handle(self) -> None:
		pass


"""
Order Item Different States
"""


@dataclass
class Queueing(ItemState):
	def handle(self) -> None:
		print("Queueing")
		self.context.state = Cooking()

@dataclass
class Cooking(ItemState):
	def handle(self) -> None:
		print("Cooking")
		self.context.state = Cooked()

@dataclass
class Cooked(ItemState):
	def handle(self) -> None:
		print("Cooked")
		self.context.state = Served()

@dataclass
class Served(ItemState):
	def handle(self) -> None:
		print("Served")

if __name__ == "__main__":
	# The client code.

	context = OrderItemContext(Queueing(), "demo")
	context.request()
	context.request()
	context.request()
