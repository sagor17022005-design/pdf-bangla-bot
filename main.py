import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন সংগ্রহ
TOKEN = os.environ.get("BOT_TOKEN")

# আপনার দেওয়া নির্দিষ্ট চ্যানেলগুলোর ইউজারনেম
TARGET_CHANNELS = {
    "বই পাড়া": "BookVillage_BoiPara",
    "ইসলামিক পিডিএফ": "Islamicpdfshomahar",
    "আলোকিত বই": "AlokitoBooks",
    "বুকস বিডি": "BooksBD",
    "বাংলা কিতাব": "banglakitab1"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user_name}!\n\n"
        "আমি **PdfBanglaBot**। আমি আপনার দেওয়া ৫টি বড় লাইব্রেরি থেকে বই খুঁজে দিতে পারি।\n\n"
        "📖 বইয়ের নাম লিখে আমাকে মেসেজ দিন।",
        parse_mode="Markdown"
    )

async def menu_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    # সার্চের জন্য টেক্সট এনকোড করা
    encoded_query = urllib.parse.quote(query)
    
    # বাটন মেনু তৈরি করা
    keyboard = []
    
    # আপনার দেওয়া ৫টি চ্যানেলের জন্য আলাদা সার্চ বাটন
    for name, username in TARGET_CHANNELS.items():
        # এই লিঙ্কটি সরাসরি চ্যানেলের ভেতরে ওই কি-ওয়ার্ড দিয়ে সার্চ করবে
        search_link = f"https://t.me/s/{username}?q={encoded_query}"
        keyboard.append([InlineKeyboardButton(f"🔍 {name}-এ খুঁজুন", url=search_link)])
    
    # একটি কমন গ্লোবাল সার্চ বাটন (পুরো টেলিগ্রামের জন্য)
    keyboard.append([InlineKeyboardButton("🌐 সব চ্যানেলে একবারে খুঁজুন", url=f"tg://search?text={encoded_query}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔎 **'{query}'** এর জন্য মেনু সার্চ রেজাল্ট:\n\n"
        "নিচের যেকোনো লাইব্রেরি বাটনে ক্লিক করলে সরাসরি ওই চ্যানেলের ভেতরে বইটি খুঁজে পাবেন।",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_search))
        
        print("PdfBanglaBot is running with Menu Search...")
        app.run_polling()
