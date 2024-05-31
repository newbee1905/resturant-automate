from pydantic import BaseModel

class UserBase(BaseModel):
	email: str

class UserForm(UserBase):
	password: str

class UserRegisterForm(UserForm):
	name: str
	type: str

class User(UserRegisterForm):
	id: int

	class Config:
		orm_mode = True

class UserData(UserBase):
	name: str
