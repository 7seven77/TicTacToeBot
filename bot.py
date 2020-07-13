# bot.py
import os

from discord.ext import commands
from dotenv import load_dotenv

# This is what a command must start with
botPrefix = '7'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=botPrefix)

@bot.command(name='hello', help='Says hello!')
async def hellp(ctx):
    await ctx.send("Hey");

bot.run(TOKEN)
