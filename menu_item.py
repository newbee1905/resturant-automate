from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dataclasses import dataclass

class Base(DeclarativeBase):
	pass

@dataclass
class MenuItem(Base):
	__tablename__ = 'menu_items'

	id: int = Column(Integer, primary_key=True)
	name: str = Column(String)
	category: str = Column(String)
	price: float = Column(Float)


if __name__ == "__main__":
	# Create an in-memory SQLite database
	engine = create_engine('sqlite:///:memory:', echo=True)

	# Create the table schema
	Base.metadata.create_all(engine)

	# Create a session to interact with the database
	Session = sessionmaker(bind=engine)
	session = Session()

	# Create some menu items
	menu_items = [
		MenuItem(name="Spaghetti Bolognese", category="Pasta", price=12.99),
		MenuItem(name="Margherita Pizza", category="Pizza", price=10.99),
		MenuItem(name="Caesar Salad", category="Salad", price=8.99)
	]

	# Add menu items to the database
	for item in menu_items:
		session.add(item)

	# Commit the changes
	session.commit()

	# Query and print all menu items
	all_menu_items = session.query(MenuItem).all()
	print("All Menu Items:")
	for item in all_menu_items:
		print(item)
