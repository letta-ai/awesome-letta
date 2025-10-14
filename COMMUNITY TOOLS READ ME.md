# 🎮 Letta Tools for the Community

A comprehensive collection of tools and utilities for Letta AI agents, including Discord integration, Spotify control, and management utilities.

## 📦 What's Included

### 🎵 Spotify Tool
- **`spotify_control.py`** - Complete Spotify integration
- **`spotify_control.json`** - Letta tool schema
- **`SETUP_GUIDE.md`** - Step-by-step setup instructions
- **`.gitignore`** - Protects your credentials

### 🎮 Discord Tools
- **`unified_discord_tool.py`** - All-in-one Discord integration (messaging, scheduling, file downloads, channel management)
- **`unified_discord_tool.json`** - Letta tool schema
- **`UNIFIED_TOOL_README.md`** - Complete setup and usage guide
- **`.gitignore`** - Protects your Discord credentials

**Features:**
- Send proactive messages (heartbeats, scheduled tasks)
- Read Discord DMs and channels
- Download files from messages
- List server channels
- Create/manage scheduled tasks

### 🔧 Management Tools
- **`simple-pull-tools.py`** - Download all tools from Letta (simplified!)
- **`simple-list-tools.py`** - List all tools from Letta (simplified!)
- **`simple-get-tool.py`** - Download single tool (simplified!)
- **`compare-tools.py`** - Compare local vs API tools
- **`push-tool.py`** - Upload single tools to Letta
- **`manage-agent-tools.py`** - Attach/detach tools from agents
- **`README.md`** - Complete management guide

---

## 🚀 Quick Start

### 1. Spotify Integration

```bash
cd spotify_tool/
# Follow SETUP_GUIDE.md for complete instructions
# 1. Create Spotify Developer App
# 2. Get credentials (Client ID, Secret, Refresh Token)
# 3. Update spotify_control.py with your credentials
# 4. Upload to Letta using management tools
```

### 2. Discord Integration

```bash
cd discord_tools/
# Set up Discord bot (see UNIFIED_TOOL_README.md)
# 1. Create Discord application and bot
# 2. Get bot token and channel IDs
# 3. Update unified_discord_tool.py with your credentials
# 4. Upload tool using management tools
```

### 3. Tool Management

```bash
cd management_tools/
# Set up your .env file with Letta credentials
python simple-list-tools.py  # List all tools
python simple-pull-tools.py  # Download all tools
python simple-get-tool.py my_tool  # Download single tool
python compare-tools.py      # Compare local vs API
python push-tool.py my_tool  # Upload single tool
```

---

## 📁 Directory Structure

```
LETTA TOOLS FOR THE COMMUNITY/
├── spotify_tool/
│   ├── spotify_control.py
│   ├── spotify_control.json
│   ├── SETUP_GUIDE.md
│   └── .gitignore
├── discord_tools/
│   ├── unified_discord_tool.py
│   ├── unified_discord_tool.json
│   ├── UNIFIED_TOOL_README.md
│   └── .gitignore
├── management_tools/
│   ├── simple-pull-tools.py
│   ├── simple-list-tools.py
│   ├── simple-get-tool.py
│   ├── compare-tools.py
│   ├── push-tool.py
│   ├── manage-agent-tools.py
│   ├── README.md
│   └── .gitignore
└── README.md
```

---

## 🔒 Security Notes

### ⚠️ IMPORTANT: Credential Protection

**Never commit files with real credentials to public repositories!**

The `.gitignore` files are configured to protect:
- Spotify credentials (Client ID, Secret, Refresh Token)
- Discord bot tokens and channel IDs
- Letta API keys
- Environment files (`.env`)

### Best Practices:
1. **Use environment variables** when possible
2. **Replace placeholders** with your actual credentials
3. **Never share credentials** in public channels
4. **Rotate tokens regularly** for security
5. **Use `.gitignore`** to prevent accidental commits

---

## 🎯 Features

### 🎵 Spotify Integration
- **Play/Pause/Stop** music control
- **Skip tracks** forward and backward
- **Volume control** (0-100%)
- **Get current track** information
- **Search and play** songs/artists/playlists
- **Queue management** (add/remove tracks)

### 🎮 Discord Integration
- **Proactive Messaging**: Send messages during heartbeats and scheduled tasks
- **Message Reading**: Read DMs and channels for context
- **File Downloads**: Download files from Discord messages
- **Channel Management**: List and organize server channels
- **Task Scheduling**: Create and manage recurring tasks and reminders

### 🔧 Management Tools
- **Simple Pull**: Download all tools with one command
- **Compare**: See differences between local and API tools
- **Push**: Upload individual tools to Letta
- **Agent Management**: Attach/detach tools from agents
- **Tool Discovery**: List and search available tools

---

## 🛠️ Requirements

### System Requirements
- Python 3.7+
- Internet connection
- Letta AI account
- Spotify Premium account (for Spotify tools)
- Discord bot (for Discord tools)

### Python Packages
```bash
pip install python-dotenv requests
```

---

## 📚 Documentation

Each tool category includes detailed documentation:

- **`spotify_tool/SETUP_GUIDE.md`** - Complete Spotify setup
- **`discord_tools/UNIFIED_TOOL_README.md`** - Discord integration guide
- **`management_tools/README.md`** - Tool management guide

---

## 🤝 Contributing

This is a community project! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit improvements
- Share your own tools

---

## 📄 License

This project is open source. Use and modify as needed for your Letta agents.

---

## 🙏 Credits

**Created by:** Mioré 🐾  
**Last Updated:** 2025-10-14

Special thanks to the Letta AI community for inspiration and feedback!

---

## 🔗 Links

- [Letta AI Documentation](https://docs.letta.com/)
- [Discord Developer Portal](https://discord.com/developers/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)