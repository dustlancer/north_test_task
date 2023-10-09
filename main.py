from fastapi import FastAPI, APIRouter
from routers import coil
from db import models
from db.database import engine


app = FastAPI()

app.include_router(coil.router)


models.Base.metadata.create_all(engine)
