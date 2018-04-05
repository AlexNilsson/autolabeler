from .languages import locales as languages
from .processing import process as processImages

from multitrans import translate
from gscraper import scrapeImages


def scrape():

  PRIMARY_LANG = 'en'
  KEYWORDS = [
    'houses',
    'window'
  ]
  LOCALES = ['en','sv']
  #LOCALES = list(languages.keys())

  # Translate keywords to locales
  search_terms = translate(KEYWORDS, LOCALES, PRIMARY_LANG)

  # Search for and download images for every keyword in every language
  for language in search_terms.keys():
    print("\nScraping Images for language: " + language)
    print("=================================")
    scrapeImages( search_queries = search_terms[language], sub_dir_name = language, output_directory='./scraper/downloads')

  print("\nScraping Complete!")

  processImages(remove_downloaded=True)
