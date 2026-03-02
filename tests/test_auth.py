def test_register(client, random_user_data):
    response = client.post("/auth/register", json=random_user_data)
    assert response.status_code == 200


def test_login(client, random_user_data):

    client.post(
        "/auth/register", json=random_user_data
    )  # routes expect karte hai data in json format to usme bheja sake isi liye ye likha hai

    response = client.post(
        "/auth/login",
        data={
            "username": random_user_data["email"],
            # ye yaha apn ne json ki jagah data isi liye kar dia kyuki apn ne login route me oauth2requestform laga rakha hai jo ki form data leta hai json nahi
            "password": random_user_data["password"],
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
