import discord
import asyncio
from datetime import datetime
import json

global CHALLENGES_FILE
CHALLENGES_FILE = 'data/challenges.json'


class ChallengeView(discord.ui.View):
    def __init__(self, day : int):
        super().__init__(timeout=None)
        self.day = day - 1
        self.challenges = json.load(open(CHALLENGES_FILE, 'r')) 

    async def save_challenges(self):
        with open(CHALLENGES_FILE, 'w') as challenges:
            challenges.write(json.dumps(self.challenges, indent=4))

    # Add the userID to the list of users who have completed the challenge under the day index.
    async def add_complete(self, userID, day):
        self.challenges[day]["completed"].append(userID)
        await self.save_challenges(); return

    @discord.ui.button(label='✓', style = discord.ButtonStyle.green, custom_id = "complete_button")
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        if interaction.user.id not in self.challenges[self.day]['completed']:
            await self.add_complete(interaction.user.id, self.day)

