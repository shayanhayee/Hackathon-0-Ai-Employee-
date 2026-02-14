---
id: 001
title: Bronze Tier Constitution Amendment
stage: constitution
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["bronze-tier", "architecture", "constraints", "local-first"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - Manual validation: Constitution file contains no unresolved placeholders
 - Manual validation: All templates updated with Bronze Tier constraints
 - Manual validation: Sync Impact Report reflects all changes
---

## Prompt

Amend the global constitution to enable Bronze Tier capabilities for the "Personal AI Employee" project.

BRONZE TIER ARCHITECTURE:

- AI Logic: Claude Code
- Memory Layer: Local Obsidian Vault (Markdown files)
- Perception Layer: Single Watcher (File System Watcher)
- Action Layer: File system operations only (no external APIs)
- Task Processing: Manual trigger via Claude CLI
- State Management: Folder-based state transitions
- No MCP servers in Bronze tier

RULES:

- AI may ONLY interact with the system via file system operations inside the Obsidian vault.
- No external API calls allowed.
- No email sending.
- No WhatsApp automation.
- No browser automation.
- No background autonomous loops.
- No Ralph Wiggum loop in Bronze tier.
- All state must be represented via folder movement:
    - /Inbox → /Needs_Action → /Plans → /Done
- Claude must never modify files outside the vault.
- No cloud usage.
- No background daemons beyond the single watcher.

This amendment authorizes Bronze Tier functionality only.

## Response snapshot

Created Personal AI Employee Constitution v1.0.0 with six core principles:

1. **Local-First Architecture**: All operations confined to Obsidian vault, no external access
2. **File System as Interface**: State represented by file location and content
3. **Manual Trigger Model**: No autonomous processing, user-initiated only
4. **Folder-Based State Machine**: /Inbox → /Needs_Action → /Plans → /Done transitions
5. **Zero External Integration**: No email, messaging, APIs, or MCP servers
6. **Markdown as Protocol**: All data in Markdown with YAML frontmatter

Updated three templates to enforce Bronze Tier constraints:
- plan-template.md: Added Bronze Tier compliance checklist and vault-specific technical context
- spec-template.md: Added tier marker and Bronze Tier constraint section in functional requirements
- tasks-template.md: Updated foundational phase with vault-specific infrastructure tasks

All placeholders resolved, version 1.0.0 ratified 2026-02-12.

## Outcome

- ✅ Impact: Constitution established with clear Bronze Tier boundaries, preventing scope creep into external integrations
- 🧪 Tests: Manual validation confirmed no unresolved placeholders, all templates aligned
- 📁 Files: 4 files created/modified (constitution + 3 templates)
- 🔁 Next prompts: Ready for feature specification (/sp.specify) or planning (/sp.plan) within Bronze Tier constraints
- 🧠 Reflection: Constitution successfully constrains AI to local file operations, ensuring privacy and simplicity. Tier progression path documented for future expansion.

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders resolved, templates updated successfully
- Graders run and results (PASS/FAIL): PASS - Constitution complete, templates aligned, no external dependencies introduced
- Prompt variant (if applicable): N/A - Initial constitution creation
- Next experiment (smallest change to try): Test constitution enforcement by attempting to create a feature spec that violates Bronze Tier constraints (should be caught by Constitution Check gate)
