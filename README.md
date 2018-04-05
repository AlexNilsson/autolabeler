# Autolabeler
automatically download and label images

## Requirements

### Tensorflow >= 1.6.0
Follow installation instructions here:
https://www.tensorflow.org/install/install_windows

```bash
pip install --upgrade --ignore-installed tensorflow
# pip install --upgrade --ignore-installed tensorflow-gpu
```

Verify installation with:
```bash
imort tensorflow as tf
print(tf.__version__)
```

### Dependencies
```
pip3 install -r requirements.txt
```
#### DEV: Update requirements.txt
```
pipreqs . --force
```

### Tensorflow models

#### 1. Download latest TF models
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md
https://github.com/tensorflow/models

Extract to C:/tensorflow/ or similar\
Add the following directories to your PYTHONPATH environment variable:
```
C:/tensorflow/model/research
C:/tensorflow/model/research/slim
```

#### 2. Unpack object_detection protos using Protoc

Select the latest protoc-x.x.x-winxx.zip\
https://github.com/google/protobuf/releases\
unpack to ./protoc/

From .../models/research/, run:
```bash
C:/autolabeler/protoc/bin/protoc.exe ./object_detection/protos/*.proto --python_out=.
```
Should return nothing, if successful

#### 3. Install object_detection
From .../models/research/, run:
```bash
python setup.py build

python setup.py install
```



## Getting started

### Gather Data
0. Run the cleanslate script to clean the project
1. Run the scraper for selected keywords and languages
2. run the postprocessing script to process the images

### Train object detection model
3. run the split script to split the data into train, test, batches
4. label train batches
5. run script to create labelmap
6. train model

### Process data
7. run script to collect all data which should be processed
8. run all data through the train model, cut, save, delete





### 3. Download an existing object_detection model

Select and download a model from the model zoo:

https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

Unpack with:
```bash
tar -xzf model-name.tar.gz
```

Move the unpacked folder to the ./data/ directory


## Training the object_detection model
goes here

### Training
py train.py --logtostderr --train_dir='C:/Users/alex/Desktop/object-detection/training/' --pipeline_config_path='C:/Users/alex/Desktop/object-detection/ssd_mobilnet_v1_pets.config'

### Exporting a checkpoint
py export_inference_graph.py --input_type image_tensor --pipeline_config_path C:/Users/alex/Desktop/object-detection/ssd_mobilnet_v1_pets.config --trained_checkpoint_prefix C:/Users/alex/Desktop/object-detection/training/model.ckpt-39 --output_directory C:/Users/alex/Desktop/object-detection/window_graph


## Running The System
goes here
