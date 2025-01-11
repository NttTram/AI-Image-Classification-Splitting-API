from fastapi import FastAPI
from router import router

## Setup FastAPI instance
app = FastAPI()
app.include_router(router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI API!"}

