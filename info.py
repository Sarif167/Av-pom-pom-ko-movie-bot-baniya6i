import re
from os import environ

# -------------------------
# Helper
# -------------------------
def str_to_bool(val, default=False):
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")

# =========================================================
# 🤖 BOT BASIC INFORMATION
# =========================================================
API_ID = int(environ.get("API_ID", "23621595"))
API_HASH = environ.get("API_HASH", "de904be2b4cd4efe2ea728ded17ca77d")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
PORT = int(environ.get("PORT", "8080"))
TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")
OWNER_USERNAME = environ.get("OWNER_USERNAME", "premiumuseronly_Bot")

# =========================================================
# 💾 DATABASE CONFIGURATION
# =========================================================
DB_URL = environ.get("DATABASE_URI", "mongodb+srv://Tigerbhai:Tigerbhai@cluster07374747.v0ojz7d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster07374747")
DB_NAME = environ.get("DATABASE_NAME", "testing")

# =========================================================
# 📢 CHANNELS & ADMINS
# =========================================================
ADMINS = int(environ.get("ADMINS", "1249672673"))

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1003184409377"))
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", "-1003184409377"))
VERIFIED_LOG = int(environ.get("VERIFIED_LOG", "-1003184409377"))

POST_CHANNEL = int(environ.get("POST_CHANNEL", "-1002314687215"))
VIDEO_CHANNEL = int(environ.get("VIDEO_CHANNEL", "-1002623534183"))
BRAZZER_CHANNEL = int(environ.get("BRAZZER_CHANNEL", "-1002259803190"))

# Auth channels list
auth_channel_str = environ.get("AUTH_CHANNEL", "-1002682431363")
AUTH_CHANNEL = [int(x) for x in auth_channel_str.split() if x.strip().lstrip("-").isdigit()]

# =========================================================
# ⚙️ FEATURES & TOGGLES  (FIXED)
# =========================================================
FSUB = str_to_bool(environ.get("FSUB"), True)
IS_VERIFY = str_to_bool(environ.get("IS_VERIFY"), True)
POST_SHORTLINK = str_to_bool(environ.get("POST_SHORTLINK"), True)
SEND_POST = str_to_bool(environ.get("SEND_POST"), True)
PROTECT_CONTENT = str_to_bool(environ.get("PROTECT_CONTENT"), False)

# =========================================================
# 🔢 LIMITS
# =========================================================
DAILY_LIMIT = int(environ.get("DAILY_LIMIT", "00"))
VERIFICATION_DAILY_LIMIT = int(environ.get("VERIFICATION_DAILY_LIMIT", "40"))
PREMIUM_DAILY_LIMIT = int(environ.get("PREMIUM_DAILY_LIMIT", "80"))

# =========================================================
# 🔗 SHORTLINK & VERIFICATION
# =========================================================
SHORTLINK_URL = environ.get("SHORTLINK_URL", "linkshortify.com")
SHORTLINK_API = environ.get("SHORTLINK_API", "74e17137f92e31cc0406fab6fcf3131bc61f8ecc")
POST_SHORTLINK_URL = environ.get("POST_SHORTLINK_URL", "linkshortify.com")
POST_SHORTLINK_API = environ.get("POST_SHORTLINK_API", "74e17137f92e31cc0406fab6fcf3131bc61f8ecc")
VERIFY_EXPIRE = int(environ.get("VERIFY_EXPIRE", "3600"))
TUTORIAL_LINK = environ.get("TUTORIAL_LINK", "https://t.me/Premium_Jaction/456")

# =========================================================
# 💳 PAYMENT SETTINGS
# =========================================================
UPI_ID = environ.get("UPI_ID", "Q855940864@ybl")
QR_CODE_IMAGE = environ.get("QR_CODE_IMAGE", "https://image.zaw-myo.workers.dev/image/10735dbf-c841-474d-a253-6c28d984c1a2")

# =========================================================
# 🖼️ IMAGES
# =========================================================
START_PIC = environ.get("START_PIC", "https://image.zaw-myo.workers.dev/image/89652e23-b14f-4aaa-b295-e9f5c93ee3b7")
AUTH_PICS = environ.get("AUTH_PICS", "https://image.zaw-myo.workers.dev/image/73e5038f-ad84-4a29-8ae8-0c7e07bc893e")
VERIFY_IMG = environ.get("VERIFY_IMG", "https://image.zaw-myo.workers.dev/image/13e5c437-0197-4239-b39f-895674d035fc")
NO_IMG = environ.get("NO_IMG", "https://image.zaw-myo.workers.dev/image/89652e23-b14f-4aaa-b295-e9f5c93ee3b7")

# =========================================================
# 🌐 WEB APP
# =========================================================
WEB_APP_URL = environ.get("WEB_APP_URL", "https://okay-biddy-nasir135-c4c04239.koyeb.app/")
