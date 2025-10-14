#!/usr/bin/env python3
"""
Get a single tool from Letta API and save it locally.

Usage:
    python simple-get-tool.py <tool_name> [--output-dir DIR]
    
Example:
    python simple-get-tool.py spotify_control
    python simple-get-tool.py send_discord_message --output-dir ./my_tools/
    
This downloads:
- tool_name.py (source code)
- tool_name.json (JSON schema)
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

# Load environment from .env file
def load_env():
    """Load environment variables from .env file."""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

load_env()
LETTA_API_KEY = os.getenv("LETTA_API_KEY")

if not LETTA_API_KEY:
    print("❌ LETTA_API_KEY not found in .env!")
    sys.exit(1)

def get_tool_from_letta(tool_name):
    """Fetch a single tool from Letta API using curl."""
    headers = {
        "Authorization": f"Bearer {LETTA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    curl_cmd = [
        "curl", "-s",
        f"https://api.letta.com/v1/tools/{tool_name}",
        "-H", f"Authorization: Bearer {LETTA_API_KEY}",
        "-H", "Content-Type: application/json"
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"❌ curl failed: {result.stderr}")
            return None
        
        if result.stdout.strip() == "":
            print(f"❌ Tool '{tool_name}' not found")
            return None
        
        return json.loads(result.stdout)
        
    except json.JSONDecodeError:
        print(f"❌ Invalid response from API")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def save_tool_files(tool, output_dir):
    """Save tool as .py and .json files."""
    tool_name = tool["name"]
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save Python source code
    if tool.get("source_code"):
        py_path = output_dir / f"{tool_name}.py"
        with open(py_path, "w") as f:
            f.write(tool["source_code"])
        print(f"✅ Saved: {tool_name}.py")
    else:
        print(f"⚠️  No source code for {tool_name} (built-in tool)")
    
    # Save JSON schema
    if tool.get("json_schema"):
        json_path = output_dir / f"{tool_name}.json"
        with open(json_path, "w") as f:
            json.dump(tool["json_schema"], f, indent=2)
        print(f"✅ Saved: {tool_name}.json")
    else:
        print(f"⚠️  No JSON schema for {tool_name}")

def main():
    parser = argparse.ArgumentParser(
        description="Get a single tool from Letta API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python simple-get-tool.py spotify_control
    python simple-get-tool.py send_discord_message --output-dir ./my_tools/
        """
    )
    
    parser.add_argument("tool_name", help="Name of the tool to download")
    parser.add_argument("--output-dir", "-o", 
                       default="tools_output",
                       help="Output directory (default: tools_output)")
    
    args = parser.parse_args()
    
    print(f"📥 Getting tool '{args.tool_name}' from Letta API...")
    print()
    
    # Get tool from API
    tool = get_tool_from_letta(args.tool_name)
    if not tool:
        sys.exit(1)
    
    # Save tool files
    output_dir = Path(args.output_dir)
    print(f"📂 Saving to: {output_dir.absolute()}")
    print()
    
    save_tool_files(tool, output_dir)
    
    print()
    print("=" * 60)
    print("✅ Done!")
    print(f"📂 Tool saved to: {output_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
