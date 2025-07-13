require('dotenv').config(); // .env fayldan token olish uchun
const TelegramBot = require('node-telegram-bot-api');

// .env fayldagi tokenni olamiz
const token = process.env.BOT_TOKEN;

// Botni polling rejimida ishga tushiramiz
const bot = new TelegramBot(token, { polling: true });

// /start komandasi ishlaganda javob beradi
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Assalomu alaykum! Men ishga tushdim 🚀');
});

// Oddiy matn yozilsa, uni qaytaradi
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  if (text !== '/start') {
    bot.sendMessage(chatId, `Siz yozdingiz: ${text}`);
  }
});
