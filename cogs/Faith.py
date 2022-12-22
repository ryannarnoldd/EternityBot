from discord.ext import commands
import discord
import json
import asyncio

global PRAYERS_FILE
PRAYERS_FILEPATH = 'data/prayers.json'

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
            
            await asyncio.sleep(1)

    async def add_prayer(self, author, prayer):
        if str(author.id) not in self.prayers["users"]:
            self.prayers["users"][str(author.id)] = {
                "current": [],
                "answered": []
            }

        self.prayers["users"][str(author.id)]["current"].insert(0, prayer)
        await self.save_prayers()

    async def answer_prayer(self, author, index):
        current_prayers = self.prayers["users"][str(author.id)]["current"]
        if str(author.id) in self.prayers["users"]:
            if index-1 <= len(current_prayers):
                prayer = current_prayers[index-1]
                current_prayers.pop(index - 1)
                self.prayers["users"][str(author.id)]["answered"].insert(0, prayer)

        await self.save_prayers()


		


    @commands.command(name='pray', brief="Here's your chance if you ever wanted to die!")
    # Have the cmd be the command and the message be the message, or the rest of the string.
    async def pray(self, ctx, cmd='', *, message=''):
        
        match cmd:
            case 'list':
                if message.startswith('<@') and message.endswith('>'):
                    id = message[2:-1]
                    user_list = self.prayers["users"][str(id)]['current']
                    if user_list:
                        await ctx.send(f'Prayers for {message}:\n{user_list}')
                    else:
                        await ctx.send(f'{message} has no prayers!')
                else:
                    author_list = self.prayers["users"][str(ctx.author.id)]['current']
                    if author_list:
                        await ctx.send(f'Your prayers:\n{author_list}')
                    else:
                        await ctx.send('You have no prayers!')


            case 'add':
                if message != '':
                    await self.add_prayer(ctx.author, message)
                    await ctx.message.reply(f'Prayer added: {message}')
                else:
                    await ctx.send('Please enter a prayer!')
                    msg = await self.bot.wait_for("message", check=None)
                    await self.add_prayer(ctx.author, msg.content)

            case 'answer':
                if message.isdigit() and int(message) <= len(self.prayers["users"][str(ctx.author.id)]["current"]):
                    await self.answer_prayer(ctx.author, int(message))
                else:
                    await ctx.send('Please enter a prayer to be answered!')
                    msg = await self.bot.wait_for("message", check=None)
                    await self.answer_prayer(ctx.author, int(msg.content))

            case other:
                await ctx.send('Please enter a valid command!')
        


async def setup(bot):
    await bot.add_cog(Faith(bot))