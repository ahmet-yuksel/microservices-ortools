import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

# for Local run
#from vrp_ortools import get_optimal_routes

#for docker container run
from .vrp_ortools import get_optimal_routes


app = FastAPI()

class InputData(BaseModel):
    matrix: list
    vehicles: list
    jobs: list

@app.post("/calc_optimal_route")
async def calc_optimal_route(data:InputData):

    routes = get_optimal_routes(data)
    return routes

# for Local run
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)