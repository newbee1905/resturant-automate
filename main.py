from user import RegularUser, KitchenStaff, WaitStaff, Manager
from menu_item import MenuItem

if __name__ == "__main__":
	# Create an in-memory SQLite database
	engine = create_engine('sqlite:///:memory:', echo=True)

	# Create the table schema
	Base.metadata.create_all(engine)

	# Create a session to interact with the database
	Session = sessionmaker(bind=engine)
	session = Session()

	# Create instances of users
	kitchen_staff_1 = KitchenStaff()
	kitchen_staff_2 = KitchenStaff()
	wait_staff = WaitStaff()
	manager = Manager()
	regular_user = RegularUser()

	# Add users to the database
	session.add(kitchen_staff)
	session.add(wait_staff)
	session.add(manager)
	session.add(regular_user)

	menu_items = [
		MenuItem(name="Spaghetti Bolognese", price=12.99),
		MenuItem(name="Margherita Pizza", price=10.99),
		MenuItem(name="Caesar Salad", price=8.99)
	]

	# Add menu items to the database
	for item in menu_items:
		session.add(item)

	# Commit the changes
	session.commit()

	# Query all users and print their types
	all_users = session.query(User).all()
	for user in all_users:
		print(user)
