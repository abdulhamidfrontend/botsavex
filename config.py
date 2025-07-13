# Bot Configuration
BOT_TOKEN = "8110277054:AAGlsNUWbpYJBKJnseAYuOP5UPGwozkbi1M"
ADMIN_ID = 1982638634

LANGUAGES = {
    'uz': {
        'welcome': '🎉 Xush kelibsiz, {}!\n\n📱 Bu bot Instagram va TikTok videolarini yuklab olish uchun ishlatiladi.\n\n📤 Video havolasini yuboring va men uni sizga yuklab beraman.\n\n💡 Qo\'llash:\n• Instagram video havolasini yuboring\n• TikTok video havolasini yuboring\n• Video avtomatik ravishda yuklab olinadi',
        'language_select': '🌐 Tilni tanlang / Выберите язык / Select language:',
        'language_changed': '✅ Til muvaffaqiyatli o\'zgartirildi!',
        'support_message': '📞 Qo\'llab-quvvatlash xizmati bilan bog\'lanish uchun xabar yozing:',
        'support_sent': '✅ Xabaringiz yuborildi! Tez orada javob beramiz.',
        'donate_message': '💝 Donat qilish:\n\n🌐 Xavola orqali:\nhttps://tirikchilik.uz/frxdvc\n\n💳 Karta raqam orqali:\n4067 0700 0070 9266\nHamidullayev Abdulhamid\n\n4231 2000 7103 8359\nVISA',
        'invalid_url': '❌ Noto\'g\'ri havola! Instagram yoki TikTok havolasini yuboring.',
        'downloading': '⏳ Video yuklanmoqda...',
        'download_error': '❌ Videoni yuklab olishda xatolik yuz berdi.',
        'video_sent': '✅ Video muvaffaqiyatli yuklandi!',
        'help_text': '📋 Mavjud komandalar:\n/start - Botni ishga tushirish\n/language - Tilni o\'zgartirish\n/support - Qo\'llab-quvvatlash\n/donate - Donat qilish\n/help - Yordam'
    },
    'en': {
        'welcome': '🎉 Welcome, {}!\n\n📱 This bot is used to download Instagram and TikTok videos.\n\n📤 Send a video link and I will download it for you.\n\n💡 Usage:\n• Send Instagram video link\n• Send TikTok video link\n• Video will be downloaded automatically',
        'language_select': '🌐 Tilni tanlang / Выберите язык / Select language:',
        'language_changed': '✅ Language changed successfully!',
        'support_message': '📞 Write a message to contact support:',
        'support_sent': '✅ Your message has been sent! We will respond soon.',
        'donate_message': '💝 Donate:\n\n🌐 Via link:\nhttps://tirikchilik.uz/frxdvc\n\n💳 Via card number:\n4067 0700 0070 9266\nHamidullayev Abdulhamid\n\n4231 2000 7103 8359\nVISA',
        'invalid_url': '❌ Invalid link! Please send Instagram or TikTok link.',
        'downloading': '⏳ Downloading video...',
        'download_error': '❌ Error occurred while downloading video.',
        'video_sent': '✅ Video downloaded successfully!',
        'help_text': '📋 Available commands:\n/start - Start the bot\n/language - Change language\n/support - Support\n/donate - Donate\n/help - Help'
    },
    'ru': {
        'welcome': '🎉 Добро пожаловать, {}!\n\n📱 Этот бот используется для скачивания видео из Instagram и TikTok.\n\n📤 Отправьте ссылку на видео, и я скачаю его для вас.\n\n💡 Использование:\n• Отправьте ссылку на видео Instagram\n• Отправьте ссылку на видео TikTok\n• Видео будет скачано автоматически',
        'language_select': '🌐 Tilni tanlang / Выберите язык / Select language:',
        'language_changed': '✅ Язык успешно изменен!',
        'support_message': '📞 Напишите сообщение для связи с поддержкой:',
        'support_sent': '✅ Ваше сообщение отправлено! Мы ответим в ближайшее время.',
        'donate_message': '💝 Пожертвовать:\n\n🌐 По ссылке:\nhttps://tirikchilik.uz/frxdvc\n\n💳 По номеру карты:\n4067 0700 0070 9266\nHamidullayev Abdulhamid\n\n4231 2000 7103 8359\nVISA',
        'invalid_url': '❌ Неверная ссылка! Пожалуйста, отправьте ссылку Instagram или TikTok.',
        'downloading': '⏳ Скачивание видео...',
        'download_error': '❌ Произошла ошибка при скачивании видео.',
        'video_sent': '✅ Видео успешно скачано!',
        'help_text': '📋 Доступные команды:\n/start - Запустить бота\n/language - Изменить язык\n/support - Поддержка\n/donate - Пожертвовать\n/help - Помощь'
    }
}

# Donation information
DONATION_INFO = {
    'link': 'https://tirikchilik.uz/frxdvc',
    'cards': [
        {
            'number': '4067 0700 0070 9266',
            'holder': 'Hamidullayev Abdulhamid'
        },
        {
            'number': '4231 2000 7103 8359',
            'type': 'VISA'
        }
    ]
}

# Video download settings
DOWNLOAD_SETTINGS = {
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'download_timeout': 30,  # seconds
    'temp_folder': 'temp_videos'
} 