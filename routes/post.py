from fastapi import APIRouter,status,HTTPException
from models.post import Post
from typing import List

post_router = APIRouter(prefix="/posts",tags=["Post"])



posts=dict()


@post_router.get('/', response_model=List[Post])
def get_posts():
    return list(posts.values())



@post_router.post('/', status_code=status.HTTP_201_CREATED)

def create_post(post: Post):

    if post.title in posts:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    posts[post.title]=post
    return post


@post_router.get('/{title}', response_model=Post)

def get_post(title: str):

    post=posts.get(title)

    if not post: 

        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return post


@post_router.put('/{title}')

def update_post(title: str, post_new):

    post_pr=posts.get(title)

    if not post_pr: 

        raise HTTPException(status.HTTP_404_NOT_FOUND)

    posts[post_new.title]=post_new

    return {'message':'post updated'}

@post_router.delete('/{title}')
def delete_post(title: str):
    post=posts.get(title)
    if not post: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    posts.pop(title)
    return {'message':'post deleted'}