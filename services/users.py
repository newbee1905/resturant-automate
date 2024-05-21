from sqlalchemy.orm import Session

# from . import models, schemas

from models.user import User
from schemas import user as schemas 

import utils

def get_user_by_email(db: Session, email: str):
	return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserForm):
	hashed_password = utils.ph.hash(user.password)
	try:
		db_user = User(name=user.name, email=user.email, password=hashed_password, type="regular_user")
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
	except:
		db.rollback()
		raise
	return db_user
