
import os
import re
import random
import pymongo
from dotenv import load_dotenv
from datetime import date, timedelta
# from replit import db

load_dotenv()
con_str = os.getenv("DB_LINK")

mongo_client = pymongo.MongoClient(con_str)

skribbl_words_db = mongo_client.skribbl_words_db
words_collection = skribbl_words_db.words

backup_collection = skribbl_words_db.words_backup

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
    word = word.strip()
    if(len(word) > MAX_WORD_LENGTH):
      print(f'{word} is to long, maximum characters allowed is ' + str(MAX_WORD_LENGTH) + " chracters")
    if bool(re.match('[א-ת0-9\s?!]+$', word)):
      __add_word__(word, "Unknown", date.today())
    else:
      print(f'{word} containe non aturaize characters and not added to the list')
    
def get_all_words(limit=0):
  wordsModel_list = words_collection.find().limit(limit)
  list_words = []
  for wordModel in wordsModel_list: 
    word = wordModel["word"];
    list_words.append(word)
  return list_words

def get_first_words(number:int):
  if number == 0:
    return None
  return add_aradelet(get_all_words(number))

def get_last_words(number:int):
  if number == 0:
    return None
  return add_aradelet(get_all_words()[-number:])

def get_random_words(random_amount:int, last_amount = 0):
  last_words = get_last_words(last_amount)
  random_words = get_all_words(count_words() - last_amount)
  random_words = random.sample(random_words, k=random_amount)
  if last_words == None:
    return add_aradelet(random_words)
  return random_words + last_words

def get_first_last(number:int):
  try:
    return get_first_words(number) + get_last_words(number)
  except TypeError:
    return None

def add_aradelet(words):
  aradelet = "ארדלת"
  if aradelet not in words:
    words.append(aradelet)
  return words

def get_author(word):
  wordModel = words_collection.find_one({"word": word.strip()})
  if wordModel is not None:
    return wordModel["author"]
  return None

def get_all_authors():
  return words_collection.distinct("author")

def get_new_authors():
  yesterday = date.today() - timedelta(1)
  authors = words_collection.distinct("author", {"date": date.today().strftime("%d/%m/%Y")})
  yester_authors = words_collection.distinct("author", {"date": yesterday.strftime("%d/%m/%Y")})

  for author in yester_authors:
    if author not in authors:
      authors.append(author)

  return authors

def count_words():
  return words_collection.count_documents({})

def count_new_words():
  yesterday = date.today() - timedelta(1)
  return words_collection.count_documents({"date": date.today().strftime("%d/%m/%Y")}) + words_collection.count_documents({"date": yesterday.strftime("%d/%m/%Y")})

def count_by_author(author):
  return words_collection.count_documents({"author": author})

def count_by_author_new(author):
  yesterday = date.today() - timedelta(1)
  return words_collection.count_documents({"author": author, "date": date.today().strftime("%d/%m/%Y")}) + words_collection.count_documents({"author": author, "date": yesterday.strftime("%d/%m/%Y")})

def takeSecond(elem):
    return elem[1]
def stats_all():
  stats = []
  authors = get_all_authors()
  for author in authors:
    count = count_by_author(author)
    stats.append((author, count))
  stats.sort(key=takeSecond, reverse=True)
  return stats

def stats_new():
  stats = []
  authors = get_new_authors()
  for author in authors:
    count = count_by_author_new(author)
    stats.append((author, count))
  stats.sort(key=takeSecond, reverse=True)
  return stats

def copy_to_backup():
  wordsModel_list = words_collection.find()
  for word in wordsModel_list:
    try:
      backup_collection.insert_one(word)
    except pymongo.errors.DuplicateKeyError:
      w = word["word"]
      print(f"word {w} alrady exists")
  print("done")