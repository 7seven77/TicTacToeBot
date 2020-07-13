# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

# This is what a command must start with
botPrefix = '7'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=botPrefix)

# Greets the user when they call it
@bot.command(name='hello', help='Says hello!')
async def hello(ctx):
    greetings = ["Hey {}!", "Hello {}", "Hey {}, how are you doing?",
                 "Yo {}", "Salam {}", "Allo {}"]
    await ctx.send(random.choice(greetings).format(ctx.author.mention));

# Displays the status of the game
@bot.command(name='status', help='Show the status of the game')
async def status(ctx):
    # If the value has not been set yet, a game is not being played
    try:
        if (board):
            print("Value has been set");
    except NameError:
        await ctx.send("No game is being played")
bot.run(TOKEN)
