import os
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

#TODO check the value is intager
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
  helper.add_words(arg)
  await ctx.send('Words added to the list')

keep_alive()
bot.run(TOKEN)