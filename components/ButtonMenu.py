import discord
from discord import ui
from typing import Optional

# take the list of data as a parameter.
class ButtonMenu(discord.ui.View):
    def __init__(self, prayers: list, title: str, user: Optional[discord.User] = None, timeout: int = 60) -> None:
        super().__init__(timeout=timeout)
        self.data = prayers
        self.title = title
        self.current_page = 1
        self.sep = 5
        self.pages = int(len(self.data) / self.sep) + 1

    def update(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == self.pages:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    async def getPage(self):
        page = self.current_page
        if isinstance(self.current_page, str):
            return page, [], []
        elif isinstance(page, discord.Embed):
            return None, [page], []
        elif isinstance(page, discord.File):
            return None, [], [page]
        elif isinstance(page, list):
            if all(isinstance(x, discord.Embed) for x in page):
                return None, page, []
            if all(isinstance(x, discord.File) for x in page):
                return None, [], page
            else:
                return TypeError("Page must be a list of either Embeds or Files")

    async def showPage(self, interaction: discord.Interaction):
        await self.update(self.current_page)
        contents, embed, files = await self.getPage(self.pages[self.current_page - 1])

        await interaction.response.edit_message(
            content=contents,
            embed=embed,
            files=files,
            view=self,
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user:
            if interaction.user.id != self.user.id:
                await interaction.response.send_message(
                    "This pagination menu is not for you.", ephemeral=True
                )
                return False
        return True

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == self.pages:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="|<", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.showPage(0, interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.showPage(self.current_page - 1, interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.showPage(self.current_page + 1, interaction)

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.showPage(self.pages, interaction)