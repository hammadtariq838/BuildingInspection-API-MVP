import cv2
import numpy as np


def before_after(before, after):
	before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
	after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

	# transform the after image to the before image
	orb_detector = cv2.ORB_create()

	# find the key points and descriptors with ORB
	before_keypoints, before_descriptors = orb_detector.detectAndCompute(before_gray, None)
	after_keypoints, after_descriptors = orb_detector.detectAndCompute(after_gray, None)

	# create a BFMatcher object
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	# match descriptors
	matches = bf.match(before_descriptors, after_descriptors)

	# sort them in the order of their distance
	matches = sorted(matches, key = lambda x:x.distance)

	matches = matches[:int(len(matches)*90)]
	no_of_matches = len(matches)

	# define empty matrices of shape no_of_matches * 2
	before_points = np.zeros((no_of_matches, 2))
	after_points = np.zeros((no_of_matches, 2))

	for i in range(len(matches)):
		before_points[i, :] = before_keypoints[matches[i].queryIdx].pt
		after_points[i, :] = after_keypoints[matches[i].trainIdx].pt

	# find the homography matrix
	h, status = cv2.findHomography(after_points, before_points, cv2.RANSAC)

	# use this matrix to transform the
	transformed_img = cv2.warpPerspective(after, h, (before.shape[1], before.shape[0]))

	return before, transformed_img
    