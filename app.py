from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Cookie
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from db import SessionLocal
from routers import users as UserRouter
from routers import menu_items as MenuItemRouter
from routers import orders as OrderRouter

from datetime import datetime, timezone

import utils

app = FastAPI()

origins = [
	"http://localhost:5173",
	"http://localhost:8000",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


app.include_router(UserRouter.router)
app.include_router(MenuItemRouter.router)
app.include_router(OrderRouter.router)
