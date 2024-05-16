import cv2
import numpy as np
import pandas as pd

def sobel_edge_detection(gray_image):
  # gray is the grayscale image - copy it to a new variable gray
	gray = gray_image.copy()
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	# Apply Sobel filter in x and y direction
	grad_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
	grad_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
	# Calculate the magnitude and direction of gradients
	magnitude = cv2.magnitude(grad_x, grad_y)
	direction = cv2.phase(grad_x, grad_y, angleInDegrees=True)
	# Normalize magnitude
	normalized_magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8) # type: ignore
	# Threshold magnitude image to get potential edges
	_, edge_candidates = cv2.threshold(normalized_magnitude, 50, 255, cv2.THRESH_BINARY)
	# Create a mask based on edge direction, ignore horizontal and vertical edges
	mask = np.logical_or(direction < 30, direction > 60)
	# apply mask to the edge candidates
	edges = np.where(mask, edge_candidates, 0).astype(np.uint8)
	# black = np.zeros_like(gray)
	kernel = np.ones((3, 3), np.uint8)
	black1 = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
	return black1


def otsu(gray_image):
	gray = gray_image.copy()
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	_, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	return threshold


def canny_edge_detection(gray_image):
	gray = gray_image.copy()
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edges = cv2.Canny(image=gray, threshold1=100, threshold2=200)
	kernel = np.ones((3, 3), np.uint8)
	black1 = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
	return black1


def crack_detection_basic(image):
	image = image.copy()
	# resize the image to 500x500
	# image = cv2.resize(image, (500, 500))
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	otsu_image = otsu(grayscale)
	canny_image = canny_edge_detection(grayscale)
	sobel_image = sobel_edge_detection(grayscale)
	
	canny_image[otsu_image == 255] = 0
	sobel_image[otsu_image == 255] = 0

	black = np.zeros_like(grayscale)
	black[canny_image == 255] = 255
	black[sobel_image == 255] = 255

	ratio = np.sum(black == 255) / black.size
	# convert to 3 channels
	black = cv2.cvtColor(black, cv2.COLOR_GRAY2BGR)
	red = np.zeros_like(black)
	red[:, :, 2] = 255
	red_mask = cv2.bitwise_and(black, red)
	result = cv2.addWeighted(image, 1, red_mask, 1, 0)

	return result, float(ratio)