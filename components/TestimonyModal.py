import discord 
from discord import Embed,  ui

class TestimonyModal(ui.Modal, title="testimony"):

    def __init__(self):
        super().__init__()
        self.text = ""

    testimony = ui.TextInput(label='Testimony', placeholder='Enter your testimony here.', required=True, style=discord.TextStyle.long)
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = Embed(title=f'Your Testimony', color=discord.Colour.blue())
        if not self.testimony.value.isspace():
            self.text = self.testimony.value
            
            embed.description = 'Your testimony has been set!'
        else:
            embed.description = 'Your testimony has not been set. Enter a valid testimony and try again.'

        await interaction.response.send_message(embed=embed, ephemeral=True)
        # await interaction.response.send_message(embed=embed, ephemeral=True)