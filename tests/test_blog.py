def test_create_blog(client, regestered_user):

    response = client.post(
        "/blog/add",
        json={"title": "test blog", "content": "testing blog content"},
        headers={"Authorization": f"Bearer {regestered_user}"},
    )
    assert response.status_code == 200


def test_all_blogs(client, regestered_user):
    response = client.get(
        "/blog/getblogs", headers={"Authorization": f"Bearer {regestered_user}"}
    )

    assert response.status_code == 200
