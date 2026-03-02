import json

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Duration, Limiter, Rate
from sqlalchemy.orm import Session

from app.core.email import send_blog_email
from app.core.jwt import decode_access_token
from app.core.redis_client import redis_client
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.Blogs import Blog
from app.models.user import User
from app.schemas.blog import BlogCreate, BlogUpdate

router = APIRouter(prefix="/blog", tags=["Blog Api"])


@router.post(
    "/add",
)
def create_blog(
    blog: BlogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):

    # current_user : User = Depends(get_current_user)    to fetch the current user
    new_blog = Blog(title=blog.title, content=blog.content, user_id=current_user.id)

    background_tasks.add_task(  # background_tasks ab ek object h.. background me kaam karne ke  liye likh sakte
        send_blog_email, current_user.email, blog.title, blog.content
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    redis_client.delete(
        "allblogs"
    )  # redis server agar running nahi raha to 111 error aayega like server error redis kisi or post port pe h

    return {"message": "blog added"}


@router.get(
    "/getblogs",
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))],
)
def get_all_blogs(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    cached_data = redis_client.get("all_blogs")  # check in redis data is present or not

    if cached_data:

        return json.loads(
            cached_data
        )  # if found then convert the json string into python object  redis data string me store karta hai

    blogs = db.query(Blog).all()  # if not found in redis then search in database

    blog_list = []  # sqlalchemy convert convert object into dictionary
    for blog in blogs:
        blog_list.append(
            {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "user_id": blog.user_id,
            }
        )

        redis_client.set("all_blogs", json.dumps(blog_list), ex=60)

    return blog_list


@router.get("/blogs/{blog_id}")
def get_single_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    blog = db.query(Blog).filter(Blog.blog_id == blog_id).first()

    if blog.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized"
        )  # 401 user unauthorized 403 is authenticated but not authorized

    return blog


@router.put("/update/{blog_id}")
def update_blog(
    blog_id: int,
    updated_data: BlogUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    blog = db.query(Blog).filter(Blog.blog_id == blog_id).first()

    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    blog.title = updated_data.title
    blog.content = updated_data.content

    db.commit()
    db.refresh(blog)

    return blog


@router.delete("/delete/{blog_id}")
def delete_blog(
    blog_id,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    blog = db.query(Blog).filter(Blog.blog_id == blog_id).first()

    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if not blog:
        raise HTTPException(status_code=404, detail="id not found")

    db.delete(blog)

    db.commit()

    return {"message": "blog deleted"}
