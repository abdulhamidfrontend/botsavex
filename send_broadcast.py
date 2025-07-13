import asyncio
import requests
from config import BOT_TOKEN, ADMIN_ID
from database import db

async def send_broadcast():
    """Send broadcast message to all users"""
    broadcast_text = """🎉 Bot yangilandi va ishga tushdi!

📱 Instagram va TikTok videolarini yuklab olish uchun havola yuboring.

🌐 3 tilda qo'llab-quvvatlash:
🇺🇿 O'zbekcha
🇬🇧 English  
🇷🇺 Русский

💡 Komandalar:
/start - Botni ishga tushirish
/language - Tilni o'zgartirish
/support - Qo'llab-quvvatlash
/donate - Donat qilish
/help - Yordam

✅ Endi bot to'liq ishlayapti!"""

    try:
        all_users = db.get_all_users()
        success_count = 0
        error_count = 0
        
        print(f"📢 {len(all_users)} foydalanuvchiga xabar yuborilmoqda...")
        
        for user_id_str in all_users.keys():
            try:
                user_id = int(user_id_str)
                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": user_id,
                        "text": broadcast_text,
                        "parse_mode": "HTML"
                    }
                )
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"✅ {user_id} ga yuborildi")
                else:
                    error_count += 1
                    print(f"❌ {user_id} ga yuborilmadi: {response.status_code}")
                
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                error_count += 1
                print(f"❌ {user_id_str} xatoligi: {e}")
        
        print(f"\n📊 Natija:")
        print(f"✅ Muvaffaqiyat: {success_count}")
        print(f"❌ Xatolik: {error_count}")
        
    except Exception as e:
        print(f"❌ Broadcast xatoligi: {e}")

if __name__ == "__main__":
    asyncio.run(send_broadcast()) 