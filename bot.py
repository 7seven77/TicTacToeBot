# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

## Functions

# Return the board in a printable format
def getBoard():
    return 'Not implemented'
    
# This is what a command must start with
botPrefix = '7'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=botPrefix)

bot.board = None

# Initialise the bot when it first becomes ready
@bot.event
async def on_ready():
    print("Ready")

# Greets the user when they call it
@bot.command(name='hello', help='Says hello!')
async def hello(ctx):
    greetings = ["Hey {}!", "Hello {}", "Hey {}, how are you doing?",
                 "Yo {}", "Salam {}", "Allo {}"]
    await ctx.send(random.choice(greetings).format(ctx.author.mention));

# Displays the status of the game
@bot.command(name='status', help='Show the status of the game')
async def status(ctx):
    if bot.board == None:
        await ctx.send("No game is being played")
    else:
        await ctx.send(getBoard())

# Start a game
@bot.command(name='start', help='Start a game')
async def start(ctx, other):
    if bot.board != None:
        await ctx.send("There is a game already being played")
    else:
        bot.board = '.........'
        await ctx.send('Starting a game')

bot.run(TOKEN)
