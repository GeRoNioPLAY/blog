from httpx import AsyncClient

from app.models import Comment, Post


async def test_get_posts_empty(client: AsyncClient) -> None:
    response = await client.get("/api/posts")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_post(client: AsyncClient) -> None:
    post_data = {
        "title": "Новый тестовый пост",
        "content": "Текст нашего тестового поста",
    }

    response = await client.post("/api/posts", json=post_data)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == post_data["title"]
    assert "id" in data


async def test_get_posts_with_data(client: AsyncClient, test_post: Post) -> None:
    response = await client.get("/api/posts")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_post.title
    assert data[0]["id"] == test_post.id


async def test_get_post_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/posts/999")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data


async def test_create_post_invalid_data(client: AsyncClient) -> None:
    post_data: dict[str, str] = {}

    response = await client.post("/api/posts", json=post_data)

    assert response.status_code == 422

    errors = response.json()["detail"]
    error_fields = [err["loc"][-1] for err in errors]

    assert "title" in error_fields
    assert "content" in error_fields

    assert all(err["type"] == "missing" for err in errors)


async def test_get_posts_with_comments(
    client: AsyncClient, test_comment: Comment
) -> None:
    response = await client.get(f"/api/posts/{test_comment.post_id}")

    assert response.status_code == 200

    data = response.json()
    data_comments = data["comments"]

    assert len(data_comments) == 1
    assert data_comments[0]["id"] == test_comment.id
    assert data_comments[0]["text"] == test_comment.text
