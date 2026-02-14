---
id: 001
title: Bronze Tier AI Employee Specification
stage: spec
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5
feature: 001-bronze-ai-employee
branch: 001-bronze-ai-employee
user: user
command: /sp.specify
labels: ["bronze-tier", "specification", "local-first", "file-watcher", "ai-employee"]
links:
  spec: specs/001-bronze-ai-employee/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-bronze-ai-employee/spec.md
 - specs/001-bronze-ai-employee/checklists/requirements.md
tests:
 - Manual validation: All mandatory sections completed
 - Manual validation: No [NEEDS CLARIFICATION] markers present
 - Manual validation: All requirements testable and unambiguous
 - Manual validation: Success criteria are measurable and technology-agnostic
---

## Prompt

Create the Bronze Tier specification for the "Personal AI Employee" project.

BRONZE GOAL:
Build a minimal local AI Employee that can detect file drops, generate task plans, and mark tasks as completed using a local Obsidian vault.

CORE REQUIREMENTS:

1. Vault Structure:
   - Dashboard.md
   - Company_Handbook.md
   - /Inbox
   - /Needs_Action
   - /Plans
   - /Done

2. Watcher Behavior:
   - Monitor /Inbox
   - On new file creation, copy it to /Needs_Action

3. AI Behavior (Claude Code):
   - Read files inside /Needs_Action
   - Interpret task content
   - Create a corresponding Plan file in /Plans
   - Update Dashboard.md
   - Move completed tasks to /Done

4. State Model:
   - Folder movement represents lifecycle
   - No database allowed
   - No external services allowed

NON-FUNCTIONAL CONSTRAINTS:

- Local-first only
- No external APIs
- No MCP
- No autonomous background reasoning loops
- No social media integration
- No email sending
- No authentication system
- No cloud components

SPEC MUST INCLUDE:

- Task lifecycle description
- Folder-based state transitions
- AI reasoning expectations
- Dashboard update rules
- Acceptance criteria
- Error handling (missing file, malformed file)

This specification defines WHAT Bronze Tier delivers.

## Response snapshot

Created comprehensive Bronze Tier AI Employee specification with:

**Three User Stories** (prioritized P1-P3):
1. P1: Task Intake via File Drop - Foundation for all task processing
2. P2: AI Task Planning - Core AI functionality transforming tasks into plans
3. P3: Task Completion and Dashboard Updates - Progress tracking and workspace organization

**22 Functional Requirements** organized by category:
- Vault Structure (FR-001 to FR-004): Folder hierarchy and core files
- File Watcher (FR-005 to FR-008): Automated file detection and copying
- AI Processing (FR-009 to FR-015): Manual trigger, plan generation, task completion
- Error Handling (FR-016 to FR-019): Logging, validation, graceful degradation
- State Management (FR-020 to FR-022): Folder-based lifecycle, no external stores

**8 Success Criteria**: All measurable and technology-agnostic
- File detection within 5 seconds
- Plan generation within 30 seconds
- Dashboard updates within 1 second
- 100% plan generation for valid tasks
- Zero external network calls
- 50 tasks per session without degradation
- Complete error logging
- Visible task lifecycle through folders

**8 Edge Cases** with handling strategies covering file deletion, non-markdown files, missing folders, name collisions, missing handbook, empty files, concurrent execution.

**Quality Validation**: All checklist items passed - no implementation details, all requirements testable, success criteria measurable, scope clearly bounded.

## Outcome

- ✅ Impact: Complete, validated specification ready for planning phase. Establishes clear Bronze Tier boundaries with local-first, file-based architecture.
- 🧪 Tests: Quality checklist validation passed (14/14 items). All requirements testable, no clarifications needed.
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: Ready for `/sp.plan` to generate implementation plan, or `/sp.clarify` if additional requirements emerge
- 🧠 Reflection: Specification successfully balances simplicity (Bronze Tier constraints) with completeness (22 requirements, 8 edge cases). User stories are independently testable, enabling incremental delivery.

## Evaluation notes (flywheel)

- Failure modes observed: None - spec completed without clarifications needed
- Graders run and results (PASS/FAIL): PASS - All quality checklist items passed, no [NEEDS CLARIFICATION] markers, all requirements testable
- Prompt variant (if applicable): N/A - Initial specification creation
- Next experiment (smallest change to try): Test specification clarity by generating implementation plan and verifying no ambiguities surface during technical design
