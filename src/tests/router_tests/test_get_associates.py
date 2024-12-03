import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

print(client)

def test_get_associates():
    response = client.get("/routers/")
    assert response.status_code == 200
    assert response.json() == [
    {
        "id": 5,
        "name": "Vinicius",
        "email": "vinicius@gmail.com",
        "cpf": "000.000.00001",
        "data_nascimento": "2000-02-23",
        "senha": "$argon2id$v=19$m=65536,t=3,p=4$T3hHRnhy/WDy7425WS9gfQ$EBqkvKqwA5zi0DCtBl0YjMQjvKJmRwpWCFAp/1Z4lhY",
        "quantidade": 5,
        "cargo": "PRESIDENTE",
        "dtassociacao": "2024-11-28"
    }
    ]