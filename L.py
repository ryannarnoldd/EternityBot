
import discord
from discord.ext import commands
import utils


class PaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 5

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title=f"User List Page {self.current_page} / {int(len(self.data) / self.sep) + 1}")
        for item in data:
            embed.add_field(name=item['label'], value=item['item'], inline=False)
        return embed

    async def update_message(self,data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

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

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.end_button.disabled = True
            self.end_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.end_button.disabled = False
            self.end_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="|<",
                       style=discord.ButtonStyle.green)
    async def start_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<",
                       style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">",
                       style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|",
                       style=discord.ButtonStyle.green)
    async def end_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep) + 1
        await self.update_message(self.get_current_page_data())


def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!", intents=intents)


    @bot.command()
    async def paginate(ctx):


        data = [{"label": "User Event", "item": f"User {i} has been added"} for i in range(1, 15)]

        pagination_view = PaginationView(timeout=None)
        pagination_view.data = data
        await pagination_view.send(ctx)


    bot.run('MTA1MzcwNDI2NDA4Nzc3MzI5NA.GC9XYy.d2oFgeMnhHpqdmqL5WswhRA7DFUmLXfj1KuvDE')


if __name__ == "__main__":
    run()