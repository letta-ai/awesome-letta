#!/usr/bin/env python3
"""
Manage tools attached to a Letta agent.

Usage:
    # List tools
    python manage-agent-tools.py list [AGENT_ID]
    
    # Attach a tool
    python manage-agent-tools.py attach <TOOL_ID> [AGENT_ID]
    
    # Detach a tool
    python manage-agent-tools.py detach <TOOL_ID> [AGENT_ID]
    
    # Replace tool (detach old, attach new)
    python manage-agent-tools.py replace <OLD_TOOL_ID> <NEW_TOOL_ID> [AGENT_ID]

Environment variables:
    LETTA_API_KEY - Required
    LETTA_AGENT_ID - Optional (can specify agent ID as argument)
"""

import os
import sys
import requests
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

def get_agent_tools(api_key, agent_id):
    """Get current tools attached to an agent."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"https://api.letta.com/v1/agents/{agent_id}",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to get agent: {response.text}")
        return None
    
    return response.json()

def update_agent_tools(api_key, agent_id, tool_ids):
    """Update the tools attached to an agent."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(
        f"https://api.letta.com/v1/agents/{agent_id}",
        json={"tool_ids": tool_ids},
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to update tools: {response.text}")
        return None

def list_tools(api_key, agent_id):
    """List all tools attached to an agent."""
    agent_data = get_agent_tools(api_key, agent_id)
    if not agent_data:
        return
    
    tools = agent_data.get('tools', [])
    print(f"\n📱 Agent: {agent_data['name']} ({agent_id})")
    print(f"🔧 Total tools: {len(tools)}\n")
    
    # Group by type
    custom_tools = [t for t in tools if t.get('tool_type') == 'custom']
    letta_core = [t for t in tools if 'letta_core' in t.get('tool_type', '')]
    letta_memory = [t for t in tools if 'memory' in t.get('tool_type', '')]
    other_tools = [t for t in tools if t not in custom_tools + letta_core + letta_memory]
    
    if custom_tools:
        print("📱 Custom Tools:")
        for t in custom_tools:
            print(f"   • {t['name']}")
            print(f"     ID: {t['id']}")
        print()
    
    if letta_core:
        print("💾 Letta Core Tools:")
        for t in letta_core:
            print(f"   • {t['name']}")
        print()
    
    if letta_memory:
        print("🧠 Memory Tools:")
        for t in letta_memory:
            print(f"   • {t['name']}")
        print()
    
    if other_tools:
        print("🔮 Other Tools:")
        for t in other_tools:
            print(f"   • {t['name']} ({t.get('tool_type', 'unknown')})")
        print()

def attach_tool(api_key, agent_id, tool_id):
    """Attach a tool to an agent."""
    agent_data = get_agent_tools(api_key, agent_id)
    if not agent_data:
        return False
    
    current_tool_ids = [t['id'] for t in agent_data.get('tools', [])]
    
    if tool_id in current_tool_ids:
        print(f"ℹ️  Tool {tool_id} is already attached")
        return True
    
    new_tool_ids = current_tool_ids + [tool_id]
    
    if update_agent_tools(api_key, agent_id, new_tool_ids):
        print(f"✅ Tool {tool_id} attached successfully")
        return True
    return False

def detach_tool(api_key, agent_id, tool_id):
    """Detach a tool from an agent."""
    agent_data = get_agent_tools(api_key, agent_id)
    if not agent_data:
        return False
    
    current_tool_ids = [t['id'] for t in agent_data.get('tools', [])]
    
    if tool_id not in current_tool_ids:
        print(f"ℹ️  Tool {tool_id} is not attached")
        return True
    
    new_tool_ids = [tid for tid in current_tool_ids if tid != tool_id]
    
    if update_agent_tools(api_key, agent_id, new_tool_ids):
        print(f"✅ Tool {tool_id} detached successfully")
        return True
    return False

def replace_tool(api_key, agent_id, old_tool_id, new_tool_id):
    """Replace one tool with another."""
    agent_data = get_agent_tools(api_key, agent_id)
    if not agent_data:
        return False
    
    current_tool_ids = [t['id'] for t in agent_data.get('tools', [])]
    
    if old_tool_id not in current_tool_ids:
        print(f"⚠️  Old tool {old_tool_id} is not attached")
        if new_tool_id in current_tool_ids:
            print(f"ℹ️  New tool {new_tool_id} is already attached")
            return True
        # Just attach the new one
        new_tool_ids = current_tool_ids + [new_tool_id]
    else:
        # Replace old with new
        new_tool_ids = [new_tool_id if tid == old_tool_id else tid for tid in current_tool_ids]
    
    if update_agent_tools(api_key, agent_id, new_tool_ids):
        print(f"✅ Replaced {old_tool_id} with {new_tool_id}")
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Get API key
    api_key = os.getenv("LETTA_API_KEY")
    if not api_key:
        print("❌ LETTA_API_KEY environment variable not set")
        sys.exit(1)
    
    # Get agent ID
    agent_id = os.getenv("LETTA_AGENT_ID")
    
    if command == "list":
        if len(sys.argv) > 2:
            agent_id = sys.argv[2]
        if not agent_id:
            print("❌ LETTA_AGENT_ID not set and no agent ID provided")
            sys.exit(1)
        list_tools(api_key, agent_id)
    
    elif command == "attach":
        if len(sys.argv) < 3:
            print("Usage: python manage-agent-tools.py attach <TOOL_ID> [AGENT_ID]")
            sys.exit(1)
        tool_id = sys.argv[2]
        if len(sys.argv) > 3:
            agent_id = sys.argv[3]
        if not agent_id:
            print("❌ LETTA_AGENT_ID not set and no agent ID provided")
            sys.exit(1)
        attach_tool(api_key, agent_id, tool_id)
    
    elif command == "detach":
        if len(sys.argv) < 3:
            print("Usage: python manage-agent-tools.py detach <TOOL_ID> [AGENT_ID]")
            sys.exit(1)
        tool_id = sys.argv[2]
        if len(sys.argv) > 3:
            agent_id = sys.argv[3]
        if not agent_id:
            print("❌ LETTA_AGENT_ID not set and no agent ID provided")
            sys.exit(1)
        detach_tool(api_key, agent_id, tool_id)
    
    elif command == "replace":
        if len(sys.argv) < 4:
            print("Usage: python manage-agent-tools.py replace <OLD_TOOL_ID> <NEW_TOOL_ID> [AGENT_ID]")
            sys.exit(1)
        old_tool_id = sys.argv[2]
        new_tool_id = sys.argv[3]
        if len(sys.argv) > 4:
            agent_id = sys.argv[4]
        if not agent_id:
            print("❌ LETTA_AGENT_ID not set and no agent ID provided")
            sys.exit(1)
        replace_tool(api_key, agent_id, old_tool_id, new_tool_id)
    
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
