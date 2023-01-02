from discord.ext import commands
from discord import app_commands
import json
import discord
from discord import ChannelType
from components.ChallengeView import ChallengeView

global CHALLENGES_FILE
CHALLENGES_FILE = 'data/challenges.json'
global CHALLENGES_CHANNEL
CHALLENGES_CHANNEL = 1059296045307285574


class Challenges(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        self.challenges = json.load(open(CHALLENGES_FILE, 'r'))

    # Send the challenge for the day in the thread in the Challenges channel.
    @app_commands.command(name="send", description="Send the challenge for the day.")
    async def send_challenge(self, interaction: discord.Interaction, day: int) -> None:
        channel = self.bot.get_channel(CHALLENGES_CHANNEL)
        embed = discord.Embed(title=f'Day {day} Challenge', description=self.challenges[day-1]['challenge'], color=discord.Colour.blue())
        view = ChallengeView(day=day)
        thread = await channel.create_thread(
            name=f'Day {day}',
            type=ChannelType.public_thread
        )

        await thread.send(embed=embed, view=view)

async def setup(bot : commands.Bot):
    await bot.add_cog(Challenges(bot))