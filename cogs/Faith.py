from discord.ext import commands
import discord

class Faith(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pray(self, ctx, *, member: discord.Member = None):
        await ctx.send(f'Pray! {member.mention}! Pray!')

async def setup(bot):
    await bot.add_cog(Faith(bot))