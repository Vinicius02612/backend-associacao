from fastapi.testclient import TestClient
import pytest
from routers import router_login
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.schema import UserToken, UserRequest
import os
from dotenv import load_dotenv
from validate_docbr import CPF
from models.models import User

from pathlib import Path

client = TestClient(router_login.router)




# Teste para a funcionalidade de login
def test_login_for_access_token(test_db):
    response = client.post("/login/token", data={"username": "santamaria@gmail.com", "password": "maria@77"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"