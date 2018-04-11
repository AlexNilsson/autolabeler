import os, json, re

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
  print('Adjusting model pipeline.config')
  try:
    with open(path_to_file, mode='rt') as f:
      config = f.read()

    for param in overrides_dict.keys():
      value = overrides_dict[param]

      if type(value) == dict:
        subDictName, subDict = param, value

        for param in subDict.keys():
          value = subDict[param]
          regex = re.escape(subDictName) + r'[\s\w\n{}:"/.]*?' + re.escape(param) + r'(:[ "\w/.:]+)'
          regex_result = re.search(regex, config)
          sub_config = regex_result.group(0)

          if type(value) == str:
            value = value.replace('\\','/')
            new_sub_config = sub_config.replace(regex_result.groups()[0], ': "{}"'.format(value))
          else:
            new_sub_config = sub_config.replace(regex_result.groups()[0], ': {}'.format(value))

          config = config.replace(sub_config, new_sub_config)
      else:
        regex = re.escape(param) + r': [0-9\w"/.:]+'

        if type(value) == str:
          config = re.sub(regex, '{}: "{}"'.format(param, value.replace('\\','/')), config)
        else:
          config = re.sub(regex, '{}: {}'.format(param, value), config)

    with open(path_to_file, mode='wt') as f:
      f.write(config)

    print('Successfully adjusted pipeline config')

  except Exception as e:
    print('Failed to adjust pipeline config: ' + str(e))
