from fastapi import FastAPI
from routes.user import user_router
from routes.post import post_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
