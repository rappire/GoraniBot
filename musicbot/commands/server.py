import discord
from config import config
from discord.ext import commands
import urllib.request
import feedparser
from mcstatus import JavaServer
import pickle


class 기타(commands.Cog):
    """마크 서버 및 기타 기능에 관련된 명령어입니다.
    """
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')
        with open("./config/wordlist.pickle","rb") as fr:
            self.reply = pickle.load(fr)
        
        
    @commands.command(name='서버', description=config.HELP_SERVER_LONG, help=config.HELP_SERVER_SHORT)
    async def 서버(self, ctx):
        try:
            ip = "58.120.8.214:25565"
            server = JavaServer.lookup(ip)
            status = server.status()
            await ctx.send("서버가 열려있습니다!!")
            await ctx.send("서버에 {}명이 접속해있습니다!!".format(status.players.online))
            if(status.raw['players']['online'] != 0):
                usersConnected = [ user['name'] for user in status.raw['players']['sample'] ]
                user = ""
                for i in usersConnected:
                    user += i + " "
                await ctx.send("접속 인원 : " + user)
            
        except:
            await ctx.send("서버가 닫혀있습니다!!")

        
    @commands.command(name='롤', description=config.HELP_LOL_LONG, help=config.HELP_LOL_SHORT)
    async def 롤(self, ctx):
        rss = "feed:https://createfeed.fivefilters.org/extract.php?url=https%3A%2F%2Fwww.leagueoflegends.com%2Fko-kr%2Fnews%2Ftags%2Fpatch-notes%2F&item=li%5Bclass%5E%3D%22style__Item%22%5D&item_title=h2&item_desc=div%5Bclass%5E%3D%22style__Category%22%5D&item_date=time+%40datetime&item_image=img+%40src&unique_url=1&max=5&order=document&guid=0"
        feed = feedparser.parse(rss)
        urllib.request.urlretrieve(feed.entries[0].links[1]["href"], "temp.png")
        image = discord.File("temp.png", filename="image.png")
        embed = discord.Embed(title=feed.entries[0].title, color=0x00ff56)
        embed.set_image(url="attachment://image.png")
        embed.add_field(name="링크", value=feed.entries[0].link, inline=True)
        await ctx.send(embed=embed, file=image)
        
        
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot == False:    
            if message.content in self.reply:
                await message.channel.send(message.content)
                
                
    @commands.command(name='추가', description="추가로 반응할 말을 추가합니다", help="추가로 반응할 말을 추가합니다")
    async def 추가(self, ctx, *, word: str):
        if word in self.reply:
            await ctx.send(word + "가 리스트에 있습니다.")
        else:
            self.reply.add(word)
            await ctx.send(word + "를 추가했습니다.")
            with open("./config/wordlist.pickle","wb") as fw:
                pickle.dump(self.reply, fw)
            
    @commands.command(name='반응', description="반응하는 말 리스트를 보여줍니다.", help="반응하는 말 리스트를 보여줍니다.")
    async def 반응(self, ctx):
        content = ""
        for i in self.reply:
            content += i + "\n" 
        emb = discord.Embed(title='반응 리스트', description = content, color=discord.Color.blue())
        await ctx.send(embed = emb)
    
    @commands.command(name='반응삭제', description="반응 리스트에서 삭제합니다.", help="반응 리스트에서 삭제합니다.")
    async def 삭제(self, ctx, *, word: str):
        if word in self.reply:
            self.reply.remove(word)
            await ctx.send(word + "를 삭제했습니다.")
            with open("./config/wordlist.pickle","wb") as fw:
                pickle.dump(self.reply, fw)
        else:
            await ctx.send(word + "가 리스트에 없습니다.")
            
                
    

async def setup(bot):
    await bot.add_cog(기타(bot))