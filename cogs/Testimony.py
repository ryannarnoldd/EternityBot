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

testimony_help = {
    'set': 'Set your testimony.',
    'view': 'View your testimony, or someone else\'s.',
    'help': 'Show this help guide.'
}

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
        await self.set_testimony(interaction.user, T.testimony.value)
    
    @app_commands.command(name="view", description="View your testimony, or someone else's.")
    @app_commands.describe(user = 'The user.')
    async def view(self, interaction: discord.Interaction, user: discord.Member = None) -> None:
        user = user or interaction.user
        
        if str(user.id) in self.testimonies:
            testimony = self.testimonies[str(user.id)]
        else:
            testimony = f'They have not set their testimony yet!'

        embed = Embed(title=f'{user.name}\'s Testimony', description=testimony, color=discord.Colour.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="help", description="Show this help guide.")
    async def help(self, interaction: discord.Interaction):
        testimonies_help = '\n'.join([f'`{cmd}` - {testimony_help[cmd]}' for cmd in testimony_help])
        await interaction.response.send_message(embed = Embed(title='Testimony Help', description=testimonies_help, color=discord.Colour.blue()), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Testimony(bot))
