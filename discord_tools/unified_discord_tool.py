"""
UNIFIED DISCORD TOOL - Complete Discord Integration for Letta
============================================================

This tool combines core Discord functionality into one powerful tool:
✅ Send messages (DMs and channels)
✅ Read messages (DMs and channels) 
✅ Download files from Discord messages
✅ Channel management (list channels)
✅ Task scheduling (create/delete/list tasks)

USAGE EXAMPLES:
---------------

1. SEND MESSAGES:
   discord_tool(action="send_message", message="Hello!", target="1234567890", target_type="channel")
   discord_tool(action="send_message", message="Hi there!", target="1234567890", target_type="user")
   discord_tool(action="send_message", message="Check this!", target="1234567890", target_type="channel", mention_users=["701608830852792391"])
   discord_tool(action="send_message", message="Important!", target="1234567890", target_type="channel", ping_everyone=True)
   # Auto-chunks messages over 2000 characters

2. READ MESSAGES:
   discord_tool(action="read_messages", target="1234567890", target_type="channel", limit=50)
   discord_tool(action="read_messages", target="1234567890", target_type="user", limit=20)

3. DOWNLOAD FILES:
   discord_tool(action="download_file", message_id="1234567890", channel_id="1234567890")

4. LIST CHANNELS:
   discord_tool(action="list_channels", server_id="1234567890")

5. SCHEDULE TASKS:
   # Today at specific time
   discord_tool(action="create_task", task_name="evening_reminder", description="Reminder for today",
                schedule="today_at_18:00", action_type="user_reminder",
                action_target="USER_ID", action_template="Don't forget to check in!")
   
   # Daily reminder
   discord_tool(action="create_task", task_name="reminder", description="Daily reminder", 
                schedule="daily", time="09:00", action_type="channel_post", 
                action_target="1234567890", action_template="Good morning!")
   
   # Specific date (European format)
   discord_tool(action="create_task", task_name="birthday", description="Mom's birthday",
                schedule="on_date", specific_date="25.12.2025", time="10:00",
                action_type="user_reminder", action_target="USER_ID", 
                action_template="🎂 Happy Birthday Mom!")
   
   # Specific date (ISO format)
   discord_tool(action="create_task", task_name="meeting", description="Important meeting",
                schedule="on_date", specific_date="2025-11-15", time="14:30",
                action_type="user_reminder", action_target="USER_ID",
                action_template="Meeting in 30 minutes!")
   
   # Weekly on specific day
   discord_tool(action="create_task", task_name="monday_standup", description="Weekly standup",
                schedule="weekly", day_of_week="monday", time="09:00",
                action_type="channel_post", action_target="CHANNEL_ID",
                action_template="📅 Time for our weekly standup!")
   
   # Monthly on specific day
   discord_tool(action="create_task", task_name="rent", description="Pay rent",
                schedule="monthly", day_of_month=1, time="10:00",
                action_type="user_reminder", action_target="USER_ID",
                action_template="💰 Rent is due today!")
   
   # Yearly reminder
   discord_tool(action="create_task", task_name="taxes", description="File taxes",
                schedule="yearly", month=4, day_of_month=15, time="09:00",
                action_type="user_reminder", action_target="USER_ID",
                action_template="📊 Tax deadline is approaching!")

6. DELETE TASKS:
   discord_tool(action="delete_task", message_id="1234567890", channel_id="1234567890")

7. LIST TASKS:
   discord_tool(action="list_tasks", tasks_channel_id="1234567890")

"""

import requests
import os
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

def discord_tool(
    action: str,
    # Message parameters
    message: str = None,
    target: str = None,
    target_type: str = None,  # "user" or "channel"
    mention_users: list = None,  # List of user IDs to mention
    ping_everyone: bool = False,  # Ping @everyone (channel only)
    ping_here: bool = False,  # Ping @here (channel only)
    # Read parameters
    limit: int = 50,
    time_filter: str = "all",
    timezone: str = "Europe/Berlin",
    show_both: bool = True,
    # Task parameters
    message_id: str = None,
    channel_id: str = None,
    # Channel parameters
    server_id: str = None,
    # Task parameters
    task_name: str = None,
    description: str = None,
    schedule: str = None,
    time: str = None,
    specific_date: str = None,
    day_of_month: int = None,
    month: int = None,
    day_of_week: str = None,
    action_type: str = None,
    action_target: str = None,
    action_template: str = None,
    tasks_channel_id: str = None
):
    """
    Unified Discord tool that handles core Discord operations.
    
    Args:
        action: The action to perform (send_message, read_messages, download_file,
                list_channels, create_task, delete_task, list_tasks)
        ... (other parameters depend on action)
    """
    
      # Configuration
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN_HERE")
    TASKS_CHANNEL_ID = os.getenv("TASKS_CHANNEL_ID", "YOUR_TASKS_CHANNEL_ID_HERE")
    DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "YOUR_DEFAULT_USER_ID_HERE")
    
    if DISCORD_BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        return {"status": "error", "message": "Discord bot token not configured. Please set DISCORD_BOT_TOKEN environment variable."}
    
    try:
        if action == "send_message":
            return _send_message(DISCORD_BOT_TOKEN, message, target, target_type, mention_users, ping_everyone, ping_here)
        
        elif action == "read_messages":
            return _read_messages(DISCORD_BOT_TOKEN, target, target_type, limit, time_filter, timezone, show_both)
        
        elif action == "download_file":
            return _download_file(DISCORD_BOT_TOKEN, message_id, channel_id)
        
        elif action == "list_channels":
            return _list_channels(DISCORD_BOT_TOKEN, server_id)
        
        elif action == "create_task":
            return _create_task(DISCORD_BOT_TOKEN, TASKS_CHANNEL_ID, DEFAULT_USER_ID, 
                              task_name, description, schedule, time, specific_date,
                              day_of_month, month, day_of_week, action_type, 
                              action_target, action_template)
        
        elif action == "delete_task":
            return _delete_task(DISCORD_BOT_TOKEN, message_id, channel_id)
        
        elif action == "list_tasks":
            return _list_tasks(tasks_channel_id or TASKS_CHANNEL_ID)
        
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}
    
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

def _send_message(bot_token, message, target, target_type, mention_users=None, ping_everyone=False, ping_here=False):
    """Send a message to Discord (DM or channel) with auto-chunking and mentions."""
    headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}
    
    # Auto-detect target type if not specified
    if not target_type:
        # Try user first (DMs), then channel
        try:
            dm_url = f"https://discord.com/api/v10/users/@me/channels"
            dm_data = {"recipient_id": target}
            dm_response = requests.post(dm_url, headers=headers, json=dm_data, timeout=10)
            
            if dm_response.status_code == 200:
                channel_id = dm_response.json()["id"]
                target_type = "user"
            else:
                channel_id = target
                target_type = "channel"
        except:
            channel_id = target
            target_type = "channel"
    else:
        if target_type == "user":
            # Create DM channel
            dm_url = f"https://discord.com/api/v10/users/@me/channels"
            dm_data = {"recipient_id": target}
            dm_response = requests.post(dm_url, headers=headers, json=dm_data, timeout=10)
            if dm_response.status_code != 200:
                return {"status": "error", "message": f"Failed to create DM: {dm_response.text}"}
            channel_id = dm_response.json()["id"]
        else:
            channel_id = target
    
    # Build mentions
    mentions_text = ""
    if target_type == "channel":  # Mentions only work in channels, not DMs
        if ping_everyone:
            mentions_text = "@everyone "
        elif ping_here:
            mentions_text = "@here "
        elif mention_users:
            mentions_text = " ".join([f"<@{user_id}>" for user_id in mention_users]) + " "
    
    # Prepend mentions to message
    full_message = mentions_text + message if mentions_text else message
    
    # Auto-chunk messages over 2000 characters
    MAX_LENGTH = 2000
    if len(full_message) <= MAX_LENGTH:
        chunks = [full_message]
    else:
        # Split by newlines first to preserve message structure
        chunks = []
        current_chunk = ""
        
        for line in full_message.split('\n'):
            if len(current_chunk) + len(line) + 1 <= MAX_LENGTH:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.rstrip('\n'))
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.rstrip('\n'))
        
        # If a single line is too long, force split it
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= MAX_LENGTH:
                final_chunks.append(chunk)
            else:
                # Force split long chunk
                for i in range(0, len(chunk), MAX_LENGTH):
                    final_chunks.append(chunk[i:i+MAX_LENGTH])
        chunks = final_chunks
    
    # Send all chunks
    message_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    sent_messages = []
    
    for i, chunk in enumerate(chunks):
        message_data = {"content": chunk}
        response = requests.post(message_url, headers=headers, json=message_data, timeout=10)
        
        if response.status_code in (200, 201):
            sent_messages.append({
                "message_id": response.json()["id"],
                "chunk": i + 1,
                "total_chunks": len(chunks)
            })
        else:
            return {
                "status": "error", 
                "message": f"Failed to send chunk {i+1}/{len(chunks)}: {response.text}",
                "sent_chunks": sent_messages
            }
    
    return {
        "status": "success",
        "message": f"Message sent to {target_type} {target} ({len(chunks)} chunk{'s' if len(chunks) > 1 else ''})",
        "message_ids": [msg["message_id"] for msg in sent_messages],
        "chunks_sent": len(chunks),
        "channel_id": channel_id,
        "target_type": target_type,
        "mentions_added": bool(mentions_text)
    }

def _read_messages(bot_token, target, target_type, limit, time_filter, timezone, show_both):
    """Read messages from Discord (DM or channel)."""
    headers = {"Authorization": f"Bot {bot_token}"}
    
    # Determine channel ID
    if target_type == "user":
        # Get DM channel
        dm_url = f"https://discord.com/api/v10/users/@me/channels"
        dm_data = {"recipient_id": target}
        dm_response = requests.post(dm_url, headers=headers, json=dm_data, timeout=10)
        if dm_response.status_code != 200:
            return {"status": "error", "message": f"Failed to access DM: {dm_response.text}"}
        channel_id = dm_response.json()["id"]
    else:
        channel_id = target
    
    # Get messages
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    response = requests.get(url, headers=headers, params={"limit": limit}, timeout=10)
    
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to read messages: {response.text}"}
    
    messages = response.json()
    
    # Apply time filtering
    if time_filter != "all":
        messages = _filter_messages_by_time(messages, time_filter, timezone)
    
    # Format messages
    formatted_messages = []
    for msg in messages:
        author = msg["author"]["username"]
        content = msg["content"]
        msg_time = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
        
        if show_both:
            msg_time_local = msg_time.astimezone(ZoneInfo(timezone))
            timestamp_display = f"{msg_time.strftime('%Y-%m-%d %H:%M:%S UTC')} / {msg_time_local.strftime('%Y-%m-%d %H:%M:%S %z')}"
        else:
            msg_time_local = msg_time.astimezone(ZoneInfo(timezone))
            timestamp_display = msg_time_local.strftime("%Y-%m-%d %H:%M:%S %z")
        
        formatted_messages.append({
            "id": msg["id"],
            "author": author,
            "content": content,
            "timestamp": timestamp_display
        })
    
    filter_desc = f" ({time_filter})" if time_filter != "all" else ""
    return {
        "status": "success",
        "message": f"Found {len(formatted_messages)} message(s){filter_desc}",
        "messages": formatted_messages,
        "count": len(formatted_messages),
        "timezone": timezone,
        "time_filter": time_filter
    }


def _download_file(bot_token, message_id, channel_id):
    """Download a file from a Discord message."""
    headers = {"Authorization": f"Bot {bot_token}"}
    
    # Get message
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to get message: {response.text}"}
    
    message = response.json()
    
    if not message.get("attachments"):
        return {"status": "error", "message": "No attachments found in message"}
    
    # Download first attachment
    attachment = message["attachments"][0]
    file_url = attachment["url"]
    filename = attachment["filename"]
    
    # Download file
    file_response = requests.get(file_url, timeout=30)
    if file_response.status_code != 200:
        return {"status": "error", "message": f"Failed to download file: {file_response.text}"}
    
    # Save file
    output_dir = Path("downloaded_files")
    output_dir.mkdir(exist_ok=True)
    
    file_path = output_dir / filename
    with open(file_path, "wb") as f:
        f.write(file_response.content)
    
    return {
        "status": "success",
        "message": f"File downloaded: {filename}",
        "filename": filename,
        "file_path": str(file_path.absolute()),
        "file_size": len(file_response.content)
    }

def _list_channels(bot_token, server_id):
    """List all channels in a Discord server."""
    headers = {"Authorization": f"Bot {bot_token}"}
    
    url = f"https://discord.com/api/v10/guilds/{server_id}/channels"
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to list channels: {response.text}"}
    
    channels = response.json()
    
    # Format channels
    formatted_channels = []
    for channel in channels:
        formatted_channels.append({
            "id": channel["id"],
            "name": channel["name"],
            "type": channel["type"],
            "position": channel.get("position", 0)
        })
    
    return {
        "status": "success",
        "message": f"Found {len(formatted_channels)} channels",
        "channels": formatted_channels,
        "count": len(formatted_channels)
    }

def _create_task(bot_token, tasks_channel_id, default_user_id, task_name, description, 
                schedule, time, specific_date, day_of_month, month, day_of_week, 
                action_type, action_target, action_template):
    """Create a scheduled task with enhanced date/time support."""
    try:
        now = datetime.now()
        one_time = schedule.startswith("in_") or schedule.startswith("tomorrow_") or schedule.startswith("today_at_") or schedule == "on_date"
        
        # --- Calculate next run time ---
        
        # SPECIFIC DATE (one-time)
        if schedule == "on_date" and specific_date:
            # Parse date (support both formats)
            if "." in specific_date:
                # European format: DD.MM.YYYY
                day, month_num, year = map(int, specific_date.split("."))
                next_run = datetime(year, month_num, day, 0, 0, 0)
            elif "-" in specific_date:
                # ISO format: YYYY-MM-DD
                year, month_num, day = map(int, specific_date.split("-"))
                next_run = datetime(year, month_num, day, 0, 0, 0)
            else:
                return {"status": "error", "message": "specific_date must be in format YYYY-MM-DD or DD.MM.YYYY"}
            
            # Set time if provided
            if time:
                hour, minute = map(int, time.split(":"))
                next_run = next_run.replace(hour=hour, minute=minute)
            
            # Validate date is in future
            if next_run <= now:
                return {
                    "status": "error", 
                    "message": f"Date {specific_date} {time or '00:00'} is in the past! Please choose a future date."
                }
        
        # ONE-TIME schedules
        elif schedule.startswith("in_") and schedule.endswith("_minutes"):
            minutes = int(schedule.split("_")[1])
            next_run = now + timedelta(minutes=minutes)
        elif schedule.startswith("in_") and schedule.endswith("_hours"):
            hours = int(schedule.split("_")[1])
            next_run = now + timedelta(hours=hours)
        elif schedule.startswith("in_") and schedule.endswith("_seconds"):
            seconds = int(schedule.split("_")[1])
            next_run = now + timedelta(seconds=seconds)
        elif schedule.startswith("today_at_"):
            time_str = schedule.split("today_at_")[1]
            hour, minute = map(int, time_str.split(":"))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            # If time already passed today, error out
            if next_run <= now:
                return {
                    "status": "error",
                    "message": f"Time {time_str} has already passed today! Current time is {now.strftime('%H:%M')}. Use 'tomorrow_at_{time_str}' or choose a later time."
                }
        elif schedule.startswith("tomorrow_at_"):
            time_str = schedule.split("tomorrow_at_")[1]
            hour, minute = map(int, time_str.split(":"))
            next_run = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # INTERVAL-BASED schedules (every_X_...)
        elif schedule.startswith("every_") and schedule.endswith("_minutes"):
            minutes = int(schedule.split("_")[1])
            next_run = now + timedelta(minutes=minutes)
        elif schedule.startswith("every_") and schedule.endswith("_hours"):
            hours = int(schedule.split("_")[1])
            next_run = now + timedelta(hours=hours)
        elif schedule.startswith("every_") and schedule.endswith("_days"):
            days = int(schedule.split("_")[1])
            next_run = now + timedelta(days=days)
        elif schedule.startswith("every_") and schedule.endswith("_weeks"):
            weeks = int(schedule.split("_")[1])
            next_run = now + timedelta(weeks=weeks)
        
        # SIMPLE RECURRING schedules
        elif schedule == "hourly":
            next_run = now + timedelta(hours=1)
        elif schedule == "minutely":
            next_run = now + timedelta(minutes=1)
        
        # DAILY with specific time
        elif schedule == "daily":
            if time:
                hour, minute = map(int, time.split(":"))
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                # If time already passed today, schedule for tomorrow
                if next_run <= now:
                    next_run += timedelta(days=1)
            else:
                next_run = now + timedelta(days=1)
        
        # WEEKLY with specific day and time
        elif schedule == "weekly":
            if day_of_week:
                # Map day names to numbers (0 = Monday, 6 = Sunday)
                days_map = {
                    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                    "friday": 4, "saturday": 5, "sunday": 6
                }
                target_day = days_map.get(day_of_week.lower())
                if target_day is None:
                    return {"status": "error", "message": f"Invalid day_of_week: {day_of_week}"}
                
                # Calculate days until target day
                current_day = now.weekday()
                days_ahead = target_day - current_day
                if days_ahead <= 0:  # Target day already passed this week
                    days_ahead += 7
                
                next_run = now + timedelta(days=days_ahead)
                
                # Set specific time if provided
                if time:
                    hour, minute = map(int, time.split(":"))
                    next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    # If we calculated today but time passed, add a week
                    if days_ahead == 0 and next_run <= now:
                        next_run += timedelta(weeks=1)
            else:
                # No specific day, just add 7 days
                next_run = now + timedelta(weeks=1)
        
        # MONTHLY with specific day and time
        elif schedule == "monthly":
            if day_of_month:
                # Validate day
                if day_of_month < 1 or day_of_month > 31:
                    return {"status": "error", "message": "day_of_month must be between 1 and 31"}
                
                # Start with current month
                next_run = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                
                # Try to set the target day
                while True:
                    try:
                        next_run = next_run.replace(day=day_of_month)
                        break
                    except ValueError:
                        # Day doesn't exist in this month (e.g. Feb 30)
                        # Move to next month
                        if next_run.month == 12:
                            next_run = next_run.replace(year=next_run.year + 1, month=1)
                        else:
                            next_run = next_run.replace(month=next_run.month + 1)
                
                # Set time if provided
                if time:
                    hour, minute = map(int, time.split(":"))
                    next_run = next_run.replace(hour=hour, minute=minute)
                
                # If this month's date already passed, go to next month
                if next_run <= now:
                    if next_run.month == 12:
                        next_run = next_run.replace(year=next_run.year + 1, month=1)
                    else:
                        next_run = next_run.replace(month=next_run.month + 1)
                    
                    # Re-validate day exists in new month
                    while True:
                        try:
                            next_run = next_run.replace(day=day_of_month)
                            break
                        except ValueError:
                            if next_run.month == 12:
                                next_run = next_run.replace(year=next_run.year + 1, month=1)
                            else:
                                next_run = next_run.replace(month=next_run.month + 1)
            else:
                # No specific day, just add a month
                next_run = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        # YEARLY with specific month, day, and time
        elif schedule == "yearly":
            if month and day_of_month:
                # Validate month and day
                if month < 1 or month > 12:
                    return {"status": "error", "message": "month must be between 1 and 12"}
                if day_of_month < 1 or day_of_month > 31:
                    return {"status": "error", "message": "day_of_month must be between 1 and 31"}
                
                # Try current year first
                try:
                    next_run = now.replace(month=month, day=day_of_month, hour=0, minute=0, second=0, microsecond=0)
                except ValueError:
                    return {"status": "error", "message": f"Invalid date: month={month}, day={day_of_month}"}
                
                # Set time if provided
                if time:
                    hour, minute = map(int, time.split(":"))
                    next_run = next_run.replace(hour=hour, minute=minute)
                
                # If date already passed this year, schedule for next year
                if next_run <= now:
                    next_run = next_run.replace(year=now.year + 1)
            else:
                # No specific date, just add a year
                next_run = now.replace(year=now.year + 1)
        
        else:
            # Default fallback
            next_run = now + timedelta(days=1)
        
        # Create task data
        task_data = {
            "task_name": task_name,
            "description": description,
            "schedule": schedule,
            "time": time,
            "specific_date": specific_date,
            "day_of_month": day_of_month,
            "month": month,
            "day_of_week": day_of_week,
            "action_type": action_type,
            "action_target": action_target or default_user_id,
            "action_template": action_template,
            "one_time": one_time,
            "created_at": now.isoformat(),
            "first_run": now.isoformat(),
            "next_run": next_run.isoformat(),
            "active": True
        }
        
        task_json = json.dumps(task_data, indent=2)
        task_type = "One-time" if one_time else "Recurring"
        
        # Format for Discord (human-readable + JSON)
        action_desc = ""
        if action_type == "user_reminder":
            action_desc = f"Discord DM → User {action_target or default_user_id}"
        elif action_type == "channel_post":
            action_desc = f"Discord Channel → {action_target}"
        
        # Build schedule description
        schedule_desc = schedule
        if specific_date:
            schedule_desc = f"on {specific_date}"
        if day_of_week:
            schedule_desc += f" ({day_of_week}s)"
        if day_of_month and not specific_date:
            schedule_desc += f" (day {day_of_month})"
        if month and not specific_date:
            months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            schedule_desc += f" ({months[month]})"
        if time:
            schedule_desc += f" at {time}"
        
        formatted_message = f"""📋 **Task: {task_name}**
├─ Description: {description}
├─ Schedule: {schedule_desc} ({task_type})
├─ Next Run: {next_run.strftime('%Y-%m-%d %H:%M')}
└─ Action: {action_desc}

```json
{task_json}
```"""
        
        # Post task to Discord channel
        headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
        
        message_url = f"https://discord.com/api/v10/channels/{tasks_channel_id}/messages"
        response = requests.post(
            message_url,
            json={"content": formatted_message},
            headers=headers,
            timeout=10
        )
        
        if response.status_code not in (200, 201):
            return {"status": "error", "message": f"Failed to store task: {response.text}"}
        
        message_id = response.json()["id"]
        
        return {
            "status": "success",
            "message": f"{task_type} task '{task_name}' created and stored!",
            "task_data": task_data,
            "message_id": message_id,
            "next_run": next_run.strftime('%Y-%m-%d %H:%M:%S'),
            "schedule_description": schedule_desc
        }
    
    except ValueError as ve:
        # Handle invalid date/time values
        return {"status": "error", "message": f"Invalid date/time value: {str(ve)}"}
    except Exception as e:
        # Catch-all for other errors
        return {"status": "error", "message": f"Error: {str(e)}"}

def _delete_task(bot_token, message_id, channel_id):
    """Delete a scheduled task."""
    headers = {"Authorization": f"Bot {bot_token}"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
    
    response = requests.delete(url, headers=headers, timeout=10)
    
    if response.status_code == 204:
        return {"status": "success", "message": f"Task message {message_id} deleted"}
    else:
        return {"status": "error", "message": f"Failed to delete: {response.text}"}

def _list_tasks(tasks_channel_id):
    """List all scheduled tasks."""
    return {
        "status": "success",
        "message": "To list tasks, use read_messages action on the tasks channel",
        "instructions": f"Call: discord_tool(action='read_messages', target='{tasks_channel_id}', target_type='channel', limit=100)"
    }


def _filter_messages_by_time(messages, time_filter, timezone):
    """Filter messages by time range."""
    now = datetime.now(ZoneInfo(timezone))
    
    if time_filter == "today":
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter == "yesterday":
        start_time = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter.startswith("last_") and time_filter.endswith("_hours"):
        hours = int(time_filter.split("_")[1])
        start_time = now - timedelta(hours=hours)
    elif time_filter.startswith("last_") and time_filter.endswith("_days"):
        days = int(time_filter.split("_")[1])
        start_time = now - timedelta(days=days)
    else:
        return messages
    
    filtered = []
    for msg in messages:
        msg_time = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
        msg_time_local = msg_time.astimezone(ZoneInfo(timezone))
        
        if time_filter == "yesterday":
            if start_time <= msg_time_local < end_time:
                filtered.append(msg)
        else:
            if msg_time_local >= start_time:
                filtered.append(msg)
    
    return filtered
