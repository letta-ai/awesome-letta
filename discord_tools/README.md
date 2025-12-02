# 🎮 Discord Tools for Letta

A comprehensive collection of Discord integration tools for Letta AI agents.

## 📋 Available Tools

### 🎯 Unified Discord Tool (Recommended)
- **`unified_discord_tool`** - All-in-one Discord tool
  - Send messages (DMs and channels)
  - Read messages with advanced filtering
  - List guilds and channels
  - Task scheduling (create/delete/list)
  - Batch operations for API credit savings
  - See [UNIFIED_TOOL_README.md](./UNIFIED_TOOL_README.md) for details

### 🎤 Voice Messages
- **`send_voice_message`** - Send voice messages using ElevenLabs TTS
  - Convert text to natural-sounding speech
  - Audio Tags for emotions and accents
  - Send to DMs or channels
  - See [VOICE_MESSAGE_README.md](./VOICE_MESSAGE_README.md) for details

### ⏰ Task Scheduler
- **`taskScheduler.ts`** - Production-ready TypeScript scheduler
  - Executes tasks created by Unified Discord Tool
  - Automatic recurring task updates
  - See [TASK_SCHEDULER_README.md](./TASK_SCHEDULER_README.md) for details

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

Set environment variables:

```bash
# Discord Bot
export DISCORD_BOT_TOKEN="your_bot_token_here"
export TASKS_CHANNEL_ID="your_tasks_channel_id"
export HEARTBEAT_LOG_CHANNEL_ID="your_heartbeat_log_channel_id"
export ALLOWED_DM_USER_ID="your_discord_user_id"
export DEFAULT_USER_ID="your_discord_user_id"

# ElevenLabs (for voice messages)
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"
export ELEVENLABS_VOICE_ID="your_voice_id"
export ELEVENLABS_MODEL_ID="eleven_multilingual_v2"  # Optional
```

### 4. Upload to Letta

Use the management tools to upload:

```bash
cd ../management_tools

# Upload unified tool (recommended)
python push-tool.py unified_discord_tool
python manage-agent-tools.py attach unified_discord_tool

# Upload voice message tool (optional)
python push-tool.py send_voice_message
python manage-agent-tools.py attach send_voice_message
```

---

## 📖 Tool Documentation

### 🎯 Unified Discord Tool

**See [UNIFIED_TOOL_README.md](./UNIFIED_TOOL_README.md) for complete documentation**

Features:
- Send messages (DMs and channels) with auto-chunking
- Read messages with advanced time filtering and keyword search
- List guilds and channels
- Task scheduling (create/delete/list/manage)
- Batch operations for API credit savings

### 🎤 Voice Message Tool

**See [VOICE_MESSAGE_README.md](./VOICE_MESSAGE_README.md) for complete documentation**

Features:
- Text-to-Speech using ElevenLabs
- Audio Tags for emotions and accents
- Send to DMs or channels
- Live progress updates
- Smart timeouts

### ⏰ Task Scheduler

**See [TASK_SCHEDULER_GUIDE.md](./TASK_SCHEDULER_GUIDE.md) for user guide**  
**See [TASK_SCHEDULER_IMPLEMENTATION.md](./TASK_SCHEDULER_IMPLEMENTATION.md) for implementation**  
**See [TASK_SCHEDULER_README.md](./TASK_SCHEDULER_README.md) for setup**

Features:
- Executes tasks created by Unified Discord Tool
- Automatic recurring task updates
- Production-ready TypeScript implementation
- Timezone handling (Berlin time → UTC)

---

## 🔧 Configuration

### Required Environment Variables

Create a `.env` file or set environment variables:

```env
# Discord Bot (Required for all tools)
DISCORD_BOT_TOKEN=your_bot_token_here
TASKS_CHANNEL_ID=your_tasks_channel_id
HEARTBEAT_LOG_CHANNEL_ID=your_heartbeat_log_channel_id
ALLOWED_DM_USER_ID=your_discord_user_id
DEFAULT_USER_ID=your_discord_user_id

# ElevenLabs (Required for voice messages)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id
ELEVENLABS_MODEL_ID=eleven_multilingual_v2  # Optional
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

### Send a Message (Unified Tool)
```python
discord_tool(
    action="send_message",
    message="Hello @everyone! 👋",
    target="1234567890",
    target_type="channel",
    mention_users=["1234567890"]
)
```

### Send a Voice Message
```python
send_voice_message(
    text="[excited] Hello! This is a voice message!",
    target="1234567890",
    target_type="channel"
)
```

### Create a Daily Reminder (Unified Tool)
```python
discord_tool(
    action="create_task",
    task_name="daily_standup",
    description="Daily team standup reminder",
    schedule="daily",
    time="09:00",
    action_type="channel_post",
    action_target="1234567890",
    action_template="📅 Daily standup in 15 minutes!"
)
```

### Read Recent Messages (Unified Tool)
```python
discord_tool(
    action="read_messages",
    target="1234567890",
    target_type="channel",
    limit=50,
    time_filter="last_24_hours"
)
```

### Batch Operations (Unified Tool)
```python
discord_tool(
    action="execute_batch",
    operations=[
        {"action": "read_messages", "target": "123", "time_filter": "today"},
        {"action": "send_message", "target": "456", "message": "Hello!"}
    ]
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

## 📚 Documentation

- **[UNIFIED_TOOL_README.md](./UNIFIED_TOOL_README.md)** - Complete guide for Unified Discord Tool
- **[VOICE_MESSAGE_README.md](./VOICE_MESSAGE_README.md)** - Voice message tool documentation
- **[TASK_SCHEDULER_GUIDE.md](./TASK_SCHEDULER_GUIDE.md)** - Task scheduler user guide
- **[TASK_SCHEDULER_IMPLEMENTATION.md](./TASK_SCHEDULER_IMPLEMENTATION.md)** - Implementation guide
- **[TASK_SCHEDULER_README.md](./TASK_SCHEDULER_README.md)** - Task scheduler setup

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15
