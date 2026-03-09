import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন সংগ্রহ
TOKEN = os.environ.get("BOT_TOKEN")

# আপনার চ্যানেলের ইউজারনেম (এটি পরিবর্তন করতে পারেন)
MY_CHANNEL = "@shibir_online_library" 

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user_name}!\n\n"
        "আমি **PdfBanglaBot**। আমি আপনাকে টেলিগ্রামের যেকোনো বাংলা PDF খুঁজে পেতে সাহায্য করব।\n\n"
        "📖 বইয়ের নাম বা লেখকের নাম লিখে আমাকে মেসেজ দিন।",
        parse_mode="Markdown"
    )

# সার্চ ফাংশন
async def global_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    # সার্চের জন্য টেক্সট ফরম্যাট করা
    encoded_query = urllib.parse.quote(query)
    
    # সার্চ লিঙ্কগুলো তৈরি
    my_library_url = f"https://t.me/s/{MY_CHANNEL[1:]}?q={encoded_query}"
    global_search_url = f"https://t.me/set_language/search?text={encoded_query}"
    google_search_url = f"https://www.google.com/search?q=filetype:pdf+{encoded_query}+bangla"

    # বাটন মেনু তৈরি
    keyboard = [
        [InlineKeyboardButton("📚 আমাদের লাইব্রেরিতে খুঁজুন", url=my_library_url)],
        [InlineKeyboardButton("🌐 পুরো টেলিগ্রামে খুঁজুন", url=global_search_url)],
        [InlineKeyboardButton("🔍 গুগল (PDF) সার্চ", url=google_search_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔎 **'{query}'** এর জন্য নিচের উৎসগুলো চেক করুন:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN variable missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # হ্যান্ডলার যোগ করা
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, global_search))
        
        print("PdfBanglaBot is running successfully...")
        app.run_polling()
