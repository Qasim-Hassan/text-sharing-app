from fastapi import FastAPI, HTTPException, Form, Depends
from .schemas import PostCreate, UserCreate, UserRead, UserUpdate
from .db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
import uuid
from .users import auth_backend, current_active_user, fastapi_users, User
from sqlalchemy.orm import selectinload

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.get("/")
def greet()-> dict:
    return {"message":"Welcome to Intuition! Sign in to continue"}

@app.post("/uploads")
async def upload_text(gotpost: PostCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    post = Post(
        blog=gotpost.text,
        user_id = user.id
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)

    return post

@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    result = await session.execute(select(Post).options(selectinload(Post.user)).order_by(Post.created_at.desc()))
    theposts = [row[0] for row in result.all()]

    res = await session.execute(select(User))
    theusers = [row[0] for row in res.all()]

    user_dict = {u.id: u.email for u in theusers}

    posts_data = []

    for p in theposts: 
        posts_data.append(
            {
                "id": str(p.id),
                "user_id": str(p.user_id),
                "blog": p.blog,
                "created_at" : p.created_at.isoformat(),
                "isowner": p.user_id == user.id,
                "email": user_dict.get(p.user_id, "Unknown")
            }
        )

    return {"posts": posts_data}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}

    except Exception as e: 
        raise HTTPException(status_code=500, detail= str(e))