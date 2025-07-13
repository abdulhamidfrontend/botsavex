#!/usr/bin/env python3
"""
Telegram Video Downloader Bot Launcher
Instagram va TikTok videolarini yuklab olish uchun Telegram bot
"""

import sys
import os
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main launcher function"""
    try:
        # Import and run the bot
        from bot import main as run_bot
        print("🚀 Bot ishga tushirilmoqda...")
        print("📱 Instagram va TikTok video yuklovchi bot")
        print("🌐 3 tilda qo'llab-quvvatlash: O'zbekcha, Inglizcha, Ruscha")
        print("=" * 50)
        
        run_bot()
        
    except ImportError as e:
        print(f"❌ Xatolik: Kerakli paketlar o'rnatilmagan: {e}")
        print("💡 Quyidagi buyruqni ishlatib paketlarni o'rnating:")
        print("pip install -r requirements.txt")
        
    except KeyboardInterrupt:
        print("\n👋 Bot to'xtatildi")
        
    except Exception as e:
        print(f"❌ Kutilmagan xatolik: {e}")
        logging.error(f"Bot xatoligi: {e}")

if __name__ == "__main__":
    main() 