import discord
from discord.ext import commands
import asyncio
import inspirobot
import random

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.group(invoke_without_command=True)
    async def info(self, ctx):
        em = discord.Embed(title = "info", description = "use .info <command> for extended information on that command", color = ctx.author.color)
        em.add_field(name = "pictochat", value = "`pictochat`, `setuser`")
        em.add_field(name = "moderation", value = "`purge`")
        em.add_field(name = "misc", value = "`inspire`, `ping`")
        await ctx.send(embed = em) 
    
   
    @info.command()
    async def ping(self, ctx):
        em = discord.Embed(title = "ping", description = "returns the bots latency", color = ctx.author.color)
        em.add_field(name = "**syntax**", value = "`.ping`")
        await ctx.send(embed = em)

    @info.command()
    async def purge(self, ctx):
        em = discord.Embed(title = "purge", description = "deletes messages, if no ammount is specified it defaults to 10", color = ctx.author.color)
        em.add_field(name = "**syntax**", value = "`.purge [ammount]`")
        await ctx.send(embed = em)
    
    @info.command()
    async def inspire(self, ctx):
        em = discord.Embed(title = "inspire", description = "sends an inspirational quote", color = ctx.author.color)
        em.add_field(name = "**syntax**", value = "`.inspire`")
        await ctx.send(embed = em)

    @info.command()
    async def pictochat(self, ctx):
        em = discord.Embed(title = "pictochat", description = "get out ur ds, works with text and a single image attachment. note: messages will be trunicated at 26 characters if sending an image.", color = ctx.author.color)
        em.add_field(name = "**syntax**", value = "`.pictochat <msg>`")
        em.add_field(name = "**aliases**", value = "`.pc <msg>`, `.picto <msg>`")
        await ctx.send(embed = em)

    @info.command()
    async def setuser(self, ctx):
        em = discord.Embed(title = "setuser", description = "sets a username for the pictochat command, a username is required. usernames are limited to 9 charecters and cannot contain spaces.", color = ctx.author.color)
        em.add_field(name = "**syntax**", value = "`.setuser <user>`")
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(info(bot))
