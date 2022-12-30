import discord
from discord.ext import commands
from discord import app_commands
import typing
from components.PrayerList import PrayerList
from discord import Embed
import json
import datetime 
from datetime import datetime
import asyncio

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'
global DATE_FORMAT
DATE_FORMAT = '%Y:%m:%d:%H:%M'

help_guide = {
    'list <user>': 'List all prayer requests of you, or someone else!',
    'add <prayer>': 'Add a prayer request to your list',
    'answer <index>': 'Mark a prayer request as answered (Praise God!)',
    'help': 'Show this help guide'
}

class Pray(commands.GroupCog, name="pray"):
    def __init__(self, bot):
        self.bot = bot
        self.prayers = json.load(open(PRAYERS_FILEPATH, 'r'))

    def get_current_prayers(self, id):
        return [prayer for prayer in self.prayers if prayer["uid"] == str(id) and not prayer["answered"]]

    def get_recent_prayers(self):
        return [prayer for prayer in self.prayers if not prayer["answered"]][:50]

    async def save_prayers(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(PRAYERS_FILEPATH, 'w') as prayers:
                prayers.write(json.dumps(self.prayers, indent=4))
            await asyncio.sleep(0.05)

    async def add_prayer(self, author, prayer, description=""):
        self.prayers.insert(0, {
            "uid": str(author.id),
            "prayer": prayer,
            "description": description,
            "time": datetime.now().strftime(DATE_FORMAT),
            "answered": False
        })
        await self.save_prayers(); return

    async def answer_prayer(self, author, index):
        prayers = [prayer for prayer in self.prayers if prayer["uid"] == str(author.id)]
        if 0 < index <= len(prayers):
            prayers[index-1]["answered"] = True
        await self.save_prayers()

    @app_commands.command(name="add", description="Add a prayer.")
    @app_commands.describe(prayer = 'The prayer.', description = 'The description.')
    async def add(self, interaction: discord.Interaction, prayer: str, description: typing.Optional[str] = '') -> None:
        await interaction.response.send_message(embed = Embed(title='Prayer Request Added', description=f'*{prayer}* added to your prayer requests!', color=discord.Colour.blue()), ephemeral=True)
        await self.add_prayer(interaction.user, prayer, description)

    @commands.hybrid_command(name= 'answer', description = 'Mark a prayer as answered. (Praise God!)')
    async def answer(self, interaction: discord.Interaction, index: int) -> None:
        await interaction.response.send_message(embed = Embed(title='Prayer Request Answered', description=f'*{self.prayers[index-1]["prayer"]}* was marked as answered! (Praise God!)', color=discord.Colour.blue()), ephemeral=True)
        await self.answer_prayer(interaction.user, index)
    
    @app_commands.command(name = 'list', description = 'List the <user>\'s prayers.')
    async def list(self, interaction: discord.Interaction, user: discord.Member) -> None:
        userID = user.id if user else interaction.user.id
        prayers = self.get_current_prayers(userID)
        view = PrayerList(prayers, f'{user.name}\'s Prayer Requests')
        await view.start(interaction)

    @app_commands.command(name = 'recent', description = 'List the recent unanswered prayers.')
    async def recent(self, interaction: discord.Interaction) -> None:
        view = PrayerList(self.get_recent_prayers(), f'Recent Prayer Requests')
        await view.start(interaction)

    @app_commands.command(name = 'help', description = 'Show this help guide!')
    async def help(self, interaction: discord.Interaction) -> None:
        prayers_help = '\n'.join([f'`{cmd}` - {help_guide[cmd]}' for cmd in help_guide])
        await interaction.response.send_message(embed = Embed(title='Prayer Request Help', description=prayers_help, color=discord.Colour.blue()), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Pray(bot))