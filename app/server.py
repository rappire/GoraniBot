from app.audio import Audio

guild_list = []
audio_list = {}

async def server_init(bot, guilds):
    for server in guilds:
        guild_list.append(server)
        audio_list[server] = Audio(bot, server)

