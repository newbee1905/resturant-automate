from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List
from dataclasses import dataclass, field
from functools import cached_property

from order_context import OrderItemContext, Queueing, Served

@dataclass
class Subject(ABC):
	"""
	The Subject interface declares a set of methods for managing subscribers.
	"""

	@abstractmethod
	def attach(self, observer: Observer) -> None:
		"""
		Attach an observer to the subject.
		"""
		pass

	@abstractmethod
	def detach(self, observer: Observer) -> None:
		"""
		Detach an observer from the subject.
		"""
		pass

	@abstractmethod
	def notify(self) -> None:
		"""
		Notify all observers about an event.
		"""
		pass

@dataclass
class OrderSubject(Subject):
	_context: OrderItemContext
	"""
	Context of the order item that is being tracked
	"""

	_observers: List[Observer] = field(default_factory=list)
	"""
	List of subribers.
	"""

	def attach(self, observer: Observer) -> None:
		print(f"Attach observer: {observer}")
		self._observers.append(observer)

	def detach(self, observer: Observer) -> None:
		print(f"Detach observer: {observer}")
		self._observers.remove(observer)

	@cached_property
	def kitchen_staff_observers(self) -> List[KitchenStaffObserver]:
		return [ob for ob in self._observers if isinstance(ob, KitchenStaffObserver)]

	@cached_property
	def wait_staff_observers(self) -> List[WaitStaffObserver]:
		return [ob for ob in self._observers if isinstance(ob, WaitStaffObserver)]

	def notify(self) -> None:
		"""
		Trigger an update in each subscriber.
		"""

		if isinstance(self._context.state, Queueing):
			for ob in self.kitchen_staff_observers:
				ob.update(self)
		elif isinstance(self._context.state, Served):
			while len(self._observers) > 0:
				self.detach(self._observers[0])
		else:
			for ob in self.wait_staff_observers:
				ob.update(self)


	def handle(self) -> None:
		self.notify()
		self._context.state.handle()

@dataclass
class Observer(ABC):
	"""
	The Observer interface declares the update method, used by subjects.
	"""

	@abstractmethod
	def update(self, subject: Subject) -> None:
		"""
		Receive update from subject.
		"""
		pass


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""

@dataclass
class KitchenStaffObserver(Observer):
	def update(self, subject: Subject) -> None:
		print(f"KitchenStaff: Reacted to the event for {subject}")


@dataclass
class WaitStaffObserver(Observer):
	def update(self, subject: Subject) -> None:
		print(f"WaitStaff: Reacted to the event for {subject}")

if __name__ == "__main__":
	context = OrderItemContext(Queueing(), "demo")

	subject = OrderSubject(context)
	print(subject)

	kitchen_staff = KitchenStaffObserver()
	wait_staff = WaitStaffObserver()

	subject.attach(kitchen_staff)
	subject.attach(wait_staff)

	print(subject.kitchen_staff_observers)
	print(subject.wait_staff_observers)

	subject.handle()
	subject.handle()
	subject.handle()
	subject.handle()

	print(subject._observers)
