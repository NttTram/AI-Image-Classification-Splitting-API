from fastapi import FastAPI
from router import router


## Setup FastAPI instance
app = FastAPI()


app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI API!"}

