from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from db import SessionLocal

from schemas import user as UserSchema
from services import user as UserService

import utils

app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post("/users/register", response_model=UserSchema.User)
def register(user: UserSchema.UserForm, db: Session = Depends(get_db)):
	db_user = UserService.get_user_by_email(db, email=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	return UserService.create_user(db=db, user=user)

@app.post("/users/login", response_model=UserSchema.User)
def login(user: UserSchema.UserForm, db: Session = Depends(get_db)):
	db_user = UserService.get_user_by_email(db, email=user.email)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	try:
		utils.ph.verify(db_user.password, user.password)
	except:
		raise HTTPException(status_code=401, detail="Wrong password")
	return db_user
