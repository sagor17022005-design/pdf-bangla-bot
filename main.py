import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম!\nআমি **PdfBanglaBot**।\nবইয়ের নাম লিখে মেসেজ দিন, আমি সব বড় লাইব্রেরি থেকে একবারে খুঁজে দেব।"
    )

async def multi_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if len(query) < 2:
        await update.message.reply_text("বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    encoded_query = urllib.parse.quote(query)
    
    # সবগুলো চ্যানেলকে একটি স্পেশাল লিঙ্কে যুক্ত করা (টেলিগ্রাম গ্লোবাল সার্চ কমান্ড)
    # এটি ইউজারের জন্য সবচেয়ে সহজ পদ্ধতি
    combined_search_url = f"tg://search?text={encoded_query}"

    keyboard = [
        [InlineKeyboardButton("🚀 সব চ্যানেলে একবারে খুঁজুন", url=combined_search_url)],
        [InlineKeyboardButton("🔍 গুগল (PDF) সরাসরি খুঁজুন", url=f"https://www.google.com/search?q=filetype:pdf+{encoded_query}+bangla")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔎 **'{query}'** বইটি সব লাইব্রেরিতে খুঁজতে নিচের বাটনে চাপ দিন।\n\n"
        "*(বাটনে চাপ দেওয়ার পর ওপরের 'Global Search' বা 'Files' ট্যাবটি দেখুন)*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, multi_search))
    app.run_polling()
