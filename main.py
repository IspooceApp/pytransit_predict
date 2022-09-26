
from core.transit_predict import *
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/maris")
async def maris():
    return "chaina"


@app.get("/transit/{num}/{lat}/{long}")
async def transit(num:int, lat: float, long: float):
    return return_data(num, lat, long)

@app.get("/calc/{num}/{lat}/{long}")
async def calc(num:int, lat: float, long: float):
    return calculate_passes(num, lat, long)





