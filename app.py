import os
import logging
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, LANGUAGES, DONATION_INFO, DOWNLOAD_SETTINGS, RENDER_PORT, WEBHOOK_URL, WEBHOOK_PATH
from video_downloader import VideoDownloader
from database import get_user_language as db_get_user_language, set_user_language as db_set_user_language, db

# Import bot functions
from bot import (
    start, show_language_selection, language_callback, language_command,
    support_command, donate_command, donate_callback, help_command,
    handle_message, broadcast_message
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize video downloader
video_downloader = VideoDownloader()

# Global application instance
application = None

async def health_check(request):
    """Health check endpoint for Render"""
    return web.Response(text="Bot is running!", status=200)

async def webhook_handler(request):
    """Handle incoming webhook requests"""
    if request.match_info.get('token') == BOT_TOKEN.split(':')[1]:
        bot_app = request.app['bot_app']
        update = Update.de_json(await request.json(), bot_app.bot)
        await bot_app.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)

async def set_webhook(bot_app):
    """Set webhook for the bot"""
    if WEBHOOK_URL:
        webhook_url = f"{WEBHOOK_URL}{WEBHOOK_PATH}/{BOT_TOKEN.split(':')[1]}"
        await bot_app.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.warning("WEBHOOK_URL not set, using polling mode")

async def on_startup(app):
    """Initialize bot on startup"""
    global application
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    app['bot_app'] = application

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("support", support_command))
    application.add_handler(CommandHandler("donate", donate_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback query handler for language selection
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    
    # Add callback query handler for donate
    application.add_handler(CallbackQueryHandler(donate_callback, pattern="^donate_"))
    
    # Add message handler for video URLs
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set webhook if WEBHOOK_URL is provided
    if WEBHOOK_URL:
        await set_webhook(application)
    else:
        # Start polling in background
        import threading
        threading.Thread(target=application.run_polling, kwargs={'allowed_updates': Update.ALL_TYPES}, daemon=True).start()
    
    logger.info("Bot started successfully!")

async def on_shutdown(app):
    """Cleanup on shutdown"""
    if application:
        await application.bot.delete_webhook()
        await application.shutdown()
    logger.info("Bot shutdown complete!")

def main():
    """Start the web application for Render"""
    try:
        # Create web application
        app = web.Application()
        
        # Add routes
        app.router.add_get('/', health_check)
        app.router.add_post(f'{WEBHOOK_PATH}/{{token}}', webhook_handler)
        
        # Add startup and shutdown handlers
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        
        # Start the web server
        print("🚀 Bot ishga tushirilmoqda...")
        print("📱 Instagram va TikTok video yuklovchi bot")
        print("🌐 3 tilda qo'llab-quvvatlash: O'zbekcha, Inglizcha, Ruscha")
        print("🌍 Render deployment mode")
        print("=" * 50)
        
        web.run_app(app, host='0.0.0.0', port=RENDER_PORT)
        
    except Exception as e:
        logger.error(f"Bot xatoligi: {e}")
        print(f"❌ Bot xatoligi: {e}")

if __name__ == '__main__':
    main() 