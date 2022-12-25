import discord
from discord.ext import commands

class highbreed(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot: commands.Bot = bot
  
  @commands.hybrid_command(name="ping")
  async def ping_command(self, ctx: commands.Context) -> None:
    """
    This command is actually used as an app command AND a message command.
    This means it is invoked with `?ping` and `/ping` (once synced, of course).
    """

    await ctx.send("Hello!")
    # we use ctx.send and this will handle both the message command and app command of sending.
    # added note: you can check if this command is invoked as an app command by checking the `ctx.interaction` attribute.

    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(highbreed(bot))