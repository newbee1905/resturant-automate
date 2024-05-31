from sqlalchemy.orm import Session

from models.orders import Order, OrderItem, OrderItemState
from schemas import orders as schemas 
from order_factory import OrderFactory

import utils

def get_order_by_id(db: Session, id: int):
	return db.query(Order).filter(Order.id == id).first()

def get_orders(db: Session, skip, limit, from_date, to_date):
	query = db.query(Order)

	if from_date:
		query = query.filter(Order.date >= from_date)
	if to_date:
		query = query.filter(Order.date <= to_date)

	return query.limit(limit).offset(skip).all()

def create_order(factory: OrderFactory, customer_id: int, orders: schemas.OrderForm) -> schemas.Order:
	try:
		db_order = factory.create_order(customer_id, orders.items)
	except:
		raise
	return db_order
