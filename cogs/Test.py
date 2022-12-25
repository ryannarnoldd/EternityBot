import discord
from discord import app_commands
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @app_commands.command(name="test", description="Test command!")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Testing, Testing, 1, 2, 3...")

async def setup(bot):
    await bot.add_cog(Test(bot), guilds=[bot.GUILD])