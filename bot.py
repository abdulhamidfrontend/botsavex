import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, LANGUAGES, DONATION_INFO, DOWNLOAD_SETTINGS
from video_downloader import VideoDownloader
from database import get_user_language as db_get_user_language, set_user_language as db_set_user_language, db

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

video_downloader = VideoDownloader()

def get_user_language(user_id):
    lang = db_get_user_language(user_id)
    if not lang:
        return 'uz'
    return lang

def get_text(user_id, key):
    lang = get_user_language(user_id)
    return LANGUAGES[lang][key]

def get_donate_message(user_id):
    lang = get_user_language(user_id)
    donate_text = LANGUAGES[lang]['donate_message']
    return donate_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_lang = db_get_user_language(user_id)
    if not user_lang:
        user_info = db.get_user_info(user_id)
        if not user_info.get('language_set'):
            await show_language_selection(update, context)
            return
    welcome_text = get_text(user_id, 'welcome').format(user_name)
    await update.message.reply_text(welcome_text)

async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        reply_func = update.message.reply_text
    elif update.callback_query:
        reply_func = update.callback_query.edit_message_text
    else:
        return
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await reply_func(
        "🌐 Tilni tanlang / Выберите язык / Select language:",
        reply_markup=reply_markup
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.callback_query:
        return
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if not query.data:
        return
    lang_code = query.data.split('_')[1]
    db_set_user_language(user_id, lang_code)
    db.set_user_info(user_id, {'language_set': True})
    await query.edit_message_text(get_text(user_id, 'language_changed'))
    user_name = query.from_user.first_name
    welcome_text = get_text(user_id, 'welcome').format(user_name)
    await context.bot.send_message(chat_id=user_id, text=welcome_text)

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_language_selection(update, context)

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    username = update.effective_user.username
    if not username:
        no_username_text = "❌ Support yozish uchun @username bo'lishi kerak!\n\n📝 Username qo'shish uchun:\n1. Telegram sozlamalariga kiring\n2. Username qo'shing\n3. Qaytadan /support buyrug'ini yuboring"
        await update.message.reply_text(no_username_text)
        return
    feedback_text = "💬 Fikringizni qoldiring:\n\nTez orada admin siz bilan bog'lanishadi."
    await update.message.reply_text(feedback_text)
    if context.user_data is None:
        context.user_data = {}
    context.user_data['waiting_for_feedback'] = True

async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    keyboard = [
        [
            InlineKeyboardButton("🌐 Xavola orqali", url="https://tirikchilik.uz/frxdvc"),
            InlineKeyboardButton("💳 Karta raqam", callback_data="donate_card")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    donate_text = "💝 Donat qilish usulini tanlang:"
    await update.message.reply_text(donate_text, reply_markup=reply_markup)

async def donate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.callback_query:
        return
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "donate_card":
        card_text = """💳 Karta raqamlar orqali donat qilish:

🏦 4067 0700 0070 9266
👤 Hamidullayev Abdulhamid

💳 4231 2000 7103 8359
🏦 VISA"""
        await query.edit_message_text(card_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    help_text = get_text(user_id, 'help_text')
    await update.message.reply_text(help_text)

def is_valid_video_url(url):
    return video_downloader.is_valid_url(url)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    url = update.message.text
    if not url:
        download_error_text = get_text(user_id, 'download_error')
        await update.message.reply_text(download_error_text)
        return
    if 'tiktok.com' in url.lower() or 'vt.tiktok.com' in url.lower():
        tiktok_message = "⚠️ TikTok video yuklash funksiyasi hozircha mavjud emas.\n\n🔧 Texnik ishlar olib borilmoqda...\n\n✅ Instagram videolarini yuklash mumkin!"
        await update.message.reply_text(tiktok_message)
        return
    downloading_text = get_text(user_id, 'downloading')
    status_message = await update.message.reply_text(downloading_text)
    try:
        video_url = video_downloader.get_video_url(url)
        temp_dir = DOWNLOAD_SETTINGS['temp_folder']
        if os.getenv("RENDER"):
            temp_dir = "/tmp"
        else:
            os.makedirs(temp_dir, exist_ok=True)
        import uuid
        filename = os.path.join(temp_dir, f"video_{uuid.uuid4().hex[:8]}.mp4")
        if video_url:
            downloaded_file = video_downloader.download_video(video_url, filename)
            if downloaded_file and os.path.exists(downloaded_file):
                file_size = os.path.getsize(downloaded_file)
                if file_size > DOWNLOAD_SETTINGS['max_file_size']:
                    os.remove(downloaded_file)
                    download_error_text = get_text(user_id, 'download_error')
                    await status_message.edit_text(download_error_text)
                    return
                if not update.effective_chat:
                    return
                with open(downloaded_file, 'rb') as video_file:
                    await context.bot.send_video(
                        chat_id=update.effective_chat.id,
                        video=video_file,
                        caption="✅ Video @savexdownloadbot orqali yuklandi!"
                    )
                os.remove(downloaded_file)
                video_sent_text = get_text(user_id, 'video_sent')
                await status_message.edit_text(video_sent_text)
                return
        download_error_text = get_text(user_id, 'download_error')
        await status_message.edit_text(download_error_text)
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        download_error_text = get_text(user_id, 'download_error')
        await status_message.edit_text(download_error_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    message_text = update.message.text
    # Komanda bo‘lsa, qaytib ket
    if message_text and message_text.startswith('/'):
        return
    user_id = update.effective_user.id
    user_lang = db_get_user_language(user_id)
    if not user_lang:
        user_info = db.get_user_info(user_id)
        if not user_info.get('language_set'):
            await show_language_selection(update, context)
            return
    if not message_text:
        return
    if context.user_data is None:
        context.user_data = {}
    if context.user_data.get('waiting_for_feedback'):
        thank_you_text = "✅ Fikringiz uchun raxmat!\n\nAdmin tez orada siz bilan bog'lanadi."
        await update.message.reply_text(thank_you_text)
        user_name = update.effective_user.first_name
        username = update.effective_user.username
        admin_message = f"📞 Yangi foydalanuvchi fikri:\n\n👤 Foydalanuvchi: {user_name}\n🆔 ID: {user_id}\n👤 Username: @{username if username else 'Yo\'q'}\n💬 Fikr: {message_text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
        context.user_data['waiting_for_feedback'] = False
        return
    if is_valid_video_url(message_text):
        await download_video(update, context)
    else:
        if any(word in message_text.lower() for word in ["support", "yordam", "помощь", "help"]):
            confirmation_text = "✅ Xabaringiz yuborildi! Tez orada javob beramiz."
            await update.message.reply_text(confirmation_text)
            user_name = update.effective_user.first_name
            username = update.effective_user.username
            admin_message = f"📞 Yangi qo'llab-quvvatlash so'rovi:\n\n👤 Foydalanuvchi: {user_name}\n🆔 ID: {user_id}\n👤 Username: @{username if username else 'Yo\'q'}\n💬 Xabar: {message_text}"
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
        else:
            invalid_url_text = get_text(user_id, 'invalid_url')
            await update.message.reply_text(invalid_url_text)

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("language", language_command))
        application.add_handler(CommandHandler("support", support_command))
        application.add_handler(CommandHandler("donate", donate_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(donate_callback, pattern="^donate_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("🚀 Bot ishga tushirilmoqda...")
        print("✅ Bot ishga tushdi!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Bot xatoligi: {e}")
        print(f"❌ Bot xatoligi: {e}")

if __name__ == '__main__':
    main() 