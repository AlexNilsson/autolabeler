import shutil
import os.path
import scraper
from scraper import scrapeImages, processImages
from obj_detection.utility import splitData, clearData, moveTrainDataToIn, moveToIn

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

#* 5. run script to create labelmap
#* 6. train model

''' Process data '''
#* 7. run script to collect all data which should be processed
def moveDataToIn():
  moveTrainDataToIn()
  moveToIn(PATH_TO_PROCESSED)

#* 8. run all data through the train model, cut, save, delete


#clearProject()
#scrape()
#processScraped()
splitTrainData()

#moveDataToIn()
