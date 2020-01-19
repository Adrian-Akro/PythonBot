import os
from discord.ext import commands
from dotenv import load_dotenv
from commands.wikipedia import Wikipedia

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='wikipedia')
async def wikipedia(ctx, *args):
    lookup_string = ''.join([a for a in args])
    wikipedia = Wikipedia(lookup_string)
    response = wikipedia.get_summary()
    print(ctx.message.author, 'sent command wikipedia with term', lookup_string)
    await ctx.send(response)

bot.run(token)
