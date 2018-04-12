import os
import numpy as np

import tensorflow as tf
import cv2
import shutil

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

from . import config as C
from .save_detections import export_detections_in_image

from .FileHandler import FileHandler
from .utility import assureDirectoryExists

def load_inference_graph(path_to_inference_graph):
  # Load a (frozen) Tensorflow model into memory.
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(path_to_inference_graph, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')
  return detection_graph

def load_label_map(path_to_label_map):
  label_map = label_map_util.load_labelmap(path_to_label_map)
  max_num_classes = label_map_util.get_max_label_map_index(label_map)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=max_num_classes, use_display_name=True)
  return label_map_util.create_category_index(categories)

def run_inference_for_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes', 'detection_masks']:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]

  return output_dict

def export_detections_in_image_using_graph(file_path, inference_graph, output_dir=C.PATH_TO_OUT_DATA, show_output=False):
  image = cv2.imread(file_path)

  # Run inference
  inference_result = run_inference_for_image(image, inference_graph)

  # Export Detections
  export_detections_in_image(image, inference_result, output_dir=output_dir)

  # Move parsed file to /parsed directory
  assureDirectoryExists(C.PATH_TO_PARSED_DATA)
  shutil.move(file_path, C.PATH_TO_PARSED_DATA)

  if show_output:
    # Overlay detection on image and show
    label_map = load_label_map(C.PATH_TO_LABEL_MAP)
    vis_util.visualize_boxes_and_labels_on_image_array(
      image,
      inference_result['detection_boxes'],
      inference_result['detection_classes'],
      inference_result['detection_scores'],
      label_map,
      instance_masks=inference_result.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)

    cv2.imshow('Object Detections', image)


  path_to_dir, basename = os.path.split(file_path)
  print('Parsed file: {}, Remaining files in dir: {}'.format(basename, len(os.listdir(path_to_dir))))

def runInference(input_dir=C.PATH_TO_IN_DATA, output_dir=C.PATH_TO_OUT_DATA, inference_graph=C.PATH_TO_INFERENCE_GRAPH):
  inference_graph = load_inference_graph(inference_graph)

  exportInference = lambda x: export_detections_in_image_using_graph(x, inference_graph)

  FileHandler \
    .forFilesIn(input_dir) \
    .withExtensions(C.ALLOWED_IMG_EXTENSIONS) \
    .call(exportInference)
