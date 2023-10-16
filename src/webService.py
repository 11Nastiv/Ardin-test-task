from fastapi import FastAPI
from src.routes import userApi, positionApi

app = FastAPI()

app.include_router(positionApi.router, tags=["position"])
app.include_router(userApi.router, tags=["user"])