from sqlalchemy import create_engine
from db import Base

import user
import menu_item
# import order

if __name__ == "__main__":
	engine = create_engine('sqlite:///:memory:', echo=True)

	Base.metadata.create_all(engine)
