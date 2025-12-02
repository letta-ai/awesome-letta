# 🎤 Discord Voice Message Tool

Send voice messages to Discord using ElevenLabs Text-to-Speech! Convert text to natural-sounding speech and send it as audio files.

## 🚀 Features

- ✅ **Text-to-Speech**: Convert any text to natural-sounding voice
- ✅ **Audio Tags Support**: Control emotion and style with tags like `[excited]`, `[whispering]`
- ✅ **DM & Channel Support**: Send voice messages to users or channels
- ✅ **Live Progress**: Real-time progress updates during generation and upload
- ✅ **Smart Timeouts**: Dynamic timeouts based on file size
- ✅ **Security**: Input validation and size limits

## 📋 Prerequisites

1. **Discord Bot Token**
   - Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
   - Get your bot token
   - Bot needs "Send Messages" and "Attach Files" permissions

2. **ElevenLabs Account**
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Get your API key from the dashboard
   - Create or select a voice (get Voice ID from voice settings)

## ⚙️ Configuration

### Environment Variables

Set these environment variables before using the tool:

```bash
export DISCORD_BOT_TOKEN="your_discord_bot_token"
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"
export ELEVENLABS_VOICE_ID="your_voice_id"
export ELEVENLABS_MODEL_ID="eleven_multilingual_v2"  # Optional, defaults to multilingual_v2
```

### Required Variables

- `DISCORD_BOT_TOKEN` - Your Discord bot token
- `ELEVENLABS_API_KEY` - Your ElevenLabs API key
- `ELEVENLABS_VOICE_ID` - Your ElevenLabs Voice ID (can also be provided per-call)

### Optional Variables

- `ELEVENLABS_MODEL_ID` - Model to use (default: `eleven_multilingual_v2`)
  - `eleven_turbo_v2_5` - Fast generation
  - `eleven_multilingual_v2` - Multilingual support
  - `eleven_v3` - Audio Tags support (alpha)

## 🎯 Usage

### Basic Example

```python
send_voice_message(
    text="Hello! This is a voice message.",
    target="123456789012345678",  # User or Channel ID
    target_type="auto"  # Auto-detect: "user" or "channel"
)
```

### With Audio Tags (Emotion)

```python
send_voice_message(
    text="[excited] Hey! I have great news! [whispering] But it's a secret...",
    target="123456789012345678",
    target_type="channel"
)
```

### With Voice Settings

```python
send_voice_message(
    text="This message has custom voice settings",
    target="123456789012345678",
    stability=0.3,  # More emotional/variable
    similarity_boost=0.8,  # Closer to original voice
    style=0.2  # Slight style exaggeration
)
```

### Reply to Message

```python
send_voice_message(
    text="[excited] I'm replying to your message!",
    target="123456789012345678",
    reply_to_message_id="987654321098765432"
)
```

## 🎭 Audio Tags

Audio Tags control **HOW** the text is spoken - they are **NOT** spoken themselves!

### Emotions

| Tag | Description | Example |
|-----|-------------|---------|
| `[excited]` | Excited/enthusiastic | `[excited] Great news!` |
| `[whispering]` | Whisper (for secrets) | `[whispering] This is a secret` |
| `[laughs]` | Laugh | `[laughs] That's hilarious!` |
| `[giggles]` | Giggle | `[giggles] Hehe` |
| `[sighs]` | Sigh | `[sighs] Oh well` |
| `[sarcastic]` | Sarcastic tone | `[sarcastic] Oh really?` |
| `[angry]` | Angry tone | `[angry] I'm upset!` |
| `[happy]` | Happy tone | `[happy] I'm so happy!` |
| `[sad]` | Sad tone | `[sad] I'm feeling down` |
| `[disgusted]` | Disgusted tone | `[disgusted] That's gross` |
| `[fearful]` | Fearful tone | `[fearful] I'm scared` |
| `[surprised]` | Surprised tone | `[surprised] What?!` |
| `[neutral]` | Neutral tone | `[neutral] Just stating facts` |
| `[nervous]` | Nervous tone | `[nervous] I'm worried` |
| `[calm]` | Calm tone | `[calm] Everything is fine` |
| `[frustrated]` | Frustrated tone | `[frustrated] This is annoying` |
| `[curious]` | Curious tone | `[curious] I wonder...` |
| `[crying]` | Crying tone | `[crying] I'm so sad` |
| `[mischievously]` | Mischievous tone | `[mischievously] Hehe` |
| `[shouts]` | Shout | `[shouts] Hey!` |
| `[clears throat]` | Clear throat | `[clears throat] Ahem` |
| `[breathing]` | Breathing sounds | `[breathing] *breath*` |
| `[inhales]` | Inhale | `[inhales] *inhale*` |
| `[exhales]` | Exhale | `[exhales] *exhale*` |

### Accents

| Tag | Description |
|-----|-------------|
| `[strong French accent]` | French accent |
| `[strong German accent]` | German accent |
| `[strong Spanish accent]` | Spanish accent |
| `[strong Italian accent]` | Italian accent |
| `[strong British accent]` | British accent |
| `[strong American accent]` | American accent |
| `[strong Russian accent]` | Russian accent |
| `[strong Japanese accent]` | Japanese accent |

**Note**: Audio Tags require `eleven_v3` model. Set `model_id="eleven_v3"` to use them.

### Example with Multiple Tags

```python
text = """[excited] Hey there! [whispering] I have a secret to tell you. 
[normal] But first, let me [clears throat] get your attention. 
[laughs] Just kidding! [happy] I'm really excited to share this with you!"""
```

## 🎛️ Voice Settings

### Stability (0.0 - 1.0)

- **0.0**: Creative, more emotional, variable
- **0.5**: Natural (default)
- **1.0**: Robust, stable, monotone

### Similarity Boost (0.0 - 1.0)

- **0.0**: Less similar to original voice
- **0.75**: Default
- **1.0**: Very similar to original voice

### Style (0.0 - 1.0)

- **0.0**: Default (no style exaggeration)
- **0.5**: Moderate style enhancement
- **1.0**: Maximum style exaggeration (may reduce stability)

### Speaker Boost

- **False**: Default (faster)
- **True**: Better similarity (slightly slower)

## 📊 Limits

- **Text Length**: Maximum 3000 characters
- **Audio File Size**: Maximum 25 MB
- **Timeout**: 
  - ElevenLabs TTS: 5 minutes
  - Discord Upload: 60 seconds base + 10 seconds per MB (max 5 minutes)

## 🔒 Security

- ✅ Input validation (text length, type checking)
- ✅ Audio size validation
- ✅ Credentials via environment variables (no hardcoding)
- ✅ Text sanitization (removes null bytes)

## 🐛 Troubleshooting

### "Discord bot token not configured"

**Solution**: Set `DISCORD_BOT_TOKEN` environment variable

### "ElevenLabs API key not configured"

**Solution**: Set `ELEVENLABS_API_KEY` environment variable

### "ElevenLabs Voice ID not configured"

**Solution**: Set `ELEVENLABS_VOICE_ID` environment variable or provide `voice_id` parameter

### "No active device found"

**Solution**: This error shouldn't occur with voice messages (they're file uploads, not playback control)

### "Request timeout"

**Solution**: 
- For very long messages, split into smaller parts
- Check your internet connection
- Try again - sometimes ElevenLabs can be slow

### Audio Tags Not Working

**Solution**: 
- Make sure you're using `eleven_v3` model: `model_id="eleven_v3"`
- Audio Tags are only supported in v3 model (alpha)

## 💡 Use Cases

- **Personal Messages**: Send emotional voice messages to users
- **Announcements**: Make channel announcements more engaging
- **Storytelling**: Narrate stories with different emotions
- **Character Voices**: Use different voices and accents for characters
- **Mood Setting**: Set the mood with appropriate emotions

## 📚 Related Documentation

- **[VOICE_MESSAGE_TOOL_IMPLEMENTATION.md](./VOICE_MESSAGE_TOOL_IMPLEMENTATION.md)** - Complete implementation guide with code examples
- **[Unified Discord Tool](./UNIFIED_TOOL_README.md)** - For text messages, task scheduling, and more
- **[Task Scheduler](./TASK_SCHEDULER_GUIDE.md)** - Schedule voice messages automatically

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15

**Part of the Discord Tools for Letta** 🎮✨

