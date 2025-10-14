# 🎮 Discord Tools for Letta

A comprehensive collection of Discord integration tools for Letta AI agents.

## 📋 Available Tools

### 📨 Messaging Tools
- **`send_discord_message`** - Send messages to Discord channels or DMs
- **`read_discord_dms`** - Read direct messages from Discord
- **`read_discord_channel`** - Read messages from Discord channels

### ⏰ Scheduling Tools  
- **`create_scheduled_task`** - Create recurring or one-time tasks
- **`delete_scheduled_task`** - Delete existing scheduled tasks
- **`list_scheduled_tasks`** - List all scheduled tasks

### 📁 File Management
- **`download_discord_file`** - Download files from Discord messages

### 🏷️ Channel Management
- **`list_discord_channels`** - List all channels in a Discord server

### 🎭 Identity/Omnipresence
- **`set_omnipresence_image`** - Set custom status images for Discord

---

## 🚀 Quick Start

### 1. Setup Discord Bot

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Enable these permissions:
   - Send Messages
   - Read Message History
   - Attach Files
   - Use External Emojis
   - Add Reactions

### 2. Get Channel/User IDs

Enable Developer Mode in Discord:
1. User Settings → Advanced → Developer Mode
2. Right-click on channels/users → "Copy ID"

### 3. Configure Tools

Edit the `.py` files and replace placeholders:

```python
# Replace these with your actual values:
DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
TASKS_CHANNEL_ID = "YOUR_TASKS_CHANNEL_ID_HERE" 
DEFAULT_USER_ID = "YOUR_DISCORD_USER_ID_HERE"
```

### 4. Upload to Letta

Use the management tools to upload:

```bash
cd ../management_tools
python push-tool.py send_discord_message
python manage-agent-tools.py attach send_discord_message
```

---

## 📖 Tool Categories

### 📨 Messaging (`messaging/`)

**send_discord_message**
- Send messages to channels or DMs
- Supports @mentions, embeds, file attachments
- Auto-formats messages nicely

**read_discord_dms** 
- Read recent DMs from the bot
- Filter by user, time range, keywords
- Returns formatted message history

**read_discord_channel**
- Read messages from any channel
- Time filtering (last X hours/days)
- Timezone conversion support

### ⏰ Scheduling (`scheduling/`)

**create_scheduled_task**
- Flexible scheduling: daily, weekly, monthly, yearly
- One-time tasks with specific dates
- Custom intervals (every X minutes/hours/days)
- Action types: user reminders, channel posts

**delete_scheduled_task**
- Remove tasks by message ID
- Clean up old or unwanted tasks

**list_scheduled_tasks**
- View all active tasks
- Nice formatting with next run times
- Task statistics and details

### 📁 File Management (`file_management/`)

**download_discord_file**
- Download any file from Discord
- Supports images, documents, videos
- Automatic file type detection
- Local storage with organized naming

### 🏷️ Channel Management (`channel_management/`)

**list_discord_channels**
- Get all channels in a server
- Filter by channel type (text, voice, etc.)
- Channel permissions and settings

### 🎭 Identity (`omnipresence/`)

**set_omnipresence_image**
- Set custom status images
- Dynamic image updates
- Branding and personalization

---

## 🔧 Configuration

### Required Environment Variables

Create a `.env` file:

```env
# Discord Bot
DISCORD_BOT_TOKEN=your_bot_token_here
TASKS_CHANNEL_ID=your_tasks_channel_id
DEFAULT_USER_ID=your_discord_user_id

# Letta API  
LETTA_API_KEY=your_letta_api_key
LETTA_AGENT_ID=your_agent_id
```

### Bot Permissions

Your Discord bot needs these permissions:
- **Send Messages** - Post in channels
- **Read Message History** - Read past messages  
- **Attach Files** - Upload/download files
- **Use External Emojis** - Rich formatting
- **Add Reactions** - Interactive features
- **Manage Messages** - Delete/edit messages (for tasks)

---

## 🎯 Usage Examples

### Send a Message
```python
send_discord_message(
    channel_id="1234567890",
    message="Hello @everyone! 👋",
    mention_users=["1234567890"]
)
```

### Create a Daily Reminder
```python
create_scheduled_task(
    task_name="daily_standup",
    description="Daily team standup reminder", 
    schedule="daily",
    time="09:00",
    action_type="channel_post",
    action_target="1234567890",
    action_template="📅 Daily standup in 15 minutes!"
)
```

### Read Recent Messages
```python
read_discord_channel(
    channel_id="1234567890",
    limit=50,
    time_filter="last_24_hours"
)
```

---

## 🔒 Security Notes

- **Never commit real tokens** to version control
- Use `.gitignore` to protect credentials
- Rotate bot tokens regularly
- Limit bot permissions to minimum required
- Monitor bot activity for unusual behavior

---

## 🐛 Troubleshooting

### "Unauthorized" Error
- Check bot token is correct
- Verify bot has proper permissions
- Ensure bot is invited to the server

### "Channel not found"
- Verify channel ID is correct
- Check bot has access to the channel
- Enable Developer Mode to get correct IDs

### "Rate limited"
- Discord has rate limits on API calls
- Add delays between requests if needed
- Use exponential backoff for retries

---

## 📚 Further Reading

- [Discord API Documentation](https://discord.com/developers/docs)
- [Discord Bot Permissions](https://discord.com/developers/docs/topics/permissions)
- [Letta API Reference](../management_tools/README.md)

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-10-14
