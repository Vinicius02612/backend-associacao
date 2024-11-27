from fastapi.testclient import TestClient

from main import app

client = TestClient(app)



def test_get_associates():
    response = client.get("/rotuers/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "João",
            "email": "vinicius@nunes",
            "cpf": "123456789",
            "data_nascimento": "12/12/12",
            "senha": "123456",
            "quantidade": 1,
            "cargo": "admin",
            "dtassociacao": "12/12/12",
            "created_at": "12/12/12",
            "updated_at": "12/12/12"
        },
        {
            "id": 2,
            "name": "maria",
            "email": "maria@nunes",
            "cpf": "123456789",
            "data_nascimento": "12/12/12",
            "senha": "123456",
            "quantidade": 1,
            "cargo": "admin",
            "dtassociacao": "12/12/12",
            "created_at": "12/12/12",
            "updated_at": "12/12/12"
        }
    ]