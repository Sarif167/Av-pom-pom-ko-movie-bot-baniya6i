import asyncio
from datetime import datetime
from pyrogram import Client
from database.users_db import db


async def premium_expiry_checker(bot: Client):
    while True:
        try:
            users = await db.get_all_users()

            for user in users:
                user_id = user.get("user_id")

                # check premium
                if user.get("premium") and user.get("expiry_date"):

                    expiry = user.get("expiry_date")

                    # agar string me hai to convert karo
                    if isinstance(expiry, str):
                        expiry = datetime.fromisoformat(expiry)

                    # expired check
                    if datetime.now() > expiry:

                        # DB update
                        await db.update_user(user_id, {
                            "premium": False,
                            "expiry_date": None
                        })

                        # message send
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

        except Exception as e:
            print(f"Premium Checker Error: {e}")

        await asyncio.sleep(60)  # 1 min loop
