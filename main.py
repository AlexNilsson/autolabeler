import shutil
import os.path
import scraper
from scraper import scrapeImages, processImages
import obj_detection.config as C
from obj_detection.utility import splitData, clearData, moveTrainDataToIn, moveToIn
from obj_detection.xml_to_tf_record import parse as create_tf_records
from obj_detection.parse_pipeline_config import adjust_pipeline_config

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
  create_tf_records()

#* 6. setup model pipeline.config
def setupModelPipelineConfig():
  MODEL = 'faster_rcnn_inception_v2_coco_2018_01_28'
  PATH_TO_MODEL = os.path.join(C.PATH_TO_DATA, MODEL)
  PATH_TO_CONFIG = os.path.join(PATH_TO_MODEL, 'pipeline.config')
  
  PATH_TO_CHECKPOINT = os.path.join(PATH_TO_MODEL, 'model.ckpt')

  PATH_TO_TRAIN_RECORD = os.path.join(C.PATH_TO_DATA, 'train_labels.record')
  PATH_TO_VALID_RECORD = os.path.join(C.PATH_TO_DATA, 'valid_labels.record')

  ADJUSTMENTS = {
    "num_classes": 1,
    "fine_tune_checkpoint": PATH_TO_CHECKPOINT,
    "label_map_path": C.PATH_TO_LABEL_MAP,
    "train_input_reader": {
      "input_path": PATH_TO_TRAIN_RECORD,
    },
    "eval_input_reader": {
      "input_path": PATH_TO_VALID_RECORD,
    }
  }

  adjust_pipeline_config(PATH_TO_CONFIG, ADJUSTMENTS)

#* 7. train model
def trainModel():
  print('train model')

''' Process data '''
#* 8. run script to collect all data which should be processed
def moveDataToIn():
  moveTrainDataToIn()
  moveToIn(PATH_TO_PROCESSED)

#* 9. run all data through the train model, cut, save, delete
def autolabelInData():
  print('parse In to Out')


#clearProject()
#scrape()
#processScraped()
#splitTrainData()
''' manual labeling step'''
#createLabelRecords()
setupModelPipelineConfig()
#trainModel()
'''when happy with training'''
#moveDataToIn()
#autolabelInData()