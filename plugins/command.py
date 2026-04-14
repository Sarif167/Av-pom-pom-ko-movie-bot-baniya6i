# ✅ NEW USER ADD
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
        try:
            await client.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT.format(me2, user_id, mention)
            )
        except Exception:
            pass

    # ❌ BUTTONS REMOVED

    await message.reply_photo(
        photo=START_PIC,
        caption=script.START_TXT.format(mention, temp.U_NAME, temp.U_NAME),
        has_spoiler=True
    )
