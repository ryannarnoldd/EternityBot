from discord.ext import commands
import discord
import json
import asyncio
from discord import Embed

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'

def embed(title, description, color=discord.Colour.blue()):
    return discord.Embed(title=title, description=description, color=color)

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


    def embed(title, description, color=discord.Colour.blue()):
        return Embed(title=title, description=description, color=color)

    async def answer_prayer(self, author, index):
        current_prayers = self.prayers["users"][str(author.id)]["current"]
        if str(author.id) in self.prayers["users"]:
            if index-1 <= len(current_prayers):
                prayer = current_prayers[index-1]
                current_prayers.pop(index - 1)
                self.prayers["users"][str(author.id)]["answered"].insert(0, prayer)
        await self.save_prayers()


    @commands.command(name='pray', brief="Here's your chance if you ever wanted to die!", aliases=['prayer', 'p'])
    # Have the cmd be the command and the message be the message, or the rest of the string.
    async def pray(self, ctx, cmd='', *, message=''):
        print('message', message)
        
        match cmd:
            case 'list':
                id = message[2:-1] if message in self.prayers["users"] else ctx.author.id
                name = self.bot.get_user(int(id)).name
                prayers = self.prayers["users"][str(id)]['current']
                prayer_list = '\n'.join([f'**{i+1}**.  {prayer}' for i, prayer in enumerate(prayers)]) if prayers else 'No prayers'   

                await ctx.message.reply(embed = embed(f'Prayers for {name}', prayer_list))


            case 'add':
                if message == '':
                    await ctx.message.reply(embed = embed('Prayer Request Add', 'Please type a prayer request to be added!'))
                    msg = await self.bot.wait_for("message" , timeout=120, check=None)

                prayer = msg.content if message == '' else message
                if message != '': msg = ctx.message

                await msg.add_reaction('✅')
                await self.add_prayer(ctx.author, prayer)

                

            case 'answer':
                if message.isdigit() and int(message) <= len(self.prayers["users"][str(ctx.author.id)]["current"]):
                    await self.answer_prayer(ctx.author, int(message))
                else:
                    await ctx.send('Please enter a prayer to be answered!')
                    msg = await self.bot.wait_for("message", check=None)
                    await self.answer_prayer(ctx.author, int(msg.content))

            case _:
                await ctx.send('Please enter a valid command!')
        


async def setup(bot):
    await bot.add_cog(Faith(bot))