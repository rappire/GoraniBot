from config.config import AI_TOKEN
import openai
from discord.ext import commands
import pickle


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sentence = {}
        self.wordcount = {}
        self.check = False

    async def fetch(self, sentence, author):
        KEY = AI_TOKEN
        openai.api_key = KEY
        model = "gpt-3.5-turbo"
        try:
            chat = openai.ChatCompletion.create(
                model=model, messages=self.sentence[author]
            )
            reply = (
                "***"
                + sentence
                + "***에 대한 답입니다 : \n\n` "
                + chat.choices[0].message.content
                + " `"
            )
            self.sentence[author].append(
                {"role": "assistant", "content": chat.choices[0].message.content}
            )
            print(self.sentence[author])
            return reply
        except:
            return "질문을 너무 빠르게 해서 에러났습니다!"

    @commands.command(name="질문")
    async def chatgpt(self, ctx, *sentneces: str):
        if self.check:
            return
        sentence = " ".join(sentneces)
        if len(sentence) >= 2000:
            await ctx.channel.send("너무 길어요")
        author = ctx.message.author
        if author not in self.sentence:
            self.sentence[author] = [
                {
                    "role": "system",
                    "content": "You are a kind helpful assistant.",
                }
            ]
        loading_message = await ctx.channel.send("***답변을 생각중입니다...***")
        self.sentence[author].append({"role": "user", "content": sentence})
        reply = await self.fetch(sentence, author)
        await ctx.channel.send(reply)
        await loading_message.delete()
        sum = 0
        for i in self.sentence[author]:
            sum += len(i)
        while sum > 10000:
            sum -= len(self.sentence[author][0])
            self.sentence[author] = self.sentence[author][1:]

    @commands.command(name="gpton")
    async def controlgpt(self, ctx):
        if self.check:
            self.check = False
            await ctx.send("GPT on")
        else:
            self.check = True
            await ctx.send("GPT off")

    @commands.command(name="reset")
    async def reset(self, ctx):
        self.sentence[ctx.message.author] = []
        await ctx.send("GPT reset")


async def setup(bot):
    await bot.add_cog(AI(bot))
