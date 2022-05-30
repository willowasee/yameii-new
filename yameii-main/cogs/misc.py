import discord
from discord.ext import commands
import inspirobot

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit=10):
        y = limit + 1
        await ctx.channel.purge(limit=y)
        await ctx.send('{} messages cleared by {}'.format(limit, ctx.author.mention), delete_after=5)

    @purge.error
    async def purge_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

   # @commands.command()
   # async def modmail(self, ctx, vent: str):
   #  if isinstance(ctx.channel, discord.channel.DMChannel):
   #      channel = self.bot.get_channel(851235532078972938)
   #      em = discord.Embed(title = "modmail", description = "{}".format(vent))
   #      em.set_footer(text = "{}".format(ctx.message.author))
   #      await channel.send(embed = em)
   
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def inspire(self, ctx: commands.Context):
        inspiration = await asyncio.get_running_loop().run_in_executor(None, inspirobot.generate)
        embed = discord.Embed(url=inspiration.url,
                              title = f"Inspiration for {ctx.author.display_name}",
                              color = ctx.author.color)
        embed.set_image(url=inspiration.url)
        await ctx.send(embed=embed)

    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong! `{0}ms`'.format(round(self.bot.latency, 1)))

def setup(bot):
    bot.add_cog(misc(bot))

