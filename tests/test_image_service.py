# from fastapi.testclient import TestClient
# from app.main import app

# import shutil
# import os

# client = TestClient(app)

# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
    

# def test_upload_file():
#     # Test uploading an image file
#     file_path = 'tests/test_img/fruits.jpg'
    
#     with open(file_path, 'rb') as file:
#         response = client.post(
#             "/upload/",
            
#             files={"files": ("fruits.jpg", file, 'image/jpg')}
#         )
        

#     assert response.status_code == 200
#     assert response.json()['Filename: '] == 'fruits.jpg'
#     os.remove(os.path.join('app/data/img', 'fruits.jpg'))
    
