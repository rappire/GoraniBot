from discord.ext import commands
from random import shuffle
import discord
from app.server import audio_list
from app.utility import get_guild
import pickle
from mcstatus import JavaServer


class 기타(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./config/wordlist.pickle", "rb") as fr:
            self.reply = pickle.load(fr)

    @commands.command(aliases=["악"])
    async def ak(self, ctx, *, num):
        try:
            num = int(num)
        except:
            await ctx.send("숫자를 넣어주세요")
            return
        # 서버를 찾음
        guild = get_guild(self.bot, ctx.message)
        if guild is None:
            return
        guild_audio = audio_list[guild]
        # 음성 서버 접속
        await guild_audio.connect(ctx)
        # 큐에 집어넣기
        await guild_audio.ak(num)

    @commands.command(aliases=["뽑기"])
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
        embed = discord.Embed(title="뽑기 결과", description=string)
        await ctx.send(embed=embed)

    @commands.command(name="서버")
    async def 서버(self, ctx):
        try:
            ip = "58.120.8.214:25565"
            server = JavaServer.lookup(ip)
            status = server.status()
            await ctx.send("서버가 열려있습니다!!")
            await ctx.send("서버에 {}명이 접속해있습니다!!".format(status.players.online))
            if status.raw["players"]["online"] != 0:
                usersConnected = [
                    user["name"] for user in status.raw["players"]["sample"]
                ]
                user = ""
                for i in usersConnected:
                    user += i + " "
                await ctx.send("접속 인원 : " + user)

        except:
            await ctx.send("서버가 닫혀있습니다!!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            if message.content in self.reply:
                await message.channel.send(message.content)

    @commands.command(
        name="추가", description="추가로 반응할 말을 추가합니다", help="추가로 반응할 말을 추가합니다"
    )
    async def 추가(self, ctx, *, word: str):
        if word in self.reply:
            await ctx.send(word + "가 리스트에 있습니다.")
        else:
            self.reply.add(word)
            await ctx.send(word + "를 추가했습니다.")
            with open("./config/wordlist.pickle", "wb") as fw:
                pickle.dump(self.reply, fw)

    @commands.command(
        name="반응", description="반응하는 말 리스트를 보여줍니다.", help="반응하는 말 리스트를 보여줍니다."
    )
    async def 반응(self, ctx):
        content = ""
        for i in self.reply:
            content += i + "\n"
        emb = discord.Embed(
            title="반응 리스트", description=content, color=discord.Color.blue()
        )
        await ctx.send(embed=emb)

    @commands.command(
        name="반응삭제", description="반응 리스트에서 삭제합니다.", help="반응 리스트에서 삭제합니다."
    )
    async def 삭제(self, ctx, *, word: str):
        if word in self.reply:
            self.reply.remove(word)
            await ctx.send(word + "를 삭제했습니다.")
            with open("./config/wordlist.pickle", "wb") as fw:
                pickle.dump(self.reply, fw)
        else:
            await ctx.send(word + "가 리스트에 없습니다.")


async def setup(bot):
    await bot.add_cog(기타(bot))
