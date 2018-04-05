import scraper
from scraper import scrapeImages, processImages

''' Gather Data '''
#* 0. Run the cleanslate script to clean the project

#scraper.downloads
#scraper.processed

#* 1. Run the scraper for selected keywords and languages
PRIMARY_LANG = 'en'
KEYWORDS = [
  'houses',
  'window'
]
LANGUAGES = ['en','sv'] #=list(scraper.languages.keys())
MAX_IMAGES_PER_SEARCH_TERM = 5

scrapeImages(KEYWORDS, primary_lang=PRIMARY_LANG, languages=LANGUAGES, limit_per_search_term=MAX_IMAGES_PER_SEARCH_TERM)


#*2. run the postprocessing script to process the images
REMOVE_DOWNLOADED = True

processImages(remove_downloaded=REMOVE_DOWNLOADED)

''' Train object detection model '''
#* 3. run the split script to split the data into train, test, batches
  NR_OF_TRAINING_IMAGES = 300     # when training the model
  NR_OF_VALIDATION_IMAGES = 100   # when evaluating this model compared to other models (select best model based on this)
  NR_OF_TEST_IMAGES = 100         # when testing this and any other model (the test score of each model)

  # count total nr om images collected,
  # error if too little

  # from processed, pick at random to fill these three folders, move rest to /in

#* 4. label train batches

#* 5. run script to create labelmap
#* 6. train model

''' Process data '''
#* 7. run script to collect all data which should be processed
  # move /train, /test, /val to ->> /in

#* 8. run all data through the train model, cut, save, delete



