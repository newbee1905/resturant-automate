from typing import Annotated, Optional, List

from fastapi import APIRouter, Depends, Cookie, HTTPException, Query

from dependencies import get_user_from_access_token, get_db, get_order_factory
from sqlalchemy.orm import Session

from schemas import orders as OrderSchema
from services import orders as OrderService
from order_factory import OrderFactory

from datetime import datetime

import utils

from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
	prefix="/orders",
	tags=["Orders"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[OrderSchema.Order])
def get_orders(
	from_date: Optional[datetime] = Query(None),
	to_date: Optional[datetime] = Query(None),
	skip: int = 0,
	limit: int = 10,
	db: Session = Depends(get_db),
	access_token: Annotated[str | None, Cookie()] = None,
):
	try:
		user = utils.jwt_decode(access_token)
	except:
		raise HTTPException(status_code=401, detail="Unauthorized to create order item")
	
	orders = OrderService.get_orders(db, skip, limit, from_date, to_date)

	if user["type"] == "regular_user" and user["id"] == orders.customer_id:
		raise HTTPException(status_code=401, detail="Unauthorized to view this order item")

	return orders

@router.get("/{id}", response_model=OrderSchema.Order)
def get_order(id: int, db: Session = Depends(get_db)):
	db_order = OrderService.get_order_by_id(db, id)
	if db_order is None:
		raise HTTPException(status_code=404, detail="Order item not found")
	return db_order

@router.post("/", response_model=OrderSchema.Order)
def create_order(order: OrderSchema.OrderForm, factory: OrderFactory = Depends(get_order_factory), access_token: Annotated[str | None, Cookie()] = None):
	try:
		user = utils.jwt_decode(access_token)
	except:
		raise HTTPException(status_code=401, detail="Unauthorized to create order item")
	
	if user["type"] != "regular_user":
		raise HTTPException(status_code=401, detail="Unauthorized to create order item")

	try:
		order = OrderService.create_order(factory=factory, customer_id=user["id"], orders=order)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=f"{e}")
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"{e}")
	return order
