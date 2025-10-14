#!/usr/bin/env python3
"""
List all tools available in your Letta account.

Usage:
    python simple-list-tools.py [--format FORMAT]
    
Example:
    python simple-list-tools.py
    python simple-list-tools.py --format json
    python simple-list-tools.py --format table
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

def get_all_tools():
    """Fetch all tools from Letta API using curl."""
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
            return None
        
        return json.loads(result.stdout)
        
    except json.JSONDecodeError:
        print(f"❌ Invalid response from API")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def format_tools_table(tools):
    """Format tools as a nice table."""
    if not tools:
        print("📋 No tools found")
        return
    
    print(f"📋 Found {len(tools)} tools in your Letta account:")
    print()
    print(f"{'Name':<30} {'Type':<20} {'Has Source':<12} {'Description'}")
    print("-" * 80)
    
    for tool in sorted(tools, key=lambda x: x.get("name", "")):
        name = tool.get("name", "unknown")[:29]
        tool_type = tool.get("tool_type", "unknown")[:19]
        has_source = "✅ Yes" if tool.get("source_code") else "❌ No"
        description = (tool.get("description", "") or tool.get("json_schema", {}).get("description", ""))[:30]
        
        print(f"{name:<30} {tool_type:<20} {has_source:<12} {description}")

def format_tools_json(tools):
    """Format tools as JSON."""
    print(json.dumps(tools, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description="List all tools from Letta API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python simple-list-tools.py
    python simple-list-tools.py --format json
    python simple-list-tools.py --format table
        """
    )
    
    parser.add_argument("--format", "-f",
                       choices=["table", "json"],
                       default="table",
                       help="Output format (default: table)")
    
    args = parser.parse_args()
    
    print("📥 Fetching tools from Letta API...")
    print()
    
    # Get tools from API
    tools = get_all_tools()
    if tools is None:
        sys.exit(1)
    
    # Format output
    if args.format == "json":
        format_tools_json(tools)
    else:
        format_tools_table(tools)
    
    print()
    print("=" * 60)
    print(f"✅ Found {len(tools)} tools total")
    print("=" * 60)

if __name__ == "__main__":
    main()
