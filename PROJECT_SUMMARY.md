# Telegram Video Downloader Bot - Project Summary

## 📁 Fayl tuzilishi / File Structure

### Asosiy fayllar / Main Files:

- `bot.py` - Asosiy bot fayli, barcha funksiyalar va komandalar
- `config.py` - Bot sozlamalari, tillar va konfiguratsiya
- `video_downloader.py` - Instagram va TikTok videolarini yuklab olish moduli
- `database.py` - Foydalanuvchi ma'lumotlarini saqlash uchun oddiy ma'lumotlar bazasi
- `run_bot.py` - Botni ishga tushirish uchun launcher script

### Qo'shimcha fayllar / Additional Files:

- `requirements.txt` - Kerakli Python paketlari
- `README.md` - To'liq hujjatlar va o'rnatish ko'rsatmalari
- `PROJECT_SUMMARY.md` - Bu fayl (loyiha tuzilishi haqida ma'lumot)

## 🚀 Bot funksiyalari / Bot Features

### ✅ Amalga oshirilgan funksiyalar:

1. **3 tilda qo'llab-quvvatlash** (O'zbekcha, Inglizcha, Ruscha)
2. **Til tanlash** - Birinchi marta botni ishlatganda til tanlash
3. **Video yuklab olish** - Instagram va TikTok videolarini yuklab olish
4. **Qo'llab-quvvatlash** - Admin bilan bog'lanish
5. **Donat qilish** - Xavola va karta raqam orqali
6. **Yordam** - Barcha komandalar haqida ma'lumot

### 🎯 Bot komandalari:

- `/start` - Botni ishga tushirish
- `/language` - Tilni o'zgartirish
- `/support` - Qo'llab-quvvatlash
- `/donate` - Donat qilish
- `/help` - Yordam

## 🔧 Texnik ma'lumotlar / Technical Details

### Bot token:

```
8110277054:AAGlsNUWbpYJBKJnseAYuOP5UPGwozkbi1M
```

### Admin ID:

```
1982638634
```

### Donat ma'lumotlari:

- **Xavola:** https://tirikchilik.uz/frxdvc
- **Karta 1:** 4067 0700 0070 9266 (Hamidullayev Abdulhamid)
- **Karta 2:** 4231 2000 7103 8359 (VISA)

## 📦 O'rnatish / Installation

### 1. Paketlarni o'rnatish:

```bash
pip install -r requirements.txt
```

### 2. Botni ishga tushirish:

```bash
python run_bot.py
```

yoki

```bash
python bot.py
```

## 🛠️ Loyihani rivojlantirish / Development

### Yangi funksiyalar qo'shish uchun:

1. `config.py` da yangi til matnlarini qo'shing
2. `bot.py` da yangi komandalar qo'shing
3. `video_downloader.py` da yangi platformalar qo'shing

### Ma'lumotlar bazasini o'zgartirish:

- `database.py` faylini tahrirlang
- JSON fayl o'rniga PostgreSQL yoki SQLite ishlatish mumkin

## 🔒 Xavfsizlik / Security

### Hozirgi cheklovlar:

- Faqat Instagram va TikTok havolalari qabul qilinadi
- Maksimal fayl hajmi: 50MB
- Yuklab olish vaqti: 30 soniya

### Tavsiya etilgan yaxshilanishlar:

- Rate limiting qo'shish
- Spam filtri
- Video sifatini tanlash imkoniyati
- Ko'proq platformalar qo'llab-quvvatlash

## 📊 Statistika / Statistics

Bot quyidagi ma'lumotlarni saqlaydi:

- Foydalanuvchi ID si
- Tanlangan til
- Foydalanish vaqti
- Yuklab olingan videolar soni

## 🐛 Xatoliklarni tuzatish / Troubleshooting

### Keng tarqalgan muammolar:

1. **Import xatoligi** - `pip install -r requirements.txt` ishlatish
2. **Bot ishlamaydi** - Token to'g'ri ekanligini tekshirish
3. **Video yuklanmaydi** - Internet aloqasini tekshirish

### Log fayllari:

- Bot xatoliklari console da ko'rsatiladi
- `user_data.json` faylida foydalanuvchi ma'lumotlari saqlanadi

## 📞 Qo'llab-quvvatlash / Support

Muammolar yoki savollar bo'lsa:

1. `/support` komandasi orqali admin bilan bog'laning
2. GitHub da issue oching
3. Telegram da admin bilan bog'laning

---

**Eslatma:** Bu bot faqat o'quv maqsadlarida yaratilgan. Foydalanishda qonuniy cheklovlarni hisobga oling.
