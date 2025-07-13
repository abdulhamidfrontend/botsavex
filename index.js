const express = require("express");
const TelegramBot = require("node-telegram-bot-api");

const app = express();
const port = process.env.PORT || 3000;

// Token
const token = "8110277054:AAGlsNUWbpYJBKJnseAYuOP5UPGwozkbi1M";
const WEBHOOK_URL = `https://botsavex.onrender.com`; // ✅ ortiqcha slash yo‘q

const bot = new TelegramBot(token);
bot.setWebHook(`${WEBHOOK_URL}/bot${token}`);

app.use(express.json());
app.post(`/bot${token}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "Salom! Webhook orqali ishga tushdim 🚀");
});

bot.on("message", (msg) => {
  if (msg.text !== "/start") {
    bot.sendMessage(msg.chat.id, `Siz yozdingiz: ${msg.text}`);
  }
});

app.listen(port, () => {
  console.log(`✅ Server ishga tushdi: ${port}`);
});
