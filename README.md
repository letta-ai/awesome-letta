# Awesome Letta [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome Letta projects, tools, tutorials, and resources for building stateful AI agents with persistent memory.

[Letta](https://www.letta.com) is the leading platform for building AI agents with persistent memory. Unlike traditional chatbots that forget everything between sessions, Letta agents remember, learn, and improve over time.

## Contents

- [Official Resources](#official-resources)
- [Tutorials & Guides](#tutorials--guides)
- [Example Projects](#example-projects)
- [Tools & Integrations](#tools--integrations)
- [Agent Templates](#agent-templates)
- [Research & Papers](#research--papers)
- [Videos & Talks](#videos--talks)
- [Community](#community)
- [Contributing](#contributing)

## Official Resources

- [Letta Website](https://www.letta.com) - Official website and product information
- [Letta Documentation](https://docs.letta.com) - Comprehensive documentation and API reference
- [Letta GitHub](https://github.com/letta-ai/letta) - Official Letta repository
- [Letta Cloud](https://app.letta.com) - Hosted Letta platform
- [Letta Blog](https://www.letta.com/blog) - Official blog with technical deep-dives and announcements
- [Letta Leaderboard](https://docs.letta.com/leaderboard) - Leaderboard to determine how to choose the best language models for your agent [[Repo]](https://github.com/letta-ai/letta-leaderboard)
- [Letta Python SDK](https://github.com/letta-ai/letta-python) - Python SDK for Letta
- [Letta TypeScript SDK](https://github.com/letta-ai/letta-node) - TypeScript SDK for Letta
- [AI Memory SDK](https://github.com/letta-ai/ai-memory-sdk) - A lightweight agent memory SDK for Letta for adding agentic memory and learning in a pluggable way

## Tutorials & Guides

### Getting Started
- [Letta Quickstart](https://docs.letta.com/quickstart) - Official quickstart guide
- [Building Your First Agent](https://docs.letta.com/guides/first-agent) - Step-by-step tutorial
- [DeepLearning.AI Course](https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/) - Free course on building with Letta
- [Create Letta demo applications](https://github.com/letta-ai/create-letta-app) - Create Letta App lets you create apps with Letta

### Advanced Topics
- [Memory Architecture Design](https://www.letta.com/blog/memory-blocks) - Guide to designing effective memory blocks
- [Letta's Filesystem](https://www.letta.com/blog/letta-filesystem) - Using Letta's filesystem capabilities
- [Multi-Agent Systems](https://docs.letta.com/guides/multi-agent) - Building coordinated agent teams
- [Custom Tools Development](https://docs.letta.com/guides/custom-tools) - Creating custom tools for agents

## Example Projects

### Open Source Projects
<!-- Add community projects here -->
- [Thought stream agent handler](https://tangled.sh/@cameron.pfiffer.org/thought-stream) - Deploy Letta agents onto the thought stream.
- [Thought stream web viewer](https://github.com/letta-ai/thought-stream-website), an ATProto-powered multi-agent chatroom.
- [Thought stream CLI](https://tangled.org/@cameron.pfiffer.org/thought-stream-cli) for using the thought stream, not unlike IRC.

### Official Examples

- [Letta Chatbot template](https://github.com/letta-ai/letta-chatbot-example) - An example Next.js chatbot application built on the Letta API, which makes each chatbot a stateful agent (agent with memory) under the hood.
- [Letta Examples Repository](https://github.com/letta-ai/letta/tree/main/examples) - Official example implementations
- [Vercel AI SDK Provider Examples](https://github.com/letta-ai/vercel-ai-sdk-provider/tree/main/examples) - AI SDK integration examples
- [Discord bot](https://github.com/letta-ai/letta-discord-bot-example) An example Discord chatbot built on the Letta API, which uses a stateful agent (agent with memory) under the hood.
- [CharacterPlus](https://github.com/letta-ai/characterai-memory) - Example CharacterAI-style web app that runs on Letta to create characters with memory.

### Use Case Examples
<!-- Categories for different types of applications -->
- [Deep research agent](https://github.com/letta-ai/deep-research)
- [DuckDB agent](https://github.com/letta-ai/letta-duckdb-agent)

## Tools & Integrations

### Official Integrations
- [Vercel AI SDK Provider](https://github.com/letta-ai/vercel-ai-sdk-provider) - Use Letta with Vercel AI SDK v5
- [Zapier Integration](https://zapier.com/apps/letta/integrations) - Use Letta with Zapier
- [Telegram](https://github.com/letta-ai/letta-telegram) - A Modal application for serving a Letta agent on Telegram.
- [Obsidian](https://github.com/letta-ai/letta-obsidian) - A Obsidian plugin for serving a Letta agent on Obsidian.
- [n8n](https://github.com/letta-ai/n8n-nodes-letta) - Connect your Letta agent to n8n workflows.

### Community Tools
<!-- Add community-built tools here -->
- Your tool here! - Submit a PR

### Development Tools
- [Letta CLI](https://docs.letta.com/cli) - Command-line interface for Letta
- [Agent Development Environment](https://www.letta.com/blog/introducing-the-agent-development-environment) - Web-based agent IDE

## Agentfiles

[Letta's agent file format](https://github.com/letta-ai/agent-file) is a standard file format for serializing statful AI
agents. Learn more about it in our [blog post](https://www.letta.com/blog/agent-file).

In this section, you should add pre-configured agent templates for common use cases:

- **Personal Assistant** - General-purpose assistant with user preferences tracking
- **Research Companion** - Knowledge accumulation and synthesis
- **Customer Support** - Context-aware support with conversation history
- **Code Review Assistant** - Codebase-aware review and suggestions
- **Learning Tutor** - Adaptive educational agent

> **Note:** Submit your agent templates via PR! Include memory block structure, tools, and use case description.

## Research & Papers

### Research
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) - Original MemGPT paper
- [Recovery-Bench: Evaluating LLMs' Ability to Recover from Mistakes](https://www.letta.com/blog/recovery-bench) - Research on agent error recovery
- [Sleep-time Compute](https://arxiv.org/abs/2504.13171) - Research on agent sleep-time compute, with accompanying [GitHub repository](https://github.com/letta-ai/sleep-time-compute) and [blog post](https://www.letta.com/blog/sleep-time-compute)
- [Terminal-Bench](https://github.com/letta-ai/letta-terminalbench) - Letta integration for terminal-bench [[Blog post]](https://www.letta.com/blog/terminal-bench)
- [Recovery-Bench](https://github.com/letta-ai/recovery-bench) - Recovery-Bench is a benchmark for evaluating the capability of LLM agents to recover from mistakes [[Blog post]](https://www.letta.com/blog/recovery-bench)

### Blog Posts & Technical Writing

#### Research & Technical Deep-Dives
- [Introducing Recovery-Bench: Evaluating LLMs' Ability to Recover from Mistakes](https://www.letta.com/blog/recovery-bench) - August 27, 2025
- [Benchmarking AI Agent Memory: Is a Filesystem All You Need?](https://www.letta.com/blog/benchmarking-ai-agent-memory) - August 12, 2025
- [Building the #1 Open Source Terminal-Use Agent Using Letta](https://www.letta.com/blog/terminal-bench) - August 5, 2025
- [Agent Memory: How to Build Agents that Learn and Remember](https://www.letta.com/blog/agent-memory) - July 7, 2025
- [Anatomy of a Context Window: A Guide to Context Engineering](https://www.letta.com/blog/context-window) - July 3, 2025
- [Letta Leaderboard: Benchmarking LLMs on Agentic Memory](https://www.letta.com/blog/letta-leaderboard) - May 29, 2025
- [Memory Blocks: The Key to Agentic Context Management](https://www.letta.com/blog/memory-blocks) - May 14, 2025
- [Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) - April 21, 2025
- [RAG is not Agent Memory](https://www.letta.com/blog/rag-is-not-agent-memory) - February 13, 2025
- [Stateful Agents: The Missing Link in LLM Intelligence](https://www.letta.com/blog/stateful-agents) - February 6, 2025
- [The AI Agents Stack](https://www.letta.com/blog/ai-agents-stack) - November 14, 2024

#### Product Announcements & Features
- [Introducing Letta Filesystem](https://www.letta.com/blog/letta-filesystem) - July 24, 2025
- [Announcing Letta Client SDKs for Python and TypeScript](https://www.letta.com/blog/announcing-our-sdks) - April 17, 2025
- [Agent File](https://www.letta.com/blog/agent-file) - April 2, 2025
- [Introducing the Agent Development Environment](https://www.letta.com/blog/introducing-the-agent-development-environment) - January 15, 2025
- [Letta v0.6.4 Release](https://www.letta.com/blog/letta-v0-6-4-release) - December 13, 2024
- [New Course on Letta with DeepLearning.AI](https://www.letta.com/blog/deeplearning-ai-course) - November 7, 2024
- [Letta v0.5.2 Release](https://www.letta.com/blog/letta-v0-5-2-release) - November 6, 2024
- [Letta v0.5.1 Release](https://www.letta.com/blog/letta-v0-5-1-release) - October 23, 2024
- [Letta v0.5 Release](https://www.letta.com/blog/letta-v0-5-release) - October 14, 2024
- [Letta v0.4.1 Release](https://www.letta.com/blog/letta-v0-4-1-release) - October 3, 2024
- [Announcing Letta](https://www.letta.com/blog/announcing-letta) - September 23, 2024
- [MemGPT is now part of Letta](https://www.letta.com/blog/memgpt-and-letta) - September 23, 2024

## Videos & Talks

### Official Videos
- The [Letta YouTube channel](https://www.youtube.com/@letta-ai) - Official Letta YouTube channel
- [Letta Memory Tool Demo](https://youtu.be/0nfNDrRKSuU) - Agents that redesign their own architecture
- [How to use Archival Memory](https://youtu.be/hFNWhrXukc0) - How to use Letta's archival memory for storing long-term memory
- [Building a self-improving deep research agent](https://youtu.be/752y4q50jmQ) - How to build a self-improving deep research agent using Letta in just a few minutes
- [An introduction to personality design](https://youtu.be/OxrO7Z8qjR4) - How to design a personality for your Letta agent
- [The basics of memory architecture](https://youtu.be/o4boci1xSbM) - How to iteratively improve a Letta agent's memory architecture
- [Adding knowledge graphs with neo4j to Letta](https://youtu.be/MK3H_Y-l4QU) - Use MCP and Letta Desktop to build a knowledge graph
- [How to use the Zapier integration](https://youtu.be/SPj2_xoNnAk) - Connect your Letta agent to any external service

### Conference Talks
- [Stateful Agents Meetup: Networks](https://youtu.be/XLjGpNwVf3U) - Recording of the Stateful Agents Meetup hosted by Letta and Nokia.

### Community Tutorials
- Coming soon - share your tutorial videos!

## Community

### Get Help & Connect
- [Discord](https://discord.gg/letta-ai) - Official Discord community
- [Forum](https://forum.letta.com) - Official Forum
- [Bluesky](https://bsky.app/profile/letta.com) - Official Bluesky profile
- [Twitter/X](https://twitter.com/Letta_AI) - Follow for updates

### Showcase
- [Community Showcase](https://discord.gg/letta-ai) - #showcase channel in Discord
- [Interact with your Letta agent using n8n and Telegram](https://github.com/raisga/telegram-letta-n8n-guide) - Guide to connect Letta agents with n8n and Telegram
- Submit your projects here via PR!

## Contributing

Contributions are welcome! Please read the [contribution guidelines](CONTRIBUTING.md) first.

**How to contribute:**
1. Fork this repository
2. Add your resource in the appropriate category
3. Ensure your addition follows the format: `[Resource Name](url) - Brief description`
4. Submit a pull request

**Criteria for inclusion:**
- Must be related to Letta or stateful agent development
- Must be functional and actively maintained (for tools/projects)
- Must provide value to the Letta community
- Preferably open source (for projects and tools)

