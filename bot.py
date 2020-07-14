# bot.py
import os
import random
import re

from discord.ext import commands
from dotenv import load_dotenv

## Functions

# Return the board in a printable format
def getBoard():
    newRow = 0;
    display = '';
    for character in bot.board:
        if character == '.':
            display += ':white_large_square:'
        else:
            display += ':' + character + ':'
        newRow += 1
        if (newRow % 3) == 0:
            display += "\n"
    return display
    
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
        taggedID = str(re.sub(r'[^\w]', '', other))
        taggerID = str(ctx.author.id)
        botID = str(bot.user.id)
        if (taggedID == taggerID):
            await ctx.send('You cannot tag yourself')
            return
        elif (taggedID == botID):
            await ctx.send('Sorry, I don\'t know how to play');
            return
        bot.board = '.........'
        await ctx.send('Starting a game')

bot.run(TOKEN)
