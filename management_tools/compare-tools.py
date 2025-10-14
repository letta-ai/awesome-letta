#!/usr/bin/env python3
"""
Compare local tools with tools on Letta API.
Shows which tools are different, missing, or new.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")
LOCAL_TOOLS_DIR = Path("tools_output")

if not LETTA_API_KEY:
    print("❌ LETTA_API_KEY not found in .env!")
    sys.exit(1)

print("📊 Comparing local tools with Letta API...")
print()

# Get tools from API using curl
curl_cmd = [
    "curl", "-s",
    "https://api.letta.com/v1/tools",
    "-H", f"Authorization: Bearer {LETTA_API_KEY}",
    "-H", "Content-Type: application/json"
]

try:
    result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"❌ curl failed: {result.stderr}")
        sys.exit(1)
    
    api_tools = json.loads(result.stdout)
    print(f"✅ Found {len(api_tools)} tools on Letta API")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Get local tools
local_tools = {}
for py_file in LOCAL_TOOLS_DIR.rglob("*.py"):
    tool_name = py_file.stem
    local_tools[tool_name] = py_file

print(f"✅ Found {len(local_tools)} local .py files\n")

# Create lookup for API tools
api_tools_dict = {tool["name"]: tool for tool in api_tools}

# Compare
print("=" * 60)
print("📋 COMPARISON RESULTS")
print("=" * 60)
print()

# Tools on API but not local
missing_local = set(api_tools_dict.keys()) - set(local_tools.keys())
if missing_local:
    print(f"⬇️  MISSING LOCALLY ({len(missing_local)} tools):")
    for name in sorted(missing_local):
        tool_type = api_tools_dict[name].get("tool_type", "unknown")
        print(f"   - {name} ({tool_type})")
    print()

# Tools local but not on API
missing_api = set(local_tools.keys()) - set(api_tools_dict.keys())
if missing_api:
    print(f"⬆️  NOT ON API ({len(missing_api)} tools):")
    for name in sorted(missing_api):
        print(f"   - {name}")
    print()

# Tools in both - check if different
print(f"🔄 TOOLS IN BOTH ({len(set(local_tools.keys()) & set(api_tools_dict.keys()))} tools):")
different_count = 0
for name in sorted(set(local_tools.keys()) & set(api_tools_dict.keys())):
    api_tool = api_tools_dict[name]
    local_file = local_tools[name]
    
    # Read local source
    with open(local_file, "r") as f:
        local_source = f.read()
    
    api_source = api_tool.get("source_code", "")
    
    if local_source.strip() != api_source.strip():
        print(f"   ⚠️  {name} - DIFFERENT")
        different_count += 1
    else:
        print(f"   ✅ {name} - identical")

print()
print("=" * 60)
print(f"Summary: {different_count} different, {len(missing_local)} missing locally, {len(missing_api)} not on API")
print("=" * 60)

