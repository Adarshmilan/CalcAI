from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(',')[1])
    img_byte = BytesIO(image_data)
    img = Image.open(img_byte)
    dict_of_vars = data.dict_of_vars
    response = analyze_image(img, dict_of_vars)
    data = []
    for res in response:
        data.append(res)
        
    print("Final Response Data:", response)
    
    return{
        "message": "Image analyzed successfully",
        "type": "success",
        "data": data
    }