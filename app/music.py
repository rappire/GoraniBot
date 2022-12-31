from discord.ext import commands
import discord
from app.server import audio_list
from app.rotate_emb import Simple
from app.audio import Timer
from app.utility import get_guild


class 음악(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['노래','p'])
    async def play(self, ctx, *, title):
        #서버를 찾음
        guild = get_guild(self.bot, ctx.message)
        if guild is None:
            return
        guild_audio = audio_list[guild]
        #음성 서버 접속
        await guild_audio.connect(ctx)
        #큐에 집어넣기
        await guild_audio.push_queue(ctx, title)
        #재생 시키기
        await guild_audio.play()
    
    @commands.command(aliases=['큐','q'])
    async def queue(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("재생중이지 않습니다.")
            return
        playlist = audio_list[current_guild].playlist
        if playlist.length() == 0:
            await ctx.send("큐가 비어있습니다")
            return
        embeds = []
        for counter, song in enumerate(playlist.play_que):
            if counter % 5 == 0:
                embeds.append(discord.Embed(title=":scroll: 큐 [{}]\n:scroll: 페이지 : [{}]".format(
                playlist.length(), counter // 5 + 1)))
            if song.title is None:
                embeds[counter // 5].add_field(name="{}.".format(str(counter + 1)), value="[{}]({})".format(
                    song.webpage_url, song.webpage_url) , inline = False)
            else:
                embeds[counter // 5].add_field(name="{}.".format(str(counter  + 1)), value="[{}]({})".format(
                    song.title, song.webpage_url) , inline = False)
        await Simple().start(ctx, pages=embeds)
    
    @commands.command(name='스킵', aliases=['sk','다음'])
    async def skip(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        #플레이 체크
        audio = audio_list[current_guild]
        audio.timer.cancel()
        audio.timer = Timer(audio.set_timer)
        if current_guild is None:
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("큐가 비어있습니다.")
            return
        audio.current_song = None
        current_guild.voice_client.stop()
        await ctx.send("곡을 스킵했습니다.")

        
async def setup(bot):
    await bot.add_cog(음악(bot))