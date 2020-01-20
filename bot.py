import os
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from commands.wikipedia import Wikipedia

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
language = os.getenv('BOT_LANG')
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='wikipedia')
async def wikipedia(ctx, *args):
    lookup_string = ' '.join([a for a in args])
    try:
        print(ctx.message.author, 'sent command wikipedia with term', lookup_string)
        wikipedia = Wikipedia(language, lookup_string)
        embed = Embed(  
                title=wikipedia.get_title(), 
                description=wikipedia.get_summary(), 
                url=wikipedia.page_url
            )
        embed.set_image(url=wikipedia.get_image())
        await ctx.send(embed=embed)
    except AttributeError:
        await ctx.send('The term query did not return any results')

bot.run(token)
