from languages import locales as languages

from multitrans import translate
from gscraper import scrapeImages

key_lang = 'en'
keywords = [
  'houses',
  'window'
]

locales = list(languages.keys())
#locales = ['en','sv']

result = translate(keywords, locales, key_lang)

for language in result.keys():
  scrapeImages( search_queries = result[language], sub_dir_name = language)
