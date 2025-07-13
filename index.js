const TelegramBot = require("node-telegram-bot-api");

// .env ishlatmasdan to'g'ridan-to'g'ri yozamiz:
const token = "8110277054:AAGlsNUWbpYJBKJnseAYuOP5UPGwozkbi1M";

const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, "Assalomu alaykum! Men ishga tushdim 🚀");
});

bot.on("message", (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  if (text !== "/start") {
    bot.sendMessage(chatId, `Siz yozdingiz: ${text}`);
  }
});
