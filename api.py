from fastapi import FastAPI
from pydantic import BaseModel
import pickle 
import json 
import pandas as pd
from transit_prediction import *
import uvicorn
app = FastAPI()

class BaseInput(BaseModel):
    no_of_transits : int



@app.post('/iss')
def recommend(input_params:BaseInput):
    print(input_params)
    input_data = input_params.json()
    input_dict = json.loads(input_data)
    print(input_dict)
    no_of_transits_ = input_dict['no_of_transits']
    transit_data = return_data(no_of_transits_)
    return transit_data

if __name__ == "__main__":
    uvicorn.run(app)