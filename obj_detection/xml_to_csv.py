import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

import io
import tensorflow as tf
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

def xml_to_array(path_to_xml):
  root = ET.parse(path_to_xml).getroot()
  array = []

  # ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

  for item in root.findall('object'):
    array.append([
      root.find('filename').text,
      int(root.find('size')[0].text),
      int(root.find('size')[1].text),
      item[0].text,
      int(item[4][0].text),
      int(item[4][1].text),
      int(item[4][2].text),
      int(item[4][3].text)
    ])

  return array

def xml_to_matrix( save_as_csv=False ):
  for folder in ['train']:
    path_to_dir = os.path.join(os.getcwd(), 'test_images', folder)

    matrix = [['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]

    for xml_file in glob.glob(path_to_dir + '/*.xml'):
      matrix += xml_to_array(xml_file)

    if save_as_csv:
      df = pd.DataFrame(matrix)
      df.to_csv('test_images/' + folder + '_labels.csv', header=None, index=None)
      print('Successfully converted xml to csv.')

#xml_to_matrix(save_as_csv=True)

def create_tf_example2(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))


def class_id_from_name(name):
  return 1

def create_tf_record(img_data):
  filename = img_data[0][0].encode('utf8') # Filename of the image. Empty if image is not from file
  width = img_data[0][1] # Image width
  height = img_data[0][2] # Image height
  encoded_image_data = None # Encoded image bytes
  image_format = None # b'jpeg' or b'png'

  columns = [column for column in zip(*img_data)]

  xmins = columns[4] # List of normalized left x coordinates in bounding box (1 per box)
  ymins = columns[5] # List of normalized top y coordinates in bounding box (1 per box)
  xmaxs = columns[6] # List of normalized right x coordinates in bounding box (1 per box)
  ymaxs = columns[7] # List of normalized bottom y coordinates in bounding box (1 per box)
  class_names = columns[3] # List of string class name of bounding box (1 per box)
  class_ids = [class_id_from_name(className) for className in class_names] # List of integer class id of bounding box (1 per box)

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(class_names),
      'image/object/class/label': dataset_util.int64_list_feature(class_ids),
  }))
  return tf_example

def xml_files_to_tf_record(xml_directory, output):

  writer = tf.python_io.TFRecordWriter(output)

  for path_to_xml in glob.glob(xml_directory + '/*.xml'):
    img_data = xml_to_array(path_to_xml)
    #print(img_data)
    tf_record = create_tf_record(img_data)
    writer.write(tf_record.SerializeToString())

  writer.close()

  print('Successfully created the TFRecords: {}'.format(output))


def main():
  for folder in ['train']:
    input_dir = os.path.join(os.getcwd(), 'test_images', folder)
    output_file = os.path.join(input_dir, folder + '_labels.record')
    xml_files_to_tf_record(input_dir, output_file)


main()
