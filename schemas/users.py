from pydantic import BaseModel

class UserBase(BaseModel):
	email: str


class UserForm(UserBase):
	password: str


class User(UserBase):
	id: int
	name: str
	type: str

	class Config:
		orm_mode = True
