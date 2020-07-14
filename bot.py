# bot.py
import os
import random
import re

from NaCMatch import NaCMatch
from discord.ext import commands
from dotenv import load_dotenv

### Functions

## functions

# Return the board in a printable format
def getBoard():
    newRow = 0;
    display = '';
    for character in bot.match.board:
        if character == '.':
            display += ':white_large_square:'
        else:
            display += ':' + character + ':'
        newRow += 1
        if (newRow % 3) == 0:
            display += "\n"
    return display

## async functions

async def showBoardState(ctx):
    if bot.match == None:
        await ctx.send("No game is being played")
    else:
        user = await bot.fetch_user(bot.match.getCurrentPlayer())
        await ctx.send('Its ' + user.mention + 's turn')
        await ctx.send(getBoard())


# This is what a command must start with
botPrefix = '7'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=botPrefix)

bot.match = None

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
    await showBoardState(ctx)

# Start a game
@bot.command(name='start', help='Start a game')
async def start(ctx, other):
    if bot.match != None:
        await ctx.send("There is a game already being played")
    else:
        taggedID = str(re.sub(r'[^\w]', '', other))
        taggerID = str(ctx.author.id)
        botID = str(bot.user.id)
        if (taggedID == taggerID):
            await ctx.send('You cannot play against yourself')
            return
        elif (taggedID == botID):
            await ctx.send('Sorry, I don\'t know how to play');
            return
        bot.match = NaCMatch(taggerID, taggedID)
        await ctx.send('Starting a game')
        await showBoardState(ctx)

# Play the game
@bot.command(name='play', help='Take your turn')
async def play(ctx, move):
    if bot.match == None:
        await ctx.send('No one has started a game')
        return
    taggerID = str(ctx.author.id)
    turn = bot.match.takeTurn(taggerID, move)
    if turn == 'Player':
        await ctx.send('It is not your turn')
    elif turn == 'Move':
        await ctx.send('That is not a valid move')
    else:
        if bot.match.isOver():
            winner = bot.match.getVictor()
            if winner == '.':
                await ctx.send('The match is a draw')
            else:
                bot.match = None
                user = await bot.fetch_user(winner)
                await ctx.send('{} wins the game'.format(user.mention))
        else:
            await showBoardState(ctx)
bot.run(TOKEN)
