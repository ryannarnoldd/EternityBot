from discord.ext import commands
import discord
from discord import app_commands

seven_deadly_sins = {
    'Pride': {
        "definition": 'The quality or state of being proud: such as inordinate self-esteem, conceit',
        "counterpart": 'Humility, Meekness, Love God, Love others, Appropriate self-worth'
    },
    'Greed': {
        "definition": 'a selfish and excessive desire for more of something (such as money) than is needed (material goods)',
        "counterpart": 'Generosity, Kindness'
    },
    'Lust': {
        "definition": 'Intense or unbridled (sexual) desire, lasciviousness',
        "counterpart": 'Love, Unselfishness'
    },
    'Envy': {
        "definition": 'Painful or resentful awareness of an advantage enjoyed by another joined with a desire to possess the same advantage',
        "counterpart": "Love, Joy, Thankfulness, Compassion, Satisfaction"
    },
    'Gluttony': {
        "definition": 'Excessive indulgence (typically food or drink)',
        "counterpart": 'Self-control, Contentment, Patience, Discernment'
    },
    'Wrath': {
        "definition": 'Strong vengeful anger or indignation',
        "counterpart": 'Peace, Gentleness, Self-control'
    },
    'Sloth': {
        "definition": 'Disinclination to action or labor, spiritual apathy, and inactivity',
        "counterpart": 'Perseverance, Diligence, Servanthood'
    }
}





#     'Greed': 'a selfish and excessive desire for more of something (such as money) than is needed (material goods)',
#     'Lust': 'Intense or unbridled (sexual) desire, lasciviousness',
#     'Envy': 'Painful or resentful awareness of an advantage enjoyed by another joined with a desire to possess the same advantage',
#     'Gluttony': 'Rxcessive indulgence (typically food or drink)',
#     'Wrath': 'Strong vengeful anger or indignation',
#     'Sloth': 'Disinclination to action or labor, spiritual apathy, and inactivity'
# }

class Sin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="sds", description="Seven Deadly Sins.")
    async def sds(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title='Seven Deadly Sins', color=discord.Colour.red())
        for sin in seven_deadly_sins:
            sin_info = f'{seven_deadly_sins[sin]["definition"]}\n**Counterpart**: *{seven_deadly_sins[sin]["counterpart"]}*'
            print(sin_info)
            embed.add_field(name=f'**{sin}**', value=sin_info, inline=False)
        
        await interaction.response.send_message(embed=embed)



async def setup(bot : commands.Bot):
    await bot.add_cog(Sin(bot))