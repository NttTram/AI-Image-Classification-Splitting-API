import os
import shutil
from app.services.image_service import upload_image, list_images

from fastapi import UploadFile
from unittest.mock import MagicMock
from unittest.mock import patch

def test_upload_image(tmp_path):
    test_file_path = tmp_path / "test_image.jpg"
    with open(test_file_path, "wb") as f:
        f.write(b"test image data")
        
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_image.jpg"
    mock_file.file = open(test_file_path, "rb")
    file_name = os.path.splitext(mock_file.filename)[0] 
    
    result = upload_image(mock_file)
    
    
    assert result["name"] == "test_image.jpg"
    assert os.path.exists(f"app/data/img/{file_name}")
    shutil.rmtree(f"app/data/img/{file_name}")
    
    
    
def test_list_images(tmp_path):
    # Create a temporary directory structure with files
    (tmp_path / "image1.jpg").write_text("dummy content")
    (tmp_path / "image2.png").write_text("dummy content")
    (tmp_path / "doc.txt").write_text("dummy content")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "image3.jpeg").write_text("dummy content")
    (subdir / "image4.gif").write_text("dummy content")
    
    with patch("app.services.image_service.img_dir", str(tmp_path)):
        result = list_images()
    
    
    
    # Check that only image files are listed
    expected_files = [
        str(tmp_path / "image1.jpg"),
        str(tmp_path / "image2.png"),
        str(subdir / "image3.jpeg")
    ] 
    
    assert sorted(result) == sorted(expected_files)
    
   