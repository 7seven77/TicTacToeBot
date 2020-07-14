# bot.py
import os
import random
import re

from discord.ext import commands
from dotenv import load_dotenv

### Functions

## functions

# If the game is complete, return the token that has won
def victory(string):
    win = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
           [1, 4, 7], [2, 5, 8], [3, 6, 9],
           [1, 5, 9], [3, 5, 7]]
    for combo in win:
        if string[combo[0] - 1] == string[combo[1] - 1] and string[combo[0] - 1] == string[combo[2] - 1] and string[combo[2] - 1] != '.':
            return string[combo[0] - 1]
    return '.'

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

## async functions

async def showBoardState(ctx):
    if bot.board == None:
        await ctx.send("No game is being played")
    else:
        if bot.turn == 1:
            user = await bot.fetch_user(bot.opponent)
        else:
            user = await bot.fetch_user(bot.challenger)
        await ctx.send('It\'s ' + user.mention + '\'s turn \n')
        await ctx.send(getBoard())


# This is what a command must start with
botPrefix = '7'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=botPrefix)

bot.board = None
bot.challenger = None
bot.opponent = None
bot.turn = None
bot.validMoves = ['1', '2' ,'3', '4', '5', '6', '7', '8', '9']

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
    if bot.board != None:
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
        bot.board = '.........'
        bot.challenger = taggerID
        bot.opponent = taggedID
        bot.turn = -1
        bot.validMoves = ['1', '2' ,'3', '4', '5', '6', '7', '8', '9']
        await ctx.send('Starting a game')

# Play the game
@bot.command(name='play', help='Take your turn')
async def play(ctx, move):
    if bot.board == None:
        await ctx.send('No one has started a game')
        return
    if bot.turn == 1:
        expectedID = bot.opponent
    else:
        expectedID = bot.challenger
    taggerID = str(ctx.author.id)
    if (taggerID != expectedID):
        await ctx.send('It is not your turn')
        return
    if not move in bot.validMoves:
        await ctx.send('This is not a valid move')
        return
    bot.validMoves.remove(move)
    if bot.turn == 1:
        icon = 'x'
    else:
        icon = 'o'
    index = int(move) - 1
    board = bot.board
    board = board[:index] + icon + board[index + 1:]
    bot.board = board
    bot.turn *= -1;
    await showBoardState(ctx)
    victor = victory(bot.board)
    if victor != '.':
        if bot.turn == -1:
            user = await bot.fetch_user(bot.opponent)
        else:
            user = await bot.fetch_user(bot.challenger)
        bot.board = None
        await ctx.send('{} has won'.format(user.mention))
    if len(bot.validMoves) == 0:
        bot.board = None
        await ctx.send('The game is a draw')
bot.run(TOKEN)
