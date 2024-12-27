# Import necessary modules and functions
import os
from fastapi.testclient import TestClient
from app.main import app

# Setup the TestClient
client = TestClient(app)


def test_file_upload():
    file_path = "tests/test_img/fruits.jpg"
    
    # Open the file inn binary mode
    with open(file_path, 'rb') as test_file:
        # Construct the payload with the file
        files = {'file' : (os.path.basename(file_path), test_file, 'image/jpg')}
        
        #Send a POST request to the upload endpoint
        response = client.post('/upload/', files=files)
        
        
    assert response.status_code == 200
    assert response.json() == {"filename" : os.path.basename(file_path)}, "Check that the filename returned is correct"
    