import os

class FileHandler:
  def __init__(self, directory):
    self.directory = directory
    self.files = []

  @staticmethod
  def forFilesIn(directory):
    obj = FileHandler(directory)

    files = []

    for f in os.listdir(directory):
      file_path = os.path.join(directory, f)
      if os.path.isfile(file_path): files.append(file_path)

    obj.files = files
    return obj

  def withExtensions(self, extensions):
    files = []
    for f in self.files:
      _, file_extension = os.path.splitext(f)

      if file_extension.lower() in extensions:
        files.append(f)

    self.files = files
    return self

  def call(self, func):
    for f in self.files:
      func(f)
