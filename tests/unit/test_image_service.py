import os
import shutil
from app.services.image_service import upload_image, list_images

from fastapi import UploadFile
from unittest.mock import MagicMock

def test_upload_image(tmp_path):
    test_file_path = tmp_path / "test_image.jpg"
    with open(test_file_path, "wb") as f:
        f.write(b"test image data")
        
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_image.jpg"
    mock_file.file = open(test_file_path, "rb")
    
    result = upload_image(mock_file)
    file_name = os.path.splitext(mock_file.filename)[0] 
    assert result["name"] == "test_image.jpg"
    assert os.path.exists(f"app/data/img/{file_name}")
    shutil.rmtree(f"app/data/img/{file_name}")