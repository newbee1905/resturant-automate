from dataclasses import dataclass, field
from typing import List

import socket

@dataclass
class Subject:
	observers: List['Observer'] = field(default_factory=list)

	def attach(self, ob: 'Observer') -> None:
		self.observers.append(ob)

	def detach(self, ob: 'Observer') -> None:
		if ob in self.observers:
			self.observers.remove(ob)

	def notify(self, message: str) -> None:	
		for ob in self.observers:
			ob.update(self, message)

@dataclass
class OrderSubject(Subject):
	id: int = field(default=0)

@dataclass
class OrderItemSubject(Subject):
	id: int = field(default=0)

@dataclass
class Observer(socket.socket):
	def update(self, subject: Subject, message: str) -> None:
		try:
			# self.sendall(message.encode('utf-8'))
			print(subject, message)
		except BrokenPipeError:
			subject.detach(self)	

if __name__ == "__main__":
	order = OrderSubject(id=1)
	ob = Observer()
	print(ob)

	order.attach(ob)
	order.notify("test")
