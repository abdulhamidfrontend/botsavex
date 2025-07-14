# Render Deployment Guide

## Bot Configuration for Render

This bot has been configured to run on Render as a web service with webhook support.

### Environment Variables

Set these environment variables in your Render dashboard:

1. **BOT_TOKEN** - Your Telegram bot token from @BotFather
2. **ADMIN_ID** - Your Telegram user ID (for admin notifications)
3. **WEBHOOK_URL** - Your Render app URL (e.g., https://your-app-name.onrender.com)
4. **PORT** - Port number (usually 8080, set automatically by Render)
5. **RENDER** - Set to any value to enable Render mode

### Deployment Steps

1. **Connect your GitHub repository to Render**

   - Go to Render dashboard
   - Click "New Web Service"
   - Connect your GitHub repository

2. **Configure the service**

   - **Name**: Your bot name
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (or paid if needed)

3. **Set Environment Variables**

   - Add all the environment variables listed above
   - Make sure to use your actual bot token and admin ID

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete
   - Your bot will be available at your Render URL

### Features

- ✅ Webhook support for real-time updates
- ✅ Health check endpoint at `/`
- ✅ Automatic webhook setup
- ✅ Temporary file handling for Render
- ✅ Database persistence in `/tmp` directory
- ✅ Multi-language support (Uzbek, English, Russian)

### Monitoring

- Check the logs in Render dashboard
- Health check: Visit your app URL to see "Bot is running!"
- Webhook endpoint: `/webhook/{token}`

### Troubleshooting

1. **Bot not responding**: Check if webhook is set correctly
2. **File download errors**: Check `/tmp` directory permissions
3. **Database issues**: Ensure `/tmp` directory is writable

### Local Development

For local development, use:

```bash
python bot.py
```

For Render deployment, use:

```bash
python app.py
```

The bot will automatically detect the environment and use appropriate settings.
