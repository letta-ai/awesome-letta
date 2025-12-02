# 🔧 Letta Tool Management Scripts

Simple, reliable scripts for managing your Letta tools using direct `curl` commands.

## 📋 Available Scripts

### 1. `simple-pull-tools.py` - Pull ALL tools from Letta

Fetches all tools from your Letta account and saves them locally.

```bash
python simple-pull-tools.py
```

**Output:**
- Saves to: `tools_output/`
- Creates `.py` files for custom tools with source code
- Creates `.json` files for all tools (schema only for built-in tools)

---

### 2. `simple-list-tools.py` - List all tools from Letta

Shows all tools available in your Letta account.

```bash
python simple-list-tools.py
python simple-list-tools.py --format json
```

**Shows:**
- Tool name, type, and description
- Whether tool has source code
- Nice table or JSON format

---

### 3. `simple-get-tool.py` - Download single tool

Downloads a specific tool from Letta API.

```bash
python simple-get-tool.py <tool_name>
python simple-get-tool.py spotify_control --output-dir ./my_tools/
```

**Example:**
```bash
python simple-get-tool.py send_discord_message
```

**Notes:**
- Downloads both `.py` and `.json` files
- Saves to `tools_output/` by default
- Works with any tool name

---

### 4. `compare-tools.py` - Compare local vs API

Shows which tools are different, missing, or new.

```bash
python compare-tools.py
```

**Shows:**
- ⬇️ Tools on API but missing locally
- ⬆️ Tools local but not on API  
- 🔄 Tools in both (and if they're different)

---

### 5. `push-tool.py` - Upload a tool to Letta

Uploads a single tool to the Letta API.

```bash
python push-tool.py <tool_name>
```

**Example:**
```bash
python push-tool.py send_discord_message
```

**Notes:**
- Finds the tool in `tools_output/` (searches recursively)
- Needs both `.py` and `.json` files
- Creates a NEW tool (doesn't update existing ones!)
- You still need to attach it to your agent separately

---

### 6. `manage-agent-tools.py` - Attach/Detach tools from agent

Manages which tools are active on your agent.

```bash
# List current tools
python manage-agent-tools.py list

# Attach a tool
python manage-agent-tools.py attach <tool_name>

# Detach a tool  
python manage-agent-tools.py detach <tool_name>
```

**Example:**
```bash
python manage-agent-tools.py attach send_discord_message
python manage-agent-tools.py detach old_tool
```

---

### 7. `letta_memory_merger.py` - Merge and upload archival memories

Merge archival memories from multiple Letta agents and upload to target agent(s).

**Features:**
- Download memories from multiple source agents
- Automatic deduplication (based on content hash)
- Upload to one or multiple target agents
- Live progress display
- Batch processing with rate limiting

```bash
# Using environment variables
export LETTA_API_KEY="sk-let-..."
python letta_memory_merger.py --source agent-123 --target agent-456

# Using command line arguments
python letta_memory_merger.py --api-key sk-let-... --source agent-123 --target agent-456

# Multiple source and target agents
python letta_memory_merger.py --source agent-123 agent-456 --target agent-789

# Custom batch settings
python letta_memory_merger.py --source agent-123 --target agent-456 --batch-size 100 --batch-delay 1.0
```

**Options:**
- `--api-key`: Letta API key (or set `LETTA_API_KEY` environment variable)
- `--source`: Source agent ID(s) to download memories from (can specify multiple)
- `--target`: Target agent ID(s) to upload merged memories to (can specify multiple)
- `--batch-size`: Batch size for uploads (default: 50)
- `--batch-delay`: Delay between batches in seconds (default: 0.5)

**Notes:**
- Automatically deduplicates memories based on content hash
- Shows live progress during download and upload
- Handles rate limiting with configurable delays
- Supports multiple endpoint formats for compatibility

---

## 🚀 Common Workflows

### Pull all current tools from Letta

```bash
cd management_tools
python simple-pull-tools.py
```

### Compare local tools with API

```bash
python compare-tools.py
```

### Update a tool

1. Edit the `.py` file locally
2. Upload new version:
   ```bash
   python push-tool.py my_tool
   ```
3. Note the new tool ID
4. Replace on agent:
   ```bash
   python manage-agent-tools.py detach my_tool  # detach old version
   python manage-agent-tools.py attach my_tool   # attach new version
   ```

---

## ⚙️ Setup

### Required Environment Variables

Create a `.env` file in the `management_tools/` directory:

```env
LETTA_API_KEY=sk-let-YOUR-API-KEY-HERE
LETTA_AGENT_ID=agent-YOUR-AGENT-ID-HERE
LETTA_BASE_URL=https://api.letta.com
```

### Required Packages

**For simple tools (recommended):**
```bash
# No additional packages needed! Uses only Python standard library + curl
```

**For advanced tools:**
```bash
pip install python-dotenv requests
```

**For memory merger:**
```bash
pip install requests urllib3
```

---

## 🎯 Why These Scripts?

**Simple & Reliable:**
- Use direct `curl` commands (proven to work)
- No complex Python HTTP libraries
- Easy to debug

**Fast:**
- Minimal dependencies
- Direct API calls
- No unnecessary processing

**Transparent:**
- Shows exactly what's happening
- Clear error messages
- JSON files are human-readable

---

## 📁 Tool Organization

Tools are organized in `tools_output/`:

```
tools_output/
├── messaging/
│   ├── send_discord_message.py
│   ├── send_discord_message.json
│   ├── read_discord_channel.py
│   └── ...
├── scheduling/
│   ├── create_scheduled_task.py
│   └── ...
├── file_management/
│   ├── download_discord_file.py
│   └── ...
├── channel_management/
│   ├── list_discord_channels.py
│   └── ...
└── omnipresence/
    ├── set_omnipresence_image.py
    └── ...
```

---

## 🔍 Troubleshooting

### "LETTA_API_KEY not found"

Make sure `.env` file exists in `LETTA tools/` directory with your API key.

### "Could not find tool_name.py"

The tool must exist in `tools_output/` (searches all subfolders).

### "curl failed"

Check your internet connection and API key validity.

### Tool upload succeeds but doesn't appear on agent

You need to attach it to the agent separately:
```bash
python manage-agent-tools.py attach tool_name
```

---

**Created by:** Mioré 🐾  
**Last Updated:** 2025-01-15

