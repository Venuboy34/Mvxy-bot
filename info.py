import re
import os
from os import environ, getenv
from Script import script

# Utility functions
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# ============================
# Bot Information Configuration
# ============================
SESSION = 'FilmziMovieBot'   # Session name for the bot
API_ID = 20288994 # API ID from my.telegram.org
API_HASH = 'd702614912f1ad370a0d18786002adbf'  # API Hash from my.telegram.org
BOT_TOKEN = '8551650456:AAHjv7hyhNFMl4borM-gLneIEcZhtLZ5-qc'    # Bot token from @BotFather

# ============================
# Bot Settings Configuration
# ============================
CACHE_TIME = 300    # Cache time in seconds (default: 5 minutes)
USE_CAPTION_FILTER = True  # Use caption filter for search results (default: True)
INDEX_CAPTION = True # Save caption db when idexing make it False if you dont use USE_CAPTION_FILTER for search results (default: True)
#Making it false will not save caption in db SO you can save some storage space
COVERX = True # Use cover image for indexed files (default: True)
# If you disable it then bot will use a default thumb for all files

PICS_URL = [https://api.aniwallpaper.workers.dev/random?type=boy] #random anime girl img each time from aniwallpaper (Experimental)
PICS = ['https://i.ibb.co/ksrvqFFw/img-8312532076.jpg', 'https://i.ibb.co/LhrhYmjz/img-8312532076.jpg', 'https://i.ibb.co/DDwXh1hJ/img-8312532076.jpg', 'https://i.ibb.co/HLsntHQm/img-8312532076.jpg']  # Sample pic
NOR_IMG = "https://graph.org/file/e20b5fdaf217252964202.jpg"
MELCOW_PHOTO = "https://graph.org/file/56b5deb73f3b132e2bb73.jpg"
SPELL_IMG = "https://graph.org/file/13702ae26fb05df52667c.jpg"
SUBSCRIPTION = 'https://graph.org/file/242b7f1b52743938d81f1.jpg'
FSUB_PICS = ['https://i.ibb.co/pr2H8cwT/img-8312532076.jpg']  # Fsub pic

# ============================
# Admin, Channels & Users Configuration
# ============================
ADMINS = [8312532076] # Replace with the actual admin ID(s) to add
CHANNELS = [-1002897456594]  # Channel id for auto indexing (make sure bot is admin)

LOG_CHANNEL = -1003382486179  # Log channel id (make sure bot is admin)
BIN_CHANNEL = -1002897456594  # Bin channel id (make sure bot is admin)
PREMIUM_LOGS = -1002897456594  # Premium logs channel id
DELETE_CHANNELS = [-1002897456594] #(make sure bot is admin)
support_chat_id = -1002897456594  # Support group id (make sure bot is admin)
reqst_channel = -1002897456594  # Request channel id (make sure bot is admin)
SUPPORT_CHAT = 'https://t.me/zerodev2'  # Support group link (make sure bot is admin)

# FORCE_SUB 
auth_req_channels = "-1002997352630"# requst to join Channel for force sub (make sure bot is admin) only for bot ADMINS  
auth_channels     = "-1003662705513"# Channels for force sub (make sure bot is admin)

# ============================
# Payment Configuration
# ============================
QR_CODE = 'https://graph.org/file/1b2471aaeb5a7f4bb5266-cddfd202f6de756926.jpg'    # QR code image for payments
OWNER_UPI_ID = 'ɴᴏ ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ'    # Owner UPI ID for payments

STAR_PREMIUM_PLANS = {
    10: "7day",
    20: "15day",    
    40: "1month", 
    55: "45day",
    75: "60day",
}  # Premium plans with their respective durations in days

# ============================
# MongoDB Configuration
# ============================
DATABASE_URI = "mongodb+srv://Zerobothost:zerobothost@cluster0.bl0tf2.mongodb.net/?appName=Cluster0"  # MongoDB URI for the database
DATABASE_NAME = "Cluster0" # Database name (default: cluster)
COLLECTION_NAME = 'Filmzi_Files' # Collection name (default: dreamcinezone_files)

# If MULTIPLE_DB Is True Then Fill DATABASE_URI2 Value Else You Will Get Error.
MULTIPLE_DB = False # Type True For Turn On MULTIPLE DB FUNTION 
DATABASE_URI2 = "mongodb+srv://Zerobothost:zerobothost@cluster0.bl0tf2.mongodb.net/?appName=Cluster0"  # MongoDB URI for the second database (if MULTIPLE_DB is True)
# ============================
# Movie Notification & Update Settings
# ============================
MOVIE_UPDATE_NOTIFICATION = True  # Notification On (True) / Off (False)
MOVIE_UPDATE_CHANNEL = -1003318483881  # Notification of sent to your channel
DREAMXBOTZ_IMAGE_FETCH = True  # On (True) / Off (False)
LINK_PREVIEW = False # Shows link preview in notification msg instead of image
ABOVE_PREVIEW = True # Shows link preview above the text in notification msg if True else below the msg
TMDB_API_KEY = '282fec93f7dac5a152e0b321327b46c4' # preffer to use your own tmdb API Key get it from https://www.themoviedb.org/settings/api
TMDB_POSTER = True # Shows TMDB poster in notification msg
LANDSCAPE_POSTER = True # Shows landscape poster in notification msg

# ============================
# Verification Settings
# ============================
IS_VERIFY = False  # Verification On (True) / Off (False)
LOG_VR_CHANNEL = -1002897456594 #Verification Channel Id 
LOG_API_CHANNEL = -1002897456594 #If Anyone Set Your Bot In Any Group And Set Shortner In That Group Then In This Channel The All Details Come
VERIFY_IMG = "https://graph.org/file/d7a2ec5a7343175789cbb-ce6b1d2e43103b5b20.jpg"

TUTORIAL = "https://t.me/Zeroboy216"   # Tutorial link for verification
TUTORIAL_2 = "https://t.me/Zeroboy216"   # Second tutorial link for verification
TUTORIAL_3 = "https://t.me/Zeroboy216"   # Third tutorial link for verification

# Verification (Must Fill All Veriables. Else You Got Error
SHORTENER_API = "a7ac9b3012c67d7491414cf272d82593c75f6cbb" # Shortener API key
SHORTENER_WEBSITE = "omegalinks.in" # Shortener website

SHORTENER_API2 = "a7ac9b3012c67d7491414cf272d82593c75f6cbb"  # Shortener API key for second website
SHORTENER_WEBSITE2 = "omegalinks.in" # Shortener website for second website

SHORTENER_API3 = "a7ac9b3012c67d7491414cf272d82593c75f6cbb"  
SHORTENER_WEBSITE3 = "omegalinks.in" # Shortener website for third website

TWO_VERIFY_GAP = 1200 # Time gap for two-step verification in seconds (default: 20 minutes)
THREE_VERIFY_GAP = 54000    

# ============================
# Channel & Group Links Configuration
# ============================
GRP_LNK = 'https://t.me/zerodev2' # Group link for the bot
OWNER_LNK = 'https://t.me/Zeroboy216' # Owner link for the bot
UPDATE_CHNL_LNK = 'https://t.me/mvxybotupdate' # Update channel link for the bot

# ============================
# User Configuration
# ============================
auth_users = [8312532076]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
PREMIUM_USER = [8312532076]

# ============================
# Miscellaneous Configuration
# ============================
ULTRA_FAST_MODE = False # Set to True for fast search, False for original search

MAX_B_TN = "5" # Maximum number of buttons in a row (default: 5)
PORT = 8080  # Port for the web server (default: 8080)
MSG_ALRT = 'Share & Support Us ♥️' # Alert message for users
DELETE_TIME = 300  #  deletion time in seconds (default: 5 minutes). Adjust as per your needs.
CUSTOM_FILE_CAPTION = f"{script.CAPTION}"   # Custom caption for files
BATCH_FILE_CAPTION = CUSTOM_FILE_CAPTION # Custom caption for batch files
IMDB_TEMPLATE = f"{script.IMDB_TEMPLATE_TXT}"     # Custom IMDB template 
MAX_LIST_ELM = None # Maximum number of elements in a list (default: None, no limit)
INDEX_REQ_CHANNEL = LOG_CHANNEL  # Index Request Channel ID (make sure bot is admin)
NO_RESULTS_MSG = True  # True if you want no results messages in Log Channel
MAX_BTN = True    # Max Button On (True) / Off (False)
P_TTI_SHOW_OFF = False    # P_TTI_SHOW_OFF On (True) / Off (False)
IMDB = False    # IMDB Results On (True) / Off (False)
TMDB_ON_SEARCH = True    # Use TMDB Poster On Search Results
AUTO_FFILTER = True # Auto Filter On (True) / Off (False)
AUTO_DELETE = True # Auto Delete On (True) / Off (False)
LONG_IMDB_DESCRIPTION = False # Long IMDB Description On (True) / Off (False)
SPELL_CHECK_REPLY = True # Spell Check Mode On (True) / Off (False)
MELCOW_NEW_USERS = False # Melcow New Users On (True) / Off (False)
PROTECT_CONTENT = False # Protect Content On (True) / Off (False)
PM_SEARCH = True  # PM Search On (True) / Off (False)
EMOJI_MODE = True  # Emoji status On (True) / Off (False)
BUTTON_MODE = True # pm & Group button or link mode (True) / Off (False)
STREAM_MODE = True # Set Stream mode True or False
PREMIUM_STREAM_MODE = False # Set Stream mode True or False only for premium users


# ============================
# Bot Configuration
# ============================

AUTH_REQ_CHANNELS = [int(ch) for ch in auth_req_channels.split() if ch and id_pattern.match(ch)] 
AUTH_CHANNELS = [int(ch) for ch in auth_channels.split() if ch and id_pattern.match(ch)]
REQST_CHANNEL = int(reqst_channel) if reqst_channel else None
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id else None
LANGUAGES = {"ᴍᴀʟᴀʏᴀʟᴀᴍ":"mal","ᴛᴀᴍɪʟ":"tam","ᴇɴɢʟɪsʜ":"eng","ʜɪɴᴅɪ":"hin","ᴛᴇʟᴜɢᴜ":"tel","ᴋᴀɴɴᴀᴅᴀ":"kan","ɢᴜᴊᴀʀᴀᴛɪ":"guj","ᴍᴀʀᴀᴛʜɪ":"mar","ᴘᴜɴᴊᴀʙɪ":"pun"}
QUALITIES = ["360P", "480P", "720P", "1080P", "1440P", "2160P", "4K"]

SEASON_COUNT = 12
SEASONS = [f"S{str(i).zfill(2)}" for i in range(1, SEASON_COUNT + 1)]

BAD_WORDS = {
    "PrivateMovieZ",
    "toonworld4all",
    "themoviesboss",
    "1tamilmv",
    "tamilblasters",
    "1tamilblasters",
    "skymovieshd",
    "extraflix",
    "hdm2",
    "moviesmod",
    "hdhub4u",
    "mkvcinemas",
    "primefix",
    "join",
    "www",
    "villa",
    "tg",
    "original"
} # Set of bad words to filter out
   

# ============================
# Server & Web Configuration
# ============================

NO_PORT = False
APP_NAME = None
ON_HEROKU = False
BIND_ADRESS = 'mvxy-bot.onrender.com'
FQDN = BIND_ADRESS
URL = "https://{}/".format(FQDN, PORT)
SLEEP_THRESHOLD = 60
WORKERS = 4
SESSION_NAME = 'dreamXBotz'
MULTI_CLIENT = False
name = 'DREAMXBOTZ'
PING_INTERVAL = 1200  # 20 minutes
ON_HEROKU = False
HAS_SSL = True
if HAS_SSL:
    URL = "https://{}/".format(FQDN)
else:
    URL = "http://{}/".format(FQDN)

# ============================
# Reactions Configuration
# ============================
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]

# ============================
# Commands Bot
# ============================
Bot_cmds = {
    "start": "Sᴛᴀʀᴛ Mᴇ Bᴀʙʏ",
    "stats": "Gᴇᴛ Bᴏᴛ Sᴛᴀᴛs",
    "alive": " Cʜᴇᴄᴋ Bᴏᴛ Aʟɪᴠᴇ ᴏʀ Nᴏᴛ ",
    "settings": "ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs",
    "id": "ɢᴇᴛ ɪᴅ ᴛᴇʟᴇɢʀᴀᴍ ",
    "info": "Gᴇᴛ Usᴇʀ ɪɴғᴏ ",
    "del_msg": "ʀᴇᴍᴏᴠᴇ ғɪʟᴇ ɴᴀᴍᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ɴᴏтɪғɪᴄᴀᴛɪᴏɴ...",
    "movie_update": "ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ...",
    "pm_search": "ᴘᴍ sᴇᴀʀᴄʜ ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ...",
    "trendlist": "Gᴇᴛ Tᴏᴘ Tʀᴀɴᴅɪɴɢ Sᴇᴀʀᴄʜ Lɪsᴛ",
    "broadcast": "ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ.",
    "grp_broadcast": "ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs",
    "send": "ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴜꜱᴇʀ.",
    "add_premium": "ᴀᴅᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ.",
    "remove_premium": "ʀᴇᴍᴏᴠᴇ ᴀɴʏ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.",
    "premium_users": "ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ.",
    "restart": "ʀᴇꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.",
    "group_cmd": "ɢʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ",
    "admin_cmd": "ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs ʟɪsᴛ.",
    "reset_group": "Group Setting Default",
    "trial_reset": "User Trial Reset",
    "remove_fsub": "Remove Forced Subscription (group admin only)",
}


#Don't Change Anything Here
if MULTIPLE_DB == False:
    DATABASE_URI = DATABASE_URI
    DATABASE_URI2 = DATABASE_URI
else:
    DATABASE_URI = DATABASE_URI
    DATABASE_URI2 = DATABASE_URI2

# ============================
# Logs Configuration
# ============================
LOG_STR = "Current Customized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for your queries.\n" if IMDB else "IMDB Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found, Users will be redirected to send /start to Bot PM instead of sending file directly.\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled, files will be sent in PM instead of starting the bot.\n")
LOG_STR += ("BUTTON_MODE is found, filename and file size will be shown in a single button instead of two separate buttons.\n" if BUTTON_MODE else "BUTTON_MODE is disabled, filename and file size will be shown as different buttons.\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be sent along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled, Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode is enabled, bot will be suggesting related movies if movie name is misspelled.\n" if SPELL_CHECK_REPLY else "Spell Check Mode is disabled.\n")
