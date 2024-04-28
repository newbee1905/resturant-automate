from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dataclasses import dataclass

class Base(DeclarativeBase):
	pass

@dataclass
class User(Base):
	__tablename__ = 'users'

	id: int = Column(Integer, primary_key=True)
	type: str = Column(String)

	__mapper_args__ = {
		'polymorphic_on': 'type',
	}

@dataclass
class RegularUser(User):
	__mapper_args__ = {
		'polymorphic_identity': 'regular_user',
	}

@dataclass
class KitchenStaff(User):
	__mapper_args__ = {
		'polymorphic_identity': 'kitchen_staff',
	}

@dataclass
class WaitStaff(User):
	__mapper_args__ = {
		'polymorphic_identity': 'wait_staff',
	}

@dataclass
class Manager(User):
	__mapper_args__ = {
		'polymorphic_identity': 'manager',
	}

	def check_order_analytics(self):
		# Implementation of check_order_analytics
		pass

	def check_crowded_times(self):
		# Implementation of check_crowded_times
		pass

	def update_menu_item(self):
		# Implementation of update_menu_item
		pass

if __name__ == "__main__":
	# Create an in-memory SQLite database
	engine = create_engine('sqlite:///:memory:', echo=True)

	# Create the table schema
	Base.metadata.create_all(engine)

	# Create a session to interact with the database
	Session = sessionmaker(bind=engine)
	session = Session()

	# Create instances of users
	kitchen_staff = KitchenStaff()
	wait_staff = WaitStaff()
	manager = Manager()
	regular_user = RegularUser()

	# Add users to the database
	session.add(kitchen_staff)
	session.add(wait_staff)
	session.add(manager)
	session.add(regular_user)

	# Commit the changes
	session.commit()

	# Query all users and print their types
	all_users = session.query(User).all()
	for user in all_users:
		print(user)
