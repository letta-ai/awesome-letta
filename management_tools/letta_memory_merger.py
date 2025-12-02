#!/usr/bin/env python3
"""
Letta Archival Memory Merger & Uploader
========================================

Merge archival memories from multiple Letta agents and upload to target agent(s).

Author: Mioré and Duzafizzl
License: MIT

Features:
- Download memories from multiple source agents
- Automatic deduplication (based on content hash)
- Upload to one or multiple target agents
- Live progress display
- Batch processing with rate limiting

Requirements:
- Python 3.8+
- requests library (pip install requests)

Usage:
1. Set your API key via environment variable: LETTA_API_KEY
2. Configure source and target agent IDs in the script or via command line
3. Run: python letta_memory_merger.py
"""

# ============================================
# CONFIGURATION - EDIT THIS SECTION
# ============================================

import os
import sys
import json
import hashlib
import time
import argparse
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("❌ Error: 'requests' library not found!")
    print("   Install it with: pip install requests")
    sys.exit(1)

# Your Letta API Key (get it from https://app.letta.com/settings)
# Can be set via environment variable or command line argument
LETTA_API_KEY = os.getenv("LETTA_API_KEY", "YOUR_API_KEY_HERE")

# Source Agent IDs (agents to download memories FROM)
# Can be configured via command line or here
# Example: ["agent-abc123-def4-5678-90ab-cdef12345678", "agent-xyz789-0123-4567-89ab-cdef01234567"]
SOURCE_AGENT_IDS = []

# Target Agent IDs (agents to upload merged memories TO)
# Can be one or multiple agents
# Example: ["agent-target-1234-5678-90ab-cdef12345678"]
TARGET_AGENT_IDS = []

# Batch size for uploads (lower = safer, higher = faster)
BATCH_SIZE = 50

# Delay between batches (seconds) - prevents rate limiting
BATCH_DELAY = 0.5

# ============================================
# DO NOT EDIT BELOW THIS LINE
# ============================================

LETTA_API_BASE = "https://api.letta.com"


class LettaAPIError(Exception):
    """Letta API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class LettaMemoryMerger:
    """Merge and upload archival memories between Letta agents"""
    
    def __init__(self, api_key: str):
        if not api_key or api_key == "YOUR_API_KEY_HERE" or api_key == "sk-let-YOUR_API_KEY_HERE":
            raise ValueError("❌ Please set your LETTA_API_KEY environment variable or pass it via --api-key!")
        
        if not api_key.startswith("sk-let-"):
            raise ValueError("❌ Invalid Letta API key format. Expected: sk-let-...")
        
        self.api_key = api_key
        self.base_url = LETTA_API_BASE
        
        # Setup session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set headers
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise LettaAPIError(f"API error: {e}", status_code=response.status_code)
        except requests.exceptions.RequestException as e:
            raise LettaAPIError(f"Request failed: {e}")
    
    def download_memories(self, agent_id: str, limit: int = 10000) -> List[Dict[str, Any]]:
        """Download archival memories from a Letta agent"""
        print(f"   📥 Downloading from {agent_id}...", end='', flush=True)
        
        all_memories = []
        current_offset = 0
        batch_size = 1000
        
        while len(all_memories) < limit:
            try:
                # Try different endpoint formats
                endpoints = [
                    f"/v1/agents/{agent_id}/archival-memory",
                    f"/v1/agents/{agent_id}/memory/archival",
                    f"/v1/agents/{agent_id}/passages"
                ]
                
                memories = []
                for endpoint in endpoints:
                    try:
                        params = {"limit": batch_size, "offset": current_offset}
                        response = self._make_request("GET", endpoint, params=params)
                        
                        if isinstance(response, list):
                            memories = response
                        elif isinstance(response, dict):
                            memories = response.get("data", response.get("memories", response.get("results", [])))
                        
                        if memories:
                            break
                    except LettaAPIError as e:
                        if e.status_code != 404:
                            raise
                        continue
                
                if not memories:
                    break
                
                all_memories.extend(memories)
                print(f"\r   📥 Downloaded {len(all_memories)} memories from {agent_id}...", end='', flush=True)
                
                if len(memories) < batch_size:
                    break
                
                current_offset += batch_size
                
            except LettaAPIError:
                break
        
        print(f"\r   ✅ Downloaded {len(all_memories)} memories from {agent_id}" + " " * 20)
        return all_memories
    
    def deduplicate_memories(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate memories based on content hash"""
        print(f"\n🔄 Deduplicating {len(memories)} memories...", end='', flush=True)
        
        seen_hashes: Set[str] = set()
        unique_memories = []
        duplicates_count = 0
        
        for mem in memories:
            text = mem.get("text") or mem.get("content") or mem.get("memory") or ""
            
            if not text or not text.strip():
                duplicates_count += 1
                continue
            
            # Create hash of normalized text
            normalized_text = text.lower().strip()
            text_hash = hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()
            
            if text_hash in seen_hashes:
                duplicates_count += 1
                continue
            
            seen_hashes.add(text_hash)
            unique_memories.append(mem)
        
        print(f"\r   ✅ Unique: {len(unique_memories)}, Duplicates removed: {duplicates_count}" + " " * 20)
        return unique_memories
    
    def upload_memory(self, memory: Dict[str, Any], agent_id: str) -> bool:
        """Upload a single memory to a Letta agent"""
        text = memory.get("text") or memory.get("content") or memory.get("memory") or ""
        if not text or not text.strip():
            return False
        
        payload = {"text": text.strip()}
        
        # Add tags if available
        tags = memory.get("tags", [])
        if tags:
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]
            payload["tags"] = tags
        
        # Add metadata if available
        metadata = memory.get("metadata", {})
        if metadata:
            payload["metadata"] = metadata
        
        # Try different endpoints
        endpoints = [
            f"/v1/agents/{agent_id}/passages",
            f"/v1/agents/{agent_id}/archival-memory"
        ]
        
        for endpoint in endpoints:
            try:
                self._make_request("POST", endpoint, json=payload)
                return True
            except LettaAPIError as e:
                if e.status_code == 404:
                    continue
                return False
        
        return False
    
    def upload_batch(self, memories: List[Dict[str, Any]], agent_id: str, batch_size: int, batch_delay: float):
        """Upload memories in batches"""
        print(f"\n📤 Uploading to {agent_id}...")
        
        stats = {"uploaded": 0, "failed": 0}
        total_batches = (len(memories) + batch_size - 1) // batch_size
        
        for batch_idx in range(0, len(memories), batch_size):
            batch = memories[batch_idx:batch_idx + batch_size]
            current_batch = (batch_idx // batch_size) + 1
            
            print(f"\n   📦 Batch {current_batch}/{total_batches} ({len(batch)} memories)")
            
            for i, memory in enumerate(batch):
                memory_num = batch_idx + i + 1
                progress_pct = (memory_num / len(memories)) * 100
                
                if self.upload_memory(memory, agent_id):
                    stats["uploaded"] += 1
                    status = "✅"
                else:
                    stats["failed"] += 1
                    status = "❌"
                
                print(f"      {status} [{memory_num}/{len(memories)}] ({progress_pct:.1f}%) - Uploaded: {stats['uploaded']}, Failed: {stats['failed']}", end='\r')
                sys.stdout.flush()
            
            print()  # Newline after batch
            time.sleep(batch_delay)
        
        print(f"\n   ✅ Completed: {stats['uploaded']} uploaded, {stats['failed']} failed")
        return stats
    
    def run(self, source_agents: List[str], target_agents: List[str], batch_size: int, batch_delay: float):
        """Main workflow: download, merge, deduplicate, upload"""
        print("="*60)
        print("🚀 LETTA ARCHIVAL MEMORY MERGER")
        print("="*60)
        
        # Step 1: Download from source agents
        print("\n" + "="*60)
        print("📥 STEP 1: Downloading memories from source agents")
        print("="*60)
        
        all_memories = []
        for idx, agent_id in enumerate(source_agents, 1):
            print(f"\n[{idx}/{len(source_agents)}]")
            memories = self.download_memories(agent_id)
            all_memories.extend(memories)
        
        if not all_memories:
            print("\n❌ No memories found!")
            return
        
        print(f"\n✅ Total downloaded: {len(all_memories)} memories")
        
        # Step 2: Deduplicate
        print("\n" + "="*60)
        print("🔄 STEP 2: Deduplicating memories")
        print("="*60)
        
        unique_memories = self.deduplicate_memories(all_memories)
        
        if not unique_memories:
            print("\n❌ No unique memories after deduplication!")
            return
        
        # Step 3: Upload to target agents
        print("\n" + "="*60)
        print("📤 STEP 3: Uploading to target agents")
        print("="*60)
        
        all_stats = {}
        for idx, agent_id in enumerate(target_agents, 1):
            print(f"\n[{idx}/{len(target_agents)}] Agent: {agent_id}")
            stats = self.upload_batch(unique_memories, agent_id, batch_size, batch_delay)
            all_stats[agent_id] = stats
        
        # Summary
        print("\n" + "="*60)
        print("✅ COMPLETE!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   Total downloaded: {len(all_memories)}")
        print(f"   Unique memories: {len(unique_memories)}")
        print(f"   Target agents: {len(target_agents)}")
        
        print(f"\n📊 Upload Statistics:")
        total_uploaded = 0
        total_failed = 0
        for agent_id, stats in all_stats.items():
            print(f"\n   {agent_id}")
            print(f"      Uploaded: {stats['uploaded']}")
            print(f"      Failed: {stats['failed']}")
            total_uploaded += stats['uploaded']
            total_failed += stats['failed']
        
        print(f"\n   Total: {total_uploaded} uploaded, {total_failed} failed")


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Merge archival memories from multiple Letta agents and upload to target agent(s)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using environment variables
  export LETTA_API_KEY="sk-let-..."
  python letta_memory_merger.py --source agent-123 --target agent-456

  # Using command line arguments
  python letta_memory_merger.py --api-key sk-let-... --source agent-123 --target agent-456

  # Multiple source and target agents
  python letta_memory_merger.py --source agent-123 agent-456 --target agent-789
        """
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=LETTA_API_KEY,
        help="Letta API key (or set LETTA_API_KEY environment variable)"
    )
    
    parser.add_argument(
        "--source",
        type=str,
        nargs="+",
        default=SOURCE_AGENT_IDS,
        help="Source agent ID(s) to download memories from"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        nargs="+",
        default=TARGET_AGENT_IDS,
        help="Target agent ID(s) to upload merged memories to"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help=f"Batch size for uploads (default: {BATCH_SIZE})"
    )
    
    parser.add_argument(
        "--batch-delay",
        type=float,
        default=BATCH_DELAY,
        help=f"Delay between batches in seconds (default: {BATCH_DELAY})"
    )
    
    args = parser.parse_args()
    
    print("\n🎯 Letta Archival Memory Merger")
    print("   by Mioré and Duzafizzl\n")
    
    # Validate configuration
    if not args.source:
        print("❌ Error: No source agent IDs provided!")
        print("   Use --source agent-id or set SOURCE_AGENT_IDS in the script.")
        sys.exit(1)
    
    if not args.target:
        print("❌ Error: No target agent IDs provided!")
        print("   Use --target agent-id or set TARGET_AGENT_IDS in the script.")
        sys.exit(1)
    
    # Initialize merger
    try:
        merger = LettaMemoryMerger(args.api_key)
    except ValueError as e:
        print(f"\n{e}")
        print("\n💡 Set LETTA_API_KEY environment variable or use --api-key argument.")
        sys.exit(1)
    
    # Run
    try:
        merger.run(args.source, args.target, args.batch_size, args.batch_delay)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

