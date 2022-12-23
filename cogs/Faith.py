from discord.ext import commands
import discord
import json
import asyncio
from discord import Embed

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'

help_guide = {
    'list <mention>': 'List all prayer requests of you, or someone else!',
    'add <prayer>': 'Add a prayer request to your list',
    'ans <number>': 'Mark a prayer request as answered (Praise God!)',
    'help': 'Show this help guide'
}


class Faith(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(PRAYERS_FILEPATH, 'r') as prayers:
            self.prayers = json.load(prayers)		
            
    async def save_prayers(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(PRAYERS_FILEPATH, 'w') as prayers:
                prayers.write(json.dumps(self.prayers, indent=4))
            await asyncio.sleep(0.05)

    async def add_prayer(self, author, prayer):
        self.prayers["users"][str(author.id)]["current"].insert(0, prayer)
        await self.save_prayers()
        return

    def get_prayer_list(self, id):
        name = self.bot.get_user(int(id)).name
        prayers = self.prayers["users"][str(id)]["current"]
        prayer_list = '\n'.join([f'**{i+1}**.  {prayer}' for i, prayer in enumerate(prayers)]) if prayers else 'No prayer requests!'
        return Embed(title=f'Prayer Requests for {name}', description=prayer_list, color=discord.Colour.blue())

    async def answer_prayer(self, author, index):
        if str(author.id) in self.prayers["users"]:
            current_prayers = self.prayers["users"][str(author.id)]["current"]
            if index <= len(current_prayers):
                prayer = current_prayers[index-1]
                current_prayers.pop(index - 1)
                self.prayers["users"][str(author.id)]["answered"].insert(0, prayer)
        await self.save_prayers()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if str(member.id) not in self.prayers["users"]:
            self.prayers["users"][str(member.id)] = {
                "current": [],
                "answered": []
            }
            await self.save_prayers()


    @commands.command(name='pray', brief="Here's your chance if you ever wanted to die!", aliases=['prayer', 'p'])
    # Have the cmd be the command and the message be the message, or the rest of the string.
    async def pray(self, ctx, cmd='', *, message=''):
        
        match cmd:

            case 'list':
                id = message[2:-1] if message in self.prayers["users"] else ctx.author.id
                await ctx.message.reply(embed = self.get_prayer_list(id))

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
                current_prayers = self.prayers["users"][str(ctx.author.id)]["current"]

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
                        print(message)

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