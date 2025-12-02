# Task Scheduler Implementation

This directory contains a **production-ready TypeScript implementation** of a Task Scheduler that works with tasks created by the Unified Discord Tool.

## 📁 Files

- **`taskScheduler.ts`** - Complete TypeScript implementation (ready to use!)
- **`TASK_SCHEDULER_GUIDE.md`** - User guide for creating and managing tasks
- **`TASK_SCHEDULER_IMPLEMENTATION.md`** - Implementation guide with examples

## 🚀 Quick Start

### For TypeScript/Node.js Discord Bots

1. **Copy the file to your project**:
   ```bash
   cp taskScheduler.ts your-bot/src/taskScheduler.ts
   ```

2. **Install dependencies**:
   ```bash
   npm install discord.js axios
   npm install -D typescript @types/node
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
   import { Client, TextChannel } from 'discord.js';
   import type { Task } from './taskScheduler';
   
   export async function sendTaskMessage(
     task: Task,
     channel?: TextChannel,
     client?: Client
   ): Promise<void> {
     // Send task to your AI agent (e.g., Letta AI)
     const message = `[⏰ SCHEDULED TASK TRIGGERED]\n\nTask: ${task.task_name}\n\n${task.action_template || ''}`;
     
     if (channel) {
       await channel.send(message);
     }
     
     // Or send to your AI API:
     // await callLettaAPI(task, channel);
   }
   ```

5. **Initialize in your bot**:
   ```typescript
   import { startTaskCheckerLoop } from './taskScheduler';
   import { Client } from 'discord.js';
   
   const client = new Client({ intents: [...] });
   
   client.once('ready', async () => {
     console.log('Bot is ready!');
     startTaskCheckerLoop(client);
   });
   
   client.login(process.env.DISCORD_TOKEN);
   ```

## ✨ Features

- ✅ **Automatic Task Reading**: Checks Tasks Channel every 60 seconds
- ✅ **Timezone Handling**: Converts Berlin time to UTC automatically
- ✅ **All Schedule Types**: Supports all schedules from Unified Discord Tool
- ✅ **Sequential Processing**: Prevents API overload with sequential task execution
- ✅ **Deduplication**: Prevents duplicate task executions
- ✅ **Auto-Update**: Automatically updates recurring tasks with new `next_run`
- ✅ **Auto-Delete**: Deletes one-time tasks after execution
- ✅ **Error Handling**: Comprehensive error handling and logging

## 📋 How It Works

1. **Task Creation**: Use Unified Discord Tool to create tasks in the Tasks Channel
2. **Task Reading**: Scheduler reads tasks from channel every 60 seconds
3. **Due Check**: Checks if `next_run <= now` (with timezone conversion)
4. **Execution**: Sends task to your AI agent via `sendTaskMessage()`
5. **Cleanup**: Updates recurring tasks or deletes one-time tasks

## 🔧 Customization

### Change Check Interval

Edit `LOOP_MS` in `taskScheduler.ts`:

```typescript
const LOOP_MS = 30_000; // Check every 30 seconds instead of 60
```

### Add Custom Action Types

Modify `triggerLetta()` function to handle custom action types:

```typescript
if (task.action_type === 'custom_action') {
  // Your custom logic here
}
```

## 📚 Documentation

- **[TASK_SCHEDULER_GUIDE.md](./TASK_SCHEDULER_GUIDE.md)** - How to create and manage tasks
- **[TASK_SCHEDULER_IMPLEMENTATION.md](./TASK_SCHEDULER_IMPLEMENTATION.md)** - Detailed implementation guide

## ⚠️ Important Notes

1. **Environment Variables**: All channel IDs and tokens must be set via environment variables
2. **sendTaskMessage()**: You must implement this function to send tasks to your AI agent
3. **Permissions**: Bot needs "Read Message History" and "Manage Messages" in Tasks Channel
4. **Timezone**: Tasks are stored in Berlin time (Europe/Berlin) and converted to UTC automatically

## 🐛 Troubleshooting

### Tasks Not Executing

- Check `TASKS_CHANNEL_ID` is correct
- Verify bot has "Read Message History" permission
- Check console logs for error messages
- Ensure `sendTaskMessage()` is implemented correctly

### Timezone Issues

- Tasks are stored in Berlin time (Europe/Berlin)
- Scheduler automatically converts to UTC for comparison
- If tasks run at wrong time, check your timezone settings

### Channel Not Found

- Verify `HEARTBEAT_LOG_CHANNEL_ID` is set correctly
- Check bot has access to all required channels
- Review console logs for channel fetch errors

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15

**Part of the Unified Discord Tool for Letta** 🎮✨

