# Task Scheduler Guide

This guide explains how to use the Task Scheduler feature in the Unified Discord Tool. The Task Scheduler allows you to create scheduled tasks that automatically execute at specific times or intervals.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Task Format](#task-format)
4. [Schedule Types](#schedule-types)
5. [Action Types](#action-types)
6. [Creating Tasks](#creating-tasks)
7. [Managing Tasks](#managing-tasks)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Task Scheduler is a feature that:
- Stores scheduled tasks as Discord messages in a dedicated channel
- Allows you to create both **one-time** and **recurring** tasks
- Supports multiple action types (user reminders, channel posts, self tasks)
- Automatically calculates next run times for recurring tasks
- Integrates with your Letta AI agent workflow

### Key Features

✅ **Automatic Scheduling**: Tasks are stored in Discord and can be executed by external schedulers  
✅ **Recurring Tasks**: Schedule daily, weekly, monthly, or custom intervals  
✅ **Multiple Action Types**: Send DMs, post to channels, or trigger agent tasks  
✅ **Timezone Support**: Times are interpreted as Europe/Berlin timezone  
✅ **Smart Defaults**: Automatic target selection based on action type  

---

## Prerequisites

Before using the Task Scheduler, ensure you have:

- ✅ Unified Discord Tool installed and configured
- ✅ `TASKS_CHANNEL_ID` environment variable set (channel where tasks are stored)
- ✅ `HEARTBEAT_LOG_CHANNEL_ID` environment variable set (for self_task actions)
- ✅ Bot has permissions to read/write messages in both channels
- ✅ Bot has permission to send DMs (for user_reminder actions)

---

## Task Format

Tasks are stored as Discord messages in JSON format. The tool automatically formats tasks when you create them.

### Basic Task Structure

```json
{
  "task_name": "My Task Name",
  "description": "What this task does",
  "schedule": "daily",
  "time": "09:00",
  "next_run": "2025-01-16T09:00:00",
  "one_time": false,
  "active": true,
  "action_type": "user_reminder",
  "action_target": "123456789012345678",
  "action_template": "Optional message template"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `task_name` | string | Name of the task (for logging and identification) |
| `schedule` | string | Schedule type (see [Schedule Types](#schedule-types)) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Human-readable description of the task |
| `time` | string | Time in HH:MM format (interpreted as Europe/Berlin timezone) |
| `specific_date` | string | Specific date for one-time tasks (YYYY-MM-DD or DD.MM.YYYY) |
| `day_of_month` | integer | Day of month (1-31) for monthly/yearly tasks |
| `month` | integer | Month (1-12) for yearly tasks |
| `day_of_week` | string | Day of week for weekly tasks (monday, tuesday, etc.) |
| `one_time` | boolean | `true` = one-time task, `false` = recurring (auto-set by tool) |
| `action_type` | string | Type of action (see [Action Types](#action-types)) |
| `action_target` | string | Discord user/channel ID (optional, uses smart defaults) |
| `action_template` | string | Message template for the task |

**Note**: The tool automatically sets `next_run`, `one_time`, `active`, and other fields based on your schedule configuration.

---

## Schedule Types

### One-Time Schedules

| Schedule | Example | Description |
|----------|---------|-------------|
| `in_X_minutes` | `in_30_minutes` | Runs once in 30 minutes |
| `in_X_hours` | `in_2_hours` | Runs once in 2 hours |
| `in_X_seconds` | `in_10_seconds` | Runs once in 10 seconds |
| `today_at_HH:MM` | `today_at_14:00` | Runs once today at 2:00 PM (or tomorrow if time passed) |
| `tomorrow_at_HH:MM` | `tomorrow_at_09:00` | Runs once tomorrow at 9:00 AM |
| `on_date` | `on_date` | Runs once on a specific date (requires `specific_date` field) |

**Note**: For one-time tasks, the tool automatically sets `one_time: true`.

### Recurring Schedules

| Schedule | Example | Description |
|----------|---------|-------------|
| `minutely` | `minutely` | Every minute |
| `hourly` | `hourly` | Every hour |
| `daily` | `daily` | Every day (use with `time` field for specific time) |
| `weekly` | `weekly` | Every 7 days (use with `time` and `day_of_week` fields) |
| `monthly` | `monthly` | Every month (use with `time` and `day_of_month` fields) |
| `yearly` | `yearly` | Every year (use with `time`, `month`, and `day_of_month` fields) |
| `every_X_minutes` | `every_30_minutes` | Every N minutes |
| `every_X_hours` | `every_3_hours` | Every N hours |
| `every_X_days` | `every_7_days` | Every N days (use with `time` field) |
| `every_X_weeks` | `every_2_weeks` | Every N weeks (use with `time` field) |

**Note**: For recurring tasks, the tool automatically sets `one_time: false` and calculates `next_run`.

### Time Field

The `time` field is optional but recommended for schedules like `daily`, `weekly`, etc.:

- Format: `"HH:MM"` (e.g., `"09:00"`, `"14:30"`)
- Timezone: Interpreted as **Europe/Berlin** timezone
- Examples:
  - `"schedule": "daily", "time": "09:00"` → Every day at 9:00 AM Berlin time
  - `"schedule": "weekly", "time": "18:00", "day_of_week": "monday"` → Every Monday at 6:00 PM Berlin time

---

## Action Types

Tasks can perform different actions when executed:

### 1. `user_reminder`

Sends a reminder directly to a user's DMs.

**Smart Default**: If `action_target` is not specified, uses `DEFAULT_USER_ID` from environment variables.

```python
discord_tool(
    action="create_task",
    task_name="Morning Reminder",
    schedule="daily",
    time="09:00",
    action_type="user_reminder",
    action_target="123456789012345678",  # Optional: User ID
    action_template="Good morning! ☀️"
)
```

**Behavior**:
- Opens a DM channel to the user
- Sends the task message to the user
- User receives the reminder in their DMs

### 2. `channel_post`

Posts a message to a specific Discord channel.

**Smart Default**: If `action_target` is not specified, uses `HEARTBEAT_LOG_CHANNEL_ID` from environment variables.

```python
discord_tool(
    action="create_task",
    task_name="Daily Update",
    schedule="daily",
    time="09:00",
    action_type="channel_post",
    action_target="987654321098765432",  # Optional: Channel ID
    action_template="Daily update time!"
)
```

**Behavior**:
- Posts message to the specified channel
- If no target specified, posts to Heartbeat Log Channel

### 3. `self_task`

Triggers an internal agent task (for autonomous actions).

**Smart Default**: Always uses `HEARTBEAT_LOG_CHANNEL_ID` from environment variables if `action_target` is not specified.

```python
discord_tool(
    action="create_task",
    task_name="Memory Organization",
    schedule="hourly",
    action_type="self_task",
    action_template="Organize memories and check for updates"
)
```

**Behavior**:
- If `action_target` is set and valid → uses that channel
- Otherwise → uses Heartbeat Log Channel (from `HEARTBEAT_LOG_CHANNEL_ID`)
- Perfect for autonomous agent tasks

---

## Creating Tasks

### Using the Unified Discord Tool

The easiest way to create tasks is using the `create_task` action:

```python
# Daily reminder
discord_tool(
    action="create_task",
    task_name="Daily Standup",
    description="Daily standup reminder",
    schedule="daily",
    time="09:00",
    action_type="user_reminder",
    action_template="📅 Time for daily standup!"
)

# Weekly channel post
discord_tool(
    action="create_task",
    task_name="Weekly Summary",
    description="Post weekly summary",
    schedule="weekly",
    day_of_week="monday",
    time="08:00",
    action_type="channel_post",
    action_target="987654321098765432",
    action_template="📊 Weekly summary time!"
)

# One-time reminder
discord_tool(
    action="create_task",
    task_name="Meeting Reminder",
    description="Remind about meeting",
    schedule="in_30_minutes",
    action_type="user_reminder",
    action_template="⏰ Meeting starts in 30 minutes!"
)
```

### Batch Task Creation

You can create multiple tasks at once using `manage_tasks`:

```python
discord_tool(
    action="manage_tasks",
    create_tasks=[
        {
            "task_name": "Morning Check",
            "schedule": "daily",
            "time": "09:00",
            "action_type": "self_task",
            "action_template": "Check system status"
        },
        {
            "task_name": "Evening Summary",
            "schedule": "daily",
            "time": "18:00",
            "action_type": "channel_post",
            "action_template": "Evening summary time"
        }
    ]
)
```

---

## Managing Tasks

### List All Tasks

```python
discord_tool(
    action="list_tasks",
    tasks_channel_id="123456789012345678"  # Optional: uses default if not specified
)
```

### Delete a Task

```python
discord_tool(
    action="delete_task",
    message_id="123456789012345678",  # Message ID of the task
    channel_id="123456789012345678"   # Tasks channel ID
)
```

### Batch Task Management

Use `manage_tasks` to list, delete, and create tasks in one call:

```python
discord_tool(
    action="manage_tasks",
    list_tasks=True,  # List all tasks
    delete_task_ids=["123456789012345678", "987654321098765432"],  # Delete tasks
    create_tasks=[...]  # Create new tasks
)
```

---

## Examples

### Example 1: Daily Morning Reminder

**Goal**: Send a good morning message to a user every day at 9:00 AM.

```python
discord_tool(
    action="create_task",
    task_name="Daily Morning Reminder",
    description="Send good morning message to user",
    schedule="daily",
    time="09:00",
    action_type="user_reminder",
    action_target="123456789012345678",
    action_template="Good morning! Have a great day! ☀️"
)
```

### Example 2: Weekly Channel Update

**Goal**: Post a weekly summary to a channel every Monday at 8:00 AM.

```python
discord_tool(
    action="create_task",
    task_name="Weekly Summary",
    description="Post weekly summary to channel",
    schedule="weekly",
    day_of_week="monday",
    time="08:00",
    action_type="channel_post",
    action_target="987654321098765432",
    action_template="Time for the weekly summary!"
)
```

### Example 3: One-Time Reminder

**Goal**: Remind a user in 30 minutes to check something.

```python
discord_tool(
    action="create_task",
    task_name="Check Logs Reminder",
    description="Remind user to check system logs",
    schedule="in_30_minutes",
    action_type="user_reminder",
    action_target="123456789012345678",
    action_template="⏰ Reminder: Time to check the system logs!"
)
```

**Note**: After execution, this task will be deleted (because it's one-time).

### Example 4: Hourly Self-Task

**Goal**: Run an autonomous agent task every hour.

```python
discord_tool(
    action="create_task",
    task_name="Hourly Memory Organization",
    description="Organize memories and check for updates",
    schedule="hourly",
    action_type="self_task",
    action_template="Organize memories, check for important updates, and review recent conversations."
)
```

**Note**: No `action_target` needed - defaults to Heartbeat Log Channel.

### Example 5: Custom Interval

**Goal**: Check something every 3 hours.

```python
discord_tool(
    action="create_task",
    task_name="Status Check",
    description="Check system status every 3 hours",
    schedule="every_3_hours",
    action_type="self_task",
    action_template="Check system status and health"
)
```

### Example 6: Specific Date Task

**Goal**: Send a birthday message on a specific date.

```python
discord_tool(
    action="create_task",
    task_name="Birthday Reminder",
    description="Send birthday message",
    schedule="on_date",
    specific_date="25.12.2025",  # Or "2025-12-25"
    time="10:00",
    action_type="user_reminder",
    action_target="123456789012345678",
    action_template="🎂 Happy Birthday!"
)
```

---

## Troubleshooting

### Task Not Executing

**Problem**: Task is created but doesn't run.

**Solutions**:
1. ✅ Verify task is stored in the Tasks Channel
2. ✅ Check `active` field is `true` (should be automatic)
3. ✅ Verify `next_run` is in the past or current time
4. ✅ Ensure you have an external scheduler (e.g., Discord bot) that reads tasks
5. ✅ Check `TASKS_CHANNEL_ID` environment variable is correct
6. ✅ Ensure bot has "Read Message History" permission

**Note**: The Unified Discord Tool creates tasks but doesn't execute them. You need an external scheduler (like a Discord bot) to read tasks from the channel and execute them.

### Task Creation Failed

**Problem**: Error when creating task.

**Solutions**:
1. ✅ Verify `TASKS_CHANNEL_ID` environment variable is set correctly
2. ✅ Check bot has "Send Messages" permission in Tasks Channel
3. ✅ Ensure Tasks Channel ID is valid and bot can access it
4. ✅ Check all required fields are provided (`task_name`, `schedule`)

### Timezone Issues

**Problem**: Task runs at wrong time.

**Solutions**:
1. ✅ Remember: `time` field is interpreted as **Europe/Berlin** timezone
2. ✅ Use ISO-8601 format for `next_run` (automatically set by tool)
3. ✅ Verify your external scheduler uses the same timezone

### Channel Not Found Errors

**Problem**: `action_target` channel not found.

**Solutions**:
1. ✅ Verify channel ID is correct (17-19 digit Discord Snowflake)
2. ✅ Ensure bot has access to the channel
3. ✅ For `self_task`: Check `HEARTBEAT_LOG_CHANNEL_ID` is set
4. ✅ Use smart defaults (don't specify `action_target` if not needed)

### DM Restriction Errors

**Problem**: Cannot send DM to user.

**Solutions**:
1. ✅ Verify `ALLOWED_DM_USER_ID` is set correctly
2. ✅ Check user has DMs enabled from server members
3. ✅ Ensure bot has permission to send DMs
4. ✅ For `user_reminder`: User must be in `ALLOWED_DM_USER_ID` list

---

## Integration with External Schedulers

The Unified Discord Tool creates tasks in Discord, but you need an external scheduler to execute them. Here are common approaches:

### Option 1: Discord Bot Scheduler

Create a Discord bot that:
1. Reads messages from the Tasks Channel every 60 seconds
2. Parses JSON tasks from code blocks
3. Checks if `next_run <= now`
4. Executes tasks (sends to Letta AI, posts messages, etc.)
5. Updates recurring tasks or deletes one-time tasks

See the [Task Scheduler Implementation Guide](./TASK_SCHEDULER_IMPLEMENTATION.md) for code examples.

### Option 2: Cron Job + Python Script

Create a Python script that:
1. Runs via cron every minute
2. Uses the Unified Discord Tool to read tasks
3. Executes due tasks
4. Updates or deletes tasks as needed

### Option 3: Letta AI Agent

Configure your Letta AI agent to:
1. Periodically check the Tasks Channel
2. Execute due tasks automatically
3. Use the Unified Discord Tool to manage tasks

---

## Security Considerations

1. **Channel Permissions**: Only give the bot necessary permissions (Read Message History, Send Messages, Manage Messages)
2. **Task Validation**: The tool validates task structure, but validate user input if tasks are created via user commands
3. **DM Restrictions**: The tool enforces DM restrictions - only users in `ALLOWED_DM_USER_ID` can receive DMs
4. **Rate Limiting**: Be aware of Discord API rate limits when creating many tasks

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all environment variables are set correctly
3. Test with a simple one-time task first
4. Ensure your bot has proper Discord permissions
5. Review the [Unified Discord Tool README](./UNIFIED_TOOL_README.md) for general setup

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15

**Part of the Unified Discord Tool for Letta** 🎮✨

