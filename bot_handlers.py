# This file contains the event handlers and command functions for the bot
# Import this file in the main bot.py

@bot.event
async def on_ready():
    print(f"{bot.user.username} готов")
    load_data()

@bot.event
async def on_message(message: Message):
    try:
        if message.author.is_bot: return
        chat_id, user_id, text = message.chat.id, message.author.user_id, message.content or ""
        generate_daily_missions(chat_id)
        await handle_points_and_exp(message, chat_id, user_id)
        if text.startswith("/"): await handle_command(message, text.lower(), chat_id, user_id)
    except Exception as e:
        print(f"Error: {e}")

async def handle_points_and_exp(message, chat_id, user_id):
    try:
        user_data, chat_data = get_global_user_data(user_id), get_chat_data(chat_id)
        current_time = time.time()
        if current_time - user_data["last_message_time"] >= COOLDOWN_MINUTES * 60:
            user_data["points"] += BASE_POINTS_PER_MESSAGE
            user_data["experience"] += EXP_PER_MESSAGE
            user_data["last_message_time"] = current_time
            user_data["total_messages"] += 1
            new_level = check_level_up(user_data)
            if new_level:
                bonus = new_level * 400000  # Reduced from 5M to 400K per level
                user_data["points"] += bonus
                await message.reply(f"🎉 سطح {new_level}! جایزه: ${bonus:,} دلار")
            completed = check_mission_progress(user_data, chat_data, "messages", 1, user_id)
            if user_data["alliance"]:
                completed.extend(check_mission_progress(user_data, chat_data, "alliance_messages", 1, user_id))
            if completed: await message.reply(f"🏆 ماموریت: {', '.join(completed)}")
            save_data()
    except Exception as e:
        print(f"Error points: {e}")

async def handle_command(message, command, chat_id, user_id):
    try:
        if command == "/start":
            await message.reply("🤖 ربات فعال!\n\n🌍 **برای شروع بازی ابتدا کشور خود را انتخاب کنید:**\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور\n\n📚 **راهنما:**\n/help - راهنمای کامل\n/game_help - راهنمای بازی\n\n🌍 **سیستم جهانی**: تمام پیشرفت‌ها، خریدها و تحقیقات شما در تمام گروه‌ها قابل دسترسی است!")
        elif command == "/help": await show_help(message)
        elif command == "/rules": await show_rules(message, chat_id)
        elif command == "/info": await user_info(message, chat_id, user_id)
        elif command == "/game_help": await game_help(message)
        elif command == "/points": await show_points(message, chat_id, user_id)
        elif command == "/military": await show_military(message, chat_id, user_id)
        elif command == "/tech": await show_tech_tree(message, chat_id, user_id)
        elif command.startswith("/research"): await research_technology(message, chat_id, user_id)
        elif command.startswith("/buy"): await buy_asset(message, chat_id, user_id)
        elif command.startswith("/attack"): await attack_user(message, chat_id, user_id)
        elif command == "/missions": await show_daily_missions(message, chat_id, user_id)
        elif command == "/leaderboard": await show_leaderboard(message, chat_id)
        elif command == "/assets": await show_all_assets(message, chat_id, user_id)
        elif command == "/global": await show_global_stats(message, user_id)
        elif command.startswith("/alliance"): await handle_alliance_command(message, chat_id, user_id)
        elif command == "/countries": await show_available_countries(message)
        elif command.startswith("/select_country"): await select_country(message, chat_id, user_id)
        elif command == "/income": await collect_income(message, chat_id, user_id)
        elif command == "/economy": await show_economy_info(message, chat_id, user_id)
        elif command.startswith("/setowner") and await is_creator(user_id, chat_id): await set_owner(message, chat_id)
        elif command.startswith("/mute") and await is_owner_or_admin(user_id, chat_id): await mute_user(message, chat_id)
        elif command.startswith("/unmute") and await is_owner_or_admin(user_id, chat_id): await unmute_user(message, chat_id)
        elif command.startswith("/ban") and await is_owner_or_admin(user_id, chat_id): await ban_user(message, chat_id)
        elif command.startswith("/warn") and await is_owner_or_admin(user_id, chat_id): await warn_user(message, chat_id)
        elif command.startswith("/setrules") and await is_owner_or_admin(user_id, chat_id): await set_rules(message, chat_id)
        elif command.startswith("/setwelcome") and await is_owner_or_admin(user_id, chat_id): await set_welcome(message, chat_id)
        else: await message.reply("🚫 دستور نامعتبر!")
    except Exception as e:
        print(f"Command error: {e}")

async def is_creator(user_id, chat_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status == "creator"
    except: return False

async def is_owner_or_admin(user_id, chat_id):
    chat_data = get_chat_data(chat_id)
    return chat_data["owner_id"] == user_id or user_id in chat_data["admins"] or await is_creator(user_id, chat_id)

async def show_help(message):
    await message.reply("🤖 راهنما:\n🌍 کشور و اقتصاد:\n/countries - مشاهده کشورهای موجود\n/select_country [کد] - انتخاب کشور\n/income - جمع‌آوری درآمد\n/economy - اطلاعات اقتصادی\n\n🎮 بازی:\n/game_help - راهنمای بازی\n/points - امتیاز\n/military - ارتش\n/assets - کاتالوگ تجهیزات\n/tech - فناوری\n/missions - ماموریت\n/attack - حمله\n/alliance_* - اتحاد\n/global - آمار جهانی")

async def show_rules(message, chat_id):
    chat_data = get_chat_data(chat_id)
    await message.reply(f"📜 قوانین:\n{chat_data['rules']}")

async def user_info(message, chat_id, user_id):
    try:
        user = message.author
        user_data = get_global_user_data(user_id)
        level = user_data.get("level", 1)
        next_exp = LEVEL_REQUIREMENTS[level] if level < len(LEVEL_REQUIREMENTS) else "MAX"
        current_exp = LEVEL_REQUIREMENTS[level-1] if level > 1 else 0
        progress = user_data["experience"] - current_exp
        alliance_info = f"🤝 اتحاد: {user_data['alliance']}\n" if user_data["alliance"] else ""
        
        # Country information
        if user_data.get("country_selected", False):
            country_code = user_data["country"]
            country_data = AVAILABLE_COUNTRIES[country_code]
            country_info = f"🏛️ کشور: {country_data['name']}\n"
        else:
            country_info = "🏛️ کشور: انتخاب نشده\n"
        
        await message.reply(f"👤 {user.first_name}\nآیدی: {user.user_id}\n{country_info}{alliance_info}"
                          f"💰 بودجه: ${user_data['points']:,}\n⭐ سطح: {level}\n"
                          f"📊 تجربه: {progress}/{next_exp}\n💪 قدرت: {calculate_total_power(user_data)}")
    except Exception as e:
        print(f"Info error: {e}")

async def game_help(message):
    await message.reply("🎮 راهنمای بازی:\n\n🌍 **ابتدا کشور انتخاب کنید:**\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور\n\n💰 **اقتصاد و درآمد:**\n/income - جمع‌آوری درآمد (هر ساعت)\n/economy - اطلاعات اقتصادی کشور\n\n🎯 **بازی اصلی:**\n/buy [نوع] [تعداد] - خرید تجهیزات\n/research [فناوری] - تحقیق فناوری\n/attack [ریپلای] - حمله به کاربران\n/missions - ماموریت روزانه\n/tech - درخت فناوری\n/military - نیروی نظامی\n/leaderboard - رتبه بندی\n\n🌍 **سیستم جهانی**: تمام پیشرفت‌ها، خریدها و تحقیقات شما در تمام گروه‌ها قابل دسترسی است!\n\n⏰ **زمان بندی پیشرفت**: با تنظیمات جدید، رسیدن به اهداف بالا حدود ۱۳-۱۵ روز زمان می‌برد.")

# -------------------- RUN BOT --------------------
if __name__ == "__main__":
    print("🚀 Starting bot...")
    load_data()
    bot.run()