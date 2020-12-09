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

@bot.command(name="give-words", help="write 75 words in chat")
async def get_words_in_chat(ctx):
  await ctx.send('working on it')
  words = helper.get_random_words(75)
  if words:
    await ctx.send(words)
  else:
    await ctx.send('no words has been found')

@bot.command(name="words-amount", help='print the amount of words in the DB')
async def get_words_number(ctx):
  num = helper.get_words_number()
  await ctx.send(f'we have **{num}** words!')

@bot.command(name='add-word', help='argu: arg:str add the coma separeted words in {arg} to the DB')
async def add_words(ctx, *, arg):
  word_list = arg.split(',')
  author = ctx.message.author
  msg_date = ctx.message.created_at
  count_words = 0
  for word in word_list:
    word = word.replace('\'', '')
    if bool(re.match('[א-ת0-9\s]+$', word)):
      helper.__add_word__(word, author.name, msg_date)
      count_words += 1
    else:
      await ctx.send(f'{word} containe non aturaize characters and not added to the list')

  await ctx.send(f'{author.name} has added {count_words} word to the list')
  await ctx.message.delete()

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