from discord.ext import commands
import discord
import json
import asyncio
from discord import Embed
# import datetime
from datetime import datetime
from operator import itemgetter

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

def time_str(self, date, format='%b. %d'):
    date_object = datetime.strptime(date, DATE_FORMAT)
    return date_object.strftime(format)	

class Faith(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(PRAYERS_FILEPATH, 'r') as prayers:
            self.prayers = json.load(prayers)

    def time_str(self, date, format='%b.%d'):
        date_object = datetime.strptime(date, DATE_FORMAT)
        return date_object.strftime(format)	

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
            has_descr = '*****' if prayer["description"] != "" else ''
            prayer_list += f'**{index}**. {prayer["prayer"]}{has_descr} `{self.time_str(prayer["time"])}`\n'

        if prayer_list == '': 'No prayers found!'
        return Embed(title=f'Prayer Requests for {name}', description=prayer_list, color=discord.Colour.blue())

    def get_recent_prayers(self, n=5):
        print(self.prayers)
        prayers = [prayer for prayer in self.prayers if not prayer["answered"]]
        # Get the n most recent prayers
        recent_prayers = prayers[:n] if len(prayers) > n else prayers
        prayer_list = ''

        for index, prayer in enumerate(recent_prayers, start=1):
            print(prayer)
            has_descr = '*****' if prayer["description"] != "" else ''
            prayer_list += f'**{index}**. {prayer["prayer"]}{has_descr} `{self.time_str(prayer["time"])}`\n'
            print('Oof')
            
        
        if prayer_list == '': 'No prayers found!'
        return Embed(title='Recent Prayer Requests', description=prayer_list, color=discord.Colour.blue())


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if str(member.id) not in self.prayers:
            self.prayers[str(member.id)] = []
            await self.save_prayers()


    @commands.command(name='pray', brief="Here's your chance if you ever wanted to die!", aliases=['prayer', 'p'])
    # Have the cmd be the command and the message be the message, or the rest of the string.
    async def pray(self, ctx, cmd='', *, message=''):
        
        match cmd:

            case 'list':
                await ctx.message.reply(embed = self.get_prayer_list(ctx.author.id))

            case 'recent':
                await ctx.message.reply(embed = self.get_recent_prayers(5))

            case 'add':
                if message == '':
                    await ctx.message.reply(embed = Embed(title='Prayer Request Add', description='Please type a prayer request to be added!', color=discord.Colour.blue()))
                    msg = await self.bot.wait_for("message" , timeout=120, check=None)
                    prayer = msg.content
                else:
                    prayer = message
                    msg = ctx.message


                await msg.reply(embed = Embed(title='Prayer Request Added', description=f'*{prayer}* added to your prayer requests!', color=discord.Colour.blue()))
                await self.add_prayer(ctx.author, prayer)

            case 'ans' | 'answer':
                current_prayers = self.prayers[str(ctx.author.id)]["current"]

                if current_prayers != []:
                    if message == '' or not message.isdigit() or not (int(message)-1 <= len(current_prayers)):
                        embed = self.get_prayer_list(ctx.author.id)
                        embed.set_footer(text='Please type the number of the prayer request you want to mark answered!')
                        await ctx.message.reply(embed = embed)
                        msg = await self.bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120)
                        print('here')

                        while not msg.content.isdigit() or not (int(msg.content)-1 <= len(current_prayers)):
                            await msg.reply(embed = Embed(description='Please type a valid number of the prayer request you want to mark answered!', color=discord.Colour.blue()))
                            msg = await self.bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)

                        message = msg.content

                    else:
                        msg = ctx.message
                    
                    await msg.reply(embed = Embed(title='Prayer Request Answered', description=f'*{current_prayers[int(message)-1]}* marked as answered!', color=discord.Colour.blue()))
                    await self.answer_prayer(ctx.author, int(message))

                else:
                    await ctx.reply(embed = Embed(title='Prayer Request Answer', description='You have no prayer requests to mark as answered!', color=discord.Colour.blue()))




            case 'help' | '' | _:
                help_text = '\n'.join([f'`{cmd}` - {desc}' for cmd, desc in help_guide.items()])
                await ctx.message.reply(embed=Embed(title='Prayer Request Help', description=help_text, color=discord.Color.blue()))



async def setup(bot):
    await bot.add_cog(Faith(bot))