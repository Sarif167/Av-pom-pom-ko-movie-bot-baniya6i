import asyncio
from datetime import datetime, timedelta
from pyrogram import Client
from database.users_db import db


async def premium_expiry_checker(bot: Client):
    while True:
        try:
            users = await db.get_all_users()

            for user in users:
                user_id = user.get("user_id")

                # check if premium active and expiry exists
                if user.get("premium") and user.get("expiry_date"):

                    expiry = user.get("expiry_date")

                    # convert string to datetime if needed
                    if isinstance(expiry, str):
                        expiry = datetime.fromisoformat(expiry)

                    # check expired
                    if datetime.now() > expiry:

                        notify_count = user.get("notify_count", 0)
                        last_notify = user.get("last_notify")

                        if last_notify:
                            try:
                                last_notify = datetime.fromisoformat(last_notify)
                            except:
                                last_notify = None

                        # send max 4 times with 30 min gap
                        if notify_count < 4:
                            if (not last_notify) or (datetime.now() - last_notify >= timedelta(minutes=30)):

                                try:
                                    await bot.send_message(
                                        chat_id=user_id,
                                        text=(
                                            "⚠️ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗘𝗫𝗣𝗜𝗥𝗘𝗗!\n\n"
                                            "Hey 👋\n"
                                            "Aapka premium plan ab expire ho gaya hai ❌\n\n"
                                            "💎 Dubara premium lene ke liye:\n"
                                            "👉 /buy command use karo\n\n"
                                            "⚡ Upgrade karo aur unlimited access pao!"
                                        )
                                    )
                                except:
                                    pass

                                # update db
                                try:
                                    await db.update_user(user_id, {
                                        "notify_count": notify_count + 1,
                                        "last_notify": datetime.now().isoformat()
                                    })
                                except:
                                    pass

        except Exception as e:
            print(f"Premium Checker Error: {e}")

        await asyncio.sleep(60)  # check every 1 min
