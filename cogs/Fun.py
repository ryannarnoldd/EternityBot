from discord.ext import commands
import discord
import random
from discord import app_commands
import asyncio




class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command(name='roll', brief='It will roll dice!', aliases=['dice','die','rolldie'])
    async def roll(self, ctx, max = '6'):
        if max.isdigit() and int(max) > 0: result = f'1-{int(max)}:  **{random.randint(1,int(max))}**'
        else: result = 'Please enter a valid number!'

        await ctx.send(embed = discord.Embed(
            title = 'Dice Roll :game_die:',
            description = result, 
            color = discord.Color.blue()
        ))

    @commands.command(name='roulette', brief="Here's your chance if you ever wanted to die!", pass_context=True, aliases=['rr', 'russian'])
    async def russianroulette(self, ctx, chance = '6'):
        if chance.isdigit() and int(chance) > 1:
            chance = random.randint(1, int(chance))
            result = "has **lived**!" if chance != 1 else "has **died**!"
            reaction = '😇' if chance != 1 else '💀'
            result = f'**{chance}** bullets\n{ctx.author.mention} {result}'
        else:
            result = f'Sorry, I don\'t think **{chance}** bullets is fair for both you and I...'
            reaction = '🧐'

        msg = await ctx.send(embed = discord.Embed(
                    title = 'Russian Roulette :gun:',
                    description = result,
                    color = discord.Colour.blue()
                ))
        
        await msg.add_reaction(reaction)


    @app_commands.command(name='affirm')
    async def affirm(self, interaction : discord.Interaction):
        affirmations = [
            'You are a good person.',
            'You are loved.',
            'You are worthy.',
            'You are enough.',
            'You are strong.',
            'You are capable.',
            'You are beautiful.',
            'You are smart.',
            'Everyone you meet is fighting a battle you know nothing about.',
            'You are not alone.',
            'You are not your mistakes.',
            'You are not your depression.',
            'You are not your anxiety.',
            'You are not your thoughts.',
            'You are not your emotions.',
            'You are not your past.',
            'You are not your failures.',
            'You are not your successes.',
        ]
        view = PrayerList(affirmations, 'Affirmations Requests!')
        await view.start(interaction)



async def setup(bot : commands.Bot):
    await bot.add_cog(Fun(bot))

class PrayerList(discord.ui.View):
    def __init__(self, prayers: list, title: str, timeout: int = 60) -> None:
        super().__init__(timeout=timeout)
        self.prayers = prayers
        self.title = title
        self.current_page = 1
        self.sep = 5
        self.pages = int(len(self.prayers) / self.sep) + 1
        self.message = None

    async def start(self, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.send_message(embed=discord.Embed(title='Fetching Prayer Requests!'), ephemeral=True)
        await asyncio.sleep(1.0)
        await self.update_page()

    async def update_page(self, page : int = 1):
        self.current_page = page
        self.update_buttons()
        page_count = f'Page {self.current_page}/{self.pages}'
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
        start = (self.current_page - 1) * self.sep
        end = start + self.sep
        return self.prayers[start:end]