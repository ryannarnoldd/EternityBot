from discord.ext import commands
import discord
import json
import asyncio
from discord import Embed

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'

help_guide = {
    'List <mention>': 'List all prayer requests of you, or someone else!',
    'Add <prayer>': 'Add a prayer request to your list',
    'Answer <index>': 'Mark a prayer request as answered (Praise God!)',
    'Help': 'Show this help guide'
}

def embed(title, description, color=discord.Colour.blue()):
    return Embed(title=title, description=description, color=color)

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
        return await self.save_prayers()

    async def get_prayer_list(self, id):
        name = self.bot.get_user(int(id)).name
        prayers = self.prayers["users"][str(id)]["current"]
        prayer_list = '\n'.join([f'**{i+1}**.  {prayer}' for i, prayer in enumerate(prayers)]) if prayers else 'No prayers'
        return embed(f'Prayer Requests for {name}', prayer_list)


    def embed(title, description, color=discord.Colour.blue()):
        return Embed(title=title, description=description, color=color)

    async def answer_prayer(self, author, index):
        if str(author.id) in self.prayers["users"]:
            current_prayers = self.prayers["users"][str(author.id)]["current"]
            if index-1 <= len(current_prayers):
                prayer = current_prayers[index-1]
                current_prayers.pop(index - 1)
                self.prayers["users"][str(author.id)]["answered"].insert(0, prayer)
        return await self.save_prayers()

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
        print('message', message)
        
        match cmd:
            case 'list':
                id = message[2:-1] if message in self.prayers["users"] else ctx.author.id
                await ctx.message.reply(embed = await self.get_prayer_list(id))

            case 'add':
                if message == '':
                    await ctx.message.reply(embed = embed('Prayer Request Add', 'Please type a prayer request to be added!'))
                    msg = await self.bot.wait_for("message" , timeout=120, check=None)

                prayer = msg.content if message == '' else message
                if message != '': msg = ctx.message

                await msg.add_reaction('✅')
                await self.add_prayer(ctx.author, prayer)

                

            case 'ans' | 'answer':
                current_prayers = self.prayers["users"][str(ctx.author.id)]["current"]
                if message.isdigit() and int(message)-1 <= len(current_prayers):
                    prayer = current_prayers[int(message)-1]
                    await self.answer_prayer(ctx.author, int(message))
                    await ctx.message.reply(embed = await embed('Prayer Request Answered', f'*{prayer}* marked as answered!'))

                else:
                    if current_prayers != []:
                        print('not empty')
                        embed = await self.get_prayer_list(ctx.author.id)
                        embed.set_footer(text='Please type the number of the prayer request you want to mark answered!')
                        await ctx.message.reply(embed = embed)

                        try:
                            msg = await self.bot.wait_for("message", 
                                check= lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and int(m.content) - 1 <= len(current_prayers), 
                                timeout=5)
                            await self.answer_prayer(ctx.author, int(msg.content))
                        except asyncio.TimeoutError:
                            await ctx.message.reply(embed = await embed('Prayer Request Answer', 'You took too long to answer!'))
                    else:
                        print('empty')
                        await ctx.message.reply(embed = await embed('Prayer Request Answer', 'You have no prayers to answer!'))

            case 'help' | _:
                help_text = '\n'.join([f'`{cmd}` - {desc}' for cmd, desc in help_guide.items()])
                await ctx.message.reply(embed = embed('Prayer Help', help_text))



async def setup(bot):
    await bot.add_cog(Faith(bot))