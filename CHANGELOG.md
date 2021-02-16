# CHANGE LOG 6 - 2021-02-16

## ADDED

### BOT COMMANDS
- stats-all: print the amount of words that each author has added to the DB
- stast-new: print the amount of words that each author has added to the DB in the last 48 hours

## CHANGES
- all-indexed command now called indexed

---

# CHANGE LOG 5 - 2021-02-08

## ADDED

### BOT COMMANDS
- first-last: send file with first and last words

## CHANGES
- help command now look better
- change most of the command names to simpler one
- merge shuffled-new-words command with random command, random command now can get optional value to send file with some last words and some random words

## DELETED
- shaffled-last-words command was deleted
- play command was deleted

---

# CHANGE LOG 4 - 2020-12-16

## ADDED

### BOT COMMANDS
- play: send the skribbl.io url
- shaffled-last-words: send file with some last words and some random words
- count-new-words: send massage with the number of words that added in the past 48 hours
- word-author: send the word author

## CHANGES
- every command that sends words allways sends ארדלת too 
- minor change to get_first_words method

---

# CHANGE LOG 3 - 2020-12-09
  NEW DB!! now using mongoDB instead of repl.it DB

## ADDED

- from now saving who wrote the word and the date that the word has been added to the DB
- added limit for words that can be added to the DB

## CHANGES
- characters allowed in words has been change


