
import os
from replit import db
import random

#TODO: add non character allowed check
def __add_word__(word):
  matches = db.prefix(word)
  if matches:
    print(f'word {word} already exists')
  else:
    print(f'word: ;{word}; has added')
    db[word] = word

def add_words(words):
  wordsList = words.split(',')
  for word in wordsList:
    __add_word__(word.strip())

def get_value(word):
  matches = db.prefix(word)
  if matches:
    return db[word]
    
def get_all_words():
  keys = db.keys()
  print(keys)
  words = ""
  for i in keys:
    word = get_value(i)
    words += f'{word}, '
    print(i)
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

#del db["43242#$@עובד"]



  