import cv2
import numpy as np


def function_colorSegmentation(image, k=3, resize_factor=0.5):
    # Resize image for faster processing using OpenCV's resize function
    small_image = cv2.resize(
        image, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_AREA)

    small_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)
    pixel_values = small_image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Optimized kmeans function
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.5)
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None,
                                      criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    labels = labels.flatten()

    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(small_image.shape)

    # Upscale to original size
    segmented_image = cv2.resize(
        segmented_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)

    return segmented_image


def function_OTSU(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh_image


def function_edgeSeg(image):
    # Convert the image color to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Reduce noise from the image
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    blur = cv2.medianBlur(gray_image, 5)

    # Apply Canny edge detector algorithm on the image to find edges
    canny = cv2.Canny(blur, 100, 200)
    return canny


def function_separateCracks(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarize the image
    _, m = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel, iterations=2)

    # Morphological closing
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find the contours
    contours, hierarchy = cv2.findContours(
        closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours
    Iout = image.copy()
    cv2.drawContours(Iout, contours, -1, (0, 0, 255), 2)

    return Iout


def handle_imageProcessing(raw_image_path, processed_image_path, process_type="otsu"):
    try:
        image = cv2.imread(raw_image_path)

        print("process_type", process_type)

        if process_type == "otsu":
            processed_image = function_OTSU(image)
        elif process_type == "edge":
            processed_image = function_edgeSeg(image)
        elif process_type == "color":
            processed_image = function_colorSegmentation(image)
        elif process_type == "separate":
            processed_image = function_separateCracks(image)
        else:
            processed_image = image

        cv2.imwrite(processed_image_path, processed_image)
        return True
    except Exception as e:
        print(e)
        return False
