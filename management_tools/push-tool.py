#!/usr/bin/env python3
"""
Push a single tool to Letta API.

Usage:
    python push-tool.py tool_name

Example:
    python push-tool.py send_discord_message
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

if len(sys.argv) < 2:
    print("Usage: python push-tool.py <tool_name> [--yes]")
    print("Example: python push-tool.py send_discord_message")
    print("         python push-tool.py send_discord_message --yes  (skip confirmation)")
    sys.exit(1)

tool_name = sys.argv[1]
auto_yes = "--yes" in sys.argv or "-y" in sys.argv

# Load environment
load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")
LOCAL_TOOLS_DIR = Path("tools_output")

if not LETTA_API_KEY:
    print("❌ LETTA_API_KEY not found in .env!")
    sys.exit(1)

# Find tool files
py_file = None
json_file = None

for f in LOCAL_TOOLS_DIR.rglob(f"{tool_name}.py"):
    py_file = f
    break

for f in LOCAL_TOOLS_DIR.rglob(f"{tool_name}.json"):
    json_file = f
    break

if not py_file or not json_file:
    print(f"❌ Could not find {tool_name}.py and {tool_name}.json")
    print(f"   Searched in: {LOCAL_TOOLS_DIR.absolute()}")
    sys.exit(1)

print(f"📤 Pushing {tool_name} to Letta API...")
print(f"   Python: {py_file}")
print(f"   JSON: {json_file}")
print()

# Read files
with open(py_file, "r") as f:
    source_code = f.read()

with open(json_file, "r") as f:
    json_schema = json.load(f)

# Create payload
payload = {
    "source_type": "python",
    "source_code": source_code,
    "tags": ["custom", "discord"],
    "json_schema": json_schema
}

# Write to temp file for curl
temp_file = Path("/tmp/letta_tool_payload.json")
with open(temp_file, "w") as f:
    json.dump(payload, f)

# Check if tool exists
print("🔍 Checking if tool exists on API...")
curl_check = [
    "curl", "-s",
    "https://api.letta.com/v1/tools",
    "-H", f"Authorization: Bearer {LETTA_API_KEY}",
    "-H", "Content-Type: application/json"
]

try:
    result = subprocess.run(curl_check, capture_output=True, text=True, timeout=30)
    api_tools = json.loads(result.stdout)
    existing_tool = next((t for t in api_tools if t["name"] == tool_name), None)
    
    if existing_tool:
        print(f"⚠️  Tool '{tool_name}' already exists (ID: {existing_tool['id']})")
        print(f"   This will CREATE A NEW VERSION, not update the existing one!")
        if not auto_yes:
            response = input("   Continue? (y/n): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                sys.exit(0)
        else:
            print("   Auto-continuing (--yes flag)")
    
except Exception as e:
    print(f"⚠️  Could not check existing tools: {e}")

# Push tool using curl
print()
print("📤 Uploading tool...")
curl_upload = [
    "curl", "-s", "-X", "POST",
    "https://api.letta.com/v1/tools",
    "-H", f"Authorization: Bearer {LETTA_API_KEY}",
    "-H", "Content-Type: application/json",
    "-d", f"@{temp_file}"
]

try:
    result = subprocess.run(curl_upload, capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        print(f"❌ curl failed: {result.stderr}")
        sys.exit(1)
    
    # Parse response
    try:
        response_data = json.loads(result.stdout)
        
        if "id" in response_data:
            print()
            print("=" * 60)
            print(f"✅ SUCCESS! Tool uploaded")
            print(f"   Tool ID: {response_data['id']}")
            print(f"   Name: {response_data.get('name')}")
            print(f"   Type: {response_data.get('tool_type')}")
            print("=" * 60)
        else:
            print()
            print("❌ Upload failed:")
            print(json.dumps(response_data, indent=2))
            sys.exit(1)
    
    except json.JSONDecodeError:
        print(f"❌ Invalid response: {result.stdout}")
        sys.exit(1)

finally:
    # Clean up temp file
    if temp_file.exists():
        temp_file.unlink()

print()
print("💡 Next step: Attach tool to agent using manage-agent-tools.py")

