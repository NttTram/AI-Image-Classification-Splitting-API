# AI-Inventory
AI API to integrate inventory system with images into different environments


fastapi==0.65.2
numpy>=1.19.2
pandas
tensorflow==2.18.0
uvicorn==0.34.0
typing-extensions>=4.0.0  # Adjust based on actual compatibility requirements
python-multipart 
#python 3.9.0

## Use pip install -r requirements.txt to test the requirements installationas

# AI Inventory API

The AI Inventory API is a powerful tool designed for detecting, recognizing, and segmenting objects in images. This project leverages TensorFlow and OpenCV to process images sent via HTTP requests, returning detailed information about the content of those images.

## Features

- Object detection and recognition using a pre-trained SSD MobileNet model.
- Image segmentation and additional processing to highlight detected objects.
- API accessible via HTTP requests, making it suitable for integration with various client-side applications.

## Requirements

This project is containerized with Docker, ensuring easy deployment and environment consistency. To run this project, you will need:

- Docker
- Docker Compose (optional for managing multi-container Docker applications)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ai-inventory-api.git
   cd ai-inventory-api


2. Build the Docker image
    ```bash
    docker build -t ai-inventory-api .

3. Run the container

    ```bash
    docker run -p 8000:8000 ai-inventory-api


### Testing with Postman
1. Make sure Docker is running.
2. open Postman and configure a new POST request to `http://localhost:8000/detect/`
3. Under the Body tab, choose `form-data`
4. In the key field, set the type to `File` and upload an image file
5. Send the request and aobserve the response
6. Open Docker desktop to Files, under `app/data/img` are where the results are stored


## Authors
- Ngoc Tram Tran (Tram Tran) - NttTram


## Acknowledgments
Hat tip to anyone whose code was used
Inspiration
etc


## License
This project is licensed under the MIT License - see the [[LICENSE.md]] file for details.