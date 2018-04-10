import os
import re
import json






MODEL_NAME = 'faster_rcnn_inception_v2_coco_2018_01_28'

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_TO_CONFIG = os.path.join(THIS_DIR, 'obj_detection/data', MODEL_NAME, 'pipeline.config')

def pipeline_config_to_dict(path_to_file):
  with open(path_to_file) as f:
    config = f.read()

  # remove spaces
  config = config.replace(' ','')

  # add colon before object notation
  config = config.replace('{',': {')

  # property declarations to strings prop: -> "prop":
  config = re.sub(r'\w+:', lambda x: '"{}":'.format(x.group()[:-1]), config)

  # add trailing comma to prop values
  config = re.sub(r':[0-9."\w/-]+\n"', lambda x: '{},\n"'.format(x.group()[:-2]), config)

  # add trailing comma to object notations
  config = config.replace('}\n"','},\n"')

  # CAPS object references to strings:  FF -> "FC"
  config = re.sub(r':\w+\n', lambda x: ':"{}"\n'.format(x.group()[1:-1]), config)
  config = re.sub(r':\w+,', lambda x: ':"{}",'.format(x.group()[1:-1]), config)

  json_string = '{' + config + '}'
  obj_dict = json.loads(json_string)

  return obj_dict

def adjust_pipeline_config(path_to_file, overrides_dict):
  with open(path_to_file, mode='rt') as f:
    config = f.read()

  for param in overrides_dict.keys():
    value = overrides_dict[param]

    if type(value) == dict:
      regex = re.escape(param) + r' {[\w\n "./{:]+}[ \n]+}'
      sub_config = re.match(regex, config)
      print(sub_config)
    else:
      regex = re.escape(param) + r': [0-9\w"/.]+'

      if type(value) == str:
        config = re.sub(regex, '{}: "{}"'.format(param, value), config)
      else:
        config = re.sub(regex, '{}: {}'.format(param, value), config)

  #with open(path_to_file, mode='wt') as f:
    #f.write(config)


adjust_pipeline_config(PATH_TO_CONFIG, {
  "num_classes": 1,
  "fine_tune_checkpoint": "PATH_TO_BE_CONFIGURED/BY/model.ckpt",
  "train_input_reader": {
    "label_map_path": "PATH_TO_BE_CONFIGURED/BY/mscoco_label_map.pbtxt",
    "input_path": "PATH_TO_BE_CONFIGURED/BY/mscoco_val.record",
  },
  "eval_input_reader": {
    "label_map_path": "PATH_TO_BE_CONFIGURED/BY/mscoco_label_map.pbtxt",
    "input_path": "PATH_TO_BE_CONFIGURED/BY/mscoco_val.record",
  }
})
