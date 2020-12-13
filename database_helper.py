
import os
import re
import random
import pymongo
from dotenv import load_dotenv
from datetime import date
# from replit import db

load_dotenv()
con_str = os.getenv("DB_LINK")

mongo_client = pymongo.MongoClient(con_str)

skribbl_words_db = mongo_client.skribbl_words_db
words_collection = skribbl_words_db.words

# words_collection.create_index([('word', pymongo.ASCENDING)], unique = True)

def __add_word__(word, author, msg_date):
  wordModel = {
    "word": word.strip(),
    "author": author,
    "date": msg_date.strftime("%d/%m/%Y")
  }
  try:
    words_collection.insert_one(wordModel)
  except pymongo.errors.DuplicateKeyError:
    print(f"word {word} alrady exists")
    
def add_words(words):
  MAX_WORD_LENGTH = 30
  words_list = words.split(',')
  for word in words_list:
    word = word.replace('\'', '')
    if(len(word) > MAX_WORD_LENGTH):
      print(f'{word} is to long, maximum characters allowed is ' + str(MAX_WORD_LENGTH) + " chracters")
    if bool(re.match('[א-ת0-9\s?!]+$', word)):
      __add_word__(word, "Unknown", date.today())
    else:
      print(f'{word} containe non aturaize characters and not added to the list')
    
def get_all_words():
  wordsModel_list = words_collection.find()
  list_words = []
  for wordModel in wordsModel_list: 
    word = wordModel["word"];
    list_words.append(word)
  return list_words

def get_first_words(number:int):
  return get_all_words()[:number]

def get_last_words(number:int):
  return get_all_words()[-number:]

def get_random_words(number:int):
  list_words = get_all_words()
  return random.sample(list_words, k=number)

def get_words_number():
  return words_collection.count_documents({})


# def insert_words_to_atlas(words):
#   author = "Unknown"
#   for word in words:
#     wordModel = {
#       "word": word.strip(),
#       "author": author,
#       "date": date.today().strftime("%d/%m/%Y")
#     }
#     try:
#       words_collection.insert_one(wordModel)
#     except pymongo.errors.DuplicateKeyError:
#       print(f"word {word} alrady exists")

# def move_forrepl_tomonde():
#   keys = db.keys()
#   words = []

#   for i in keys:
#     words.append(i)

#   insert_words_to_atlas(words)
#   print("done")
  