import discord
import os
import dotenv
from discord.ext import commands
from dotenv.main import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot("!")

@bot.event
async def on_ready():
    channel = bot.get_channel(654908754017386523)
    print(channel)
    print(type(channel))

bot.run(token)