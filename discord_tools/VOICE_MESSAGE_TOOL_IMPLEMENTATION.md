# Voice Message Tool Implementation Guide

This guide explains how to implement the Voice Message Tool in your own Discord bot. It provides complete code examples and step-by-step instructions.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [File Structure](#file-structure)
3. [Implementation](#implementation)
4. [Integration](#integration)
5. [Testing](#testing)

---

## Prerequisites

Before implementing the Voice Message Tool, ensure you have:

- ✅ Python 3.7+
- ✅ `requests` library: `pip install requests`
- ✅ Discord bot token
- ✅ ElevenLabs API key
- ✅ An AI agent service (e.g., Letta AI) that supports custom tools

---

## File Structure

Create these files:

```
your-bot/
├── tools/
│   ├── send_voice_message.json    # Tool definition
│   └── send_voice_message.py      # Python implementation
└── .env                           # Environment variables
```

---

## Implementation

### 1. send_voice_message.py

Create `tools/send_voice_message.py`:

```python
"""
Discord Voice Message Tool - ElevenLabs TTS Integration
Sends voice messages to Discord using ElevenLabs Text-to-Speech
"""

import requests
import os
import sys
from typing import Optional

# Configuration from environment
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_v3")

# Security: Input validation
MAX_TEXT_LENGTH = 3000
MAX_AUDIO_SIZE_MB = 25

# Timeout configuration
ELEVENLABS_TIMEOUT = 300  # 5 minutes for TTS generation
DISCORD_UPLOAD_TIMEOUT_BASE = 60  # Base timeout: 60 seconds
DISCORD_UPLOAD_TIMEOUT_PER_MB = 10  # Additional 10 seconds per MB


def send_voice_message(
    text: str,
    target: str,
    target_type: str = "auto",
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    style: Optional[float] = None,
    use_speaker_boost: Optional[bool] = None,
    reply_to_message_id: Optional[str] = None
):
    """
    Sends a voice message to Discord using ElevenLabs TTS.
    
    Args:
        text: The text to convert to speech. Supports Audio Tags for v3 model (e.g., [excited], [whispering]).
        target: Discord User ID (for DM) or Channel ID (for channel message)
        target_type: "user" for DM, "channel" for channel, or "auto" for automatic detection
        voice_id: Optional: ElevenLabs Voice ID (default: configured voice)
        model_id: Optional: Model ID (default: configured model, e.g., "eleven_v3" for Audio Tags support)
        stability: Voice stability (0.0-1.0, default: 0.5)
        similarity_boost: Similarity boost (0.0-1.0, default: 0.75)
        style: Style exaggeration (0.0-1.0, default: 0.0)
        use_speaker_boost: Enable Speaker Boost (default: False)
        reply_to_message_id: Optional: Message ID to reply to
    
    Returns:
        Dict with status, message details, and audio info
    """
    
    # Security: Input validation
    if not text or not isinstance(text, str):
        return {
            "status": "error",
            "message": "Text is required and must be a string"
        }
    
    # Sanitize text
    sanitized_text = text.replace('\0', '').strip()
    
    if len(sanitized_text) == 0:
        return {
            "status": "error",
            "message": "Text cannot be empty"
        }
    
    if len(sanitized_text) > MAX_TEXT_LENGTH:
        return {
            "status": "error",
            "message": f"Text too long ({len(sanitized_text)} chars). Maximum is {MAX_TEXT_LENGTH} characters."
        }
    
    try:
        # Step 1: Generate audio using ElevenLabs API
        voice_id_to_use = voice_id or ELEVENLABS_VOICE_ID
        model_id_to_use = model_id or ELEVENLABS_MODEL_ID
        
        elevenlabs_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id_to_use}"
        
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Build request body
        request_body = {
            "text": sanitized_text,
            "model_id": model_id_to_use
        }
        
        # Add voice settings
        voice_settings = {}
        if stability is not None:
            voice_settings["stability"] = max(0.0, min(1.0, stability))
        if similarity_boost is not None:
            voice_settings["similarity_boost"] = max(0.0, min(1.0, similarity_boost))
        if style is not None:
            voice_settings["style"] = max(0.0, min(1.0, style))
        if use_speaker_boost is not None:
            voice_settings["use_speaker_boost"] = use_speaker_boost
        
        # Default settings if none provided
        if not voice_settings:
            voice_settings = {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": False
            }
        
        request_body["voice_settings"] = voice_settings
        
        # Generate audio with progress logging
        print(f"🎤 STEP 1: Generating voice message with ElevenLabs (text length: {len(sanitized_text)} chars)...")
        print(f"   This may take a while for long messages, please wait...", flush=True)
        sys.stdout.flush()
        
        tts_response = requests.post(
            elevenlabs_url,
            json=request_body,
            headers=headers,
            timeout=ELEVENLABS_TIMEOUT
        )
        
        if tts_response.status_code != 200:
            error_detail = tts_response.text
            try:
                error_json = tts_response.json()
                if "detail" in error_json:
                    error_detail = error_json["detail"].get("message", str(error_json))
            except:
                pass
            
            return {
                "status": "error",
                "message": f"ElevenLabs API error ({tts_response.status_code}): {error_detail}"
            }
        
        audio_data = tts_response.content
        
        # Security: Validate audio size
        audio_size_mb = len(audio_data) / (1024 * 1024)
        print(f"✅ STEP 1 COMPLETE: Audio generated ({audio_size_mb:.2f}MB, {len(audio_data)} bytes)", flush=True)
        sys.stdout.flush()
        
        if audio_size_mb > MAX_AUDIO_SIZE_MB:
            return {
                "status": "error",
                "message": f"Audio file too large ({audio_size_mb:.2f}MB). Maximum is {MAX_AUDIO_SIZE_MB}MB."
            }
        
        # Step 2: Send to Discord
        # Calculate dynamic timeout based on file size (larger files need more time)
        discord_upload_timeout = DISCORD_UPLOAD_TIMEOUT_BASE + int(audio_size_mb * DISCORD_UPLOAD_TIMEOUT_PER_MB)
        # Cap at 5 minutes maximum
        discord_upload_timeout = min(discord_upload_timeout, 300)
        
        print(f"📤 STEP 2: Uploading to Discord ({audio_size_mb:.2f}MB, timeout: {discord_upload_timeout}s)...", flush=True)
        sys.stdout.flush()
        
        discord_headers = {
            "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Determine channel ID
        channel_id = None
        is_dm = False
        
        if target_type == "user" or (target_type == "auto" and target.startswith("7")):
            # Try to create DM channel
            dm_url = "https://discord.com/api/v10/users/@me/channels"
            dm_data = {"recipient_id": target}
            dm_response = requests.post(dm_url, headers=discord_headers, json=dm_data, timeout=10)
            
            if dm_response.status_code == 200:
                channel_id = dm_response.json()["id"]
                is_dm = True
            else:
                return {
                    "status": "error",
                    "message": f"Failed to create DM channel: {dm_response.text}"
                }
        else:
            channel_id = target
            is_dm = False
        
        # Prepare Discord message with audio attachment
        # Discord requires multipart/form-data for file uploads
        files = {
            "file": ("voice_message.mp3", audio_data, "audio/mpeg")
        }
        
        data = {}
        if reply_to_message_id:
            data["message_reference"] = {
                "message_id": reply_to_message_id
            }
        
        # Send message with attachment
        message_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        
        # Use requests with files parameter for multipart upload
        # Dynamic timeout based on file size - larger files need more time
        send_response = requests.post(
            message_url,
            headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"},  # Don't set Content-Type, requests will set it
            files=files,
            data=data,
            timeout=discord_upload_timeout
        )
        
        if send_response.status_code not in (200, 201):
            print(f"❌ STEP 2 FAILED: Discord returned {send_response.status_code}", flush=True)
            sys.stdout.flush()
            return {
                "status": "error",
                "message": f"Failed to send Discord message ({send_response.status_code}): {send_response.text}"
            }
        
        sent_message = send_response.json()
        print(f"✅ STEP 2 COMPLETE: Voice message sent successfully to Discord!", flush=True)
        sys.stdout.flush()
        
        # Build result
        target_desc = f"User {target} (DM)" if is_dm else f"Channel {channel_id}"
        
        result = {
            "status": "success",
            "message": f"Voice message sent to {target_desc}",
            "target": target,
            "target_type": "dm" if is_dm else "channel",
            "channel_id": channel_id,
            "message_id": sent_message.get("id"),
            "audio_size_kb": round(audio_size_mb * 1024, 2),
            "text_length": len(sanitized_text),
            "voice_id": voice_id_to_use,
            "model_id": model_id_to_use,
            "timestamp": sent_message.get("timestamp")
        }
        
        return result
        
    except requests.exceptions.Timeout as e:
        # Try to determine which request timed out based on error context
        error_msg = str(e)
        # Check if we're in the Discord upload phase (discord_upload_timeout would be defined)
        if 'discord_upload_timeout' in locals():
            timeout_source = "Discord upload"
            timeout_duration = discord_upload_timeout
        else:
            # Must be ElevenLabs TTS generation phase
            timeout_source = "ElevenLabs TTS generation"
            timeout_duration = ELEVENLABS_TIMEOUT
        
        print(f"⏰ TIMEOUT: {timeout_source} timed out after {timeout_duration}s", flush=True)
        sys.stdout.flush()
        
        return {
            "status": "error",
            "message": f"Request timeout - {timeout_source} took longer than {timeout_duration} seconds. For very long messages, this may happen. Please try again or split the message into smaller parts."
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }
```

### 2. send_voice_message.json

Create `tools/send_voice_message.json`:

```json
{
  "name": "send_voice_message",
  "description": "Send a voice message to Discord using ElevenLabs Text-to-Speech. Converts text to speech and sends it as an audio file. CRITICAL: Audio Tags in brackets [ ] are NOT spoken - they control HOW the text is spoken! Example: [excited] Hey! will be spoken excitedly WITHOUT saying '[excited]'. Available Audio Tags: EMOTIONS: [excited] (excited), [whispering] (whispering), [laughs] (laughing), [giggles] (giggling), [sighs] (sighing), [sarcastic] (sarcastic), [angry] (angry), [happy] (happy), [sad] (sad), [disgusted] (disgusted), [fearful] (fearful), [surprised] (surprised), [neutral] (neutral), [nervous] (nervous), [calm] (calm), [frustrated] (frustrated), [curious] (curious), [crying] (crying), [mischievously] (mischievous), [shouts] (shouting), [clears throat] (clearing throat), [breathing] (breathing), [inhales] (inhaling), [exhales] (exhaling). ACCENTS: [strong French accent], [strong German accent], [strong Spanish accent], [strong Italian accent], [strong British accent], [strong American accent], [strong Russian accent], [strong Japanese accent]. Use this for personal messages, emotional moments, or when you want to show personality.",
  "parameters": {
    "type": "object",
    "properties": {
      "text": {
        "type": "string",
        "description": "The text to convert to speech. CRITICAL: Audio Tags in brackets [ ] are NOT spoken - they control the emotion! Example: [excited] Hey! will be spoken excitedly WITHOUT saying '[excited]'. Available Audio Tags: EMOTIONS: [excited] (excited/enthusiastic), [whispering] (whispering for secrets), [laughs] (laughing), [giggles] (giggling), [sighs] (sighing), [sarcastic] (sarcastic tone), [angry] (angry tone), [happy] (happy tone), [sad] (sad tone), [disgusted] (disgusted tone), [fearful] (fearful tone), [surprised] (surprised tone), [neutral] (neutral tone), [nervous] (nervous tone), [calm] (calm tone), [frustrated] (frustrated/annoyed tone), [curious] (curious tone), [crying] (crying tone), [mischievously] (mischievous tone), [shouts] (shouting), [clears throat] (clearing throat), [breathing] (breathing sounds), [inhales] (inhaling), [exhales] (exhaling). ACCENTS: [strong French accent], [strong German accent], [strong Spanish accent], [strong Italian accent], [strong British accent], [strong American accent], [strong Russian accent], [strong Japanese accent]. Maximum 3000 characters."
      },
      "target": {
        "type": "string",
        "description": "Discord User ID (for DM) or Channel ID (for channel message)"
      },
      "target_type": {
        "type": "string",
        "enum": ["user", "channel", "auto"],
        "description": "Specify 'user' for DM, 'channel' for channel message, or 'auto' for automatic detection (default: auto)"
      },
      "voice_id": {
        "type": "string",
        "description": "Optional: ElevenLabs Voice ID (default: configured voice from ELEVENLABS_VOICE_ID environment variable)"
      },
      "model_id": {
        "type": "string",
        "description": "Optional: Model ID. Default: 'eleven_v3' (Eleven v3 alpha - supports Audio Tags!). See ElevenLabs Docs for available models."
      },
      "stability": {
        "type": "number",
        "description": "Voice stability (for v3: 0.0=Creative, 0.5=Natural, 1.0=Robust, default: 0.5). Lower = more emotional/variable, Higher = more stable/monotone"
      },
      "similarity_boost": {
        "type": "number",
        "description": "Similarity boost (0.0-1.0, default: 0.75). How close to the original voice it should be"
      },
      "style": {
        "type": "number",
        "description": "Style exaggeration (0.0-1.0, default: 0.0). Enhances the style of the original speaker. May reduce stability."
      },
      "use_speaker_boost": {
        "type": "boolean",
        "description": "Enable Speaker Boost for better similarity (default: False). Slightly increases latency."
      },
      "reply_to_message_id": {
        "type": "string",
        "description": "Optional: Discord Message ID to reply to"
      }
    },
    "required": ["text", "target"]
  }
}
```

---

## Integration

### Step 1: Environment Variables

Create a `.env` file:

```env
DISCORD_BOT_TOKEN=your_bot_token
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id
ELEVENLABS_MODEL_ID=eleven_v3
```

### Step 2: Install Dependencies

```bash
pip install requests python-dotenv
```

### Step 3: Load Environment Variables

In your Python script, load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

Or set them in your system environment.

### Step 4: Register Tool with AI Agent

Register the tool with your AI agent service. The exact method depends on your service:

**For Letta AI**:
```bash
python manage-agent-tools.py --add send_voice_message
```

**For other services**: Follow your service's tool registration documentation.

---

## Testing

### Test 1: Simple Voice Message

Test with a simple message:

```python
result = send_voice_message(
    text="Hello! This is a test voice message.",
    target="123456789012345678",  # User ID
    target_type="user"
)

print(result)
```

**Expected**: Returns `{"status": "success", ...}` and sends voice message to user's DMs.

### Test 2: Audio Tags

Test with Audio Tags:

```python
result = send_voice_message(
    text="[excited] Hey! [laughs] This is so cool!",
    target="123456789012345678",
    target_type="user"
)

print(result)
```

**Expected**: Voice message is spoken with excitement and includes a laugh.

### Test 3: Channel Message

Test sending to a channel:

```python
result = send_voice_message(
    text="[calm] Good morning everyone!",
    target="987654321098765432",  # Channel ID
    target_type="channel"
)

print(result)
```

**Expected**: Voice message is posted to the channel.

### Test 4: Error Handling

Test error handling with invalid input:

```python
result = send_voice_message(
    text="",  # Empty text
    target="123456789012345678",
    target_type="user"
)

print(result)  # Should return error
```

**Expected**: Returns `{"status": "error", "message": "Text cannot be empty"}`.

---

## Customization

### Change Timeouts

Edit timeout constants:

```python
ELEVENLABS_TIMEOUT = 600  # 10 minutes instead of 5
DISCORD_UPLOAD_TIMEOUT_BASE = 120  # 2 minutes instead of 60 seconds
```

### Change Limits

Edit limits:

```python
MAX_TEXT_LENGTH = 5000  # Increase from 3000
MAX_AUDIO_SIZE_MB = 50  # Increase from 25MB
```

### Add Custom Voice Settings

Add default voice settings:

```python
# In send_voice_message function, modify default settings:
if not voice_settings:
    voice_settings = {
        "stability": 0.3,  # More creative
        "similarity_boost": 0.9,  # Higher similarity
        "style": 0.5,  # Enhanced style
        "use_speaker_boost": True  # Enable speaker boost
    }
```

---

## Security Considerations

1. **API Keys**: Never hardcode API keys. Always use environment variables.
2. **Input Validation**: The tool validates text length and sanitizes input.
3. **File Size Limits**: Audio files are limited to prevent abuse.
4. **Error Messages**: Don't expose sensitive information in error messages.

---

## Best Practices

1. **Progress Logging**: The tool includes progress logging for long operations
2. **Dynamic Timeouts**: Timeouts adjust based on file size
3. **Error Handling**: Comprehensive error handling for all failure cases
4. **Input Validation**: Validate all inputs before processing

---

## Related Documentation

- **[VOICE_MESSAGE_README.md](./VOICE_MESSAGE_README.md)** - User guide and feature documentation
- **[UNIFIED_TOOL_README.md](./UNIFIED_TOOL_README.md)** - Unified Discord Tool documentation

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15

**Part of the Discord Tools for Letta** 🎮✨

