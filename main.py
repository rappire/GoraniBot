import discord
from discord.ext import commands
import asyncio
from app.server import server_init

from config import config

bot = commands.Bot(
    command_prefix=config.BOT_PREFIX,
    intents=discord.Intents.all(),
    case_insensitive=True,
)


async def load_cog():
    for extension in config.BOT_COG:
        await bot.load_extension(extension)


# 봇 상태 메시지 설정
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game(name=config.BOT_STATUS)
    )
    # 서버별 초기 설정
    await server_init(bot, bot.guilds)
    for i in bot.guilds:
        print(f"{i.name} 접속 완료")
    print("봇 시작")


if __name__ == "__main__":
    if config.BOT_TOKEN == "":
        print("봇의 토큰이 없습니다")
        exit()
    asyncio.run(load_cog())
    bot.run(config.BOT_TOKEN)
