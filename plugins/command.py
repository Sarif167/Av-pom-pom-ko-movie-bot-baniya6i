from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_db import db
from Script import script
from info import LOG_CHANNEL, START_PIC
from utils import temp

# ================================
# 🚀 START COMMAND
# ================================
@Client.on_message(filters.private & filters.command("start"))
async def start_cmd(client: Client, message: Message):

    user_id = message.from_user.id
    mention = message.from_user.mention

    # ✅ NEW USER ADD
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
        try:
            await client.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT.format(mention, user_id, mention)
            )
        except Exception:
            pass

    # ❌ BUTTONS REMOVED (no reply_markup)

    await message.reply_photo(
        photo=START_PIC,
        caption=script.START_TXT.format(mention, temp.U_NAME, temp.U_NAME),
        has_spoiler=True
    )
