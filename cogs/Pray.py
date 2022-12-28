import discord
from discord.ext import commands
from discord import app_commands
import typing
from components.PrayerList import PrayerList
from discord import Embed
import json

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'
global DATE_FORMAT
DATE_FORMAT = '%Y:%m:%d:%H:%M'

help_guide = {
    'list <mention>': 'List all prayer requests of you, or someone else!',
    'add <prayer>': 'Add a prayer request to your list',
    'ans <number>': 'Mark a prayer request as answered (Praise God!)',
    'help': 'Show this help guide'
}



class Pray(commands.GroupCog, name="pray"):
    def __init__(self, bot):
        self.bot = bot

        with open(PRAYERS_FILEPATH, 'r') as prayers:
            self.prayers = json.load(prayers)

    def get_prayer_list(self, id):
        name = self.bot.get_user(int(id)).name
        user_prayers = [prayer for prayer in self.prayers if prayer["uid"] == str(id)]
        prayer_list = ''

        return user_prayers

    @app_commands.command(name="help", description="Pray for others or yourself.")
    async def help(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from help", ephemeral=True)
    
    @app_commands.command(name="list", description="List the prayers.")
    async def list(self, interaction: discord.Interaction) -> None:
        theList = self.get_prayer_list(interaction.user.id)
        view = PrayerList(theList, 'Prayer Requeests for me')
        await view.start(interaction)

    @app_commands.command(name="recent", description="List the recent n prayers.")
    async def recent(self, interaction: discord.Interaction, n: int = 5) -> None:
        view = PrayerList([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 'hi')
        await interaction.response.send_message("Hello from recent", ephemeral=True, view=view)

    @app_commands.command(name="add", description="Add a prayer.")
    @app_commands.describe(
        prayer="The prayer",
        description="The description"
    )
    async def add(self, interaction: discord.Interaction, prayer: str, description: typing.Optional[str] = '') -> None:
        await interaction.response.send_message(f"Hello from add {prayer} {description}", ephemeral=True)

    @app_commands.command(name="answer", description="Mark a prayer as answered. (Praise God!)")
    async def answer(self, interaction: discord.Interaction, index: int) -> None:
        await interaction.response.send_message(f"Hello from answer {index}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Pray(bot))
