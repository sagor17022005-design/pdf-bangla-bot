import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Variable setup
TOKEN = os.environ.get("BOT_TOKEN")
# আপনার নিজের চ্যানেলের ইউজারনেম (এটি সঠিক থাকলে হাত দেওয়ার প্রয়োজন নেই)
MY_CHANNEL = "@shibir_online_library" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user_name}!\n\n"
        "আমি **PdfBanglaBot**। আমি আপনাকে টেলিগ্রাম ও ইন্টারনেটের যেকোনো বাংলা PDF খুঁজে পেতে সাহায্য করব।\n\n"
        "📖 বইয়ের নাম বা লেখকের নাম লিখে আমাকে মেসেজ দিন।",
        parse_mode="Markdown"
    )

async def global_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    # সার্চের জন্য টেক্সট ফরম্যাট করা
    encoded_query = urllib.parse.quote(query)
    
    # সংশোধিত সার্চ লিঙ্কগুলো (Error Fix)
    # ১. আপনার চ্যানেলের লিঙ্ক
    my_library_url = f"https://t.me/s/{MY_CHANNEL[1:]}?q={encoded_query}"
    
    # ২. পুরো টেলিগ্রামে গ্লোবাল সার্চ (এটি সরাসরি অ্যাপের সার্চ অপশন খুলে দেবে)
    global_search_url = f"tg://search?text={encoded_query}"
    
    # ৩. গুগল স্পেশাল পিডিএফ সার্চ
    google_search_url = f"https://www.google.com/search?q=filetype:pdf+{encoded_query}+bangla"

    # বাটন মেনু
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
        print("Error: BOT_TOKEN missing in Variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, global_search))
        
        print("PdfBanglaBot is updated and running...")
        app.run_polling()
