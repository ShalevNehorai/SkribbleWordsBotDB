
from replit import db
import random
import re

def __add_word__(word):
  matches = db.prefix(word)
  if matches:
    print(f'word {word} already exists')
  else:
    db[word] = word
    print(f'word: ;{word}; has added')
    
def add_words(words):
  words_list = words.split(',')
  for word in words_list:
    word = word.replace('\'', '')
    if bool(re.match('[א-ת0-9\s]+$', word)):
      __add_word__(word)
    else:
      print(f'{word} containe non aturaize characters and not added to the list')

def get_value(word):
  matches = db.prefix(word)
  if matches:
    return db[word]
    
def get_all_words():
  keys = db.keys()
  words = ""
  for i in keys:
    word = get_value(i)
    words += f'{word}, '
  return words

def get_first_words(number:int):
  keys = db.keys()
  list_words = []

  for i in keys:
    list_words.append(get_value(i))

  return list_words[:number]

def get_last_words(number:int):
  keys = db.keys()
  list_words = []

  for i in keys:
    list_words.append(get_value(i))

  return list_words[-number:]

def get_random_words(number:int):
  keys = db.keys()
  list_words = []

  for i in keys:
    list_words.append(get_value(i))

  if len(list_words) < number:
    number = len(list_words)
  
  return random.sample(list_words, k=number)

def get_words_number():
  keys = db.keys()
  return len(keys)



def delete_key(key):  
  matches = db.prefix(key)
  if matches:
    del db[key]
    print(f'delete key: {key}')
  else:
    print('the key not exists')

def delete_all_list():
  keys = db.keys()
  for key in keys:
    delete_key(key)
  print('all keys deleted')

  