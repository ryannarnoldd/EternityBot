import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
import random

greetings = ['hello', 'hi', 'hey', 'yo', 'sup', 'wassup']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

# On ready event.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# On message event.
@bot.event
async def on_message(message):
    if message.author == bot.user: return

    print(f'{message.author.mention}')

    # If the message contains any of the greetings, reply with a greeting!
    if any(greet in message.content.lower().strip() for greet in greetings):
        await message.reply('Hello!')

    # Processes commands registered with the bot.
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