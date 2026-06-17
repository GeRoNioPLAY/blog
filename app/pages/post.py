from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from app.core.deps import SessionDep
from app.core.templating import templates
from app.crud import comment as crud_comment
from app.crud import post as crud_post
from app.schemas.comment import CommentCreate
from app.schemas.post import PostCreate

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def post_list(request: Request, db: SessionDep) -> HTMLResponse:
    posts = await crud_post.get_posts(db)
    return templates.TemplateResponse(request, "posts/list.html", {"posts": posts})


@router.get("/posts/create", response_class=HTMLResponse)
async def post_create(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "posts/create.html", {})


@router.post("/posts/create", response_class=HTMLResponse, response_model=None)
async def post_create_submit(
    request: Request,
    db: SessionDep,
    title: str = Form(default=""),
    content: str = Form(default=""),
) -> HTMLResponse | RedirectResponse:
    try:
        post_in = PostCreate(title=title, content=content)
    except ValidationError:
        return templates.TemplateResponse(
            request,
            "posts/create.html",
            {"error": "Заголовок и содержание не могут быть пустыми"},
            status_code=422,
        )
    post = await crud_post.create_post(post_in, db)
    return RedirectResponse(url=f"/posts/{post.id}", status_code=303)


@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def post_detail(post_id: int, request: Request, db: SessionDep) -> HTMLResponse:
    post = await crud_post.get_post_with_comments(post_id, db)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(request, "posts/detail.html", {"post": post})


@router.post("/posts/{post_id}/comments", response_class=HTMLResponse)
async def add_comment(
    post_id: int, request: Request, db: SessionDep, text: str = Form(...)
) -> HTMLResponse:
    post = await crud_post.get_post_by_id(post_id, db)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = await crud_comment.create_comment(CommentCreate(text=text), post_id, db)
    count = await crud_comment.get_comments_count(post_id, db)
    return templates.TemplateResponse(
        request, "partials/comment.html", {"comment": comment, "comments_count": count}
    )
