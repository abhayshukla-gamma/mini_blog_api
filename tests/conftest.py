import uuid

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()  # pytets framework ke andar aata hai reusable and constint testing env deta hai they manage setup of databases and handle cleanup
def client():  # fixture object jisse ham test karenge fastapi routes
    return TestClient(app)  # appp ko testing env me run jisme testing perform karenge


@pytest.fixture()
def random_user_data():
    return {"email": f"test_{uuid.uuid4()}@gmail.com", "password": "123456"}


@pytest.fixture()
def regestered_user(client, random_user_data):

    # pehle register
    client.post("/auth/register", json=random_user_data)

    # ab login

    response = client.post(
        "/auth/login",
        data={
            "username": random_user_data["email"],
            "password": random_user_data["password"],
        },
    )
    token = response.json()[
        "access_token"
    ]  # this data fron fake server is coming in raw json format .json()convert it into dictionary

    return token
