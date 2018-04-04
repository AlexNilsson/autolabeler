from languages import locales as languages

from multitrans import translate
from gscraper import scrapeImages

#* 0. Setup
key_lang = 'en'
keywords = [
  'houses',
  'window'
]

locales = list(languages.keys())
locales = ['en','sv']

#* 1. Translate keywords to locales
search_terms = translate(keywords, locales, key_lang)

#* 2. Search for and download images for every keyword in every language
for language in search_terms.keys():
  print("\n Scraping Images for language: " + language)
  print("=================================")
  scrapeImages( search_queries = search_terms[language], sub_dir_name = language)

#* 3. Run ImageDetection Inference
#https://www.youtube.com/watch?v=Rgpfk6eYxJA&t=2s

#* 4. Cut & Save Identified, Delete rest

#* 5. Profit!

