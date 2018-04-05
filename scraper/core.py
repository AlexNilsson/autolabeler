from multitrans import translate
from gscraper import scrapeImages


def scrape(keywords, primary_lang='en', languages=['en'], limit_per_search_term=5):
  # Translate keywords to locales
  search_terms = translate(keywords, languages, primary_lang)

  # Search for and download images for every keyword in every language
  for language in search_terms.keys():
    print("\nScraping Images for language: " + language)
    print("=================================")
    scrapeImages( search_queries = search_terms[language], sub_dir_name = language, output_directory='./scraper/downloads', limit=limit_per_search_term)

  print("\nScraping Complete!")
