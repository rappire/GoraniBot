import os
import discord
from discord.ext import commands
from discord import Intents
import asyncio

from config import config
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from musicbot.utils import guild_to_audiocontroller, guild_to_settings

initial_extensions = ['musicbot.commands.music', 'musicbot.commands.server',
                      'musicbot.commands.general', 'musicbot.plugins.button'
                      ,'musicbot.commands.help']

bot = commands.Bot(command_prefix=config.BOT_PREFIX,intents=Intents.all(),
                   pm_help=True, case_insensitive=True)


async def start():
    for extension in initial_extensions:
        await bot.load_extension(extension)


@bot.event
async def on_ready():
    print(config.STARTUP_MESSAGE)
    await bot.change_presence(status = discord.Status.online, activity=discord.Game(name="산에서 달리기"))

    for guild in bot.guilds:
        await register(guild)
        print("Joined {}".format(guild.name))

    print(config.STARTUP_COMPLETE_MESSAGE)


@bot.event
async def on_guild_join(guild):
    print(guild.name)
    await register(guild)


async def register(guild):

    guild_to_settings[guild] = Settings(guild)
    guild_to_audiocontroller[guild] = AudioController(bot, guild)

    sett = guild_to_settings[guild]

    try:
        await guild.me.edit(nick=sett.get('default_nickname'))
    except:
        pass

    if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
        return

    vc_channels = guild.voice_channels

    if sett.get('vc_timeout') == False:
        if sett.get('start_voice_channel') == None:
            try:
                await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            except Exception as e:
                print(e)

        else:
            for vc in vc_channels:
                if vc.id == sett.get('start_voice_channel'):
                    try:
                        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    except Exception as e:
                        print(e)


if __name__ == '__main__':

    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if config.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit
    asyncio.run(start())
    bot.run(config.BOT_TOKEN)
