# This file is for generating default data for demoing the application
# as well as for testing purpose
#
# In addition, Manager a.k.a. Admin will need to be manually created

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, SessionLocal
from db import engine

from models.users import RegularUser, Manager
from models.menu_items import MenuItem
from models.orders import Order, OrderItem, OrderItemStates
from order_factory import OrderFactory

import os
import random

import utils

def read_image_file(file_path):
	with open(file_path, 'rb') as file:
		return file.read()

def format_name_from_filename(filename):
	name, _ = os.path.splitext(filename)
	name = name.replace('_', ' ').title()
	return name

if __name__ == "__main__":
	# engine = create_engine('sqlite:///:memory:', echo=True)

	Base.metadata.create_all(engine)

	# Create a session to interact with the database
	session = SessionLocal()
	# Session = sessionmaker(bind=engine)
	# session = Session()


	# menu_items = [
	# 	MenuItem(name="Spaghetti Bolognese", price=12.99),
	# 	MenuItem(name="Margherita Pizza", price=10.99),
	# 	MenuItem(name="Caesar Salad", price=8.99)
	# ]
	image_directory = 'images'
	menu_items = []

	for filename in os.listdir(image_directory):
		if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
			name = format_name_from_filename(filename)
			price = random.randint(20, 25)
			image_path = os.path.join(image_directory, filename)
			thumbnail = read_image_file(image_path)
			menu_items.append(MenuItem(name=name, price=price, thumbnail=thumbnail))

	regular_user = RegularUser(name="John Doe", email="john.doe@gmail.com", password=utils.ph.hash("password"))

	admin_user = Manager(name="Jack Aaron", email="jack.rondo@gmail.com", password=utils.ph.hash("password1"))


	session.add_all(menu_items)
	session.add(regular_user)
	session.add(admin_user)

	session.commit()

	print(menu_items)
	# print(menu_items[0].thumbnail)
	print(regular_user)
	print(admin_user)
