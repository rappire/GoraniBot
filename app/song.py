import datetime
import discord

class Song():
    def __init__(self, url = None, title = None, duration = None, webpage_url=None ,thumbnail = None, requester = None, uploader = None):
        self.url = url
        self.title = title
        self.duration = duration
        self.thumbnail = thumbnail
        self.requester = requester
        self.uploader = uploader
        self.webpage_url = webpage_url
    
    def output(self, play):
        embed = discord.Embed(title=play,description = f"[{self.title}]({self.webpage_url})", color=discord.colour.Colour.random())
        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)
        if self.uploader is not None:
            embed.add_field(name="업로더", value=self.uploader, inline=True)
        if self.duration is not None:
            embed.add_field(name="길이", value=f"{str(datetime.timedelta(seconds=self.duration))}", inline=True)
        if self.requester is not None:
            embed.add_field(name="요청자", value=self.requester, inline=True)
        
        return embed
        