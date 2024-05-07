import cv2
# import numpy as np
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
import io


def process_image_with_otsu(image_path):
    # Read the image
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    _, img_otsu = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply Otsu's thresholding a second time
    _, img_otsu_twice = cv2.threshold(
        img_otsu, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert the processed image back to an in-memory file
    is_success, buffer = cv2.imencode(".jpg", img_otsu_twice)
    io_buf = io.BytesIO(buffer)
    return ImageFile(io_buf, name='processed.jpg')
