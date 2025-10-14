# 🎵 Spotify Control Tool - Setup Guide

Complete guide to set up Spotify integration for your Letta AI agent.

---

## 📋 Prerequisites

- Spotify Premium account (required for playback control)
- Spotify Developer account (free)
- Terminal/Command Prompt access
- A web browser

---

## 🚀 Quick Start

### Step 1: Create Spotify Developer App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click **"Create app"** (top right)
4. Fill in the form:
   - **App name:** `Letta AI Music Control` (or any name)
   - **App description:** `AI assistant with Spotify integration`
   - **Redirect URI:** `http://127.0.0.1:8888/callback`
   - **Which API/SDKs are you planning to use?**
     - ✅ Check **"Web API"**
     - ✅ Check **"Web Playback SDK"** (important!)
5. Accept the Terms of Service
6. Click **"Save"**

### Step 2: Get Your Credentials

1. Click on your newly created app
2. Click **"Settings"** (top right)
3. Note down:
   - **Client ID** (visible immediately) - looks like: `x7y8z9a0b1c2d3e4f5g6h7i8j9k0l1m2`
   - **Client Secret** (click "View client secret") - looks like: `m9n8o7p6q5r4s3t2u1v0w9x8y7z6a5b4`

**⚠️ IMPORTANT:** Treat these like passwords - never share publicly!

### Step 3: Get Authorization Code

#### 3.1 Create the Authorization URL

Replace `YOUR_CLIENT_ID` with your actual Client ID:

```
https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://127.0.0.1:8888/callback&scope=user-read-private user-read-email playlist-read-private user-library-read user-top-read playlist-modify-public playlist-modify-private
```

**Example** (with mockup data):
```
https://accounts.spotify.com/authorize?client_id=x7y8z9a0b1c2d3e4f5g6h7i8j9k0l1m2&response_type=code&redirect_uri=http://127.0.0.1:8888/callback&scope=user-read-private user-read-email playlist-read-private user-library-read user-top-read playlist-modify-public playlist-modify-private
```

#### 3.2 Open the URL in Browser

1. Copy your created URL
2. Paste it into your browser's address bar
3. Press Enter

#### 3.3 Authorize the App

1. You'll be redirected to Spotify
2. Log in (if needed)
3. Click **"Agree"**

#### 3.4 Copy the Authorization Code

After agreeing, you'll be redirected to a page that **doesn't load** - this is normal!

The URL in your address bar looks like:
```
http://127.0.0.1:8888/callback?code=BQBfKFZOTWKHXO0aoXR5B4yGnNv...
```

**Copy everything after `code=`** until the end of the URL!
 
 

**  - that's your Refresh Token! 🎉

---

## 🔧 Configuration

### For Letta Cloud

You need to hardcode the credentials in the tool source code:

1. Open `spotify_control.py`
2. Find this section (around line 20):

```python
SPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
SPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
SPOTIFY_REFRESH_TOKEN = "YOUR_REFRESH_TOKEN_HERE"
```

3. Replace with your values:

```python
SPOTIFY_CLIENT_ID = "your_actual_client_id_here"
SPOTIFY_CLIENT_SECRET = "your_actual_client_secret_here"
SPOTIFY_REFRESH_TOKEN = "your_actual_refresh_token_here"
```

**⚠️ IMPORTANT:** 
- **Never commit this file with real credentials to a public repo!**
- Add `spotify_control.py` to `.gitignore` if sharing publicly
- Or use a separate `spotify_credentials.py` file (also in `.gitignore`)

---

### For Local Testing

Create a `.env` file in the `spotify_tool/` directory:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REFRESH_TOKEN=your_refresh_token_here
```

Then test:

```bash
cd spotify_tool
python3 spotify_control.py
```

---

## 📤 Upload to Letta

```bash
cd spotify_tool
python upload-tool.py spotify_control --attach-to-agent YOUR_AGENT_ID
```

---

## 🧪 Testing

### Test 1: Get Now Playing

Ask your agent:
```
"What am I listening to on Spotify right now?"
```

### Test 2: Search

```
"Search for Bohemian Rhapsody on Spotify"
```

### Test 3: Play Music

```
"Play some lofi hip hop"
```

### Test 4: Create Playlist

```
"Create a playlist called 'AI Generated Vibes'"
```

---

## 🎯 Available Actions

| Action | Description | Example |
|--------|-------------|---------|
| `search` | Search tracks/artists/albums/playlists | "Search for Queen" |
| `play` | Play specific content | "Play Bohemian Rhapsody" |
| `pause` | Pause playback | "Pause the music" |
| `next` | Skip to next track | "Next song" |
| `previous` | Previous track | "Previous song" |
| `now_playing` | Get current track | "What's playing?" |
| `create_playlist` | Create new playlist | "Make a playlist" |
| `add_to_playlist` | Add tracks | "Add this to my playlist" |
| `my_playlists` | List playlists | "Show my playlists" |

---

## ⚠️ Common Issues

### "No active device found"

**Solution:** Open Spotify on a device (phone, computer, smart speaker) and start playing something. The tool will use that active device.

### "Invalid token" / "Authentication failed"

**Solution:** Your refresh token may have expired. Re-run the authentication flow

### "Missing credentials"

**Solution:** Make sure you've set the credentials in the tool source code or environment variables.

---

## 🔒 Security Notes

1. **Refresh Tokens** don't expire (unless revoked)
2. **Access Tokens** expire after 1 hour (auto-refreshed by the tool)
3. **Never share** your Client Secret or Refresh Token publicly
4. If credentials leak, revoke them in the [Spotify Dashboard](https://developer.spotify.com/dashboard/)

---

## 📚 Files

- `spotify_control.py` - Main tool implementation
- `spotify_control.json` - Letta tool schema
- `SETUP_GUIDE.md` - This setup guide

---

## 🎵 What Your Agent Can Do

With this tool, your AI can:

- 🎧 **Be your DJ** - Play music based on mood, time of day, or activity
- 🔍 **Music discovery** - Search and recommend new tracks
- 📋 **Playlist curator** - Create and manage playlists automatically
- 🎶 **Ambiance control** - Set the vibe for coding, studying, or relaxing
- 🤖 **Autonomous music taste** - Develop its own "musical preferences"

---

## 💡 Example Workflows

### Morning Routine

```
Agent: "Good morning! Let me start your day with some upbeat music."
→ Searches for "morning motivation playlist"
→ Plays it
```

### Coding Session

```
User: "I'm about to code for 3 hours"
Agent: "Creating a focus playlist for you..."
→ Searches for lofi/ambient tracks
→ Creates playlist
→ Adds 20 tracks
→ Starts playing
```

### Mood-based

```
User: "I'm feeling nostalgic"
Agent: "I see you're vibing with the past. Let me find some classics..."
→ Searches based on user's previous listening (if stored in archival memory)
→ Plays relevant tracks
```

---

**Enjoy your AI DJ! 🎵🤖⚡**

For questions or issues, refer to this guide or the [Spotify Web API docs](https://developer.spotify.com/documentation/web-api).
