import discord
from discord.ext import commands
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont
from textwrap import TextWrapper
import sqlite3
from pilmoji import Pilmoji
import requests

con = sqlite3.connect('/root/pictocord.db')
c = con.cursor()

class pictocord(commands.Cog):
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
        chan = message.channel
        if message.author.id != 855103658773839892:
         if chan.id == 775775046949142570:
              await message.delete()
              c.execute("select user from main where id = ?", (message.author.id,))
              row = c.fetchone()
              if row[0] is None:
               cmdchan = self.bot.get_channel(775558682297368596)
               await cmdchan.send('{}, Please set a username using `.setuser`'.format(message.author.mention))
              else:   
                 var = str(message.content)
                 msg = var.replace(".pictochat ", "")
                 w1 = TextWrapper(26, break_long_words=True)
                 lines1 = w1.wrap(msg)
                 temp = msg.replace(lines1[0], "")
                 w2 = TextWrapper(36, break_long_words=True)
                 lines2 = w2.wrap(temp.lstrip())
                 img = Image.open('/root/yameii/cogs/picto.png')
                 draw = Pilmoji(img)
                 font = ImageFont.truetype('/root/yameii/cogs/pictochat.ttf', 15)
                 draw.text((8, 10), row[0], fill='blue', font=font)
                 draw.text((66, 13), lines1[0], fill='black', font=font)
                 draw.text((9, 29), '\n'.join(lines2), fill='black', font=font)
                 img.save('/root/yameii/cogs/pictomessage.png')
                 with open('/root/yameii/cogs/pictomessage.png', "rb") as fh:
                  f = discord.File(fh, filename='pictomessage.png')
                 await chan.send(file=f)

    @commands.command()
    async def setuser(self, ctx, user: str):
     var = str(ctx.message.content)
     var2 = var.replace(".setuser {}".format(user), "")
     if len(var2) == 0:
         if len(user) < 10:
          c.execute("update main set user = ? where id = ?", (user, ctx.author.id))
          await ctx.send('Username updated!')
          c.connection.commit()
         else:
             await ctx.send('Usernames have a character limit of **9**!')
     else:
         await ctx.send('Usernames cannot contain spaces!')

    @commands.command(aliases=['picto', 'pc'])
    async def pictochat(self, ctx,):
     if len(ctx.message.attachments) == 0:
      run = await gen(ctx)
      if run == 'err':
       pass
      else: 
       await ctx.message.delete()
       with open('/root/yameii/cogs/pictomessage.png', "rb") as fh:
        f = discord.File(fh, filename='pictomessage.png')
       await ctx.send(file=f)
     else:
      run = await genimg(ctx)
      if run == 'err':
       pass
      else: 
       await ctx.message.delete()
       with open('/root/yameii/cogs/pictomessage.png', "rb") as fh:
        f = discord.File(fh, filename='pictomessage.png')
       await ctx.send(file=f)

async def gen(ctx):
    c.execute("select user from main where id = ?", (ctx.author.id,))
    row = c.fetchone()
    if row[0] is None:
         await ctx.send('Please set a username using `.setuser`')
         return 'err'
    else:   
      var = str(ctx.message.content)
      var2 = var.replace(".pictochat ", "")
      msg = var2.replace(".pictochat", "")
      w1 = TextWrapper(26, break_long_words=True)
      lines1 = w1.wrap(msg)
      temp = msg.replace(lines1[0], "")
      w2 = TextWrapper(36, break_long_words=True)
      lines2 = w2.wrap(temp.lstrip())
      if len(lines1) == 0:
        img = Image.open('/root/yameii/cogs/picto.png')
        draw = Pilmoji(img)
        font = ImageFont.truetype('/root/yameii/cogs/pictochat.ttf', 15)
        draw.text((8, 10), row[0], fill='blue', font=font)
        img.save('/root/yameii/cogs/pictomessage.png')
      else:  
        img = Image.open('/root/yameii/cogs/picto.png')
        draw = Pilmoji(img)
        font = ImageFont.truetype('/root/yameii/cogs/pictochat.ttf', 15)
        draw.text((8, 10), row[0], fill='blue', font=font)
        draw.text((66, 13), lines1[0], fill='black', font=font)
        draw.text((9, 29), '\n'.join(lines2), fill='black', font=font)
        img.save('/root/yameii/cogs/pictomessage.png')

async def genimg(ctx):
     c.execute("select user from main where id = ?", (ctx.author.id,))
     row = c.fetchone()
     if row[0] is None:
         await ctx.send('Please set a username using `.setuser`')
         return 'err'
     else:   
      img_data = requests.get(ctx.message.attachments[0].url).content
      with open('/root/yameii/cogs/temp.png', 'wb') as handler:
        handler.write(img_data)  
      png = Image.open('/root/yameii/cogs/temp.png')
      var = str(ctx.message.content)
      var2 = var.replace(".pictochat ", "")
      msg = var2.replace(".pictochat", "")
      w = TextWrapper(26, break_long_words=True)
      lines = w.wrap(msg)
      if len(lines) == 0:
       img = Image.open('/root/yameii/cogs/picto.png')
       draw = Pilmoji(img)
       font = ImageFont.truetype('/root/yameii/cogs/pictochat.ttf', 15)
       draw.text((8, 10), row[0], fill='blue', font=font)
       rpng = png.resize((116, 56))
       rpng = rpng.convert("RGBA")
       img = img.convert("RGBA")
       img.paste(rpng, (66, 26), rpng)
       img.save('/root/yameii/cogs/pictomessage.png')
      else:
       img = Image.open('/root/yameii/cogs/picto.png')
       draw = Pilmoji(img)
       font = ImageFont.truetype('/root/yameii/cogs/pictochat.ttf', 15)
       draw.text((8, 10), row[0], fill='blue', font=font)
       draw.text((66, 13), lines[0], fill='black', font=font)
       rpng = png.resize((116, 56))
       rpng = rpng.convert("RGBA")
       img = img.convert("RGBA")
       img.paste(rpng, (66, 26), rpng)
       img.save('/root/yameii/cogs/pictomessage.png') 

    
    

def setup(bot):
    bot.add_cog(pictocord(bot))
