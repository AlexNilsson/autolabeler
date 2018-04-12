import os.path

PATH_TO_TF_MODELS = 'C:/tensorflow/models'
PATH_TO_TRAIN_PY = os.path.join(PATH_TO_TF_MODELS, 'research/object_detection/train.py')
PATH_TO_EVAL_PY = os.path.join(PATH_TO_TF_MODELS, 'research/object_detection/eval.py')
PATH_TO_EXPORT_INFERENCE_GRAPH_PY = os.path.join(PATH_TO_TF_MODELS, 'research/object_detection/export_inference_graph.py')

PATH_TO_DATA = os.path.join(os.path.dirname(__file__), 'data' )

MODEL = 'faster_rcnn_inception_v2_coco_2018_01_28'
PATH_TO_MODEL = os.path.join(PATH_TO_DATA, MODEL)
PATH_TO_PIPELINE_CONFIG = os.path.join(PATH_TO_MODEL, 'pipeline.config')

PATH_TO_TRAIN_DIR = os.path.join(PATH_TO_MODEL, 'train')
PATH_TO_EVAL_DIR = os.path.join(PATH_TO_MODEL, 'eval')
PATH_TO_INFERENCE_GRAPHS = os.path.join(PATH_TO_MODEL, 'inference')
PATH_TO_INFERENCE_GRAPH = os.path.join(PATH_TO_INFERENCE_GRAPHS, 'frozen_inference_graph.pb')


PATH_TO_TRAIN_RECORD = os.path.join(PATH_TO_DATA, 'train_labels.record')
PATH_TO_VALID_RECORD = os.path.join(PATH_TO_DATA, 'valid_labels.record')




PATH_TO_LABEL_MAP = os.path.join(PATH_TO_DATA, 'label_map.pbtxt' )

ALLOWED_IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png']

PATH_TO_TRAIN_DATA = os.path.join(os.path.dirname(__file__), 'images/train' )
PATH_TO_VALID_DATA = os.path.join(os.path.dirname(__file__), 'images/valid' )
PATH_TO_TEST_DATA = os.path.join(os.path.dirname(__file__), 'images/test' )

PATH_TO_IN_DATA = os.path.join(os.path.dirname(__file__), 'images/in' )
PATH_TO_OUT_DATA = os.path.join(os.path.dirname(__file__), 'images/out' )
PATH_TO_PARSED_DATA = os.path.join(os.path.dirname(__file__), 'images/parsed' )
