from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile ## upload file
from .router import router


## Setup FastAPI instance
app = FastAPI()


app.innclude_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI API!"}

