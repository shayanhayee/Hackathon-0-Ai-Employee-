---
id: 002
title: Bronze Tier Technical Plan
stage: plan
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5
feature: 001-bronze-ai-employee
branch: 001-bronze-ai-employee
user: user
command: /sp.plan
labels: ["bronze-tier", "technical-plan", "architecture", "python-watchdog", "file-watcher"]
links:
  spec: specs/001-bronze-ai-employee/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-bronze-ai-employee/plan.md
 - specs/001-bronze-ai-employee/research.md
 - specs/001-bronze-ai-employee/data-model.md
 - specs/001-bronze-ai-employee/contracts/task-file.schema.md
 - specs/001-bronze-ai-employee/contracts/plan-file.schema.md
 - specs/001-bronze-ai-employee/contracts/dashboard.schema.md
 - specs/001-bronze-ai-employee/quickstart.md
tests:
 - Manual validation: Constitution Check passed (all 11 items)
 - Manual validation: All Phase 0 and Phase 1 artifacts created
 - Manual validation: No external dependencies beyond Python libraries
---

## Prompt

Create the Bronze Tier technical plan for the "Personal AI Employee".

The plan must strictly follow the Bronze specification and constitution.

WATCHER PLAN:
1. Use Python watchdog library
2. Monitor /Inbox directory
3. Copy new files to /Needs_Action
4. Log actions in console

AI PROCESSING PLAN:
1. Manual Claude CLI invocation
2. Claude reads /Needs_Action
3. Claude generates structured Plan file in /Plans
4. Claude updates Dashboard.md
5. Claude moves completed tasks to /Done

DATA PLAN:
1. No database
2. All state stored as Markdown
3. Folder transitions define status

INTEGRATION PLAN:
1. File drop → Watcher copies
2. User runs Claude
3. Claude processes tasks
4. Files transition to next state

CONSTRAINTS:
- No external APIs
- No MCP servers
- No autonomous loops
- No background reasoning engine

The plan must describe HOW Bronze works without introducing Silver features.

## Response snapshot

Created comprehensive Bronze Tier technical plan with complete Phase 0 and Phase 1 artifacts:

**Implementation Plan** (plan.md):
- Two-component architecture: Python watcher + Claude CLI commands
- Technical context: Python 3.11+, watchdog 3.0+, PyYAML, pathlib
- Constitution Check: All 11 items passed (vault-only, no APIs, manual triggers, folder-based state)
- Project structure: /watcher directory, /vault folders, .claude/commands
- Architecture decisions: Foreground watcher, CLI commands, folder-based state, append-only error log
- Performance targets: <5s detection, <30s plan generation, <1s dashboard update
- Deployment: Manual local setup, no automation

**Phase 0: Research** (research.md):
- 6 technology decisions documented with rationale
- Python watchdog selected for cross-platform file monitoring
- PyYAML + plain text for markdown parsing
- Python pathlib for file operations
- Claude Code CLI for AI processing
- Python config.py for configuration
- Append-only errors.md for logging
- All decisions comply with Bronze Tier constitution

**Phase 1: Data Model** (data-model.md):
- 5 core entities defined: Task File, Plan File, Dashboard, Company Handbook, Error Log
- Entity relationships and naming conventions
- State transitions and lifecycle documentation
- Storage estimates: 3-10 MB for 1000 tasks
- Constitutional compliance verified

**Phase 1: File Format Contracts** (contracts/):
- task-file.schema.md: YAML frontmatter + markdown body, validation rules, examples
- plan-file.schema.md: AI-generated plan structure, required sections, naming convention
- dashboard.schema.md: Real-time status overview, update triggers, health indicators

**Phase 1: Quickstart Guide** (quickstart.md):
- Complete setup instructions (15 minutes)
- Prerequisites and installation steps
- Usage workflows: starting watcher, creating tasks, processing, completing
- Troubleshooting guide
- Advanced usage patterns
- Configuration reference

**Total Artifacts**: 7 files created, ~15,000 words of documentation

## Outcome

- ✅ Impact: Complete technical plan ready for task generation. All Bronze Tier constraints enforced, no Silver features introduced.
- 🧪 Tests: Constitution Check passed (11/11 items). All Phase 0 and Phase 1 artifacts created and validated.
- 📁 Files: 7 files created (plan, research, data-model, 3 contracts, quickstart)
- 🔁 Next prompts: Ready for `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Plan successfully balances technical detail with Bronze Tier simplicity. Two-component architecture (watcher + CLI) maintains manual trigger model while providing useful automation. All decisions traceable to constitutional principles.

## Evaluation notes (flywheel)

- Failure modes observed: None - all artifacts created successfully, constitution compliance verified
- Graders run and results (PASS/FAIL): PASS - Constitution Check 11/11, all required artifacts present, no external dependencies beyond approved Python libraries
- Prompt variant (if applicable): N/A - Initial plan creation
- Next experiment (smallest change to try): Generate tasks and verify plan provides sufficient detail for implementation without ambiguity
