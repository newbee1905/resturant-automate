from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Cookie
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse

from db import SessionLocal
from routers import users as UserRouter
from routers import menu_items as MenuItemRouter
from routers import orders as OrderRouter

from datetime import datetime, timezone

import utils

app = FastAPI()

app.include_router(UserRouter.router)
app.include_router(MenuItemRouter.router)
app.include_router(OrderRouter.router)
