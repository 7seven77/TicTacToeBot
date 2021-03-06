# bot.py
import os
import random
import re

import discord

from NaCMatch import NaCMatch
from discord.ext import commands
from dotenv import load_dotenv

##### Functions

### functions

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

#####

# Returns a string representing the ID of the mention
def extractID(mention):
    return str(re.sub(r'[^\w]', '', mention))
    
### async functions

# Shows the state of the game to the user
async def showBoardState(ctx):
    if bot.match == None:
        await ctx.send("No game is being played")
    else:
        user = await getUser(bot.match.getCurrentPlayer())
        await ctx.send('Its ' + user.mention + 's turn')
        await ctx.send(getBoard())

#####
        
# Returns true if the ID given is a valid user
async def isValidID(test):
    try:
        user = await getUser(test)
        return True
    except:
        return False

#####
    
# Returns the user associated with an ID
async def getUser(userID):
    try:
        return await bot.fetch_user(userID)
    except:
        return None

##### Bot stuff
    
# This is what a command must start with
botPrefix = '7'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=botPrefix)

bot.match = None

##### Events

# Initialise the bot when it first becomes ready
@bot.event
async def on_ready():
    bot.acceptorID = None
    bot.challengerID = None
    await bot.change_presence(activity=discord.Game(name="Noughts and Crosses 7help"))
    print("Ready")

##### Commands
    
# Greets the user when they call it   
@bot.command(name='hello', help='Says hello!')
async def hello(ctx):
    greetings = ["Hey {}!", "Hello {}", "Hey {}, how are you doing?",
                 "Yo {}", "Salam {}", "Allo {}"]
    await ctx.send(random.choice(greetings).format(ctx.author.mention));

#####
    
# Displays the status of the game
@bot.command(name='status', help='Show the status of the game')
async def status(ctx):
    if bot.acceptorID != None:
        await ctx.send('{} must accept or decline the challenge'.format((await getUser(bot.acceptorID)).mention))
        return
    await showBoardState(ctx)

#####
    
# Start a game
@bot.command(name='start', help='Start a game (Tag a user)')
async def start(ctx, other):
    if other == 'help':
        await ctx.send('''```7start @user\n@user - Tag the user you would like to play with```''')
        return
    if bot.match != None:
        await ctx.send("There is a game already being played")
        return
    if bot.acceptorID != None:
        await ctx.send('There is already a game proposal active')
    else:
        taggedID = extractID(other)
        if not await isValidID(taggedID):
            await ctx.send('That is not a valid user')
            return
        taggerID = str(ctx.author.id)
        botID = str(bot.user.id)
        if (taggedID == taggerID):
            await ctx.send('You cannot play against yourself')
            return
        elif (taggedID == botID):
            await ctx.send('Sorry, I don\'t know how to play');
            return
        bot.acceptorID = taggedID
        bot.challengerID = taggerID
        await ctx.send('{} has challenged {} to a match!'.format((await getUser(taggerID)).mention, (await getUser(taggedID)).mention))
        await ctx.send('Use the command \'7accept\' to start the match or \'7decline\' to reject the proposal')

#####

# Accept a challenge
@bot.command(name='accept', help='Accept the challenge and start a match')
async def accept(ctx):
    if bot.match != None:
        await ctx.send("There is a game already being played")
        return
    if bot.acceptorID == None:
        await ctx.send('There is no game proposol active')
        return
    if (str(ctx.author.id) != bot.acceptorID):
        await ctx.send('You cannot accept the challenge')
        return
    bot.match = NaCMatch(bot.challengerID, bot.acceptorID)
    await ctx.send('Starting a game')
    await showBoardState(ctx)

#####

# Decline a challenge
@bot.command(name='decline', help='Decline the challenge')
async def decline(ctx):
    if bot.match != None:
        await ctx.send("There is a game already being played")
        return
    if bot.acceptorID == None:
        await ctx.send('There is no game proposol active')
        return
    if (str(ctx.author.id) != bot.acceptorID):
        await ctx.send('You cannot decline the challenge')
        return
    bot.acceptorID = None
    bot.challengerID = None
    await ctx.send('You have declined the challenge')
#####
        
# Play the game
@bot.command(name='play', help='Take your turn (The move you want to play)')
async def play(ctx, move):
    if move == 'help':
        await ctx.send('''```7play move\nmove - Enter a valid move, where you would like to place your token```Enter the number that correspond to the cell you want to play your token at:\n:one: :two: :three:\n:four: :five: :six:\n:seven: :eight: :nine:''')
        return
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
                bot.acceptorID = None
                bot.challengerID = None
                user = await getUser(winner)
                await ctx.send('{} wins the game'.format(user.mention))
        else:
            await showBoardState(ctx)

#####

# Forfeit the match
@bot.command(name='surrender', help='Give up and lose the match')
async def surrender(ctx):
    if bot.match == None:
        await ctx.send('There is no game being played')
        return
    user = str(ctx.author.id)
    if not (user == bot.match.challenger or user == bot.match.opponent):
        await ctx.send('You are not in this game')
        return
    players = bot.match.getPlayers()
    players.remove(user)
    winner = players[0]
    bot.match = None
    bot.acceptorID = None
    bot.challengerID = None
    await ctx.send('{} has won the game'.format((await getUser(winner)).mention))

bot.run(TOKEN)
