import asyncio

import discord
from config import config
from discord.ext import commands
from musicbot import linkutils, utils
from youtube_search import YoutubeSearch
import pickle


class 음악(commands.Cog):
    """ 음악 플레이와 관련된 명령어들입니다.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='노래', description=config.HELP_YT_LONG, help=config.HELP_YT_SHORT,
                      aliases=['p', 'yt','play'])
    async def _play_song(self, ctx, *, track: str):

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if (await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        if track.isspace() or not track:
            return

        if await utils.play_check(ctx) == False:
            return

        # reset timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if audiocontroller.playlist.loop == True:
            await ctx.send("Loop is enabled! Use {}loop to disable".format(config.BOT_PREFIX))
            return
        
        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)

    @commands.command(name='루프', description=config.HELP_LOOP_LONG, help=config.HELP_LOOP_SHORT, aliases=['l', 'loop'])
    async def _loop(self, ctx):

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if len(audiocontroller.playlist.playque) < 1 and current_guild.voice_client.is_playing() == False:
            await ctx.send("No songs in queue!")
            return

        if audiocontroller.playlist.loop == False:
            audiocontroller.playlist.loop = True
            await ctx.send("Loop enabled :arrows_counterclockwise:")
        else:
            audiocontroller.playlist.loop = False
            await ctx.send("Loop disabled :x:")


    @commands.command(name='셔플', description=config.HELP_SHUFFLE_LONG, help=config.HELP_SHUFFLE_SHORT,
                      aliases=["sh", "shuffle"])
    async def _shuffle(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Queue is empty :x:")
            return

        audiocontroller.playlist.shuffle()
        await ctx.send("Shuffled queue :twisted_rightwards_arrows:")

        for song in list(audiocontroller.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(audiocontroller.preload(song))


    @commands.command(name='일시정지', description=config.HELP_PAUSE_LONG, help=config.HELP_PAUSE_SHORT, aliases = ["pause"])
    async def _pause(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await ctx.send("Playback Paused :pause_button:")

    @commands.command(name='큐', description=config.HELP_QUEUE_LONG, help=config.HELP_QUEUE_SHORT,
                      aliases=['q', "queue", "플레이리스트", "리스트"])
    async def _queue(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Queue is empty :x:")
            return

        playlist = utils.guild_to_audiocontroller[current_guild].playlist

        # Embeds are limited to 25 fields
        if config.MAX_SONG_PRELOAD > 25:
            config.MAX_SONG_PRELOAD = 25

        embed = discord.Embed(title=":scroll: Queue [{}]".format(
            len(playlist.playque)), color=config.EMBED_COLOR, inline=False)

        for counter, song in enumerate(list(playlist.playque)[:config.MAX_SONG_PRELOAD], start=1):
            if song.info.title is None:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.webpage_url, song.info.webpage_url), inline=False)
            else:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.title, song.info.webpage_url), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='정지', description=config.HELP_STOP_LONG, help=config.HELP_STOP_SHORT, aliases=['st', "stop"])
    async def _stop(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await ctx.send("Stopped all sessions :octagonal_sign:")

    @commands.command(name='이동', description=config.HELP_MOVE_LONG, help=config.HELP_MOVE_SHORT, aliases=['mv', "move"])
    async def _move(self, ctx, *args):
        if len(args) != 2:
            ctx.send("Wrong number of arguments")
            return

        try:
            oldindex, newindex = map(int, args)
        except ValueError:
            ctx.send("Wrong argument")
            return

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Queue is empty :x:")
            return
        try:
            audiocontroller.playlist.move(oldindex - 1, newindex - 1)
        except IndexError:
            await ctx.send("Wrong position")
            return
        await ctx.send("Moved")

    @commands.command(name='스킵', description=config.HELP_SKIP_LONG, help=config.HELP_SKIP_SHORT, aliases=['sk', 'skip', '다음'])
    async def _skip(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Queue is empty :x:")
            return
        current_guild.voice_client.stop()
        await ctx.send("Skipped current song :fast_forward:")

    @commands.command(name='비우기', description=config.HELP_CLEAR_LONG, help=config.HELP_CLEAR_SHORT, aliases=['cl', 'clear'])
    async def _clear(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        await ctx.send("Cleared queue :no_entry_sign:")

    @commands.command(name='이전', description=config.HELP_PREV_LONG, help=config.HELP_PREV_SHORT, aliases=['back', 'prev'])
    async def _prev(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].prev_song()
        await ctx.send("Playing previous song :track_previous:")

    @commands.command(name='재생', description=config.HELP_RESUME_LONG, help=config.HELP_RESUME_SHORT, aliases=['resume'])
    async def _resume(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()
        await ctx.send("Resumed playback :arrow_forward:")

    @commands.command(name='정보', description=config.HELP_SONGINFO_LONG, help=config.HELP_SONGINFO_SHORT,
                      aliases=["np", 'songinfo'])
    async def _songinfo(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.send(embed=song.info.format_output(config.SONGINFO_SONGINFO))

    @commands.command(name='기록', description=config.HELP_HISTORY_LONG, help=config.HELP_HISTORY_SHORT, aliases=["history"])
    async def _history(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await ctx.send(utils.guild_to_audiocontroller[current_guild].track_history())

    @commands.command(name='볼륨', aliases=["vol", "volume"], description=config.HELP_VOL_LONG, help=config.HELP_VOL_SHORT)
    async def _volume(self, ctx, *args):
        if ctx.guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return

        if await utils.play_check(ctx) == False:
            return

        if len(args) == 0:
            await ctx.send("Current volume: {}% :speaker:".format(utils.guild_to_audiocontroller[ctx.guild]._volume))
            return

        try:
            volume = args[0]
            volume = int(volume)
            if volume > 100 or volume < 0:
                raise Exception('')
            current_guild = utils.get_guild(self.bot, ctx.message)

            if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
                await ctx.send('Volume set to {}% :sound:'.format(str(volume)))
            else:
                await ctx.send('Volume set to {}% :loud_sound:'.format(str(volume)))
            utils.guild_to_audiocontroller[current_guild].volume = volume
        except:
            await ctx.send("Error: Volume must be a number 1-100")
    

    @commands.command(name='삭제', description=config.HELP_MOVE_LONG, help=config.HELP_MOVE_SHORT, aliases=['d', "delete"])
    async def delete(self, ctx, *args):
        if len(args) != 1:
            ctx.send("Wrong number of arguments")
            return

        try:
            print(args)
            index = int(args[0]) - 1
        except ValueError:
            ctx.send("Wrong argument")
            return

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Queue is empty :x:")
            return
        try:
            audiocontroller.playlist.delete(index)
        except IndexError:
            await ctx.send("Wrong position")
            return
        await ctx.send("삭제했습니다")
        
    
    @commands.command(name='검색', description="유튜브 검색 10개 를 보여주고 선택합니다.", help="유튜브 검색 10개 를 보여주고 선택합니다.",aliases=["s"])
    async def _find_song(self, ctx, *, title: str):
        songcount = config.SONGCOUNT
        if title.isspace() or not title:
            return
        results = YoutubeSearch(title, max_results=songcount).to_dict()

        # 1번 
        # emb = discord.Embed(title='리스트', description = "\u200b", color=discord.Color.blue())
        # for i in range(10):
        #     content = "{}: {}".format(str(i+1), results[i]["title"])
        #     emb.add_field(name = '\u200b', value = content, inline = False)
        # await ctx.send(embed = emb)
        
        #2번 
        content = ""
        for i in range(songcount):
            temp = "{} : {}".format(str(i+1), results[i]["title"])[:60]
            content += temp + "\n\n"
        emb = discord.Embed(title='해당 번호를 입력해주세요', description = content, color=discord.Color.blue())
        await ctx.send(embed = emb)
        pos = 0
        
        def check(m: discord.Message):
            def inner_check(message): 
                if message.author != ctx.author:
                    return False
                if message.channel.id != ctx.channel.id :
                    return False
                try: 
                    int(message.content)
                    if int(message.content) <= songcount and int(message.content) >= 1:
                        return True 
                    return False
                except ValueError:
                    return False
            return inner_check(m)
        
        try:
            msg = await self.bot.wait_for(event = "message", check=check, timeout = 20.0)
            pos = int(msg.content) - 1
        except asyncio.TimeoutError:
            await ctx.send("타임아웃입니다!")
            return
        else:
            track = "https://www.youtube.com/watch?v={}".format(results[pos]["id"])
            await self.songplay(ctx, track)
            
            
            # current_guild = utils.get_guild(self.bot, ctx.message)
            # audiocontroller = utils.guild_to_audiocontroller[current_guild]

            # if (await utils.is_connected(ctx) == None):
            #     if await audiocontroller.uconnect(ctx) == False:
            #         return

            # if await utils.play_check(ctx) == False:
            #     return

            # # reset timer
            # audiocontroller.timer.cancel()
            # audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

            # if audiocontroller.playlist.loop == True:
            #     await ctx.send("Loop is enabled! Use {}loop to disable".format(config.BOT_PREFIX))
            #     return

            # song = await audiocontroller.process_song(track)

            # if song is None:
            #     await ctx.send(config.SONGINFO_ERROR)
            #     return

            # if song.origin == linkutils.Origins.Default:

            #     if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
            #         await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            #     else:
            #         await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

            # elif song.origin == linkutils.Origins.Playlist:
            #     await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)


    @commands.command(name='재생목록', description="ㅁㄴㅇ", help="ㅁㄴㅇ",aliases=["playlist", "pl"])
    async def _my_song(self, ctx):
        with open("./config/playlist.pickle","rb") as pl:
            playlist = pickle.load(pl)
        try:
            custom_playlist = playlist[ctx.author.id]
        except:
            print("no playlist")
            return
        content = ""
        for i in range(len(custom_playlist)):
            temp = "{} : {}".format(str(i+1), custom_playlist[i]["title"])[:60]
            content += temp + "\n\n"
        emb = discord.Embed(title='이것이 당신의 재생목록입니다.', description = content, color=discord.Color.blue())
        await ctx.send(embed = emb)

    ""
    @commands.command(name='재생목록재생', description="개인 재생목록 재생", help="개인 재생목록 재생",aliases=["pp"])
    async def _my_play(self, ctx):
        with open("./config/playlist.pickle","rb") as pl:
            playlist = pickle.load(pl)
        try:
            custom_playlist = playlist[ctx.author.id]
        except:
            print("no playlist")
            return
        for i in custom_playlist:
            track = i["url"]
            await self.songplay(ctx,track)
        
        
    @commands.command(name='재생목록추가', description="개인 재생목록에 추가", help="개인 재생목록에 추가",aliases=["push","ps"])
    async def _my_push(self, ctx):
        try:
            pl = open("./config/playlist.pickle","rb")
            playlist = pickle.load(pl)
            pl.close()
        except:
            playlist = {}
            
        try:
            playlist[ctx.author.id]
        except:
            playlist[ctx.author.id] = []
        
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        playlist[ctx.author.id].append({"title" : song.info.title, "url" : song.info.webpage_url})
        await ctx.send(song.info.title + "을 추가했습니다.")
        with open("./config/playlist.pickle","wb") as pl:
            pickle.dump(playlist,pl)
        
        
    async def songplay(self, ctx, track):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if (await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        if await utils.play_check(ctx) == False:
            return

        # reset timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if audiocontroller.playlist.loop == True:
            await ctx.send("Loop is enabled! Use {}loop to disable".format(config.BOT_PREFIX))
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)


async def setup(bot):
    await bot.add_cog(음악(bot))
