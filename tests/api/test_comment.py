from httpx import AsyncClient

from app.models import Post


async def test_create_comment(client: AsyncClient, test_post: Post) -> None:
    comment_data = {"text": "Текст комментария"}
    response = await client.post(
        f"/api/posts/{test_post.id}/comments", json=comment_data
    )

    assert response.status_code == 201

    data = response.json()
    assert data["text"] == comment_data["text"]
    assert "id" in data
