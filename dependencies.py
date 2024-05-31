from typing import Annotated

from schemas import users as UserSchema

from fastapi import Cookie, HTTPException
from db import SessionLocal

from order_factory import OrderFactory

import utils

async def get_user_from_access_token(access_token: Annotated[str | None, Cookie()] = None) -> UserSchema.User:
	try:
		user = utils.jwt_decode(access_token)
	except:
		raise HTTPException(status_code=401, detail="Invalid Token")

	return user

async def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

async def get_order_factory():
	db = SessionLocal()
	order_factory = OrderFactory(session=db)
	try:
		yield order_factory
	finally:
		db.close()
