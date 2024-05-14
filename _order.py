from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base

from models.user import RegularUser
from models.menu_item import MenuItem
from models.order import Order, OrderItem
from order_factory import OrderFactory

if __name__ == "__main__":
	engine = create_engine('sqlite:///:memory:', echo=True)

	Base.metadata.create_all(engine)

	# Create a session to interact with the database
	Session = sessionmaker(bind=engine)
	session = Session()

	menu_items = [
		MenuItem(name="Spaghetti Bolognese", price=12.99),
		MenuItem(name="Margherita Pizza", price=10.99),
		MenuItem(name="Caesar Salad", price=8.99)
	]

	regular_user = RegularUser(name="John Doe")

	for item in menu_items:
		session.add(item)
	session.add(regular_user)

	session.commit()

	items = [1, 1, 2]

	print(menu_items)
	print(regular_user)

	f = OrderFactory(session)

	order_item_contexts = f.create_order(regular_user.id, items)
	print(order_item_contexts)