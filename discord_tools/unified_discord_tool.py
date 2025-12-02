"""
UNIFIED DISCORD TOOL - Complete Discord Integration for Letta
============================================================

This tool combines core Discord functionality into one powerful tool:
✅ Send messages (DMs and channels)
✅ Read messages (DMs and channels) with advanced filtering
✅ Guild/Server management (list guilds)
✅ Channel management (list channels)
✅ Task scheduling (create/delete/list tasks)

ADVANCED TIME FILTERING:
------------------------
✅ Today between 12-13: start_time="12:00", end_time="13:00"
✅ Yesterday between X-Y: start_time="yesterday 14:00", end_time="yesterday 16:00"
✅ Date X between time Y-Z: start_time="2024-11-07 09:00", end_time="2024-11-07 17:00"
✅ Last Thursday (full day): time_filter="last_thursday"
✅ Last Thursday 10-12: time_filter="last_thursday", start_time="10:00", end_time="12:00"
✅ Keyword search: search_keywords="bug error deployment"
✅ Combined: Weekday + time range + keywords possible!

SMART PAGINATION & RESULT LIMITS:
----------------------------------
✅ Automatically searches the ENTIRE message history (up to 5000 messages back)
✅ Intelligently stops when time range is reached
✅ Returns ONLY messages within the selected time range
✅ Finds messages from days/weeks ago - even in very active chats!
✅ Efficient: Fetches only as many messages as needed
⚠️  Keyword search: Max 10 results (prevents overload, shows newest first)
💡 Best Practice: Combine keywords WITH time filters for precise results!

USAGE EXAMPLES:
---------------

1. SEND MESSAGES:
   discord_tool(action="send_message", message="Hello!", target="1234567890", target_type="channel")
   discord_tool(action="send_message", message="Hi there!", target="1234567890", target_type="user")

2. READ MESSAGES:
   # Basic reading
   discord_tool(action="read_messages", target="1234567890", target_type="channel", limit=50)
   
   # Time filters (predefined - full day)
   discord_tool(action="read_messages", target="1234567890", target_type="channel", time_filter="today")
   discord_tool(action="read_messages", target="1234567890", target_type="channel", time_filter="yesterday")
   discord_tool(action="read_messages", target="1234567890", target_type="channel", time_filter="last_thursday")
   
   # Weekday filter + custom time range!
   discord_tool(action="read_messages", target="1234567890", target_type="channel",
                time_filter="last_thursday", start_time="10:00", end_time="12:00")  # Last Thursday 10-12h!
   
   # Custom time ranges
   discord_tool(action="read_messages", target="1234567890", target_type="channel", 
                start_time="yesterday 12:00", end_time="yesterday 13:00")
   discord_tool(action="read_messages", target="1234567890", target_type="channel",
                start_time="12:00", end_time="13:00")  # Today 12-13!
   discord_tool(action="read_messages", target="1234567890", target_type="channel",
                start_time="2024-11-07 09:00", end_time="2024-11-07 17:00")  # Specific date range
   
   # Keyword search (BEST PRACTICE: Always with time filter!)
   discord_tool(action="read_messages", target="1234567890", target_type="channel", 
                time_filter="last_3_days", search_keywords="bug error")
   
   # Combined filters (RECOMMENDED!)
   discord_tool(action="read_messages", target="1234567890", target_type="channel", 
                time_filter="today", search_keywords="deployment")
   discord_tool(action="read_messages", target="1234567890", target_type="channel",
                time_filter="last_thursday", start_time="10:00", end_time="12:00",
                search_keywords="meeting")

3. LIST GUILDS (ALL SERVERS):
   discord_tool(action="list_guilds")
   discord_tool(action="list_guilds", include_channels=True)  # With channels in one call!

4. LIST CHANNELS:
   discord_tool(action="list_channels", server_id="1234567890")

5. SCHEDULE TASKS:
   # Today at specific time
   discord_tool(action="create_task", task_name="evening_reminder",
                schedule="today_at_18:00", action_type="user_reminder",
                action_template="Check in before dinner!")
   
   # Daily reminder
   discord_tool(action="create_task", task_name="daily_reminder", 
                schedule="daily", time="09:00", action_type="channel_post", 
                action_target="1234567890", action_template="Good morning!")
   
   # Weekly on Saturday at 21:00
   discord_tool(action="create_task", task_name="saturday_checkin",
                schedule="weekly", day_of_week="saturday", time="21:00",
                action_type="user_reminder", action_template="Saturday night check-in!")
   
   # Specific date
   discord_tool(action="create_task", task_name="birthday",
                schedule="on_date", specific_date="25.12.2025", time="10:00",
                action_type="user_reminder", action_template="🎂 Happy Birthday!")
   
   # One-time (in X hours/minutes)
   discord_tool(action="create_task", task_name="quick_reminder", 
                schedule="in_10_hours", action_type="user_reminder",
                action_template="Time to check deployment!")

6. DELETE TASKS:
   discord_tool(action="delete_task", message_id="1234567890", channel_id="1234567890")

7. LIST TASKS:
   discord_tool(action="list_tasks", tasks_channel_id="1234567890")

REAL-WORLD QUERY EXAMPLES:
---------------------------
User asks: "Show me messages from today between 12 and 13"
→ discord_tool(action="read_messages", target="...", start_time="12:00", end_time="13:00")

User asks: "What was written yesterday between 14 and 16?"
→ discord_tool(action="read_messages", target="...", start_time="yesterday 14:00", end_time="yesterday 16:00")

User asks: "Search all messages with 'bug' from last Thursday"
→ discord_tool(action="read_messages", target="...", time_filter="last_thursday", search_keywords="bug")

User asks: "Show me messages from last Thursday between 10 and 12"
→ discord_tool(action="read_messages", target="...", time_filter="last_thursday", start_time="10:00", end_time="12:00")

User asks: "Show me messages from November 5th between 9 and 17"
→ discord_tool(action="read_messages", target="...", start_time="2024-11-05 09:00", end_time="2024-11-05 17:00")

User asks: "What was written last Monday afternoon?"
→ discord_tool(action="read_messages", target="...", time_filter="last_monday", start_time="14:00", end_time="18:00")

User asks: "Search for 'deployment' in the last 3 days"
→ discord_tool(action="read_messages", target="...", time_filter="last_3_days", search_keywords="deployment")
⚠️ NOT: discord_tool(action="read_messages", target="...", search_keywords="deployment") ← Limited to 10, may miss too many matches!

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
    search_keywords: str = None,
    start_time: str = None,
    end_time: str = None,
    # Task parameters
    message_id: str = None,
    channel_id: str = None,
    # Channel parameters
    server_id: str = None,
    include_channels: bool = True,
    # Task parameters (for create_task)
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
    tasks_channel_id: str = None,
    # Batch task management (for manage_tasks)
    list_tasks: bool = False,
    delete_task_ids: list = None,
    create_tasks: list = None,
    # Batch operations (for execute_batch)
    operations: list = None
):
    """
    Unified Discord tool that handles core Discord operations.
    
    Args:
        action: The action to perform (send_message, read_messages,
                list_guilds, list_channels, create_task, delete_task, list_tasks,
                manage_tasks - BATCH task operations,
                execute_batch - ULTIMATE POWER: Execute ANY combination in ONE call!)
        ... (other parameters depend on action)
    
    POWER USER TIP: Use execute_batch to combine multiple operations and save API credits!
    Example: Read messages + List guilds + Manage tasks = 1 API call instead of 3!
    """
    
    # Configuration
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN_HERE")
    TASKS_CHANNEL_ID = os.getenv("TASKS_CHANNEL_ID", "YOUR_TASKS_CHANNEL_ID_HERE")
    HEARTBEAT_LOG_CHANNEL_ID = os.getenv("HEARTBEAT_LOG_CHANNEL_ID", "YOUR_HEARTBEAT_LOG_CHANNEL_ID_HERE")
    # 🔒 HARDCODED: User's Discord User ID (DM restriction - only this user can receive DMs)
    ALLOWED_DM_USER_ID = os.getenv("ALLOWED_DM_USER_ID", "YOUR_USER_ID_HERE")
    DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", ALLOWED_DM_USER_ID)
    
    if DISCORD_BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        return {"status": "error", "message": "Discord bot token not configured. Please set DISCORD_BOT_TOKEN environment variable."}
    
    try:
        if action == "send_message":
            return _send_message(DISCORD_BOT_TOKEN, message, target, target_type, 
                               mention_users, ping_everyone, ping_here, ALLOWED_DM_USER_ID)
        
        elif action == "read_messages":
            return _read_messages(DISCORD_BOT_TOKEN, target, target_type, limit, time_filter, timezone, show_both, search_keywords, start_time, end_time)
        
        elif action == "list_guilds":
            return _list_guilds(DISCORD_BOT_TOKEN, include_channels)
        
        elif action == "list_channels":
            return _list_channels(DISCORD_BOT_TOKEN, server_id)
        
        elif action == "create_task":
            return _create_task(DISCORD_BOT_TOKEN, TASKS_CHANNEL_ID, HEARTBEAT_LOG_CHANNEL_ID, DEFAULT_USER_ID, 
                              task_name, description, schedule, time, specific_date,
                              day_of_month, month, day_of_week, action_type, 
                              action_target, action_template)
        
        elif action == "delete_task":
            return _delete_task(DISCORD_BOT_TOKEN, message_id, channel_id)
        
        elif action == "list_tasks":
            return _list_tasks(DISCORD_BOT_TOKEN, tasks_channel_id or TASKS_CHANNEL_ID)
        
        elif action == "manage_tasks":
            return _manage_tasks(DISCORD_BOT_TOKEN, TASKS_CHANNEL_ID, HEARTBEAT_LOG_CHANNEL_ID, DEFAULT_USER_ID,
                                list_tasks, delete_task_ids, create_tasks)
        
        elif action == "execute_batch":
            if not operations or not isinstance(operations, list):
                return {"status": "error", "message": "execute_batch requires 'operations' parameter as a list"}
            return _execute_batch(operations, DISCORD_BOT_TOKEN, TASKS_CHANNEL_ID, HEARTBEAT_LOG_CHANNEL_ID, DEFAULT_USER_ID, ALLOWED_DM_USER_ID)
        
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}
    
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

def _send_message(bot_token, message, target, target_type, mention_users=None, ping_everyone=False, ping_here=False, allowed_dm_user_id=None):
    """Send a message to Discord (DM or channel) with mentions/pings and auto-chunking."""
    # 🔒 DM RESTRICTION: Only allow DMs to configured user ID
    if not allowed_dm_user_id:
        allowed_dm_user_id = os.getenv("ALLOWED_DM_USER_ID", "YOUR_USER_ID_HERE")
    
    # Check if trying to send DM to unauthorized user (explicit user type)
    if target_type == "user" and target != allowed_dm_user_id:
        return {
            "status": "error",
            "message": f"🔒 DM restriction: Can only send DMs to user {allowed_dm_user_id}, but target was {target}"
        }
    
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
                # 🔒 DM RESTRICTION: Validate after auto-detection
                if target != allowed_dm_user_id:
                    return {
                        "status": "error",
                        "message": f"🔒 DM restriction: Can only send DMs to user {allowed_dm_user_id}, but target was {target}"
                    }
            else:
                channel_id = target
                target_type = "channel"
        except:
            channel_id = target
            target_type = "channel"
    else:
        if target_type == "user":
            # 🔒 DM RESTRICTION: Validate before creating DM channel
            if target != allowed_dm_user_id:
                return {
                    "status": "error",
                    "message": f"🔒 DM restriction: Can only send DMs to user {allowed_dm_user_id}, but target was {target}"
                }
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

def _read_messages(bot_token, target, target_type, limit, time_filter, timezone, show_both, search_keywords=None, start_time=None, end_time=None):
    """Read messages from Discord (DM or channel) with advanced filtering and smart pagination."""
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
    
    # Fetch messages with smart pagination if time filters OR keywords are used
    if time_filter != "all" or start_time or end_time or search_keywords:
        messages = _fetch_messages_with_pagination(bot_token, channel_id, time_filter, timezone, start_time, end_time, limit)
    else:
        # Simple fetch for "all" without any filtering
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        response = requests.get(url, headers=headers, params={"limit": limit}, timeout=10)
        
        if response.status_code != 200:
            return {"status": "error", "message": f"Failed to read messages: {response.text}"}
        
        messages = response.json()
    
    # Apply time filtering
    if time_filter != "all" or start_time or end_time:
        messages = _filter_messages_by_time(messages, time_filter, timezone, start_time, end_time)
    
    # Apply keyword search with result limit
    results_limited = False
    if search_keywords:
        messages = _filter_messages_by_keywords(messages, search_keywords)
        # IMPORTANT: Limit results to prevent overload
        MAX_RESULTS = 10
        if len(messages) > MAX_RESULTS:
            results_limited = True
            original_count = len(messages)
            messages = messages[:MAX_RESULTS]
    
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
    
    # Build filter description
    filter_parts = []
    if time_filter != "all":
        filter_parts.append(f"time: {time_filter}")
    if start_time or end_time:
        filter_parts.append(f"custom range: {start_time or 'start'} - {end_time or 'now'}")
    if search_keywords:
        filter_parts.append(f"keywords: '{search_keywords}'")
    
    filter_desc = f" ({', '.join(filter_parts)})" if filter_parts else ""
    
    # Add warning if results were limited
    message_text = f"Found {len(formatted_messages)} message(s){filter_desc}"
    if results_limited:
        message_text += f" [LIMITED: {original_count} total matches, showing first 10. Add time filter for better results!]"
    
    return {
        "status": "success",
        "message": message_text,
        "messages": formatted_messages,
        "count": len(formatted_messages),
        "timezone": timezone,
        "time_filter": time_filter,
        "search_keywords": search_keywords,
        "results_limited": results_limited
    }

def _fetch_messages_with_pagination(bot_token, channel_id, time_filter, timezone, start_time_str=None, end_time_str=None, max_messages=5000):
    """
    Fetch messages with smart pagination - goes back in time until reaching the desired time range.
    Only returns messages within the specified time range.
    """
    headers = {"Authorization": f"Bot {bot_token}"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    all_messages = []
    oldest_message_id = None
    messages_fetched = 0
    max_iterations = 50  # Safety limit (50 * 100 = 5000 messages max) - increased for active chats
    
    # Calculate the time range we're looking for
    now = datetime.now(ZoneInfo(timezone))
    target_start = None
    target_end = None
    
    # Determine reference day for weekday filters
    reference_day = now
    if time_filter and time_filter.startswith("last_"):
        weekday_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        for day_name, day_num in weekday_map.items():
            if day_name in time_filter.lower():
                days_back = (now.weekday() - day_num) % 7
                if days_back == 0:
                    days_back = 7
                reference_day = now - timedelta(days=days_back)
                break
    
    # Parse time range
    if start_time_str:
        target_start = _parse_time_string(start_time_str, timezone, reference_day)
    elif time_filter == "today":
        target_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter == "yesterday":
        target_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter and time_filter.startswith("last_") and "hours" in time_filter:
        hours = int(time_filter.split("_")[1])
        target_start = now - timedelta(hours=hours)
    elif time_filter and time_filter.startswith("last_") and "days" in time_filter:
        days = int(time_filter.split("_")[1])
        target_start = now - timedelta(days=days)
    elif time_filter and time_filter.startswith("last_"):
        # Weekday filter without custom time - use start of day
        target_start = reference_day.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if end_time_str:
        target_end = _parse_time_string(end_time_str, timezone, reference_day)
    elif time_filter == "yesterday":
        target_end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter and time_filter.startswith("last_") and any(day in time_filter for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
        # Weekday filter without custom time - use end of day
        target_end = reference_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # If no time range specified, just return recent messages
    if not target_start and not target_end:
        response = requests.get(url, headers=headers, params={"limit": 100}, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    
    # Pagination loop
    for iteration in range(max_iterations):
        params = {"limit": 100}
        if oldest_message_id:
            params["before"] = oldest_message_id
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            break
        
        batch = response.json()
        if not batch:
            break
        
        messages_fetched += len(batch)
        
        # Check messages in batch
        for msg in batch:
            msg_time = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
            msg_time_local = msg_time.astimezone(ZoneInfo(timezone))
            
            # Check if message is in our target range
            in_range = True
            if target_start and msg_time_local < target_start:
                in_range = False
            if target_end and msg_time_local > target_end:
                in_range = False
            
            if in_range:
                all_messages.append(msg)
        
        # Check if we've gone too far back in time
        oldest_msg_in_batch = batch[-1]
        oldest_time = datetime.fromisoformat(oldest_msg_in_batch["timestamp"].replace("Z", "+00:00"))
        oldest_time_local = oldest_time.astimezone(ZoneInfo(timezone))
        
        # If oldest message in batch is before our target start, we can stop
        if target_start and oldest_time_local < target_start:
            break
        
        # Set up for next iteration
        oldest_message_id = batch[-1]["id"]
        
        # Safety check
        if messages_fetched >= max_messages:
            break
    
    return all_messages

def _list_guilds(bot_token, include_channels=True):
    """
    List all guilds (servers) the bot is a member of WITH their channels.
    DEFAULT behavior: Shows servers AND channels in ONE call to save API credits.
    Set include_channels=False to only show servers without channels (rare use case).
    """
    headers = {"Authorization": f"Bot {bot_token}"}
    
    url = "https://discord.com/api/v10/users/@me/guilds"
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to list guilds: {response.text}"}
    
    guilds = response.json()
    
    # Format guilds with useful information
    formatted_guilds = []
    for guild in guilds:
        guild_data = {
            "id": guild["id"],
            "name": guild["name"],
            "owner": guild.get("owner", False),
            "permissions": guild.get("permissions", "0"),
            "features": guild.get("features", [])
        }
        
        # Optionally fetch channels for this guild
        if include_channels:
            channels_url = f"https://discord.com/api/v10/guilds/{guild['id']}/channels"
            channels_response = requests.get(channels_url, headers=headers, timeout=10)
            
            if channels_response.status_code == 200:
                channels = channels_response.json()
                guild_data["channels"] = [
                    {
                        "id": channel["id"],
                        "name": channel["name"],
                        "type": channel["type"],
                        "position": channel.get("position", 0)
                    }
                    for channel in channels
                ]
                guild_data["channel_count"] = len(channels)
            else:
                guild_data["channels"] = []
                guild_data["channel_count"] = 0
                guild_data["channels_error"] = f"Failed to fetch channels: {channels_response.status_code}"
        
        formatted_guilds.append(guild_data)
    
    message = f"Found {len(formatted_guilds)} guilds"
    if include_channels:
        total_channels = sum(guild.get("channel_count", 0) for guild in formatted_guilds)
        message += f" with {total_channels} total channels"
    
    return {
        "status": "success",
        "message": message,
        "guilds": formatted_guilds,
        "count": len(formatted_guilds),
        "include_channels": include_channels
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

def _create_task(bot_token, tasks_channel_id, heartbeat_log_channel_id, default_user_id, task_name, description, 
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
        # 🎯 Smart defaults when action_target is not explicitly set:
        # - user_reminder → User's DMs (DEFAULT_USER_ID)
        # - self_task, channel_post, etc. → Heartbeat Log Channel
        if not action_target:
            if action_type == "user_reminder":
                final_action_target = default_user_id  # 💬 DMs
            else:
                final_action_target = heartbeat_log_channel_id  # 🧠 Heartbeat space
        else:
            final_action_target = action_target  # ✅ Explicit target set
        
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
            "action_target": final_action_target,
            "action_template": action_template,
            "one_time": one_time,
            "created_at": now.isoformat(),
            "first_run": now.isoformat(),
            "next_run": next_run.isoformat(),
            "active": True
        }
        
        # Post to tasks channel
        headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}
        message_url = f"https://discord.com/api/v10/channels/{tasks_channel_id}/messages"
        
        # Build schedule info line
        schedule_info = f"{schedule}"
        if time:
            schedule_info += f" at {time}"
        if next_run:
            next_run_readable = next_run.strftime("%Y-%m-%d %H:%M:%S")
            schedule_info += f" (runs at: {next_run_readable})"
        
        # Build action description with smart defaults shown
        if not action_target:
            if action_type == "user_reminder":
                action_desc = f"{action_type} → 💬 User's DMs (default)"
            else:
                action_desc = f"{action_type} → 🧠 Heartbeat Log (default)"
        else:
            action_desc = f"{action_type} → {action_target}"
        
        formatted_message = f"""📋 **Task: {task_name}**
├─ Description: {description}
├─ Schedule: {schedule_info}
├─ One-time: {"Yes" if one_time else "No"}
└─ Action: {action_desc}

```json
{json.dumps(task_data, indent=2)}
```"""
        
        response = requests.post(message_url, json={"content": formatted_message}, headers=headers, timeout=10)
        
        if response.status_code in (200, 201):
            return {
                "status": "success",
                "message": f"Task '{task_name}' created!",
                "task_data": task_data,
                "message_id": response.json()["id"],
                "next_run": next_run.strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {"status": "error", "message": f"Failed to create task: {response.text}"}
    
    except ValueError as ve:
        # Handle invalid date/time values
        return {"status": "error", "message": f"Invalid date/time value: {str(ve)}"}
    except Exception as e:
        # Catch-all for other errors
        return {"status": "error", "message": f"Error creating task: {str(e)}"}

def _delete_task(bot_token, message_id, channel_id):
    """Delete a scheduled task."""
    headers = {"Authorization": f"Bot {bot_token}"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
    
    response = requests.delete(url, headers=headers, timeout=10)
    
    if response.status_code == 204:
        return {"status": "success", "message": f"Task message {message_id} deleted"}
    else:
        return {"status": "error", "message": f"Failed to delete: {response.text}"}

def _list_tasks(bot_token, tasks_channel_id):
    """
    List all scheduled tasks from the tasks channel.
    Fetches and parses task messages to show current scheduled tasks.
    
    💰 TIP: Use manage_tasks instead to combine list + delete + create in ONE call!
    """
    headers = {"Authorization": f"Bot {bot_token}"}
    
    try:
        # Fetch messages from tasks channel
        url = f"https://discord.com/api/v10/channels/{tasks_channel_id}/messages"
        response = requests.get(url, headers=headers, params={"limit": 100}, timeout=10)
        
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"Failed to fetch tasks: HTTP {response.status_code}",
                "error": response.text
            }
        
        messages = response.json()
        
        # Parse task messages (contain ```json blocks)
        tasks = []
        for msg in messages:
            content = msg.get('content', '')
            if '```json' in content:
                try:
                    # Extract JSON from code block
                    json_start = content.find('```json') + 7
                    json_end = content.find('```', json_start)
                    if json_end > json_start:
                        task_json = content[json_start:json_end].strip()
                        task_data = json.loads(task_json)
                        task_data['message_id'] = msg['id']  # Add message ID for reference
                        tasks.append(task_data)
                except (json.JSONDecodeError, ValueError):
                    continue
        
        return {
            "status": "success",
            "message": f"Found {len(tasks)} scheduled task(s) in channel {tasks_channel_id}",
            "tasks": tasks,
            "count": len(tasks),
            "total_messages": len(messages)
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error listing tasks: {str(e)}"
        }

def _manage_tasks(bot_token, tasks_channel_id, heartbeat_log_channel_id, default_user_id, list_tasks, delete_task_ids, create_tasks):
    """
    Batch task management - list, delete, and create tasks in ONE API call.
    Saves API credits by combining operations.
    """
    results = {
        "status": "success",
        "operations_performed": [],
        "tasks_listed": None,
        "tasks_deleted": [],
        "tasks_created": [],
        "errors": []
    }
    
    headers = {"Authorization": f"Bot {bot_token}"}
    
    # STEP 1: List tasks (if requested)
    if list_tasks:
        try:
            url = f"https://discord.com/api/v10/channels/{tasks_channel_id}/messages"
            response = requests.get(url, headers=headers, params={"limit": 100}, timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                task_count = len([m for m in messages if '```json' in m.get('content', '')])
                results["tasks_listed"] = {
                    "count": task_count,
                    "total_messages": len(messages),
                    "message": f"Found {task_count} task(s) in channel"
                }
                results["operations_performed"].append("list")
            else:
                results["errors"].append({
                    "operation": "list_tasks",
                    "error": f"Failed to fetch tasks: HTTP {response.status_code}"
                })
        except Exception as e:
            results["errors"].append({
                "operation": "list_tasks",
                "error": f"Exception: {str(e)}"
            })
    
    # STEP 2: Delete tasks (if requested)
    if delete_task_ids:
        results["operations_performed"].append("delete")
        
        for task_id in delete_task_ids:
            try:
                if not task_id:
                    continue
                    
                delete_url = f"https://discord.com/api/v10/channels/{tasks_channel_id}/messages/{task_id}"
                response = requests.delete(delete_url, headers=headers, timeout=10)
                
                if response.status_code == 204:
                    results["tasks_deleted"].append({
                        "message_id": task_id,
                        "status": "success"
                    })
                else:
                    results["tasks_deleted"].append({
                        "message_id": task_id,
                        "status": "failed",
                        "error": f"HTTP {response.status_code}: {response.text}"
                    })
                    results["errors"].append({
                        "operation": "delete_task",
                        "task_id": task_id,
                        "error": f"Failed to delete: {response.text}"
                    })
            except Exception as e:
                results["tasks_deleted"].append({
                    "message_id": task_id,
                    "status": "error",
                    "error": str(e)
                })
                results["errors"].append({
                    "operation": "delete_task",
                    "task_id": task_id,
                    "error": f"Exception: {str(e)}"
                })
    
    # STEP 3: Create new tasks (if requested)
    if create_tasks and isinstance(create_tasks, list):
        results["operations_performed"].append("create")
        
        for i, task_spec in enumerate(create_tasks):
            try:
                # Validate required fields
                if not isinstance(task_spec, dict):
                    results["errors"].append({
                        "operation": "create_task",
                        "task_index": i,
                        "error": "Task spec must be a dictionary"
                    })
                    continue
                
                if "task_name" not in task_spec or "schedule" not in task_spec:
                    results["errors"].append({
                        "operation": "create_task",
                        "task_index": i,
                        "error": "Missing required fields: task_name and schedule"
                    })
                    continue
                
                # Call the create task function (reuse existing logic)
                task_result = _create_task(
                    bot_token, 
                    tasks_channel_id,
                    heartbeat_log_channel_id,
                    default_user_id,
                    task_spec.get("task_name"),
                    task_spec.get("description"),
                    task_spec.get("schedule"),
                    task_spec.get("time"),
                    task_spec.get("specific_date"),
                    task_spec.get("day_of_month"),
                    task_spec.get("month"),
                    task_spec.get("day_of_week"),
                    task_spec.get("action_type"),
                    task_spec.get("action_target"),
                    task_spec.get("action_template")
                )
                
                if task_result.get("status") == "success":
                    results["tasks_created"].append({
                        "task_name": task_spec.get("task_name"),
                        "status": "success",
                        "message_id": task_result.get("message_id")
                    })
                else:
                    results["tasks_created"].append({
                        "task_name": task_spec.get("task_name"),
                        "status": "failed",
                        "error": task_result.get("message")
                    })
                    results["errors"].append({
                        "operation": "create_task",
                        "task_name": task_spec.get("task_name"),
                        "error": task_result.get("message")
                    })
            except Exception as e:
                results["tasks_created"].append({
                    "task_name": task_spec.get("task_name", f"task_{i}"),
                    "status": "error",
                    "error": str(e)
                })
                results["errors"].append({
                    "operation": "create_task",
                    "task_index": i,
                    "error": f"Exception: {str(e)}"
                })
    
    # Build summary message
    summary_parts = []
    if results["tasks_listed"]:
        summary_parts.append(f"Listed {results['tasks_listed']['count']} tasks")
    if results["tasks_deleted"]:
        success_deletes = len([t for t in results["tasks_deleted"] if t["status"] == "success"])
        summary_parts.append(f"Deleted {success_deletes}/{len(results['tasks_deleted'])} tasks")
    if results["tasks_created"]:
        success_creates = len([t for t in results["tasks_created"] if t["status"] == "success"])
        summary_parts.append(f"Created {success_creates}/{len(results['tasks_created'])} tasks")
    
    # Determine overall status
    if results["errors"]:
        if summary_parts:
            results["status"] = "partial_success"
            results["message"] = f"Partial success: {', '.join(summary_parts)}. {len(results['errors'])} error(s) occurred."
        else:
            results["status"] = "error"
            results["message"] = f"All operations failed. {len(results['errors'])} error(s) occurred."
    else:
        if summary_parts:
            results["message"] = f"Success: {', '.join(summary_parts)}"
        else:
            results["message"] = "No operations performed (nothing requested)"
    
    return results

def _execute_batch(operations, bot_token, tasks_channel_id, heartbeat_log_channel_id, default_user_id, allowed_dm_user_id):
    """
    Execute multiple Discord operations in ONE API call.
    MASSIVE API credit savings by batching operations together.
    
    Each operation is executed independently - if one fails, others continue.
    """
    results = {
        "status": "success",
        "total_operations": len(operations),
        "successful_operations": 0,
        "failed_operations": 0,
        "operation_results": [],
        "errors": []
    }
    
    for i, operation in enumerate(operations):
        operation_result = {
            "operation_index": i,
            "action": operation.get("action", "unknown"),
            "status": "pending"
        }
        
        try:
            # Validate operation structure
            if not isinstance(operation, dict):
                operation_result["status"] = "error"
                operation_result["error"] = "Operation must be a dictionary"
                results["failed_operations"] += 1
                results["errors"].append({
                    "operation_index": i,
                    "error": "Operation must be a dictionary"
                })
                results["operation_results"].append(operation_result)
                continue
            
            action = operation.get("action")
            if not action:
                operation_result["status"] = "error"
                operation_result["error"] = "Missing 'action' parameter"
                results["failed_operations"] += 1
                results["errors"].append({
                    "operation_index": i,
                    "error": "Missing 'action' parameter"
                })
                results["operation_results"].append(operation_result)
                continue
            
            # Prevent recursive execute_batch (security/performance)
            if action == "execute_batch":
                operation_result["status"] = "error"
                operation_result["error"] = "Recursive execute_batch not allowed"
                results["failed_operations"] += 1
                results["errors"].append({
                    "operation_index": i,
                    "action": action,
                    "error": "Recursive execute_batch not allowed"
                })
                results["operation_results"].append(operation_result)
                continue
            
            # Execute the operation by calling the appropriate internal function
            # Map actions to their handler functions
            if action == "send_message":
                result = _send_message(
                    bot_token,
                    operation.get("message"),
                    operation.get("target"),
                    operation.get("target_type"),
                    operation.get("mention_users"),
                    operation.get("ping_everyone", False),
                    operation.get("ping_here", False),
                    allowed_dm_user_id
                )
            elif action == "read_messages":
                result = _read_messages(
                    bot_token,
                    operation.get("target"),
                    operation.get("target_type"),
                    operation.get("limit", 50),
                    operation.get("time_filter", "all"),
                    operation.get("timezone", "Europe/Berlin"),
                    operation.get("show_both", True),
                    operation.get("search_keywords"),
                    operation.get("start_time"),
                    operation.get("end_time")
                )
            elif action == "list_guilds":
                result = _list_guilds(
                    bot_token,
                    operation.get("include_channels", True)
                )
            elif action == "list_channels":
                result = _list_channels(
                    bot_token,
                    operation.get("server_id")
                )
            elif action == "create_task":
                result = _create_task(
                    bot_token,
                    tasks_channel_id,
                    heartbeat_log_channel_id,
                    default_user_id,
                    operation.get("task_name"),
                    operation.get("description"),
                    operation.get("schedule"),
                    operation.get("time"),
                    operation.get("specific_date"),
                    operation.get("day_of_month"),
                    operation.get("month"),
                    operation.get("day_of_week"),
                    operation.get("action_type"),
                    operation.get("action_target"),
                    operation.get("action_template")
                )
            elif action == "delete_task":
                result = _delete_task(
                    bot_token,
                    operation.get("message_id"),
                    operation.get("channel_id")
                )
            elif action == "list_tasks":
                result = _list_tasks(
                    bot_token,
                    operation.get("tasks_channel_id", tasks_channel_id)
                )
            elif action == "manage_tasks":
                result = _manage_tasks(
                    bot_token,
                    tasks_channel_id,
                    heartbeat_log_channel_id,
                    default_user_id,
                    operation.get("list_tasks", False),
                    operation.get("delete_task_ids"),
                    operation.get("create_tasks")
                )
            else:
                result = {"status": "error", "message": f"Unknown action: {action}"}
            
            # Store result
            operation_result["status"] = result.get("status", "unknown")
            operation_result["result"] = result
            
            if result.get("status") == "success":
                results["successful_operations"] += 1
            else:
                results["failed_operations"] += 1
                results["errors"].append({
                    "operation_index": i,
                    "action": action,
                    "error": result.get("message", "Unknown error")
                })
        
        except Exception as e:
            operation_result["status"] = "error"
            operation_result["error"] = str(e)
            results["failed_operations"] += 1
            results["errors"].append({
                "operation_index": i,
                "action": operation.get("action", "unknown"),
                "error": f"Exception: {str(e)}"
            })
        
        results["operation_results"].append(operation_result)
    
    # Determine overall status
    if results["failed_operations"] == 0:
        results["status"] = "success"
        results["message"] = f"All {results['successful_operations']} operations completed successfully"
    elif results["successful_operations"] == 0:
        results["status"] = "error"
        results["message"] = f"All {results['failed_operations']} operations failed"
    else:
        results["status"] = "partial_success"
        results["message"] = f"Partial success: {results['successful_operations']} succeeded, {results['failed_operations']} failed"
    
    return results


def _filter_messages_by_time(messages, time_filter, timezone, custom_start=None, custom_end=None):
    """Filter messages by time range with support for custom times."""
    now = datetime.now(ZoneInfo(timezone))
    start_time = None
    end_time = None
    reference_day = now  # Default reference day is today
    
    # First, check if we have a weekday filter to determine the reference day
    if time_filter and time_filter.startswith("last_"):
        weekday_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        for day_name, day_num in weekday_map.items():
            if day_name in time_filter.lower():
                days_back = (now.weekday() - day_num) % 7
                if days_back == 0:
                    days_back = 7  # Last occurrence, not today
                reference_day = now - timedelta(days=days_back)
                # If no custom times, use full day
                if not custom_start and not custom_end:
                    start_time = reference_day.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_time = reference_day.replace(hour=23, minute=59, second=59, microsecond=999999)
                break
    
    # Parse custom time ranges (using reference_day if weekday filter was set)
    if custom_start:
        start_time = _parse_time_string(custom_start, timezone, reference_day)
    
    if custom_end:
        end_time = _parse_time_string(custom_end, timezone, reference_day)
    
    # Apply other predefined time filters if not already set
    if not start_time and not end_time:
        if time_filter == "today":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_filter == "yesterday":
            start_time = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_filter and time_filter.startswith("last_") and time_filter.endswith("_hours"):
            hours = int(time_filter.split("_")[1])
            start_time = now - timedelta(hours=hours)
        elif time_filter and time_filter.startswith("last_") and time_filter.endswith("_days"):
            days = int(time_filter.split("_")[1])
            start_time = now - timedelta(days=days)
    
    # If no time filter applied, return all messages
    if not start_time and not end_time:
        return messages
    
    # Filter messages
    filtered = []
    for msg in messages:
        msg_time = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
        msg_time_local = msg_time.astimezone(ZoneInfo(timezone))
        
        # Check if message is within range
        if start_time and end_time:
            if start_time <= msg_time_local <= end_time:
                filtered.append(msg)
        elif start_time:
            if msg_time_local >= start_time:
                filtered.append(msg)
        elif end_time:
            if msg_time_local <= end_time:
                filtered.append(msg)
    
    return filtered

def _parse_time_string(time_str, timezone, reference_time):
    """Parse flexible time strings like '12:00', 'yesterday 14:30', '2024-11-07 10:00'."""
    time_str = time_str.strip().lower()
    
    try:
        # ISO format: "2024-11-07 10:00" or "2024-11-07T10:00:00"
        if "t" in time_str or len(time_str.split("-")) == 3:
            if "t" in time_str:
                parsed = datetime.fromisoformat(time_str)
            else:
                parsed = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            return parsed.replace(tzinfo=ZoneInfo(timezone))
        
        # Time only: "12:00" or "14:30"
        if ":" in time_str and " " not in time_str:
            time_parts = time_str.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            return reference_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Relative day + time: "yesterday 14:30", "today 09:00"
        if " " in time_str:
            parts = time_str.split(" ", 1)
            day_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else "00:00"
            
            # Parse time
            time_parts = time_part.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            
            # Parse day
            if day_part == "yesterday":
                base_time = reference_time - timedelta(days=1)
            elif day_part == "today":
                base_time = reference_time
            else:
                base_time = reference_time
            
            return base_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
    except (ValueError, IndexError):
        pass
    
    # Fallback: return reference time
    return reference_time

def _filter_messages_by_keywords(messages, keywords):
    """Filter messages by keyword search (case-insensitive, supports multiple keywords)."""
    if not keywords:
        return messages
    
    # Split keywords by comma or space
    keyword_list = [k.strip().lower() for k in keywords.replace(",", " ").split() if k.strip()]
    
    filtered = []
    for msg in messages:
        content = msg.get("content", "").lower()
        # Check if ANY keyword matches
        if any(keyword in content for keyword in keyword_list):
            filtered.append(msg)
    
    return filtered
