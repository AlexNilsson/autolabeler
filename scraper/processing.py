import os
import numpy as np
import cv2
import shutil

def process(remove_downloaded = True):

  PATH_TO_DIR = os.path.dirname(__file__)

  PATH_TO_DOWNLOADS = os.path.join(PATH_TO_DIR, 'downloads')
  PATH_TO_PROCESSED = os.path.join(PATH_TO_DIR, 'processed')
  MAX_SIZE = np.array([1080, 720])

  processed = removed = resized = 0

  # Create/Clean processed directory
  if os.path.exists(PATH_TO_PROCESSED):
    shutil.rmtree(PATH_TO_PROCESSED)
  os.makedirs(PATH_TO_PROCESSED)

  # Process images in downloads directory
  for language in os.listdir(PATH_TO_DOWNLOADS):
    for image_file_name in os.listdir(os.path.join(PATH_TO_DOWNLOADS, language)):

      image_path = os.path.join(PATH_TO_DOWNLOADS, language, image_file_name)

      # remove empty files
      if os.stat(image_path).st_size <= 0:
        os.remove(image_path)
        removed +=1
        continue

      # resize large images
      img = cv2.imread(image_path)
      img_size = tuple(img.shape[1::-1])

      if np.greater(img_size, MAX_SIZE).any():
        sf = np.divide(MAX_SIZE, img_size).min()
        img = cv2.resize(img, (0,0), fx=sf, fy=sf)
        resized += 1

      filename, file_extension = os.path.splitext(image_file_name)

      processed += 1
      cv2.imwrite(os.path.join(PATH_TO_PROCESSED, 'image-' + str(processed) + file_extension ), img)

  # remove downloads
  if remove_downloaded: shutil.rmtree(PATH_TO_DOWNLOADS)

  print('\nProcessed ' + str(processed) + ' files')
  print('Removed: ' + str(removed))
  print('Resized: ' + str(resized))


