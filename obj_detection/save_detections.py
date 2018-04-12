import os
import cv2
import numpy as np
from PIL import Image

from .utility import generate_id

def export_detections_in_image( image, inference_result, output_dir,
  min_score_thresh = .5,
  max_boxes = 5):

  image = np.asarray(image, order='F')

  scores = inference_result['detection_scores']
  boxes = inference_result['detection_boxes']

  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] > min_score_thresh:

      h, w, c = image.shape

      # coordinates of bounding box in pixel space
      x1 = int(min(round(boxes[i][1] * w), w))
      y1 = int(min(round(boxes[i][0] * h), h))
      x2 = int(min(round(boxes[i][3] * w), w))
      y2 = int(min(round(boxes[i][2] * h), h))

      croppedImage = image[y1:y2, x1:x2]

      # Flip color channels to RGB
      croppedImage = croppedImage[...,[2,1,0]]

      result = Image.fromarray(croppedImage)

      result.save(os.path.join(output_dir, '{}.jpg'.format(generate_id())))
