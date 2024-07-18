from fastapi import FastAPI

from app.router import router as meteo_router

app = FastAPI()
app.include_router(meteo_router)
