import asyncio
import time
import math
import os
import logging
import aiohttp
from shortzy import Shortzy

from info import SHORTLINK_API, SHORTLINK_URL, AUTH_CHANNEL, AUTH_PICS
from database.users_db import db
from pyrogram.enums import ParseMode
from Script import script

from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait, 
    InputUserDeactivated, 
    UserIsBlocked, 
    PeerIdInvalid, 
    UserNotParticipant, 
    ChatAdminRequired
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------- TEMP ---------------- #
class temp(object):
    ME = None
    U_NAME = None
    B_NAME = None
    B_LINK = None
    BOT = None
    USERS_CANCEL = False
    CANCEL = False  
    START_TIME = 0  
    CURRENT = 0    

# ---------------- FORCE SUB ---------------- #
async def is_user_joined(bot, message: Message) -> bool:
    if not AUTH_CHANNEL:
        return True

    user_id = message.from_user.id    
    not_joined_channels = []
    
    for channel_id in AUTH_CHANNEL:
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            try:
                chat = await bot.get_chat(channel_id)
                invite_link = await bot.export_chat_invite_link(channel_id)
                not_joined_channels.append((chat.title, invite_link))
            except ChatAdminRequired:
                await message.reply_text(
                    text=(
                        "<i>🔒 Bot is not admin in channel.\n"
                        "Contact developer:</i> "
                        "<b><a href='https://t.me/AV_SUPPORT_GROUP'>Click Here</a></b>"
                    ),
                    parse_mode=ParseMode.HTML
                )
                return False
            except Exception:
                continue
        except Exception:
            continue

    if not_joined_channels:
        try:
            if AUTH_PICS:
                await message.reply_photo(
                    photo=AUTH_PICS,
                    caption=script.AUTH_TXT.format(message.from_user.mention),
                    reply_markup=None,
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.reply_text(
                    text=script.AUTH_TXT.format(message.from_user.mention),
                    reply_markup=None,
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            logger.error(e)
            
        return False

    return True

# ---------------- TIME ---------------- #
def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    time_list.reverse()
    return ":".join(str(x) + time_suffix_list[i] for i, x in enumerate(time_list))

# ---------------- SIZE ---------------- #
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# ---------------- SECONDS ---------------- #
async def get_seconds(time_string):
    value = int(''.join(filter(str.isdigit, time_string)))
    if "min" in time_string:
        return value * 60
    if "h" in time_string:
        return value * 3600
    if "d" in time_string:
        return value * 86400
    return value

# ---------------- PROGRESS ---------------- #
def get_progress_bar(percent, length=10):
    filled = int(length * percent / 100)
    return '🟩' * filled + '⬜️' * (length - filled)

# ---------------- BROADCAST ---------------- #
async def users_broadcast(user_id, message, is_pin):
    try:
        m = await message.copy(chat_id=user_id)
        if is_pin:
            try:
                await m.pin()
            except:
                pass
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await users_broadcast(user_id, message, is_pin)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        await db.delete_user(user_id)
        return False, "Removed"
    except Exception:
        return False, "Error"

# ---------------- SHORTLINK ---------------- #
async def get_shortlink(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://{SHORTLINK_URL}/api",
                params={"api": SHORTLINK_API, "url": link}
            ) as resp:
                data = await resp.json()
                return data.get("shortenedUrl") or link
    except:
        return link

# ---------------- SHORTZY ---------------- #
async def get_shortlink_av(url):
    try:
        shortzy = Shortzy(SHORTLINK_API, SHORTLINK_URL)
        return await shortzy.convert(url)
    except:
        return url

# ---------------- AUTO DELETE ---------------- #
async def auto_delete_message(message, dlt_msg):
    await asyncio.sleep(600)
    try:
        await dlt_msg.delete()
        await message.delete()
    except:
        pass
# ---------------- RANDOM NAME ---------------- #
import random
import string

def generate_weird_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ---------------- THUMBNAIL ---------------- #
async def generate_thumbnail(file):
    return None
