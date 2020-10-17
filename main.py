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

@bot.command(name="all-words")
async def get_all_words(ctx):
  words = helper.get_all_words()
  if words:
    await ctx.send(words)
  else:
    await ctx.send('no words has been found')

@bot.command(name="first-words")
async def get_first_words(ctx, number:int):
  words = helper.get_first_words(number)
  if words:
    await ctx.send(', '.join(words))
  else:
    await ctx.send('no words has been found')

@bot.command(name="last-words")
async def get_last_words(ctx, number:int):
  words = helper.get_last_words(number)
  if words:
    await ctx.send(', '.join(words))
  else:
    await ctx.send('no words has been found')

@bot.command(name="random-words")
async def get_random_words(ctx, number:int):
  words = helper.get_random_words(number)
  if words:
    await ctx.send(', '.join(words))
  else:
    await ctx.send('no words has been found')

@bot.command(name="words-amount")
async def get_words_number(ctx):
  num = helper.get_words_number()
  await ctx.send(num)

@bot.command(name='add-word')
async def add_words(ctx, *, arg):
  word_list = arg.split(',')
  count_words = 0
  for word in word_list:
    if bool(re.match('[א-ת0-9\s]+$', word)):
      helper.__add_word__(word)
      count_words += 1
    else:
      await ctx.send(f'{word} contine non aturaize characters and not added to the list')

  await ctx.send(f'{count_words} Words added to the list')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.CheckFailure):
    await ctx.send('you don\'t have permission for this command')
  elif isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(f'missing command argument {error.param}')
  elif isinstance(error, commands.errors.BadArgument):
    await ctx.send(f'parameter must be number')
  elif isinstance(error, commands.errors.CommandNotFound):
    print('command not found')
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