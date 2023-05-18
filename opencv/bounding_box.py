import numpy as np
import cv2
import os


#path = 'C:/Users/TymB/exercises-for-college/opencv/pliers'
#file_names = os.listdir(path)
'''
for file_name in file_names:
    # Check if the file is an image (you can modify the condition to suit your needs)
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        # Build the full path to the image file
        image_path = os.path.join(path, file_name)

        # Load and display the image
        image = cv2.imread(image_path)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
'''


def make_bbox(path):
    image = cv2.imread(path)
    #cv2.imshow('1', image)
    # cv2.waitKey()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 240, 255, cv2.THRESH_BINARY_INV)[1]

    canny = cv2.Canny(gray, 50, 255)
    # Find contours, obtain bounding box, extract and save ROI
    ROI_number = 0
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    bbox = []

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

        bbox.append((x, y, w, h))
    cv2.imshow('a', image)
    cv2.waitKey()
    size = image.shape[0], image.shape[1]

    bbox_sorted = sorted(bbox, key=lambda b: b[2]*b[3], reverse=True)
    max_bbox = bbox_sorted[0]

    yolo_x = (max_bbox[0] + max_bbox[2] / 2) / size[0]
    yolo_y = (max_bbox[1] + max_bbox[3] / 2) / size[1]
    yolo_w = max_bbox[2] / size[0]
    yolo_h = max_bbox[3] / size[1]

    return (yolo_x, yolo_y, yolo_w, yolo_h)
