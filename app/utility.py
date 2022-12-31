import re

def get_url(content):
    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    if re.search(regex, content):
        result = regex.search(content)
        url = result.group(0)
        return url
    else:
        return None
    
#url을 확인해서 유튜브인지 제목인지 체크
def check_url(text:str):
    if text.isspace():
        return "space"
    if "https://www.youtu" in text or "https://youtu.be" in text:
        return "youtube"
    return "title"

#url을 확인해서 플레이리스트인지 체크
def check_playlist(url):
    if "playlist?list=" in url:
        return True
    return False

#메세지로부터 서버를 알려줌
def get_guild(bot, message):
    if message.guild is not None:
        return message.guild
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if message.author in channel.members:
                return guild
    return None