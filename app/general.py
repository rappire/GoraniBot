from discord.ext import commands
from random import seed, uniform, shuffle
import asyncio, discord
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

    @commands.command()
    async def ak(self, num):
        seed()
        for i in range(num):
            while(self.guild.voice_client.is_playing()):
                time = uniform(0.2,0.7)
                await asyncio.sleep(time)
                self.guild.voice_client.stop()
            self.guild.voice_client.play(discord.FFmpegPCMAudio(source='config/AK.mp3'))
        while(self.guild.voice_client.is_playing()):
            await asyncio.sleep(1)
        self.timer = None
        await self.disconnect()
    
    @commands.command()
    async def 뽑기(self, ctx, num):
        num = int(num)
        current_guild = get_guild(self.bot, ctx.message)
        for i in current_guild.voice_channels:
            if ctx.message.author in i.members:
                arr = i.members
                shuffle(arr)
                embed = discord.Embed(title="뽑기 결과")
                for i in range(num):
                    man = arr.pop()
                    if man.nick is None:
                        embed.add_field(name =f"{i+1}.",value=f"{man.name}", inline = False)
                    else:
                        embed.add_field(name =f"{i+1}", value=f"{man.nick}", inline = False)
                await ctx.send(embed = embed)
        
async def setup(bot):
    await bot.add_cog(기타(bot))