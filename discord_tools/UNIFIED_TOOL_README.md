# 🎮 Unified Discord Tool

**One tool to rule them all!** This single tool replaces all 7 separate Discord tools with a unified, powerful interface.

## 🚀 Why Unified?

**Before:** 7 separate tools
- `send_discord_message.py`
- `read_discord_dms.py` 
- `read_discord_channel.py`
- `list_discord_channels.py`
- `download_discord_file.py`
- `create_scheduled_task.py`
- `delete_scheduled_task.py`
- `list_scheduled_tasks.py`

**After:** 1 unified tool
- `unified_discord_tool.py` ✅

**Note:** File download is included, but omnipresence features are not included in this unified tool.

## 📋 All Actions in One Tool

### 1. 📨 Send Messages
```python
# Send DM
discord_tool(
    action="send_message",
    message="Hello there!",
    target="1234567890",
    target_type="user"
)

# Send to channel
discord_tool(
    action="send_message", 
    message="Hello channel!",
    target="1234567890",
    target_type="channel"
)

# Auto-detect (tries user first, then channel)
discord_tool(
    action="send_message",
    message="Hello!",
    target="1234567890"
)
```

### 2. 📖 Read Messages
```python
# Read channel messages
discord_tool(
    action="read_messages",
    target="1234567890",
    target_type="channel",
    limit=50,
    time_filter="last_24_hours"
)

# Read DMs
discord_tool(
    action="read_messages",
    target="1234567890", 
    target_type="user",
    limit=20
)
```

### 3. 📁 Download Files
```python
discord_tool(
    action="download_file",
    message_id="1234567890",
    channel_id="1234567890"
)
```

### 4. 🏷️ List Channels
```python
discord_tool(
    action="list_channels",
    server_id="1234567890"
)
```

### 5. ⏰ Create Tasks
```python
discord_tool(
    action="create_task",
    task_name="daily_reminder",
    description="Daily standup reminder",
    schedule="daily",
    time="09:00",
    action_type="channel_post",
    action_target="1234567890",
    action_template="📅 Daily standup in 15 minutes!"
)
```

### 6. 🗑️ Delete Tasks
```python
discord_tool(
    action="delete_task",
    message_id="1234567890",
    channel_id="1234567890"
)
```

### 7. 📋 List Tasks
```python
discord_tool(
    action="list_tasks",
    tasks_channel_id="1234567890"
)
```


## ⚙️ Configuration

### Environment Variables
```env
DISCORD_BOT_TOKEN=your_bot_token_here
TASKS_CHANNEL_ID=your_tasks_channel_id
DEFAULT_USER_ID=your_discord_user_id
```

### Bot Permissions
Your Discord bot needs these permissions:
- **Send Messages** - Post in channels
- **Read Message History** - Read past messages
- **Attach Files** - Upload/download files
- **Use External Emojis** - Rich formatting
- **Add Reactions** - Interactive features
- **Manage Messages** - Delete/edit messages

## 🎯 Benefits

### ✅ Simplicity
- **One tool** instead of 7 separate tools
- **Consistent interface** across all operations
- **Single configuration** file

### ✅ Power
- **Auto-detection** of target types
- **Smart defaults** for common operations
- **Comprehensive error handling**

### ✅ Efficiency
- **Fewer tool attachments** to your agent
- **Reduced complexity** in tool management
- **Better performance** with unified code

### ✅ Maintainability
- **Single codebase** to maintain
- **Consistent updates** across all features
- **Easier debugging** and testing

## 🔄 Migration from Separate Tools

### Old Way (7 tools):
```python
# Send message
send_discord_message(channel_id="123", message="Hello!")

# Read messages  
read_discord_channel(channel_id="123", limit=50)

# Download file
download_discord_file(message_id="123", channel_id="456")

# List channels
list_discord_channels(server_id="123")

# Create task
create_scheduled_task(task_name="reminder", ...)
```

### New Way (1 tool):
```python
# Send message
discord_tool(action="send_message", target="123", message="Hello!")

# Read messages
discord_tool(action="read_messages", target="123", limit=50)

# Download file
discord_tool(action="download_file", message_id="123", channel_id="456")

# List channels
discord_tool(action="list_channels", server_id="123")

# Create task
discord_tool(action="create_task", task_name="reminder", ...)
```

## 🚀 Quick Start

1. **Upload the unified tool:**
   ```bash
   cd management_tools
   python push-tool.py unified_discord_tool
   ```

2. **Attach to your agent:**
   ```bash
   python manage-agent-tools.py attach unified_discord_tool
   ```

3. **Detach old tools:**
   ```bash
   python manage-agent-tools.py detach send_discord_message
   python manage-agent-tools.py detach read_discord_dms
   python manage-agent-tools.py detach read_discord_channel
   python manage-agent-tools.py detach list_discord_channels
   python manage-agent-tools.py detach download_discord_file
   python manage-agent-tools.py detach create_scheduled_task
   python manage-agent-tools.py detach delete_scheduled_task
   python manage-agent-tools.py detach list_scheduled_tasks
   ```

4. **Start using the unified tool!**

## 🔒 Security

- **Environment variables** for all credentials
- **Input validation** for all parameters
- **Error handling** for API failures
- **Rate limiting** awareness

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

**Created by:** Mioré 🐾  
**Last Updated:** 2025-10-14

**One tool to rule them all!** 🎮✨
