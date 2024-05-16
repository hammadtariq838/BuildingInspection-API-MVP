import os
import cv2
import numpy as np

# Function for color segmentation (e.g., detecting moss)
def moss_detection(image):
    # if image is already grayscale, convert to BGR
    lower_color = np.array([25, 50, 50])
    upper_color = np.array([80, 255, 255])

    image = image.copy()
    if len(image.shape) == 2:
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Convert to HSV color space
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask with the specified color range
    mask = cv2.inRange(hsv_img, lower_color, upper_color)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)

    meta = {
      "lower_color": [int(i) for i in lower_color],
      "upper_color": [int(i) for i in upper_color]
    }

    return result, meta
