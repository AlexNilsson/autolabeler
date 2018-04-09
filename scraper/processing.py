import os, shutil, string, random
import numpy as np
import cv2

from removedupes import removeDuplicates


def generate_id(size=8, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def process(remove_downloaded = True, remove_duplicates = True, clear_processed = True):
  PATH_TO_DIR = os.path.dirname(__file__)

  PATH_TO_DOWNLOADS = os.path.join(PATH_TO_DIR, 'downloads')
  PATH_TO_PROCESSED = os.path.join(PATH_TO_DIR, 'processed')
  MAX_SIZE = np.array([1080, 720])

  n_processed = n_removed_empty = n_resized = 0

  # Create/Clean processed directory
  if os.path.exists(PATH_TO_PROCESSED):
    if clear_processed:
      shutil.rmtree(PATH_TO_PROCESSED)
      os.makedirs(PATH_TO_PROCESSED)
  else:
      os.makedirs(PATH_TO_PROCESSED)


  # Process images in downloads directory
  for language in os.listdir(PATH_TO_DOWNLOADS):
    for image_file_name in os.listdir(os.path.join(PATH_TO_DOWNLOADS, language)):

      image_path = os.path.join(PATH_TO_DOWNLOADS, language, image_file_name)

      # remove empty files
      if os.stat(image_path).st_size <= 0:
        os.remove(image_path)
        n_removed_empty +=1
        continue

      # resize large images
      try:
        img = cv2.imread(image_path)
        img_size = tuple(img.shape[1::-1])
      except:
        continue

      if np.greater(img_size, MAX_SIZE).any():
        sf = np.divide(MAX_SIZE, img_size).min()
        img = cv2.resize(img, (0,0), fx=sf, fy=sf)
        n_resized += 1

      filename, file_extension = os.path.splitext(image_file_name)

      cv2.imwrite(os.path.join(PATH_TO_PROCESSED, 'img-' + generate_id() + file_extension ), img)
      n_processed += 1
      print('Processed: ' + str(n_processed))

  # remove downloads
  if remove_downloaded: shutil.rmtree(PATH_TO_DOWNLOADS)

  # remove duplicates in /processed
  if remove_duplicates: removeDuplicates(PATH_TO_PROCESSED)

  print('\nProcessed ' + str(n_processed) + ' files')
  print('Removed Empty: ' + str(n_removed_empty))
  print('Resized: ' + str(n_resized))


