import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

import tensorflow as tf
from object_detection.utils import dataset_util

from . import config as C

def class_id_from_name(name):

  with open(C.PATH_TO_LABEL_MAP, 'r') as f:
    labelmap = f.read()

    #TODO: automatically create labelmap from xml data
    #print(labelmap)

  return 1

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

def create_tf_record(img_data, directory):

  filename = img_data[0][0]

  print('parsing data for file: {}'.format(filename))

   # File Extension
  __, file_extension = os.path.splitext(filename)
  image_format = file_extension[1:]

   # Encoded image bytes
  with tf.gfile.GFile(os.path.join(directory, filename), 'rb') as fid:
    encoded_image_data = fid.read()

  # img_data grouped by columns [c1,c2,...]
  columns = [column for column in zip(*img_data)]

  class_names = [str.encode(cn) for cn in columns[3]]
  class_ids = [class_id_from_name(className) for className in class_names]

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(img_data[0][2]),
      'image/width': dataset_util.int64_feature(img_data[0][1]),
      'image/filename': dataset_util.bytes_feature(str.encode(filename)),
      'image/source_id': dataset_util.bytes_feature(str.encode(filename)),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(str.encode(image_format)),
      'image/object/bbox/xmin': dataset_util.float_list_feature(columns[4]),
      'image/object/bbox/xmax': dataset_util.float_list_feature(columns[6]),
      'image/object/bbox/ymin': dataset_util.float_list_feature(columns[5]),
      'image/object/bbox/ymax': dataset_util.float_list_feature(columns[7]),
      'image/object/class/text': dataset_util.bytes_list_feature(class_names),
      'image/object/class/label': dataset_util.int64_list_feature(class_ids),
  }))
  return tf_example

def xml_files_to_tf_record(xml_directory, output_file, save_csv=False, csv_output_file=''):

  writer = tf.python_io.TFRecordWriter(output_file)

  if save_csv: csv_matrix = [['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]

  for path_to_xml in glob.glob(xml_directory + '/*.xml'):
    img_data = xml_to_array(path_to_xml)
    if len(img_data) > 0:
      tf_record = create_tf_record(img_data, xml_directory)
      writer.write(tf_record.SerializeToString())
      if save_csv: csv_matrix += img_data

  writer.close()

  if save_csv:
    df = pd.DataFrame(csv_matrix)
    df.to_csv(csv_output_file, header=None, index=None)

  print('Successfully created the TFRecords: {}'.format(output_file))

def parse():
  INPUT_DIR = 'images'
  OUTPUT_DIR = C.PATH_TO_DATA
  FOLDERS_TO_PARSE = ['train','test','valid']
  THIS_DIR = os.path.dirname(os.path.realpath(__file__))
  SAVE_CSV = False

  for folder in FOLDERS_TO_PARSE:
    input_dir = os.path.join(THIS_DIR, INPUT_DIR, folder)
    output_record_file = os.path.join(OUTPUT_DIR, folder + '_labels.record')
    output_csv_file = os.path.join(OUTPUT_DIR, folder + '_labels.csv')
    xml_files_to_tf_record(input_dir, output_record_file, save_csv=SAVE_CSV, csv_output_file=output_csv_file)
