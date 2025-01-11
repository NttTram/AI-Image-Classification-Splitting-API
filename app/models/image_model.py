from pydantic import BaseModel, Field
from typing import Optional

class ImageModel(BaseModel):
    id: Optional[int] = Field(default=None, description="The ID of the image")
    name:  str = Field(..., description="The name of the image")
    description: Optional[str] = Field(default=None, description="A brief description of the image")