from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import calculator, csv
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()

origins = ["http://localhost", "http://localhost:8080",
           "http://localhost:5173", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    Start connection to startup.resul
    """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """
    Disconnect from the database.resul
    """
    await database.disconnect()


app.include_router(calculator.router,
                   prefix="/calculator",
                   tags=["calculator"])
app.include_router(csv.router)
