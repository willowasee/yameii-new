# YAMEII
# written with love by alexis!#0013
# using the discord.py rewrite & py3

import discord
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(type=discord.ActivityType.listening, name="crying on my ds | .info for help")
bot = commands.Bot(command_prefix=".", intents=intents, activity=activity, status=discord.Status.online)
bot.remove_command("help")

@bot.command()
async def load(ctx, extention):
     bot.load_extension(f'cogs.{extention}')
     await ctx.send(f'{extention} was loaded!')

@bot.command()
async def unload(ctx, extention):
     bot.unload_extension(f'cogs.{extention}')
     await ctx.send(f'{extention} was unloaded!')

@bot.command()
async def reload(ctx, extention):
     bot.unload_extension(f'cogs.{extention}')
     bot.load_extension(f'cogs.{extention}')
     await ctx.send(f'{extention} was reloaded!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'loaded {filename[:-3]}')

bot.run('ODU1MTAzNjU4NzczODM5ODky.YMtnVw.rTunZmrwwQOhLml7dOKG82_1FEE')
