from discord.ext import commands
import discord
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', brief='It will roll dice!', aliases=['dice','die','rolldie'])
    async def roll(self, ctx, max = '6'):
        if max.isdigit() and int(max) > 0: result = f'1-{int(max)}:  **{random.randint(1,int(max))}**'
        else: result = 'Please enter a valid number!'

        await ctx.send(embed = discord.Embed(
            title = 'Dice Roll :game_die:',
            description = result, 
            color = discord.Color.blue()
        ))


    @commands.command(name='roulette', brief="Here's your chance if you ever wanted to die!", pass_context=True, aliases=['rr', 'russian'])
    async def russianroulette(self, ctx, chance = '6'):
        if chance.isdigit() and int(chance) > 1:
            chance = random.randint(1, int(chance))
            result = "has **lived**!" if chance != 1 else "has **died**!"
            reaction = '😇' if chance != 1 else '💀'
            result = f'**{chance}** bullets\n{ctx.author.mention} {result}'
        else:
            result = f'Sorry, I don\'t think **{chance}** bullets is fair for both you and I...'
            reaction = '🧐'

        msg = await ctx.send(embed = discord.Embed(
                    title = 'Russian Roulette :gun:',
                    description = result,
                    color = discord.Colour.blue()
                ))
        
        await msg.add_reaction(reaction)

async def setup(bot):
    await bot.add_cog(Fun(bot))