import discord
from discord import app_commands
from discord.ext import commands

class Pray(commands.GroupCog, name="pray"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.command(name="list")
    async def list(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from list", ephemeral=True)
    
    @app_commands.command(name="add")
    async def add(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from add", ephemeral=True)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Pray(bot))