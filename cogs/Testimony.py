import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from discord import Embed
import json
import asyncio
from components.TestimonyModal import TestimonyModal

global TESTIMONIES_FILE
TESTIMONIES_FILE = 'data/testimonies.json'
testimony = ''

class Testimony(commands.GroupCog, name="testimony"):
    global testing
    def __init__(self, bot):
        self.bot = bot
        self.testimonies = json.load(open(TESTIMONIES_FILE, 'r'))

    async def save_testimonies(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(TESTIMONIES_FILE, 'w') as testimonies:
                testimonies.write(json.dumps(self.testimonies, indent=4))
            await asyncio.sleep(0.05)
    
    async def set_testimony(self, author, testimony):
        if not testimony.isspace():
            self.testimonies[str(author.id)] = testimony
            await self.save_testimonies(); return

    @app_commands.command(name="set", description="Set your testimony.")
    async def set(self, interaction: discord.Interaction):
        T = TestimonyModal()
        await asyncio.create_task(interaction.response.send_modal(T))
        while await T.wait(): await asyncio.sleep(0.05)

        # if not T.testimony.value.isspace():
        #     description = 'Your testimony has been set!'
        await self.set_testimony(interaction.user, T.testimony.value)
        # else:
        #     description = 'Your testimony has not been set. Enter a valid testimony and try again.'
        # embed = discord.Embed(title=f'Your Testimony', description=description, color=discord.Colour.blue())
        # await interaction.response.send_message(embed=embed, ephemeral=True)


    
    # @app_commands.command(name="view", description="View your testimony, or someone else's.")
    # @app_commands.describe(user = 'The user.')
    # async def view(self, interaction: discord.Interaction, user: discord.Member = None) -> None:
    #     if user is None: user = interaction.user
    #     if user.id in self.testimonies:
    #         testimony = self.testimonies[user.id]
    #     else:
    #         testimony = f'They have not set their testimony yet!'

    #     await interaction.response.send_message(embed = Embed(title=f'{user.name}\'s Testimony', description=testimony, color=discord.Colour.blue()), ephemeral=True)        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Testimony(bot))
