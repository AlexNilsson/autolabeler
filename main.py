import shutil
import os.path
import scraper
from scraper import scrapeImages, processImages
import obj_detection.config as C
from obj_detection.utility import splitData, clearData, moveTrainDataToIn, moveToIn
from obj_detection.xml_to_tf_record import parse as create_tf_records
from obj_detection.parse_pipeline_config import adjust_pipeline_config
from obj_detection.inference import runInference

PATH_TO_THIS_DIR = os.path.dirname(__file__)

PATH_TO_PROCESSED = os.path.join(PATH_TO_THIS_DIR, 'scraper/processed')

''' Gather Data '''
#* 0. Run the cleanslate script to clean the project
def clearProject():

  if os.path.exists(PATH_TO_PROCESSED): shutil.rmtree(PATH_TO_PROCESSED)
  clearData()

#* 1. Run the scraper for selected keywords and languages
def scrape():
  PRIMARY_LANG = 'en'
  KEYWORDS = [
    'window',
    'window outside',
    'window inside'
  ]
  LANGUAGES = ['en','sv','de','es'] #=list(scraper.languages.keys())
  MAX_IMAGES_PER_SEARCH_TERM = 100

  scrapeImages(KEYWORDS, primary_lang = PRIMARY_LANG, languages = LANGUAGES, limit_per_search_term = MAX_IMAGES_PER_SEARCH_TERM)

#*2. run the postprocessing script to process the images
def processScraped():
  REMOVE_DOWNLOADED = True

  processImages(remove_downloaded = REMOVE_DOWNLOADED, clear_processed=False)

''' Train object detection model '''
#* 3. run the split script to split the data into train, test, batches
def splitTrainData():
  NR_OF_TRAINING_IMAGES = 200    # 50% when training the model
  NR_OF_VALIDATION_IMAGES = 100   # 25% when evaluating this model compared to other models (select best model based on this)
  NR_OF_TEST_IMAGES = 100         # 25% when testing this and any other model (the test score of each model)

  splitData(PATH_TO_PROCESSED, n_train=NR_OF_TRAINING_IMAGES, n_valid=NR_OF_VALIDATION_IMAGES, n_test=NR_OF_TEST_IMAGES)

#* 4. label train batches

#* 5. create tf records (encoding training data & labels for: train, eval, test )
def createLabelRecords():
  create_tf_records(
    normalize_box_coords=True,
    save_csv=True
    )

#* 6. setup model pipeline.config
def setupModelPipelineConfig():
  PATH_TO_CHECKPOINT = os.path.join(C.PATH_TO_MODEL, 'model.ckpt')

  ADJUSTMENTS = {
    "num_classes": 1,
    "fine_tune_checkpoint": PATH_TO_CHECKPOINT,
    "label_map_path": C.PATH_TO_LABEL_MAP,
    "train_input_reader": {
      "input_path": C.PATH_TO_TRAIN_RECORD,
    },
    "eval_input_reader": {
      "input_path": C.PATH_TO_VALID_RECORD,
    },
    "eval_config": {
      "num_examples": len(os.listdir(C.PATH_TO_VALID_DATA))
    }
  }

  adjust_pipeline_config(C.PATH_TO_PIPELINE_CONFIG, ADJUSTMENTS)

#* 7. train model
def trainModel():
  command = 'start cmd /K py {} --logtostderr --pipeline_config_path={} --train_dir={}'.format(
  C.PATH_TO_TRAIN_PY.replace('\\','/'),
  C.PATH_TO_PIPELINE_CONFIG.replace('\\','/'),
  C.PATH_TO_TRAIN_DIR.replace('\\','/'))
  os.popen(command)

def evalModel():
  # fr. Tensorflow: The eval job will periodically poll the train directory for new checkpoints and evaluate them on a test dataset.
  command = 'start cmd /K py {} --logtostderr --pipeline_config_path={} --checkpoint_dir={} --eval_dir={}'.format(
  C.PATH_TO_EVAL_PY.replace('\\','/'),
  C.PATH_TO_PIPELINE_CONFIG.replace('\\','/'),
  C.PATH_TO_TRAIN_DIR.replace('\\','/'),
  C.PATH_TO_EVAL_DIR.replace('\\','/'))
  os.popen(command)

def exportInferenceGraph(checkpoint_step=None):
  # Will export the model with highest checkpoint_step if None is specified
  checkpoint_base_name = 'model.ckpt-'

  if checkpoint_step == None:
    for f in reversed(os.listdir(C.PATH_TO_TRAIN_DIR)):
      if os.path.isfile(os.path.join(C.PATH_TO_TRAIN_DIR, f)) and checkpoint_base_name in f:
        checkpoint = os.path.splitext(f)[0]
        break
  else:
    checkpoint = checkpoint_base_name + str(checkpoint_step)

  command = 'start cmd /C py {} --logtostderr --input_type="image_tensor" --pipeline_config_path={} --trained_checkpoint_prefix={} --output_directory={}'.format(
    C.PATH_TO_EXPORT_INFERENCE_GRAPH_PY.replace('\\','/'),
    C.PATH_TO_PIPELINE_CONFIG.replace('\\','/'),
    os.path.join(C.PATH_TO_TRAIN_DIR, checkpoint).replace('\\','/'),
    C.PATH_TO_INFERENCE_GRAPHS.replace('\\','/')
  )
  os.popen(command)

''' Process data '''
#* 8. run script to collect all data which should be processed
def moveDataToIn():
  moveTrainDataToIn()
  moveToIn(PATH_TO_PROCESSED)

#* 9. run all data through the train model, cut, save, delete
def parseInData():
  runInference()
  print('parse In to Out')


#clearProject()
#scrape()
#processScraped()
#splitTrainData()
''' manual labeling step'''
#createLabelRecords()
#setupModelPipelineConfig()
#trainModel()
#evalModel()
'''when happy with training'''
#exportInferenceGraph()
#moveDataToIn()
parseInData()
