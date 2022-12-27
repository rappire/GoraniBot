BOT_TOKEN: str = "OTg5ODAxNDQ5NzU0MDkxNTMw.GQWXu9.nEFXiHiPJPqEQFMyW2lHSEV8vhzN7i2zIcedHM"
SPOTIFY_ID: str = ""
SPOTIFY_SECRET: str = ""

BOT_PREFIX = "?"

EMBED_COLOR = 0x4dd4d0  #replace after'0x' with desired hex code ex. '#ff0188' >> '0xff0188'

SUPPORTED_EXTENSIONS = ('.webm', '.mp4', '.mp3', '.avi', '.wav', '.m4v', '.ogg', '.mov')

MAX_SONG_PRELOAD = 5  #maximum of 25

COOKIE_PATH = "/config/cookies/cookies.txt"

GLOBAL_DISABLE_AUTOJOIN_VC = False

VC_TIMEOUT = 10 #seconds
VC_TIMOUT_DEFAULT = True  #default template setting for VC timeout true= yes, timeout false= no timeout
ALLOW_VC_TIMEOUT_EDIT = True  #allow or disallow editing the vc_timeout guild setting

AK = True
SONGCOUNT = 10

STARTUP_MESSAGE = "Starting Bot..."
STARTUP_COMPLETE_MESSAGE = "Startup Complete"

NO_GUILD_MESSAGE = 'Error: Please join a voice channel or enter the command in guild chat'
USER_NOT_IN_VC_MESSAGE = "Error: Please join the active voice channel to use commands"
WRONG_CHANNEL_MESSAGE = "Error: Please use configured command channel"
NOT_CONNECTED_MESSAGE = "Error: Bot not connected to any voice channel"
ALREADY_CONNECTED_MESSAGE = "Error: Already connected to a voice channel"
CHANNEL_NOT_FOUND_MESSAGE = "Error: Could not find channel"
DEFAULT_CHANNEL_JOIN_FAILED = "Error: Could not join the default voice channel"
INVALID_INVITE_MESSAGE = "Error: Invalid invitation link"

ADD_MESSAGE= "To add this bot to your own Server, click [here]" #brackets will be the link text

INFO_HISTORY_TITLE = "Songs Played:"
MAX_HISTORY_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15

SONGINFO_UPLOADER = "업로더: "
SONGINFO_DURATION = "길이: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "좋아요: "
SONGINFO_DISLIKES = "싫어요: "
SONGINFO_NOW_PLAYING = "현재 재생중"
SONGINFO_QUEUE_ADDED = "플레이리스트에 추가됨"
SONGINFO_SONGINFO = "곡 정보"
SONGINFO_ERROR = "Error: Unsupported site or age restricted content. To enable age restricted content check the documentation/wiki."
SONGINFO_PLAYLIST_QUEUED = "Queued playlist :page_with_curl:"
SONGINFO_UNKNOWN_DURATION = "Unknown"

HELP_ADDBOT_SHORT = "Add Bot to another server"
HELP_ADDBOT_LONG = "Gives you the link for adding this bot to another server of yours."
HELP_CONNECT_SHORT = "Connect bot to voicechannel"
HELP_CONNECT_LONG = "Connects the bot to the voice channel you are currently in"
HELP_DISCONNECT_SHORT = "Disonnect bot from voicechannel"
HELP_DISCONNECT_LONG = "Disconnect the bot from the voice channel and stop audio."

HELP_SETTINGS_SHORT = "View and set bot settings"
HELP_SETTINGS_LONG = "View and set bot settings in the server. Usage: {}settings setting_name value".format(BOT_PREFIX)

HELP_HISTORY_SHORT = "재생했던 곡 정보를 보여줍니다."
HELP_HISTORY_LONG = "재생했던 " + str(MAX_TRACKNAME_HISTORY_LENGTH) + "개의 곡 정보를 보여줍니다."
HELP_PAUSE_SHORT = "음악을 일시정지합니다."
HELP_PAUSE_LONG = "음악을 일시정지 합니다. [재생]으로 다시 재생시킬수있습니다."
HELP_VOL_SHORT = "볼륨을 변경합니다."
HELP_VOL_LONG = "플레이어의 볼륨을 변경합니다. 1~100 사이의 숫자를 넣으면 됩니다."
HELP_PREV_SHORT = "이전 곡으로 이동합니다."
HELP_PREV_LONG = "이전 곡을 다시 재생합니다."
HELP_RESUME_SHORT = "음악을 다시 재생시킵니다."
HELP_RESUME_LONG = "음악을 다시 재생시킵니다."
HELP_SKIP_SHORT = "Skip a song"
HELP_SKIP_LONG = "Skips the currently playing song and goes to the next item in the queue."
HELP_SONGINFO_SHORT = "Info about current Song"
HELP_SONGINFO_LONG = "Shows details about the song currently being played and posts a link to the song."
HELP_STOP_SHORT = "Stop Music"
HELP_STOP_LONG = "Stops the AudioPlayer and clears the songqueue"
HELP_MOVE_LONG = f"{BOT_PREFIX}move [position] [new position]"
HELP_MOVE_SHORT = 'Moves a track in the queue'
HELP_YT_SHORT = "Play a supported link or search on youtube"
HELP_YT_LONG = ("$p [link/video title/key words/playlist-link/soundcloud link/spotify link/bandcamp link/twitter link]")
HELP_PING_SHORT = "Pong"
HELP_PING_LONG = "Test bot response status"
HELP_CLEAR_SHORT = "Clear the queue."
HELP_CLEAR_LONG = "Clears the queue and skips the current song."
HELP_LOOP_SHORT = "Loops the currently playing song, toggle on/off."
HELP_LOOP_LONG = "Loops the currently playing song and locks the queue. Use the command again to disable loop."
HELP_QUEUE_SHORT = "Shows the songs in queue."
HELP_QUEUE_LONG = "Shows the number of songs in queue, up to 10."
HELP_SHUFFLE_SHORT = "Shuffle the queue"
HELP_SHUFFLE_LONG = "Randomly sort the songs in the current queue"
HELP_CHANGECHANNEL_SHORT = "Change the bot channel"
HELP_CHANGECHANNEL_LONG = "Change the bot channel to the VC you are in"

HELP_SERVER_SHORT = "서버 정보"
HELP_SERVER_LONG = "마크 서버 상태를 보여줍니다"
HELP_LOL_SHORT = "롤 패치노트"
HELP_LOL_LONG = "최신 롤 패치노트를 보여줍니다"
ABSOLUTE_PATH = '' #do not modify
