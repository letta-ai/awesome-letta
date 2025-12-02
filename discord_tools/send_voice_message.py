"""
Discord Voice Message Tool - ElevenLabs TTS Integration
Sends voice messages to Discord using ElevenLabs Text-to-Speech
"""

import requests
import os
import sys
from typing import Optional

# Configuration from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN_HERE")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY_HERE")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "YOUR_ELEVENLABS_VOICE_ID_HERE")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")  # Default model

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
    Sends a voice message to Discord using ElevenLabs Text-to-Speech.
    
    Args:
        text: The text to convert to speech. Supports Audio Tags for v3 model (e.g. [excited], [whispering]).
              See ELEVENLABS_AUDIO_TAGS_GUIDE.md for complete tag documentation.
        target: Discord User ID (for DM) or Channel ID (for channel message)
        target_type: "user" for DM, "channel" for channel, or "auto" for automatic detection
        voice_id: Optional: ElevenLabs Voice ID (default: configured voice)
        model_id: Optional: Model ID (default: configured model, e.g. "eleven_v3" for Audio Tags support)
        stability: Voice stability (0.0-1.0, default: 0.5)
        similarity_boost: Similarity boost (0.0-1.0, default: 0.75)
        style: Style exaggeration (0.0-1.0, default: 0.0)
        use_speaker_boost: Enable Speaker Boost (default: False)
        reply_to_message_id: Optional: Message ID to reply to
    
    Returns:
        Dict with status, message details, and audio info
    """
    
    # Validate credentials
    if DISCORD_BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        return {
            "status": "error",
            "message": "Discord bot token not configured. Please set DISCORD_BOT_TOKEN environment variable."
        }
    
    if ELEVENLABS_API_KEY == "YOUR_ELEVENLABS_API_KEY_HERE":
        return {
            "status": "error",
            "message": "ElevenLabs API key not configured. Please set ELEVENLABS_API_KEY environment variable."
        }
    
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
        
        if voice_id_to_use == "YOUR_ELEVENLABS_VOICE_ID_HERE":
            return {
                "status": "error",
                "message": "ElevenLabs Voice ID not configured. Please set ELEVENLABS_VOICE_ID environment variable or provide voice_id parameter."
            }
        
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

