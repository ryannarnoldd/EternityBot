import discord
from discord.ext import commands
from discord import app_commands
import typing
# Import file in the folder components!
# from components.PrayerList import PrayerList
class Pray(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#     @app_commands.command(name="help", description="Pray for others or yourself.")
#     async def help(self, interaction: discord.Interaction) -> None:
#         await interaction.response.send_message("Hello from help", ephemeral=True)
    

#     @app_commands.command(name="recent", description="List the recent n prayers.")
#     async def recent(self, interaction: discord.Interaction, n: int = 5) -> None:
#         await interaction.response.send_message(f"Hello from recent {n}", ephemeral=True)

#     @app_commands.command(name="add", description="Add a prayer.")
#     @app_commands.describe(
#         prayer="The prayer",
#         description="The description"
#     )
#     async def add(self, interaction: discord.Interaction, prayer: str, description: typing.Optional[str] = '') -> None:
#         await interaction.response.send_message(f"Hello from add {prayer} {description}", ephemeral=True)

#     @app_commands.command(name="answer", description="Mark a prayer as answered. (Praise God!)")
#     async def answer(self, interaction: discord.Interaction, index: int) -> None:
#         await interaction.response.send_message(f"Hello from answer {index}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Pray(bot))
