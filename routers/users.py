from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from dependencies import get_user_from_access_token, get_db
from sqlalchemy.orm import Session

from schemas import users as UserSchema
from services import users as UserService

import utils

router = APIRouter(
	prefix="/users",
	tags=["Users"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=UserSchema.User)
def register(user: UserSchema.UserRegisterForm, db: Session = Depends(get_db)):
	db_user = UserService.get_user_by_email(db, email=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	return UserService.create_user(db=db, user=user)

@router.post("/login", response_model=UserSchema.User)
def login(user: UserSchema.UserForm, db: Session = Depends(get_db)):
	db_user = UserService.get_user_by_email(db, email=user.email)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	try:
		utils.ph.verify(db_user.password, user.password)
	except:
		raise HTTPException(status_code=401, detail="Wrong password")
	payload = {
		"email": db_user.email,
		"id": db_user.id,
		"name": db_user.name,
		"type": db_user.type,
	}
	response = JSONResponse(content=payload)
	token = utils.jwt_encode(payload)
	response.set_cookie(key="access_token", value=token, httponly=True)
	return response

@router.get("/auth", response_model=UserSchema.User)
def auth(user: UserSchema.User = Depends(get_user_from_access_token)):
	exp = user["exp"]
	user.pop("exp")
	response = JSONResponse(content=user)

	if exp - datetime.now(tz=timezone.utc).timestamp() < 5 * 24 * 60 * 60:
		token = utils.jwt_encode(user)
		response.set_cookie(key="access_token", value=token, httponly=True)

	return response
