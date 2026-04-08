import asyncio
import logging
import random
import string
import pytz
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from info import (
    VERIFIED_LOG, TIMEZONE, VERIFY_IMG,
    TUTORIAL_LINK, IS_VERIFY
)
from database.users_db import db
from utils import temp, get_shortlink_av, auto_delete_message
from Script import script

logger = logging.getLogger(__name__)

# --- MAIN VERIFICATION CHECKER ---
async def av_x_verification(client, message):
    user_id = message.from_user.id

    # ✅ PREMIUM BYPASS
    if await db.has_premium_access(user_id):
        return True

    # 1. Check if Verification ON hai ya OFF
    if not IS_VERIFY:
        return True

    # 2. Check last verified time (24h system)
    user_data = await db.get_user(user_id)
    last_verified = user_data.get("last_verified") if user_data else None

    if last_verified:
        ist = pytz.timezone(TIMEZONE)
        now = datetime.now(ist)

        # Agar 24 ghante ke andar verify kiya hai → skip
        if (now - last_verified) < timedelta(hours=24):
            return True

    # 3. Already verified flag (backup check)
    user_verified = await db.is_user_verified(user_id)
    if user_verified:
        return True

    # ------------------------------------------------
    # GENERATE VERIFY LINK
    # ------------------------------------------------
    file_id = None
    if message.command and len(message.command) > 1:
        file_id = message.command[1]

    verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    await db.create_verify_id(user_id, verify_id, file_id)

    long_url = f"https://telegram.me/{temp.U_NAME}?start=avbotz_{user_id}_{verify_id}"
    verify_url = await get_shortlink_av(long_url)

    buttons = [[
        InlineKeyboardButton(text="⚠️ ᴠᴇʀɪғʏ ⚠️", url=verify_url),
        InlineKeyboardButton(text="❗ ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ ❗", url=TUTORIAL_LINK)
    ]]

    user_name = message.from_user.first_name

    try:
        bin_text = script.VERIFICATION_TEXT.format(user_name, "1/1")
    except:
        bin_text = script.VERIFICATION_TEXT.format(user_name)

    dlt = await message.reply_text(
        text=bin_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

    asyncio.create_task(auto_delete_message(message, dlt))
    return False


# --- VERIFICATION SUCCESS HANDLER ---
async def verify_user_on_start(client, message):
    try:
        if not message.command or len(message.command) < 2:
            return False

        data = message.command[1].split("_")
        if len(data) < 3:
            return False

        user_id = int(data[1])
        verify_id = data[2]

        if message.from_user.id != user_id:
            await message.reply("<b>This link is not for you!</b>")
            return True

        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("<b>Lɪɴᴋ Exᴘɪʀᴇᴅ ᴏʀ Aʟʀᴇᴀᴅʏ Usᴇᴅ... Tʀʏ Aɢᴀɪɴ.</b>")
            return True

        ist = pytz.timezone(TIMEZONE)
        current_time = datetime.now(tz=ist)

        # ✅ Update verification time (IMPORTANT FIX)
        await db.update_notcopy_user(user_id, {"last_verified": current_time})
        await db.update_verify_id_info(user_id, verify_id, {"verified": True})

        stored_file_id = verify_id_info.get("file_id")
        if stored_file_id:
            file_link = f"https://t.me/{temp.U_NAME}?start={stored_file_id}"
        else:
            file_link = f"https://t.me/{temp.U_NAME}?start=help"

        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("📂 ɢᴇᴛ ʀᴇǫᴜᴇsᴛᴇᴅ ғɪʟᴇ 📂", url=file_link)
        ]])

        txt = script.VERIFY_COMPLETE_TEXT

        if VERIFIED_LOG:
            try:
                await client.send_message(
                    VERIFIED_LOG,
                    script.VERIFIED_TXT.format(
                        message.from_user.mention,
                        user_id,
                        datetime.now(ist).strftime('%d_%B_%Y'),
                        "1"
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to send log: {e}")

        await message.reply_photo(
            photo=VERIFY_IMG,
            caption=txt.format(message.from_user.mention),
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )
        return True

    except Exception as e:
        logger.error(f"Verify Error: {e}")
        return False
