from fastapi import FastAPI
# from router import router
from app.routers.image_router import router as image_router


## Setup FastAPI instance
app = FastAPI()
app.include_router(image_router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI API!"}

