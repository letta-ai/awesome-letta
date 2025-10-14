#!/usr/bin/env python3
"""
Simple script to pull ALL tools from Letta API and save them as individual files.
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
OUTPUT_DIR = Path("tools_output")

if not LETTA_API_KEY:
    print("❌ LETTA_API_KEY not found in .env!")
    sys.exit(1)

print("📥 Fetching all tools from Letta API...")
print()

# Use curl to get all tools (we know this works!)
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
    
    tools = json.loads(result.stdout)
    print(f"✅ Found {len(tools)} tools!\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)
print(f"📂 Saving to: {OUTPUT_DIR.absolute()}\n")

# Save each tool
for i, tool in enumerate(tools, 1):
    tool_name = tool.get("name")
    tool_type = tool.get("tool_type", "unknown")
    
    print(f"{i}. {tool_name} ({tool_type})")
    
    # Save Python source code
    if tool.get("source_code"):
        py_file = OUTPUT_DIR / f"{tool_name}.py"
        with open(py_file, "w") as f:
            f.write(tool["source_code"])
        print(f"   ✅ Saved: {tool_name}.py")
    else:
        print(f"   ⚠️  No source code (built-in tool)")
    
    # Save JSON schema
    if tool.get("json_schema"):
        json_file = OUTPUT_DIR / f"{tool_name}.json"
        with open(json_file, "w") as f:
            json.dump(tool["json_schema"], f, indent=2)
        print(f"   ✅ Saved: {tool_name}.json")
    
    print()

print("=" * 60)
print(f"✅ Done! Saved {len(tools)} tools to {OUTPUT_DIR.absolute()}")
print("=" * 60)

