import os.path

PATH_TO_DATA = os.path.join(os.path.dirname(__file__), 'data' )

PATH_TO_LABEL_MAP = os.path.join(PATH_TO_DATA, 'label_map.pbtxt' )

PATH_TO_TRAIN_DATA = os.path.join(os.path.dirname(__file__), 'images/train' )
PATH_TO_VALID_DATA = os.path.join(os.path.dirname(__file__), 'images/valid' )
PATH_TO_TEST_DATA = os.path.join(os.path.dirname(__file__), 'images/test' )

PATH_TO_IN_DATA = os.path.join(os.path.dirname(__file__), 'images/in' )
PATH_TO_OUT_DATA = os.path.join(os.path.dirname(__file__), 'images/out' )
