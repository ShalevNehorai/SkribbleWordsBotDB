import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import database_helper as helper

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')
  await bot.change_presence(activity=discord.Game('skribbl.io'))

@bot.command(name="play", help='send link to Skribbl.io')
async def play(ctx):
  await ctx.send("https://skribbl.io/")

@bot.command(name="all-words", help="return file with all the words in the DB")
async def get_all_words(ctx):
  await ctx.send('making the file')
  words = helper.get_all_words()
  if words:
    with open("words.txt", "w") as file:
      file.write(', '.join(words))
    with open("words.txt", "rb") as file:
      await ctx.send("Your file is:", file=discord.File(file, "words.txt"))
  else:
    await ctx.send('no words has been found')

@bot.command(name="all-indexed", help="return indexed file of all the words")
async def get_all_words_sorted(ctx):
  await ctx.send('making the file')
  words = helper.get_all_words()
  if words:
    with open("words.txt", "w") as file:
      file.write("\n".join([f'{i+1}: {w}' for i, w in enumerate(words)]))
    with open("words.txt", "rb") as file:
      await ctx.send("Your file is:", file=discord.File(file, "words.txt"))
  else:
    await ctx.send('no words has been found')

@bot.command(name="first-words", help='argu: number:int return file with the {number} first words')
async def get_first_words(ctx, number:int):
  await ctx.send('making the file')
  words = helper.get_first_words(number)
  if words:
    with open("words.txt", "w") as file:
      file.write(', '.join(words))
    with open("words.txt", "rb") as file:
      await ctx.send("Your file is:", file=discord.File(file, "words.txt"))
  else:
    await ctx.send('no words has been found')

@bot.command(name="last-words", help='argu: number:int return file with the {number} last words')
async def get_last_words(ctx, number:int):
  await ctx.send('making the file')
  words = helper.get_last_words(number)
  if words:
    with open("words.txt", "w") as file:
      file.write(', '.join(words))
    with open("words.txt", "rb") as file:
      await ctx.send("Your file is:", file=discord.File(file, "words.txt"))
  else:
    await ctx.send('no words has been found')

@bot.command(name="random-words", help='argu: number:int return file with {number} random words')
async def get_random_words(ctx, number:int):
  await ctx.send('making the file')
  words = helper.get_random_words(number)
  if words:
    with open("words.txt", "w") as file:
      file.write(', '.join(words))
    with open("words.txt", "rb") as file:
      await ctx.send("Your file is:", file=discord.File(file, "words.txt"))
  else:
    await ctx.send('no words has been found')

@bot.command(name="words-in-chat", help="write 75 words in chat")
async def get_words_in_chat(ctx):
  await ctx.send('working on it')
  words = helper.get_random_words(75)
  if words:
    await ctx.send(words)
  else:
    await ctx.send('no words has been found')

@bot.command(name="shuffled-last-words", help='argu: last:int, random:int return file with {last} last words and {random} random words')
async def get_last_and_random_words(ctx, last_amount:int, random_amount:int):
  await ctx.send('making the file')
  words = helper.get_last_and_random_words(last_amount, random_amount)
  if words:
    with open("words.txt", "w") as file:
      file.write(', '.join(words))
    with open("words.txt", "rb") as file:
      await ctx.send("Your file is:", file=discord.File(file, "words.txt"))
  else:
    await ctx.send('no words has been found')

@bot.command(name="words-amount", help='print the amount of words in the DB')
async def get_words_number(ctx):
  num = helper.count_words()
  await ctx.send(f'we have **{num}** words!')

@bot.command(name="count-new-words", help='print the amount of words that added in the past 48 hours')
async def count_new_words(ctx):
  num = helper.count_new_words()
  await ctx.send(f'**{num}** words added')

@bot.command(name='add-word', help='argu: arg:str add the coma separeted words in {arg} to the DB')
async def add_words(ctx, *, arg):
  MAX_WORD_LENGTH = 30
  word_list = arg.split(',')
  author = ctx.message.author
  msg_date = ctx.message.created_at
  count_words = 0
  for word in word_list:
    word = word.replace('\'', '')
    if(len(word) > MAX_WORD_LENGTH):
      await ctx.send(f'{word} is to long, maximum characters allowed is ' + str(MAX_WORD_LENGTH) + " chracters")
    elif bool(re.match('[א-ת0-9\s?!]+$', word)):
      helper.__add_word__(word, author.name, msg_date)
      count_words += 1
    else:
      await ctx.send(f'{word} containe non aturaize characters and not added to the list')

  await ctx.send(f'{author.name} has added {count_words} word to the list')
  try:
    await ctx.message.delete()
  except:
    pass

@bot.command(name='word-author', help='argu: word:str print the word author')
async def get_author(ctx, *, word):
  author = helper.get_author(word)
  if author is not None:
    await ctx.send(f'**{author}** is the author')
  else:
    await ctx.send("Word is not existing")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.CheckFailure):
    await ctx.send('you don\'t have permission for this command')
  elif isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(f'missing command argument: {error.param}')
  elif isinstance(error, commands.errors.BadArgument):
    await ctx.send(f'parameter must be number')
  elif isinstance(error, commands.errors.CommandNotFound):
    print('command not found')
    await ctx.send(f'command not found')
  else:
    await ctx.send('some error occured with the command')
    guild = ctx.guild
    log_channel = discord.utils.get(guild.channels, name='error-logs')
    if log_channel:
      await log_channel.send(error)
    else:
      await ctx.send(error)

keep_alive()
bot.run(TOKEN)