from discord.ext import commands
import discord
import json
import asyncio
from discord import Embed
# import datetime
from datetime import datetime
from operator import itemgetter
from discord import app_commands

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'
global DATE_FORMAT
DATE_FORMAT = '%Y:%m:%d:%H:%M'

help_guide = {
    'list <mention>': 'List all prayer requests of you, or someone else!',
    'add <prayer>': 'Add a prayer request to your list',
    'ans <number>': 'Mark a prayer request as answered (Praise God!)',
    'help': 'Show this help guide'
}

class Faith(commands.GroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

        with open(PRAYERS_FILEPATH, 'r') as prayers:
            self.prayers = json.load(prayers)

    def time_str(self, date, format='%b.%d'):
        date_object = datetime.strptime(date, DATE_FORMAT)
        return date_object.strftime(format)	
    
    def embed(self, title, description, color=discord.Color.blue()):
        return Embed(title=title, description=description, color=color)

    async def save_prayers(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(PRAYERS_FILEPATH, 'w') as prayers:
                prayers.write(json.dumps(self.prayers, indent=4))
            await asyncio.sleep(0.05)

    async def add_prayer(self, author, prayer, description=""):
        self.prayers.insert(0, {
            "uid": str(author.id),
            "prayer": prayer,
            "description": description,
            "time": datetime.now().strftime(DATE_FORMAT),
            "answered": False
        })

        await self.save_prayers()
        return

    async def answer_prayer(self, author, index):
        prayers = self.prayers[str(author.id)]
        if 0 < index <= len(prayers):
            prayers[index-1]["answered"] = True
        await self.save_prayers()


    def get_prayer_list(self, id):
        name = self.bot.get_user(int(id)).name
        user_prayers = [prayer for prayer in self.prayers if prayer["uid"] == str(id)]
        prayer_list = ''

        for index, prayer in enumerate(user_prayers, start=1):
            has_descr = '*' if prayer["description"] != "" else ''
            prayer_list += f'**{index}**. {prayer["prayer"]}{has_descr} `{self.time_str(prayer["time"])}`\n'

        if prayer_list == '': 'No prayers found!'
        return Embed(title=f'Prayer Requests for {name}', description=prayer_list, color=discord.Colour.blue())

    def get_recent_prayers(self, n=5):
        prayers = [prayer for prayer in self.prayers if not prayer["answered"]]
        recent_prayers = prayers[:n] if len(prayers) > n else prayers
        prayer_list = ''

        for index, prayer in enumerate(recent_prayers):
            has_descr = '*' if prayer["description"] != "" else ''
            prayer_list += f'**{index+1}**. {prayer["prayer"]}{has_descr} `{self.time_str(prayer["time"])}`\n'
            
        
        if prayer_list == '': 'No prayers found!'
        return Embed(title='Recent Prayer Requests', description=prayer_list, color=discord.Colour.blue())

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     if str(member.id) not in self.prayers:
    #         self.prayers[str(member.id)] = []
    #         await self.save_prayers()


    # @commands.group(name='prayer', invoke_without_command=True, aliases=['pray', 'p', '*'])
    # async def prayer(self, ctx):
    #     help_text = '\n'.join([f'`{cmd}` - {desc}' for cmd, desc in help_guide.items()])
    #     await ctx.message.reply(embed=Embed(title='Prayer Request Help', description=help_text, color=discord.Color.blue()))
    


    # @app_commands.command(name='list',  description='List all prayer requests of you, or someone else!')
    # async def list(self, interaction: discord.Interaction):
    #     # await ctx.send('hi')
    #     print('grethy')

    #     data = []

    #     for i in range(1,15):
    #         data.append({
    #             "label": "User Event",
    #             "item": f"User {i} has been added"
    #         })

    #     print('hi')

    #     pagination_view = PrayerList(data, 'hi')

    #     print('hi2')
    #     await pagination_view.send(interaction)


    # @app_commands.command(name='recent', description='List the N most recent prayer requests')
    # async def recent(self, ctx, n : int = 5):
    #     await ctx.message.reply(embed = self.get_recent_prayers(n))

    @app_commands.command(name='add',  description='Add a prayer request to your list')
    async def add(self, ctx, *, message : str =''):
        if message == '':
            await ctx.message.reply(embed = Embed(title='Prayer Request Add', description='Please type a prayer request to be added!', color=discord.Colour.blue()))
            msg = await self.bot.wait_for("message" , timeout=120, check=None)
            prayer = msg.content
        else:
            prayer = message
            msg = ctx.message


        await msg.reply(embed = Embed(title='Prayer Request Added', description=f'*{prayer}* added to your prayer requests!', color=discord.Colour.blue()))
        await self.add_prayer(ctx.author, prayer)

    # @app_commands.command(name='answer',  description='Mark a prayer request as answered')
    # async def answer(self, ctx, *, index : int = ''):
    #     current_prayers = self.prayers[str(ctx.author.id)]["current"]

    #     if current_prayers != []:
    #         if message == '' or not message.isdigit() or not (int(message)-1 <= len(current_prayers)):
    #             embed = self.get_prayer_list(ctx.author.id)
    #             embed.set_footer(text='Please type the number of the prayer request you want to mark answered!')
    #             await ctx.message.reply(embed = embed)
    #             msg = await self.bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120)
    #             print('here')

    #             while not msg.content.isdigit() or not (int(msg.content)-1 <= len(current_prayers)):
    #                 await msg.reply(embed = Embed(description='Please type a valid number of the prayer request you want to mark answered!', color=discord.Colour.blue()))
    #                 msg = await self.bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)

    #             message = msg.content

    #         else:
    #             msg = ctx.message
            
    #         await msg.reply(embed = Embed(title='Prayer Request Answered', description=f'*{current_prayers[int(message)-1]}* marked as answered!', color=discord.Colour.blue()))
    #         await self.answer_prayer(ctx.author, int(message))

    #     else:
    #         await ctx.reply(embed = Embed(title='Prayer Request Answer', description='You have no prayer requests to mark as answered!', color=discord.Colour.blue()))

    # @app_commands.command(name='help',  description='Get help with the prayer request system')
    # async def help(self, ctx):
    #     prayer_help = '\n'.join([f'`{cmd.brief}` - {cmd.description}' for cmd in self.bot.get_command('prayer').commands])
    #     await ctx.message.reply(embed = self.embed(title='Prayer Request Help', description=prayer_help, color=discord.Colour.blue()))






async def setup(bot):
    await bot.add_cog(Faith(bot))