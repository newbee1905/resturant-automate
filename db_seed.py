# This file is for generating default data for demoing the application
# as well as for testing purpose
#
# In addition, Manager a.k.a. Admin will need to be manually created

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, SessionLocal
from db import engine

from models.user import RegularUser, Manager
from models.menu_item import MenuItem
from models.order import Order, OrderItem, OrderItemStates
from order_factory import OrderFactory

import utils

if __name__ == "__main__":
	# engine = create_engine('sqlite:///:memory:', echo=True)

	Base.metadata.create_all(engine)

	# Create a session to interact with the database
	session = SessionLocal()
	# Session = sessionmaker(bind=engine)
	# session = Session()


	menu_items = [
		MenuItem(name="Spaghetti Bolognese", price=12.99),
		MenuItem(name="Margherita Pizza", price=10.99),
		MenuItem(name="Caesar Salad", price=8.99)
	]

	regular_user = RegularUser(name="John Doe", email="john.doe@gmail.com", password=utils.ph.hash("password"))

	admin_user = Manager(name="Jack Aaron", email="jack.rondo@gmail.com", password=utils.ph.hash("password1"))


	for item in menu_items:
		session.add(item)
	session.add(regular_user)
	session.add(admin_user)

	session.commit()

	items = [1, 1, 2]

	print(menu_items)
	print(regular_user)
	print(admin_user)

	# f = OrderFactory(session)

	# order_items = f.create_order(regular_user.id, items)
	# print(order_items)

	# order_items[0].state = OrderItemStates[order_items[0].state]
	# session.commit()
	# print(order_items[0])
