from httpx import AsyncClient

from app.models import Post


async def test_get_posts_empty(client: AsyncClient) -> None:
    response = await client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_post(client: AsyncClient) -> None:
    post_data = {
        "title": "Новый тестовый пост",
        "content": "Текст нашего тестового поста",
    }

    response = await client.post("/posts", json=post_data)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == post_data["title"]
    assert "id" in data


async def test_get_posts_with_data(client: AsyncClient, test_post: Post) -> None:
    response = await client.get("/posts")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_post.title
    assert data[0]["id"] == test_post.id
