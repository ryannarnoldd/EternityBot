import discord
from discord.ext import commands
from discord import app_commands
import typing

class Pray(commands.GroupCog, name="pray"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="help", description="Pray for others or yourself.")
    async def help(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from help", ephemeral=True)
    
    @app_commands.command(name="list", description="List all prayers.")
    async def list(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from list", ephemeral=True)

    @app_commands.command(name="recent", description="List the recent n prayers.")
    async def recent(self, interaction: discord.Interaction, n: int = 5) -> None:
        await interaction.response.send_message(f"Hello from recent {n}", ephemeral=True)

    @app_commands.command(name="add", description="Add a prayer.")
    async def add(self, interaction: discord.Interaction, prayer: str, description: typing.Optional[str] = '') -> None:
        await interaction.response.send_message(f"Hello from add {prayer} {description}", ephemeral=True)

    @app_commands.command(name="answer", description="Mark a prayer as answered. (Praise God!)")
    async def answer(self, interaction: discord.Interaction, index: int) -> None:
        await interaction.response.send_message(f"Hello from answer {index}", ephemeral=True)

    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Pray(bot))