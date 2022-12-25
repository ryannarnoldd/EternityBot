import asyncio
import discord
from discord.ext import commands
import os
from discord import app_commands
from dotenv import load_dotenv
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context # or a subclass of yours
load_dotenv()

GUILD = discord.Object(id=1045498586105913345)

class Bot(commands.Bot):
    GUILD = discord.Object(id=1045498586105913345)
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

bot = Bot()
bot.remove_command('help')

# On ready event.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# On message event.
# Bot is not able to use commands.
@bot.event
async def on_message(message):
    if message.author == bot.user: return
    await bot.process_commands(message) 

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'Loading {filename[:-3]}...')
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load_cogs()
    await bot.start(os.getenv('TOKEN'))

asyncio.run(main())