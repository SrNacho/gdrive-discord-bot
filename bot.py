import discord
import os
from discord import colour
import dotenv
from discord.ext import commands
from dotenv.main import load_dotenv
from service.mainscrapper import bot
from discord import File
from discord import Embed

botmain = bot()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot("!")

@bot.event
async def on_ready():
    channel = bot.get_channel(654908754017386523)
    embed = Embed(title="@everyone Nuevo cambio en el drive del colegio!",embed="rich",colour=0xc27c0e,_author="Nacho")
    
    while True:
        if botmain.start() == 200:
            faile = File("./imgs/{f}-imagen.png".format(f=botmain.d))
            await channel.send(file=faile,embed=embed)
            print(botmain.d)

bot.run(TOKEN)