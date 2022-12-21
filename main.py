import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

# Search Hybrid Commands for more information on how to use this.


load_dotenv()

greetings = ['hello', 'hi', 'hey', 'yo', 'sup', 'wassup']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# On ready event.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# On message event.
@bot.event
async def on_message(message):
    if message.author == bot.user: return

    # If the message contains any of the greetings, reply with a greeting!
    if any(greet in message.content.lower().strip() for greet in greetings):
        await message.reply('Hello!')

    # Processes commands registered with the bot.
    await bot.process_commands(message)

# Roll command.
@bot.command(name='roll', brief='It will roll dice!', aliases=['dice','die','rolldie'])
async def roll(ctx, max = '6'):
    if max.isdigit() and int(max) > 0: result = f'1-{int(max)}:  **{random.randint(1,int(max))}**'
    else: result = 'Please enter a valid number!'

    await ctx.send(embed = discord.Embed(
        title = 'Dice Roll',
        description = result, 
        color = discord.Color.blue()
    ))


@bot.command(name='roulette', brief="Here's your chance if you ever wanted to die!", pass_context=True, aliases=['rr', 'russian'])
async def russianroulette(ctx, chance = '6'):
    if chance.isdigit() and int(chance) > 1:
        chance = random.randint(1, int(chance))
        result = "has **lived**!" if chance != 1 else "has **died**!"
        reaction = '😇' if chance != 1 else '💀'
        result = f'**{chance}** bullets\n{ctx.author.mention} {result}'
    else:
        result = f'Sorry, I don\'t think **{chance}** bullets is fair for both you and I...'
        reaction = '🧐'

    msg = await ctx.send(embed = discord.Embed(
                title = 'Russian Roulette',
                description = result,
                color = discord.Colour.blue()
            ))
    
    await msg.add_reaction(reaction)



bot.run(os.getenv('TOKEN'))