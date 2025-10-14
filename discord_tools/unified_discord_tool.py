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
   discord_tool(action="create_task", task_name="reminder", description="Daily reminder", 
                schedule="daily", time="09:00", action_type="channel_post", 
                action_target="1234567890", action_template="Good morning!")

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
                              task_name, description, schedule, time, action_type, 
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
                schedule, time, action_type, action_target, action_template):
    """Create a scheduled task."""
    # This is a simplified version - you can expand this with full scheduling logic
    now = datetime.now()
    
    task_data = {
        "task_name": task_name,
        "description": description,
        "schedule": schedule,
        "time": time,
        "action_type": action_type,
        "action_target": action_target or default_user_id,
        "action_template": action_template,
        "created_at": now.isoformat(),
        "active": True
    }
    
    # Post to tasks channel
    headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}
    message_url = f"https://discord.com/api/v10/channels/{tasks_channel_id}/messages"
    
    formatted_message = f"""📋 **Task: {task_name}**
├─ Description: {description}
├─ Schedule: {schedule} at {time or 'default time'}
└─ Action: {action_type} → {action_target or default_user_id}

```json
{json.dumps(task_data, indent=2)}
```"""
    
    response = requests.post(message_url, json={"content": formatted_message}, headers=headers, timeout=10)
    
    if response.status_code in (200, 201):
        return {
            "status": "success",
            "message": f"Task '{task_name}' created!",
            "task_data": task_data,
            "message_id": response.json()["id"]
        }
    else:
        return {"status": "error", "message": f"Failed to create task: {response.text}"}

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
