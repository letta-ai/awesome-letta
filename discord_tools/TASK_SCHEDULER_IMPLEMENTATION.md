# Task Scheduler Implementation Guide

This guide explains how to implement an external scheduler that reads tasks from the Tasks Channel and executes them. The Unified Discord Tool creates tasks, but you need a scheduler to actually run them.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Implementation Options](#implementation-options)
4. [Python Scheduler Example](#python-scheduler-example)
5. [Node.js/TypeScript Scheduler Example](#nodejstypescript-scheduler-example)
6. [Integration with Letta AI](#integration-with-letta-ai)

---

## Overview

The Task Scheduler system works in two parts:

1. **Task Creation** (Unified Discord Tool)
   - Creates tasks as Discord messages in the Tasks Channel
   - Formats tasks as JSON in code blocks
   - Sets `next_run` timestamps automatically

2. **Task Execution** (External Scheduler)
   - Reads tasks from the Tasks Channel periodically
   - Checks if tasks are due (`next_run <= now`)
   - Executes tasks (sends to Letta AI, posts messages, etc.)
   - Updates recurring tasks or deletes one-time tasks

**💡 Recommended**: Use the provided [`taskScheduler.ts`](./taskScheduler.ts) file - it's production-ready and handles all edge cases!

---

## Architecture

### How It Works

```
┌─────────────────────┐
│ Unified Discord    │
│ Tool (Python)      │───► Creates tasks in Tasks Channel
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Tasks Channel       │
│ (Discord)           │───► Stores tasks as JSON messages
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ External Scheduler  │───► Reads tasks every 60 seconds
│ (Your Bot/Script)   │───► Executes due tasks
└─────────────────────┘───► Updates/deletes tasks
```

### Task Message Format

Tasks are stored as Discord messages with this format:

````
📋 **Task: Morning Reminder**
├─ Description: Daily good morning message
├─ Schedule: daily at 09:00
├─ Next Run: 2025-01-16 09:00:00
└─ Action: user_reminder → 123456789012345678

```json
{
  "task_name": "Morning Reminder",
  "description": "Daily good morning message",
  "schedule": "daily",
  "time": "09:00",
  "next_run": "2025-01-16T09:00:00",
  "one_time": false,
  "active": true,
  "action_type": "user_reminder",
  "action_target": "123456789012345678",
  "action_template": "Good morning! ☀️"
}
```
````

---

## Implementation Options

### Option 1: Python Scheduler (Recommended for Letta)

- ✅ Easy integration with Letta AI
- ✅ Can use Unified Discord Tool to read tasks
- ✅ Simple to set up and maintain

### Option 2: Node.js/TypeScript Scheduler

- ✅ Good for Discord.js bots
- ✅ Type-safe with TypeScript
- ✅ Native Discord.js integration

### Option 3: Cron Job + Script

- ✅ Simple and reliable
- ✅ Works with any language
- ✅ Easy to schedule

---

## Python Scheduler Example

### Basic Structure

```python
import requests
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TASKS_CHANNEL_ID = os.getenv("TASKS_CHANNEL_ID")
HEARTBEAT_LOG_CHANNEL_ID = os.getenv("HEARTBEAT_LOG_CHANNEL_ID")
LETTA_API_KEY = os.getenv("LETTA_API_KEY")
LETTA_AGENT_ID = os.getenv("LETTA_AGENT_ID")

def read_tasks_from_channel():
    """Read tasks from Discord channel."""
    url = f"https://discord.com/api/v10/channels/{TASKS_CHANNEL_ID}/messages?limit=100"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return []
    
    messages = response.json()
    tasks = []
    
    for msg in messages:
        content = msg.get('content', '')
        if '```json' in content:
            # Extract JSON from code block
            json_start = content.find('```json') + 7
            json_end = content.find('```', json_start)
            if json_end > json_start:
                try:
                    task_json = content[json_start:json_end].strip()
                    task = json.loads(task_json)
                    task['message_id'] = msg['id']
                    tasks.append(task)
                except json.JSONDecodeError:
                    continue
    
    return tasks

def check_due_tasks(tasks):
    """Check which tasks are due for execution."""
    now = datetime.now(ZoneInfo("UTC"))
    due = []
    
    for task in tasks:
        if not task.get('active', True):
            continue
        
        next_run_str = task.get('next_run')
        if not next_run_str:
            continue
        
        # Parse next_run (handle timezone)
        if 'Z' in next_run_str or '+' in next_run_str or next_run_str.count('-') > 2:
            next_run = datetime.fromisoformat(next_run_str.replace('Z', '+00:00'))
        else:
            # No timezone - interpret as Berlin time
            next_run = datetime.fromisoformat(next_run_str).replace(tzinfo=ZoneInfo("Europe/Berlin"))
            next_run = next_run.astimezone(ZoneInfo("UTC"))
        
        if next_run <= now:
            due.append(task)
    
    return due

def execute_task(task):
    """Execute a task by sending it to Letta AI."""
    action_type = task.get('action_type', 'self_task')
    action_target = task.get('action_target')
    action_template = task.get('action_template', '')
    
    # Determine target channel
    if action_type == 'user_reminder':
        # Open DM channel to user
        target_channel_id = action_target
        # ... implement DM channel creation ...
    elif action_type == 'channel_post':
        target_channel_id = action_target or HEARTBEAT_LOG_CHANNEL_ID
    else:  # self_task
        target_channel_id = action_target or HEARTBEAT_LOG_CHANNEL_ID
    
    # Send to Letta AI
    task_message = f"[⏰ SCHEDULED TASK TRIGGERED]\n\nTask: {task.get('task_name')}\n\n{action_template}"
    
    # Call Letta AI API
    # ... implement Letta API call ...
    
    return True

def update_recurring_task(task):
    """Update a recurring task with new next_run time."""
    # Calculate next run based on schedule
    # ... implement schedule calculation ...
    
    # Update message in Discord channel
    # ... implement message update ...
    
    return True

def delete_task(message_id):
    """Delete a one-time task after execution."""
    url = f"https://discord.com/api/v10/channels/{TASKS_CHANNEL_ID}/messages/{message_id}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    
    response = requests.delete(url, headers=headers, timeout=10)
    return response.status_code == 204

def scheduler_loop():
    """Main scheduler loop - runs every 60 seconds."""
    while True:
        try:
            tasks = read_tasks_from_channel()
            due = check_due_tasks(tasks)
            
            for task in due:
                execute_task(task)
                
                if task.get('one_time', False):
                    delete_task(task['message_id'])
                else:
                    update_recurring_task(task)
        
        except Exception as e:
            print(f"Error in scheduler: {e}")
        
        time.sleep(60)  # Wait 60 seconds

if __name__ == "__main__":
    scheduler_loop()
```

### Using with Unified Discord Tool

You can use the Unified Discord Tool to read tasks:

```python
from unified_discord_tool import discord_tool

def read_tasks():
    """Read tasks using Unified Discord Tool."""
    result = discord_tool(
        action="read_messages",
        target=TASKS_CHANNEL_ID,
        target_type="channel",
        limit=100
    )
    
    if result.get('status') == 'success':
        messages = result.get('messages', [])
        tasks = []
        
        for msg in messages:
            content = msg.get('content', '')
            if '```json' in content:
                # Parse JSON task
                # ... extract and parse ...
        
        return tasks
    
    return []
```

---

## Node.js/TypeScript Scheduler Example

### Ready-to-Use Implementation

**We provide a complete, production-ready TypeScript implementation!**

📁 **File**: [`taskScheduler.ts`](./taskScheduler.ts)

This is a fully functional scheduler that:
- ✅ Reads tasks from Discord channel every 60 seconds
- ✅ Handles timezone conversion (Berlin time → UTC)
- ✅ Supports all schedule types from the Unified Discord Tool
- ✅ Processes tasks sequentially to prevent API overload
- ✅ Includes deduplication to prevent duplicate executions
- ✅ Updates recurring tasks automatically
- ✅ Deletes one-time tasks after execution

### Quick Setup

1. **Copy the file**:
   ```bash
   cp taskScheduler.ts your-bot/src/taskScheduler.ts
   ```

2. **Install dependencies**:
   ```bash
   npm install discord.js axios
   ```

3. **Set environment variables**:
   ```env
   DISCORD_TOKEN=your_bot_token
   TASKS_CHANNEL_ID=your_tasks_channel_id
   HEARTBEAT_LOG_CHANNEL_ID=your_heartbeat_log_channel_id
   DISCORD_CHANNEL_ID=your_default_channel_id
   ```

4. **Implement `sendTaskMessage()`** in your `messages.ts`:
   ```typescript
   export async function sendTaskMessage(
     task: Task,
     channel?: TextChannel,
     client?: Client
   ): Promise<void> {
     // Send task to your AI agent (e.g., Letta AI)
     // ... your implementation ...
   }
   ```

5. **Initialize in your bot**:
   ```typescript
   import { startTaskCheckerLoop } from './taskScheduler';
   
   client.once('ready', async () => {
     console.log('Bot is ready!');
     startTaskCheckerLoop(client);
   });
   ```

### Basic Structure (Reference)

If you want to build your own, here's the basic structure:

```typescript
import axios from 'axios';
import { Client, TextChannel } from 'discord.js';

const DISCORD_TOKEN = process.env.DISCORD_BOT_TOKEN || '';
const TASKS_CHANNEL_ID = process.env.TASKS_CHANNEL_ID || '';
const HEARTBEAT_LOG_CHANNEL_ID = process.env.HEARTBEAT_LOG_CHANNEL_ID || '';

interface Task {
  task_name?: string;
  next_run?: string;
  active?: boolean;
  one_time?: boolean;
  schedule?: string;
  time?: string;
  message_id?: string;
  action_type?: string;
  action_target?: string;
  action_template?: string;
  [key: string]: unknown;
}

async function readTasksFromChannel(): Promise<Task[]> {
  const url = `https://discord.com/api/v10/channels/${TASKS_CHANNEL_ID}/messages?limit=100`;
  const headers = { Authorization: `Bot ${DISCORD_TOKEN}` };
  
  const response = await axios.get(url, { headers, timeout: 10000 });
  if (response.status !== 200) return [];
  
  const messages = response.data || [];
  const tasks: Task[] = [];
  
  for (const msg of messages) {
    const content = String(msg?.content || '');
    if (content.includes('```json')) {
      const jsonStart = content.indexOf('```json') + 7;
      const jsonEnd = content.indexOf('```', jsonStart);
      if (jsonEnd > jsonStart) {
        try {
          const taskJson = content.substring(jsonStart, jsonEnd).trim();
          const task = JSON.parse(taskJson) as Task;
          task.message_id = msg.id;
          tasks.push(task);
        } catch (e) {
          // Ignore invalid JSON
        }
      }
    }
  }
  
  return tasks;
}

function checkDueTasks(tasks: Task[]): Task[] {
  const now = new Date();
  const due: Task[] = [];
  
  for (const task of tasks) {
    if (task.active === false) continue;
    const nextRunStr = task.next_run;
    if (!nextRunStr) continue;
    
    const nextRun = new Date(nextRunStr);
    if (!isNaN(nextRun.getTime()) && nextRun <= now) {
      due.push(task);
    }
  }
  
  return due;
}

async function executeTask(task: Task, client: Client): Promise<boolean> {
  const actionType = task.action_type || 'self_task';
  const actionTarget = task.action_target;
  
  let targetChannel: TextChannel | undefined;
  
  if (actionType === 'user_reminder' && actionTarget) {
    try {
      const user = await client.users.fetch(actionTarget);
      const dmChannel = await user.createDM();
      targetChannel = dmChannel as any;
    } catch (e) {
      console.error('Failed to open DM:', e);
    }
  } else if (actionType === 'channel_post' || actionType === 'self_task') {
    const channelId = actionTarget || HEARTBEAT_LOG_CHANNEL_ID;
    if (channelId) {
      try {
        const ch = await client.channels.fetch(channelId);
        if (ch && 'send' in ch) {
          targetChannel = ch as TextChannel;
        }
      } catch (e) {
        console.error('Failed to fetch channel:', e);
      }
    }
  }
  
  if (targetChannel) {
    const message = `[⏰ SCHEDULED TASK TRIGGERED]\n\nTask: ${task.task_name}\n\n${task.action_template || ''}`;
    await targetChannel.send(message);
    return true;
  }
  
  return false;
}

async function updateRecurringTask(task: Task): Promise<boolean> {
  // Calculate next run based on schedule
  // ... implement schedule calculation ...
  
  // Update message in Discord
  // ... implement message update ...
  
  return true;
}

async function deleteTask(messageId: string): Promise<boolean> {
  const url = `https://discord.com/api/v10/channels/${TASKS_CHANNEL_ID}/messages/${messageId}`;
  const headers = { Authorization: `Bot ${DISCORD_TOKEN}` };
  
  const response = await axios.delete(url, { headers, timeout: 10000 });
  return response.status === 204;
}

export function startTaskScheduler(client: Client): void {
  console.log('🗓️  Task Scheduler started');
  
  setInterval(async () => {
    try {
      const tasks = await readTasksFromChannel();
      const due = checkDueTasks(tasks);
      
      for (const task of due) {
        const success = await executeTask(task, client);
        if (success) {
          if (task.one_time) {
            await deleteTask(task.message_id!);
          } else {
            await updateRecurringTask(task);
          }
        }
      }
    } catch (e) {
      console.error('Error in scheduler:', e);
    }
  }, 60000); // Check every 60 seconds
}
```

---

## Integration with Letta AI

### Sending Tasks to Letta

When executing a task, you can send it to your Letta AI agent:

```python
import requests

def send_to_letta(task, target_channel_id):
    """Send task to Letta AI agent."""
    letta_api_key = os.getenv("LETTA_API_KEY")
    letta_agent_id = os.getenv("LETTA_AGENT_ID")
    letta_base_url = os.getenv("LETTA_BASE_URL", "https://api.letta.com")
    
    # Format task message
    task_message = f"""[⏰ SCHEDULED TASK TRIGGERED]

Task: {task.get('task_name')}
Description: {task.get('description', '')}

{task.get('action_template', '')}

Please execute this task and respond in the Discord channel {target_channel_id}."""
    
    # Call Letta API
    url = f"{letta_base_url}/agents/{letta_agent_id}/messages"
    headers = {
        "Authorization": f"Bearer {letta_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": task_message,
        "channel_id": target_channel_id,
        "metadata": {
            "task_id": task.get('message_id'),
            "task_name": task.get('task_name'),
            "action_type": task.get('action_type')
        }
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return response.status_code == 200
```

---

## Security Considerations

1. **Environment Variables**: Store all sensitive data (tokens, IDs) in environment variables
2. **Error Handling**: Implement proper error handling to prevent crashes
3. **Rate Limiting**: Be aware of Discord API rate limits
4. **Task Validation**: Validate task structure before execution
5. **Deduplication**: Prevent the same task from running multiple times

---

## Testing

### Test 1: One-Time Task

Create a task that runs in 2 minutes:

```python
discord_tool(
    action="create_task",
    task_name="Test Task",
    schedule="in_2_minutes",
    action_type="self_task",
    action_template="This is a test"
)
```

**Expected**: Task executes once and is deleted.

### Test 2: Recurring Task

Create a task that runs every minute:

```python
discord_tool(
    action="create_task",
    task_name="Recurring Test",
    schedule="minutely",
    action_type="self_task"
)
```

**Expected**: Task executes every minute and updates `next_run`.

---

## Support

For more information:

- See [TASK_SCHEDULER_GUIDE.md](./TASK_SCHEDULER_GUIDE.md) for user documentation
- See [UNIFIED_TOOL_README.md](./UNIFIED_TOOL_README.md) for tool setup

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15

**Part of the Unified Discord Tool for Letta** 🎮✨

