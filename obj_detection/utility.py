import os, random, shutil, string

from . import config as C

def generate_id(size=10, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def moveRandomFiles(from_dir, to_dir, n=1):
  files = os.listdir(from_dir)
  selected_files = random.sample(files, n)

  for f in selected_files:
    shutil.move(os.path.join(from_dir, f), to_dir)

def splitData(data_dir, n_train = 0, n_valid = 0, n_test = 0):

  assureDirectoryExists(C.PATH_TO_TRAIN_DATA)
  assureDirectoryExists(C.PATH_TO_VALID_DATA)
  assureDirectoryExists(C.PATH_TO_TEST_DATA)

  n_files_to_split = n_train + n_valid + n_test
  n_files_dir = len(os.listdir(data_dir))

  try:
    if n_files_to_split <= n_files_dir:
      moveRandomFiles(data_dir, C.PATH_TO_TRAIN_DATA, n_train)
      moveRandomFiles(data_dir, C.PATH_TO_VALID_DATA, n_valid)
      moveRandomFiles(data_dir, C.PATH_TO_TEST_DATA, n_test)
    else:
      raise ValueError('ERROR: Not possible to split ' + str(n_files_to_split) + ' files from ' + str(data_dir) + ' containing only ' + str(n_files_dir) + '!')

  except ValueError as e: print(e)

  print('Data split completed!')

def removeDirectoryIfExists(directory):
  if os.path.exists(directory):
    shutil.rmtree(directory)

def assureDirectoryExists(directory):
  if os.path.exists(directory) == False:
    os.makedirs(directory)

def clearDirectory(directory):
  removeDirectoryIfExists(directory)
  os.makedirs(directory)

def clearData():
  # clear train, test, valid - data
  # clear output data
  clearDirectory(C.PATH_TO_TRAIN_DATA)
  clearDirectory(C.PATH_TO_VALID_DATA)
  clearDirectory(C.PATH_TO_TEST_DATA)
  clearDirectory(C.PATH_TO_OUT_DATA)
  clearDirectory(C.PATH_TO_IN_DATA)

def moveFileToIn(path_to_file):
  # move a valid img file to C.PATH_TO_IN_DATA folder
  _, file_extension = os.path.splitext(path_to_file)
  if file_extension.lower() in C.ALLOWED_IMG_EXTENSIONS:
    try:
      shutil.move(path_to_file, C.PATH_TO_IN_DATA)
    except Exception as e:
      print(str(e))

def moveTrainDataToIn():
  # move all files from C.PATH_TO_TRAIN_DATA, C.PATH_TO_VALID_DATA, C.PATH_TO_TEST_DATA
  # to C.PATH_TO_IN_DATA folder
  files = []
  files += [ os.path.join(C.PATH_TO_TRAIN_DATA, f) for f in os.listdir(C.PATH_TO_TRAIN_DATA) ]
  files += [ os.path.join(C.PATH_TO_VALID_DATA, f) for f in os.listdir(C.PATH_TO_VALID_DATA) ]
  files += [ os.path.join(C.PATH_TO_TEST_DATA, f) for f in os.listdir(C.PATH_TO_TEST_DATA) ]

  assureDirectoryExists(C.PATH_TO_IN_DATA)

  for f in files:
    moveFileToIn(f)

def moveToIn(directory):
  # Move all files from <directory> to C.PATH_TO_IN_DATA folder
  assureDirectoryExists(C.PATH_TO_IN_DATA)
  for f in os.listdir(directory):
    moveFileToIn(os.path.join(directory,f))
