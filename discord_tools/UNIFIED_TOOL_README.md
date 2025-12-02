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
# User reminder (sends DM to user)
discord_tool(
    action="create_task",
    task_name="daily_reminder",
    description="Daily standup reminder",
    schedule="daily",
    time="09:00",
    action_type="user_reminder",
    action_template="📅 Daily standup in 15 minutes!"
)

# Channel post (posts to specified channel)
discord_tool(
    action="create_task",
    task_name="daily_announcement",
    description="Daily announcement",
    schedule="daily",
    time="09:00",
    action_type="channel_post",
    action_target="1234567890",  # Target channel ID
    action_template="📅 Good morning everyone!"
)

# Self task (logs to Heartbeat Log Channel by default)
discord_tool(
    action="create_task",
    task_name="system_check",
    description="System health check",
    schedule="hourly",
    action_type="self_task",
    action_template="🔍 Running system health check..."
)
```

**Note:** Tasks are stored as messages in the **Tasks Channel**. The `action_target` determines where the task executes:
- `user_reminder` → Sends DM to user (uses DEFAULT_USER_ID if not specified)
- `channel_post` → Posts to specified channel (uses Heartbeat Log Channel if not specified)
- `self_task` → Logs to Heartbeat Log Channel (default for system tasks)

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

### Required Discord Channels

**You need to create TWO Discord channels for this tool to work properly:**

1. **Tasks Channel** 📋
   - **Purpose:** Stores all scheduled tasks as Discord messages
   - **Usage:** The tool creates task messages here that can be read, updated, or deleted
   - **How to get ID:** Right-click channel → Copy Channel ID (Developer Mode must be enabled)
   - **Example:** Create a channel named `#scheduled-tasks` or `#bot-tasks`

2. **Heartbeat Log Channel** 🧠
   - **Purpose:** Used for internal agent tasks and system logging
   - **Usage:** Default target for `self_task` and `channel_post` actions when no explicit target is set
   - **How to get ID:** Right-click channel → Copy Channel ID (Developer Mode must be enabled)
   - **Example:** Create a channel named `#heartbeat-log` or `#agent-logs`

**Why two channels?**
- **Tasks Channel:** Keeps all scheduled tasks organized in one place for easy management
- **Heartbeat Log Channel:** Separates system/agent operations from user-facing tasks, making logs cleaner

### Environment Variables
```env
DISCORD_BOT_TOKEN=your_bot_token_here
TASKS_CHANNEL_ID=your_tasks_channel_id
HEARTBEAT_LOG_CHANNEL_ID=your_heartbeat_log_channel_id
ALLOWED_DM_USER_ID=your_discord_user_id
DEFAULT_USER_ID=your_discord_user_id
```

**Required Variables:**
- `DISCORD_BOT_TOKEN` - Your Discord bot token (get from Discord Developer Portal)
- `TASKS_CHANNEL_ID` - Channel ID where scheduled tasks are stored
- `HEARTBEAT_LOG_CHANNEL_ID` - Channel ID for agent/system logging
- `ALLOWED_DM_USER_ID` - User ID that can receive DMs (security restriction)
- `DEFAULT_USER_ID` - Default user ID for user reminders (usually same as ALLOWED_DM_USER_ID)

### Bot Permissions
Your Discord bot needs these permissions:
- **Send Messages** - Post in channels (required for Tasks & Heartbeat channels)
- **Read Message History** - Read past messages (required to read tasks)
- **Attach Files** - Upload/download files
- **Use External Emojis** - Rich formatting
- **Add Reactions** - Interactive features
- **Manage Messages** - Delete/edit messages (required to delete tasks)

**Important:** Make sure your bot has access to both the Tasks Channel and Heartbeat Log Channel!

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

1. **Create Discord Channels:**
   - Create a channel for scheduled tasks (e.g., `#scheduled-tasks`)
   - Create a channel for heartbeat logs (e.g., `#heartbeat-log`)
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click each channel → Copy Channel ID

2. **Set Environment Variables:**
   ```bash
   export DISCORD_BOT_TOKEN="your_bot_token_here"
   export TASKS_CHANNEL_ID="your_tasks_channel_id"
   export HEARTBEAT_LOG_CHANNEL_ID="your_heartbeat_log_channel_id"
   export ALLOWED_DM_USER_ID="your_discord_user_id"
   export DEFAULT_USER_ID="your_discord_user_id"
   ```

3. **Upload the unified tool:**
   ```bash
   cd management_tools
   python push-tool.py unified_discord_tool
   ```

4. **Attach to your agent:**
   ```bash
   python manage-agent-tools.py attach unified_discord_tool
   ```

5. **Detach old tools:**
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

6. **Start using the unified tool!**

## 📚 Additional Documentation

### Task Scheduler

The Unified Discord Tool includes a powerful Task Scheduler feature. Learn more:

- **[TASK_SCHEDULER_GUIDE.md](./TASK_SCHEDULER_GUIDE.md)** - Complete guide on creating and managing scheduled tasks
  - How to create tasks
  - All schedule types and action types
  - Examples and troubleshooting

- **[TASK_SCHEDULER_IMPLEMENTATION.md](./TASK_SCHEDULER_IMPLEMENTATION.md)** - Guide for implementing an external scheduler
  - How to build a scheduler that executes tasks
  - Python and TypeScript examples
  - Integration with Letta AI

- **[taskScheduler.ts](./taskScheduler.ts)** - Production-ready TypeScript implementation
  - Complete, working scheduler code
  - Ready to copy into your Discord bot project
  - See [TASK_SCHEDULER_README.md](./TASK_SCHEDULER_README.md) for setup instructions

**Note**: The Unified Discord Tool creates tasks in Discord, but you need an external scheduler (Discord bot, cron job, etc.) to actually execute them. We provide a ready-to-use TypeScript implementation in `taskScheduler.ts`!

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
- Verify channel ID is correct (check both Tasks Channel and Heartbeat Log Channel)
- Check bot has access to both required channels
- Enable Developer Mode to get correct IDs (User Settings → Advanced → Developer Mode)
- Make sure you copied the full channel ID (long number string)

### "Task creation failed"
- Verify TASKS_CHANNEL_ID environment variable is set correctly
- Check bot has "Send Messages" permission in Tasks Channel
- Ensure Tasks Channel ID is valid and bot can access it

### "Heartbeat log channel error"
- Verify HEARTBEAT_LOG_CHANNEL_ID environment variable is set correctly
- Check bot has "Send Messages" permission in Heartbeat Log Channel
- Ensure Heartbeat Log Channel ID is valid and bot can access it

### "Rate limited"
- Discord has rate limits on API calls
- Add delays between requests if needed
- Use exponential backoff for retries

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-12-02

**One tool to rule them all!** 🎮✨
