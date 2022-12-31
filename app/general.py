from discord.ext import commands
from random import shuffle
import discord
from app.server import audio_list
from app.utility import get_guild

class 기타(commands.Cog):
    def __init__(self, bot):
        self.bot = bot      
          
    @commands.command(aliases=['악'])
    async def ak(self, ctx, *,num):
        try: 
            num = int(num)
        except:
            await ctx.send("숫자를 넣어주세요")
            return
        #서버를 찾음
        guild = get_guild(self.bot, ctx.message)
        if guild is None:
            return
        guild_audio = audio_list[guild]
        #음성 서버 접속
        await guild_audio.connect(ctx)
        #큐에 집어넣기
        await guild_audio.ak(num)
    
    @commands.command(aliases=['뽑기'])
    async def draw(self, ctx, num):
        num = int(num)
        current_guild = get_guild(self.bot, ctx.message)
        for i in current_guild.voice_channels:
            if ctx.message.author in i.members:
                arr = i.members
        shuffle(arr)
        string = ""
        for i in range(num):
            man = arr.pop()
            if man.nick is None:
                string += f"{i+1}. {man.name}\n"
            else:
                string += f"{i+1}. {man.nick}\n"
        embed = discord.Embed(title="뽑기 결과", description= string)
        await ctx.send(embed = embed)
        
async def setup(bot):
    await bot.add_cog(기타(bot))