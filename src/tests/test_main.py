import json

from starlette.testclient import TestClient
from .inputdata import input_data
from .outputdata import output_data
from ..app.main import app

client = TestClient(app)




def test_calc_optimal_route(test_app):

    response = test_app.post("/calc_optimal_route",data=json.dumps(input_data))
    assert response.status_code == 200
    assert response.json() == output_data