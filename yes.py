import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
load_dotenv()
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class yes(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.sync = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1045498586105913345))
        self.sync = True
        print("Bot Is Online")

bot = yes()
tree = app_commands.CommandTree(bot)
    
@tree.command(name='echo', description='Pong!', guild=discord.Object(id=1045498586105913345))
async def ping(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

bot.run(os.getenv('TOKEN'))