from fastapi import FastAPI, UploadFile, File
# from router import router
from app.routers.image_router import router as image_router


## Setup FastAPI instance
app = FastAPI()
app.include_router(image_router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI API!"}


# @app.post("/upload/")
# async def upload_file_endpoint(file: UploadFile = File(...)):
#     filename = file.filename
#     return {"filename": filename}