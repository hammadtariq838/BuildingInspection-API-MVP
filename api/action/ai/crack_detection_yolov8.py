import logging
import os
from typing import Any
from ultralytics import YOLO
import cv2

current_dir = os.path.dirname(os.path.abspath(__file__))
pretrained_model_path = os.path.join(current_dir, 'pretrained/crack_detection_yolov8.pt')


class CrackDetectionYOLOv8:
  __model: Any = None

  def __init__(self):
    pretrained_model_exists = os.path.exists(pretrained_model_path)
    if pretrained_model_exists:
      self.__load_model()
    else:
      raise FileNotFoundError(f"Pretrained model not found at {pretrained_model_path}")


  @property
  def model(self):
    return self.__model
  @model.setter
  def model(self, value):
    if value is not self.__model:
      raise ValueError("Cannot change the model once it is set!")
    return self.__model
  @model.getter
  def model(self):
    return self.__model


  def __load_model(self):
    if not os.path.exists(pretrained_model_path):
      raise FileNotFoundError(f"Pretrained model not found at {pretrained_model_path}")
    self.__model = YOLO(pretrained_model_path)
    return True
  

  def predict_image(self, image):
    results = self.__model(image)
    meta = []
    # length of results is the number of images
    length_results = len(results)
    for res in results:
      boxes = res.boxes
      length_boxes = len(boxes.xyxy)
      for i in range(len(boxes.xyxy)):
        box = boxes.xyxy[i]
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        confidence = boxes.conf[i]
        txt = f"Crack: {confidence:.3f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 36, 12), 2)
        # 1/10 of the image height
        temp = int(image.shape[0]/25)
        cv2.putText(image, txt, (x1, y1+temp), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,36,12), 2)
        meta.append({
          "x1": x1,
          "y1": y1,
          "x2": x2,
          "y2": y2,
          "confidence": confidence
        })
    return image, meta
  