import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

GUILD = discord.Object(id=1045498586105913345)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

bot = Bot()
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def hi(ctx):
    await ctx.send('Hello!')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    await bot.process_commands(message) 

async def load_cogs():
    for file in os.listdir('cogs'):
            if file.endswith('.py'):
                await bot.load_extension(f'cogs.{file[:-3]}')
                print(f'Loaded {file[:-3]}...')
        
async def main():
    await load_cogs()
    await bot.start(os.getenv('TOKEN'))

asyncio.run(main())