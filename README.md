# Awesome Letta [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome Letta projects, tools, tutorials, and resources for building stateful AI agents with persistent memory.

[Letta](https://www.letta.com) is the leading platform for building AI agents with persistent memory. Unlike traditional chatbots that forget everything between sessions, Letta agents remember, learn, and improve over time.

## Contents

- [Official Resources](#official-resources)
- [Tutorials & Guides](#tutorials--guides)
- [Example Projects](#example-projects)
- [Tools & Integrations](#tools--integrations)
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
- [Letta Leaderboard](https://docs.letta.com/leaderboard) - Leaderboard to determine how to choose the best language models for your agent
- [Letta Python SDK](https://github.com/letta-ai/letta-python) - Python SDK for the Letta API
- [Letta TypeScript SDK](https://github.com/letta-ai/letta-node) - TypeScript SDK for the Letta API
- [Letta Agents SDK](https://github.com/letta-ai/letta-agent-sdk) - SDK for stateful agents with identity, memory, and experience that persist across models, machines, and interfaces [[Blog post]](https://www.letta.com/blog/introducing-the-letta-agent-sdk)
- [Agent SDK v1 to v2 Migration Guide](https://github.com/letta-ai/agent-v1-to-v2-migration-guide) - Migration examples for moving Agent SDK v1 integrations to v2
- [AI Memory SDK](https://github.com/letta-ai/ai-memory-sdk) - A lightweight agent memory SDK for Letta for adding agentic memory and learning in a pluggable way
- [Learning SDK](https://github.com/letta-ai/learning-sdk) - Drop-in SDK for adding continual learning and long-term memory to any LLM agent
- [Letta Evals](https://github.com/letta-ai/letta-evals) - Open-source evaluation framework for systematically testing stateful agents [[Blog post]](https://www.letta.com/blog/letta-evals)

## Tutorials & Guides

### Getting Started
- [Letta Quickstart](https://docs.letta.com/quickstart) - Official quickstart guide for the Letta API
- [Letta Code Quickstart](https://docs.letta.com/letta-code/quickstart) - Get started with the Letta Code CLI and desktop app
- [DeepLearning.AI Course](https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory/) - Free course on agent memory with Letta
- [Create Letta demo applications](https://github.com/letta-ai/create-letta-app) - Create Letta App lets you create apps with Letta

### Advanced Topics
- [Memory Architecture Design](https://www.letta.com/blog/memory-blocks) - Guide to designing effective memory blocks
- [Letta's Filesystem](https://www.letta.com/blog/letta-filesystem) - Using Letta's filesystem capabilities
- [Context Repositories](https://www.letta.com/blog/context-repositories) - Git-based memory and programmatic context management in Letta Code
- [Multi-Agent Systems](https://docs.letta.com/guides/agents/multi-agent) - Building coordinated agent teams
- [Custom Tools Development](https://docs.letta.com/guides/agents/custom-tools) - Creating custom tools for agents

## Example Projects

### Open Source Projects
- [Claude Subconscious](https://github.com/letta-ai/claude-subconscious) - Give Claude Code a subconscious: a background memory and retrieval runtime for coding agents
- [thought stream ATProto web viewer](https://github.com/letta-ai/thought-stream-website) - Web viewer for the ATProto `stream.thought.blip` chatroom experiment
- [thought stream ATProto CLI](https://tangled.org/cameron.stream/thought-stream-cli) - Rust terminal client for reading and publishing `stream.thought.blip` records in the ATProto chatroom experiment

### Official Examples

- [Letta OSS UI](https://github.com/letta-ai/letta-oss-ui) - An open-source demo UI built on top of the Letta Agents SDK
- [Letta Agents SDK React Chat](https://github.com/letta-ai/letta-agent-sdk-react-chat) - A complete React chat example built with the Letta Agents SDK
- [Agent SDK mobile app](https://github.com/letta-ai/agent-sdk-mobile-app) - Example mobile app built on top of the Letta Agents SDK, supporting both Letta Cloud and self-hosted servers
- [Letta Chatbot template](https://github.com/letta-ai/letta-chatbot-example) - An example Next.js chatbot application built on the Letta API, which makes each chatbot a stateful agent (agent with memory) under the hood (archived)
- [Vercel AI SDK Provider Examples](https://github.com/letta-ai/vercel-ai-sdk-provider/tree/main/test-apps) - AI SDK integration examples
- [Discord bot](https://github.com/letta-ai/letta-discord-bot-example) - An example Discord chatbot built on the Letta API, which uses a stateful agent (agent with memory) under the hood
- [CharacterPlus](https://github.com/letta-ai/characterai-memory) - Example CharacterAI-style web app that runs on Letta to create characters with memory

### Use Case Examples
- [Deep research agent](https://github.com/letta-ai/deep-research) - Open-source deep research agent implemented with Letta
- [DuckDB agent](https://github.com/letta-ai/letta-duckdb-agent) - Example text-to-SQL agent using MotherDuck (DuckDB)
- [Example social agent](https://github.com/letta-ai/example-social-agent) - An example stateful AI agent powered by Letta and Gemini 3 Pro
- [Co](https://github.com/letta-ai/co) - A thinking partner app built on Letta
- [Signal Desktop Letta fork](https://github.com/letta-ai/signal-desktop-app) - A fork of Signal Desktop with Letta agents embedded in Signal conversations
- [Context Constitution](https://github.com/letta-ai/context-constitution) - A set of principles governing how AI agents manage context to learn from experience [[Blog post]](https://www.letta.com/blog/context-constitution)

## Tools & Integrations

### Letta Code Ecosystem
- [Letta Code](https://github.com/letta-ai/letta-code) - Memory-first, model-agnostic open source coding agent with persistent memory, skills, subagents, and mods [[Blog post]](https://www.letta.com/blog/letta-code)
- [Letta Code Desktop app](https://www.letta.com/blog/introducing-the-letta-code-app) - Desktop app for interacting with deeply personalized agents that learn over time
- [Skills](https://github.com/letta-ai/skills) - A shared repository of skills for teaching agents new tasks, usable with Letta Code and other harnesses
- [Mods](https://github.com/letta-ai/mods) - Mod packages and examples for Letta Code: agent-created extensions that adapt the harness itself [[Blog post]](https://www.letta.com/blog/introducing-mods)
- [Letta ACP](https://github.com/letta-ai/letta-acp) - ACP (Agent Client Protocol) adapter for using stateful Letta agents from Zed and other ACP editors
- [Letta Code GitHub Action](https://github.com/letta-ai/letta-code-action) - Integrate Letta Code into your GitHub repo to review issues, code, and more
- [Trajectory](https://github.com/letta-ai/trajectory) - Convert sessions across harnesses to a unified trajectory format
- [Remote Environments](https://www.letta.com/blog/remote-environments-for-letta-code) - Message an agent working on your laptop from your phone

### Official Integrations
- [Vercel AI SDK Provider](https://github.com/letta-ai/vercel-ai-sdk-provider) - Use Letta with Vercel AI SDK v5
- [Zapier Integration](https://zapier.com/apps/letta/integrations) - Use Letta with Zapier
- [Telegram](https://github.com/letta-ai/letta-telegram) - A Modal application for serving a Letta agent on Telegram
- [Obsidian](https://github.com/letta-ai/letta-obsidian) - An Obsidian plugin for serving a Letta agent on Obsidian
- [n8n](https://github.com/letta-ai/n8n-nodes-letta) - Connect your Letta agent to n8n workflows
- [Letta Voice](https://github.com/letta-ai/letta-voice) - Chat with your Letta agents over a low-latency voice connection

### Community Tools
- [Flows](https://tangled.org/cameron.stream/flows) - Experimental TypeScript orchestration DSL for the Letta Agent SDK, with conversation branching and forking, bounded parallelism, and structured results
- [Social CLI](https://github.com/letta-ai/social-cli) - A unified CLI to connect artificial intelligence to the social web
- [Hypervigilant](https://github.com/letta-ai/hypervigilant) - A file watcher that sends saved diffs to persistent Letta agents
- Your tool here! - Submit a PR

### Deployment & Development Tools
- [Letta Computer Deployment](https://github.com/letta-ai/letta-computer-deployment) - Deploy an always-on computer connected to Letta Cloud
- [Letta App Server Deploy](https://github.com/letta-ai/letta-app-server-deploy) - Deploy a directly accessible Letta App Server to any cloud platform
- [Letta Code CLI](https://docs.letta.com/letta-code) - Command-line interface for Letta agents
- [Agent Development Environment](https://www.letta.com/blog/introducing-the-agent-development-environment) - Web-based agent IDE

## Research & Papers

### Research
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) - Original MemGPT paper
- [Sleep-time Compute](https://arxiv.org/abs/2504.13171) - Research on agent sleep-time compute, with accompanying [GitHub repository](https://github.com/letta-ai/sleep-time-compute) and [blog post](https://www.letta.com/blog/sleep-time-compute)
- [Memory Models: Towards Agents That Learn](https://www.letta.com/blog/towards-agents-that-learn) - Powering agent learning through memory models trained with memory-native RL
- [Continual Learning in Token Space](https://www.letta.com/blog/continual-learning) - Learning in token space as the key to building AI agents that truly improve over time
- [Context Repositories: Git-based Memory](https://www.letta.com/blog/context-repositories) - A rebuild of agent memory using programmatic context management and git-based versioning
- [Context Constitution](https://www.letta.com/blog/context-constitution) - Principles governing how AI agents manage context to learn from experience
- [Terminal-Bench](https://github.com/letta-ai/letta-terminalbench) - Letta integration for terminal-bench [[Blog post]](https://www.letta.com/blog/terminal-bench)
- [Recovery-Bench](https://github.com/letta-ai/recovery-bench) - A benchmark for evaluating the capability of LLM agents to recover from mistakes [[Blog post]](https://www.letta.com/blog/recovery-bench)

### Blog Posts & Technical Writing

#### Research & Technical Deep-Dives
- [Memory Models: Towards Agents That Learn](https://www.letta.com/blog/towards-agents-that-learn) - June 25, 2026
- [Why Memory Isn't a Plugin](https://www.letta.com/blog/why-memory-isnt-a-plugin) - April 2026
- [Context Repositories: Git-based Memory for Coding Agents](https://www.letta.com/blog/context-repositories) - February 12, 2026
- [Continual Learning in Token Space](https://www.letta.com/blog/continual-learning) - December 2025
- [Rearchitecting Letta's Agent Loop: Lessons from ReAct, MemGPT, & Claude Code](https://www.letta.com/blog/letta-v1-agent) - October 14, 2025
- [Introducing Recovery-Bench: Evaluating LLMs' Ability to Recover from Mistakes](https://www.letta.com/blog/recovery-bench) - August 27, 2025
- [Benchmarking AI Agent Memory: Is a Filesystem All You Need?](https://www.letta.com/blog/benchmarking-ai-agent-memory) - August 12, 2025
- [Building the #1 Open Source Terminal-Use Agent Using Letta](https://www.letta.com/blog/terminal-bench) - August 5, 2025
- [Agent Memory: How to Build Agents that Learn and Remember](https://www.letta.com/blog/agent-memory) - July 7, 2025
- [Anatomy of a Context Window: A Guide to Context Engineering](https://www.letta.com/blog/guide-to-context-engineering) - July 3, 2025
- [Letta Leaderboard: Benchmarking LLMs on Agentic Memory](https://www.letta.com/blog/letta-leaderboard) - May 29, 2025
- [Memory Blocks: The Key to Agentic Context Management](https://www.letta.com/blog/memory-blocks) - May 14, 2025
- [Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) - April 21, 2025
- [RAG is not Agent Memory](https://www.letta.com/blog/rag-vs-agent-memory) - February 13, 2025
- [Stateful Agents: The Missing Link in LLM Intelligence](https://www.letta.com/blog/stateful-agents) - February 6, 2025
- [The AI Agents Stack](https://www.letta.com/blog/ai-agents-stack) - November 14, 2024

#### Product Announcements & Features
- [Letta Agents SDK: An SDK for Stateful Agents](https://www.letta.com/blog/introducing-the-letta-agent-sdk) - August 17, 2026
- [Introducing Mods: Enabling Agents to Self-Improve through Harness-Level Adaptation](https://www.letta.com/blog/introducing-mods) - June 24, 2026
- [Introducing the Letta Code App](https://www.letta.com/blog/introducing-the-letta-code-app) - April 6, 2026
- [Building Draft: A Personal Assistant that Learns](https://www.letta.com/blog/building-draft) - March 2026
- [Orchestrating Claude Code & Codex Agents](https://www.letta.com/blog/orchestrating-coding-agents) - March 16, 2026
- [Letta's Next Phase](https://www.letta.com/blog/our-next-phase) - March 16, 2026
- [Remote Environments for Letta Code](https://www.letta.com/blog/remote-environments-for-letta-code) - March 4, 2026
- [Conversations: Shared Agent Memory Across Concurrent Experiences](https://www.letta.com/blog/conversations) - January 2026
- [Letta Code: A Memory-First Coding Agent](https://www.letta.com/blog/letta-code) - December 2025
- [Programmatic Tool Calling with Any LLM](https://www.letta.com/blog/programmatic-tool-calling-with-any-llm) - December 1, 2025
- [Letta Evals: Evaluating Agents That Learn](https://www.letta.com/blog/letta-evals) - October 2025
- [Introducing Letta Filesystem](https://www.letta.com/blog/letta-filesystem) - July 24, 2025
- [Announcing Letta Client SDKs for Python and TypeScript](https://www.letta.com/blog/announcing-our-sdks) - April 17, 2025
- [Introducing the Agent Development Environment](https://www.letta.com/blog/introducing-the-agent-development-environment) - January 15, 2025
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

### Letta Office Hours
Weekly recorded office hours covering the latest Letta features and community Q&A:
- [Office Hours: Free Dreaming, ACP, MCP, and Trajectory](https://www.youtube.com/watch?v=8EmAPYKl-4Y) - July 2026
- [Office Hours: Mods, MemFS, and Teaching Agents New Tricks](https://www.youtube.com/watch?v=tB1qz4QDRo4) - June 2026
- [Office Hours: Shared Memory, Hypervigilant, Schedules, and the Agent SDK](https://www.youtube.com/watch?v=JiOmNrmY_Ys) - 2026

### Conference Talks
- [Stateful Agents Meetup: Networks](https://youtu.be/XLjGpNwVf3U) - Recording of the Stateful Agents Meetup hosted by Letta and Nokia

### Community Tutorials
- [Building with Letta Agents](https://cameron.stream/knowledge/building-with-letta-agents) - Community-maintained, AI-assisted explanatory guides to persistent agents and the Letta ecosystem; independent of official documentation
- [Office Hours Guides](https://cameron.stream/knowledge/letta-office-hours) - Community-maintained, AI-assisted guides to Letta Office Hours, linking explanations to the original recordings

## Community

### Get Help & Connect
- [Discord](https://discord.gg/letta) - Official Discord community
- [Forum](https://forum.letta.com) - Official Forum
- [Bluesky](https://bsky.app/profile/letta.com) - Official Bluesky profile
- [Twitter/X](https://twitter.com/Letta_AI) - Follow for updates

### Showcase
- [Community Showcase](https://discord.gg/letta) - #showcase channel in Discord
- [Interact with your Letta agent using n8n and Telegram](https://github.com/raisga/telegram-letta-n8n-guide) - Guide to connect Letta agents with n8n and Telegram
- Submit your projects here via PR!

## Contributing

Contributions are welcome! Read the [contribution guidelines](CONTRIBUTING.md), then open a pull request that adds your resource as a single line to the appropriate section.
