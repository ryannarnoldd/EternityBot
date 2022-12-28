import discord
import asyncio
from datetime import datetime

global DATE_FORMAT
DATE_FORMAT = '%Y:%m:%d:%H:%M'

class PrayerList(discord.ui.View):
    def __init__(self, prayers: list, title: str, timeout: int = 60) -> None:
        super().__init__(timeout=timeout)
        self.prayers = prayers
        self.title = title
        self.current_page = 1
        self.sep = 5
        self.pages = int(len(self.prayers) / self.sep) + 1
        self.interaction = None

    def time_str(self, date, format='%b.%d'):
        date_object = datetime.strptime(date, DATE_FORMAT)
        return date_object.strftime(format)	

    async def start(self, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.send_message(embed=discord.Embed(title='Fetching Prayer Requests!'), ephemeral=True)
        await asyncio.sleep(1.0)
        await self.update_page()

    async def update_page(self, page : int = 1):
        self.current_page = page
        self.update_buttons()
        page_count = f'Page {self.current_page}/{self.pages}'
        for index, prayer in enumerate(self.prayers, start=1):
            has_descr = '*' if prayer["description"] != "" else ''
            prayer_list += f'**{index}**. {prayer["prayer"]}{has_descr} `{self.time_str(prayer["time"])}`\n'
        prayers = '\n'.join([f'{i}. {prayer}' for i, prayer in enumerate(self.get_prayers(), start=self.sep * (self.current_page - 1) + 1)])
        embed = discord.Embed(title = f'{self.title} {page_count}', description = prayers)
        await self.interaction.edit_original_response(embed=embed, view=self)

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green)
    async def start_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.update_page(1)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.update_page(self.current_page - 1)

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.update_page(self.current_page + 1)

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    async def end_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.update_page(self.pages)

    def update_buttons(self):
        if self.current_page == 1:
            self.start_button.disabled = True
            self.prev_button.disabled = True
            self.start_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.start_button.disabled = False
            self.prev_button.disabled = False
            self.start_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == self.pages:
            self.next_button.disabled = True
            self.end_button.disabled = True
            self.end_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.end_button.disabled = False
            self.end_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary
        
    def get_prayers(self):
        start = self.sep * (self.current_page - 1)
        end = start + self.sep
        return self.prayers[start:end]