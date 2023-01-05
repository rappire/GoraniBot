import asyncio
import discord
from youtube_search import YoutubeSearch
import yt_dlp
import config.config as config
from app.song import Song
from app.playlist import Playlist
from app.utility import check_url
from random import seed, uniform


class Timer:
    def __init__(self, callback):
        self._callback = callback
        self._task = asyncio.create_task(self.job())

    async def job(self):
        await asyncio.sleep(config.TIMEOUT)
        await self._callback()

    def cancel(self):
        self._task.cancel()


class Audio:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.channel = None
        self.playlist = Playlist()
        self.current_song = None
        self.timer = None
        self.volume = config.VOLUME

    async def connect(self, ctx):
        self.timer = Timer(self.set_timer)
        if ctx.author.voice is None:
            await ctx.send("음성 채널에 접속해 주세요")
            return
        if self.guild.voice_client is None:
            await ctx.author.voice.channel.connect(reconnect=True, timeout=None)
            self.channel = ctx.author.voice.channel
            return
        if self.channel != ctx.author.voice.channel:
            await self.disconnect()
            await ctx.author.voice.channel.connect(reconnect=True, timeout=None)
            return

    async def disconnect(self):
        self.playlist.empty()
        try:
            self.timer.cancel()
        except:
            pass
        self.current_song = None
        self.guild.voice_client.stop()
        await self.guild.voice_client.disconnect(force=True)

    async def push_queue(self, ctx, title):
        # Url 확인
        result = check_url(title)
        if result == "space":
            await ctx.send("노래를 입력해주세요")
            return
        if result == "title":
            url = await self.search_youtube(title)
        else:
            url = title.split("&list=")[0]
        downloader = yt_dlp.YoutubeDL(config.YTDL_options)
        info = downloader.extract_info(url=url, download=False)
        thumbnail = info.get("thumbnails")[len(info.get("thumbnails")) - 1]["url"]
        song = Song(
            url=info.get("url"),
            title=info.get("title"),
            duration=info.get("duration"),
            webpage_url=info.get("webpage_url"),
            thumbnail=thumbnail,
            requester=ctx.author.name,
            uploader=info.get("uploader"),
        )

        self.playlist.add(song)
        self.timer = Timer(self.set_timer)

        if self.current_song is None:
            await ctx.send(embed=song.output("현재 재생중"))
            print(f"{song.title} 재생")
        else:
            await ctx.send(embed=song.output("플레이리스트에 추가됨"))
            print(f"{song.title} 추가")

    async def play(self):
        if self.current_song is None:
            if self.playlist.isempty():
                return
            self.current_song = self.playlist.next()
            self.guild.voice_client.play(
                discord.FFmpegPCMAudio(
                    self.current_song.url,
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                ),
                after=lambda e: self.next_play(),
            )

            self.guild.voice_client.source = discord.PCMVolumeTransformer(
                self.guild.voice_client.source
            )
            self.guild.voice_client.source.volume = float(self.volume) / 100.0

    def next_play(self):
        self.current_song = None
        if self.playlist.isempty():
            return
        self.bot.loop.create_task(self.play())

    async def set_timer(self):
        if self.guild.voice_client == None:
            return
        if len(self.guild.voice_client.channel.voice_states) == 1:
            await self.disconnect()
            return

        if self.guild.voice_client.is_playing():
            self.timer = Timer(self.set_timer)  # restart timer
            return

        await self.disconnect()

    async def search_youtube(self, title):
        results = YoutubeSearch(title, max_results=1).to_dict()
        videocode = results[0]["id"]
        return "https://www.youtube.com/watch?v={}".format(videocode)

    async def ak(self, num):
        seed()
        try:
            self.timer.cancel()
        except:
            pass
        for i in range(num):
            while self.guild.voice_client.is_playing():
                time = uniform(0.2, 0.7)
                await asyncio.sleep(time)
                self.guild.voice_client.stop()
            self.guild.voice_client.play(discord.FFmpegPCMAudio(source="config/AK.mp3"))
        while self.guild.voice_client.is_playing():
            await asyncio.sleep(1)

        self.timer = None
        await self.disconnect()
