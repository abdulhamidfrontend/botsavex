const express = require("express");
const TelegramBot = require("node-telegram-bot-api");

const app = express();
const port = process.env.PORT || 3000;

// Tokenni bevosita yozamiz (agar .env ishlamayotgan bo‘lsa)
const token = "8110277054:AAGlsNUWbpYJBKJnseAYuOP5UPGwozkbi1M";

// Botni webhook rejimida ishga tushiramiz
const bot = new TelegramBot(token);
bot.setWebHook(`https://<RENDER-APP-NOMI>.onrender.com/bot${token}`);

// Telegram webhookni qabul qiladigan endpoint
app.use(express.json());
app.post(`/bot${token}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// /start komandasi
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "Salom! Webhook orqali ishga tushdim 🚀");
});

// Oddiy matn
bot.on("message", (msg) => {
  if (msg.text !== "/start") {
    bot.sendMessage(msg.chat.id, `Siz yozdingiz: ${msg.text}`);
  }
});

app.listen(port, () => {
  console.log(`Server ishga tushdi: ${port}`);
});
