# Testes para a rota de usuários associados
from fastapi.testclient import TestClient


from routers import router_user_associate

client = TestClient(router_user_associate.router)


def test_view_user_associate():
    response = client.get("/users")
    assert response.json()
    assert response.status_code == 200
    