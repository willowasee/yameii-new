import discord
from discord.ext import commands
from discord.utils import get
import sqlite3
import random
import string
import re

con = sqlite3.connect('C:\yameii-main\discord.db')
c = con.cursor()

class databaseinteractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        c.execute("SELECT id FROM main")
        rows = c.fetchall()
        if (message.author.id,) in rows:
           pass
        else:
            c.execute("INSERT INTO main(id) VALUES(?)", (message.author.id,))
            c.connection.commit()

   
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
         if user.id != 855103658773839892:
          c.execute("select id from users where v = ?", (reaction.message.id,))
          if c.fetchone()[0] is not None:
           v = c.fetchone()[0]
           if str(reaction.emoji) == '✅':
                  member = reaction.message.guild.get_member(v)
                  channel = self.bot.get_channel(855345854914887692)
                  await channel.send("<@{}> was verified".format(v))
                  c.execute("update users set v = 'verified' where id = ?", (v,))
                  c.connection.commit()
                  var = discord.utils.get(reaction.message.guild.roles, name = 'unverified')
                  await member.remove_roles(var)
                  var = discord.utils.get(reaction.message.guild.roles, name = 'member <3')
                  await member.add_roles(var)
                  channel = self.bot.get_channel(850961814987472897)
                  await channel.send(f'welcome <@{v}>! check out <#851144414684381194> also fill out a pronoun chart in <#851136868175314954> and introduce yourself in <#851203511991271485> if you’d like!')

           else: 
            if str(reaction.emoji) == '❌':
             channel = self.bot.get_channel(855345854914887692)
             member = reaction.message.guild.get_member(v)
             c.execute('''UPDATE users SET v = 'kicked' WHERE id = ?''', (v,))
             c.connection.commit()
             await channel.send("<@{}> was kicked".format(v))
             await member.kick(reason='did not pass verification')



    @commands.command()
    async def start(self, ctx):
       c.execute("select v from users where id = ?", (ctx.message.author.id,))
       check1 = c.fetchone()[0]
       if check1 != 'verified':
        member = ctx.message.author
        channel = ctx.message.guild.system_channel
        x = '''Please answer the following questions in one message;
           
            Have you read the rules, if so what is your *least* fav rule and why?
            Why do you want to join Be Trans Throw Hands?
            How did you find this server?
            What is your age, are you trans or cis? If you don't want to disclose this please tell us why via modmail- use `.modmail "message goes here"` in a dm with me, please note the quotation marks in the command are required.

            Please make sure you fill out the questions **in one message!**'''
        em = discord.Embed(title = "welcome to be trans throw hands", description = "{}".format(x))
        await channel.send("<@{}>".format(ctx.message.author.id), embed = em)
        
        def check(m):
             return m.author == ctx.author and m.channel == ctx.channel

        msg = await self.bot.wait_for("message", check = check)
        await ctx.send(f"thank you, <@{ctx.author.id}> your response has been sent to the mods who will look over it asap!")
        channel = self.bot.get_channel(855345854914887692)
        em = discord.Embed(title = "verify new user?", description = '''The user said,
         **{.content}**'''.format(msg))
        em.set_footer(text = "{.author} React with ✅ to verify and ❌ to kick".format(msg))
        message = await channel.send(embed = em)
        c.execute("update users set v = ? where id = ?", (message.id, ctx.author.id))
        c.connection.commit()
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
       await member.ban(reason=reason)
       await ctx.send(f'User {member} has been banned')
       c.execute('''UPDATE users SET v = 'banned' WHERE id = ?''', (member,))
       c.connection.commit()

    @ban.error
    async def ban_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
   
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        print(member)
        await member.kick(reason=reason)
        c.execute('''UPDATE users SET v = 'kicked' WHERE id = ?''', (member,))
        c.connection.commit()
        await ctx.send(f'User {member} has been kicked')

    @kick.error
    async def kick_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

    @commands.command()
    @commands.has_role("sexy booster")
    async def database(self, ctx, sql: str, save: str):
     em = discord.Embed(title = "database interaction", description = "database interactions are not saved by default", color = ctx.author.color)
     if save == 'yes':
         c.execute(sql)
         c.connection.commit()
         em.add_field(name = "result", value = "command executed sucsessfuly")
     else:
         c.execute(sql)
         rows = c.fetchall()
         em.add_field(name = "result", value = "{}".format(rows))
     await ctx.send(embed = em)

    @database.error
    async def database_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

def setup(bot):
    bot.add_cog(databaseinteractions(bot))
