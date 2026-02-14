# Implementation Plan: Bronze Tier AI Employee

**Branch**: `001-bronze-ai-employee` | **Date**: 2026-02-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-bronze-ai-employee/spec.md`

## Summary

Build a minimal local AI Employee system that detects file drops in an Obsidian vault, generates task plans via Claude Code CLI, and manages task lifecycle through folder-based state transitions. The system consists of two independent components: (1) a Python file watcher that monitors /Inbox and copies files to /Needs_Action, and (2) Claude Code CLI commands that process tasks, generate plans, update dashboard, and move completed tasks. All state is represented through file location and Markdown content, with zero external dependencies.

## Technical Context

**Language/Version**: Python 3.11+ (for watcher component)
**Primary Dependencies**: watchdog 3.0+ (file system monitoring), PyYAML (frontmatter parsing), pathlib (file operations)
**Storage**: Markdown files in Obsidian vault (Bronze Tier: local file system only)
**Testing**: Manual file inspection and folder transition validation
**Target Platform**: Local Windows/macOS/Linux with Obsidian vault
**Project Type**: Local file-based automation (Bronze Tier)
**Performance Goals**: File detection <5s, plan generation <30s, dashboard update <1s
**Constraints**: No external APIs, no network calls, vault-only operations, manual triggers only
**Scale/Scope**: 50 tasks per session, 1000 files in vault, single user environment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Bronze Tier Compliance** (MANDATORY):
- [x] All operations confined to Obsidian vault directory
- [x] No external API calls or network operations
- [x] No autonomous background processes (watcher only copies files, does not process)
- [x] State transitions via folder movement only (/Inbox → /Needs_Action → /Plans → /Done)
- [x] All data stored as Markdown files
- [x] Manual trigger model enforced (Claude CLI invoked by user, not automatically)

**Additional Constitutional Compliance**:
- [x] File System as Interface: All I/O through file operations (read, write, move, delete)
- [x] Markdown as Protocol: Task files, plans, dashboard, errors all in Markdown format
- [x] Local-First Architecture: No cloud services, no external dependencies beyond local Python libraries
- [x] Folder-Based State Machine: Task lifecycle visible through folder structure
- [x] Zero External Integration: No email, messaging, APIs, or MCP servers

**Status**: ✅ PASSED - All constitutional requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-bronze-ai-employee/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - technology decisions
├── data-model.md        # Phase 1 output - entity definitions
├── quickstart.md        # Phase 1 output - setup instructions
├── contracts/           # Phase 1 output - file format schemas
│   ├── task-file.schema.md
│   ├── plan-file.schema.md
│   └── dashboard.schema.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
watcher/
├── watcher.py           # Main file watcher script
├── config.py            # Configuration (vault path, folders)
├── file_handler.py      # File copy logic with collision handling
└── requirements.txt     # Python dependencies

vault/                   # Obsidian vault (user-managed)
├── Dashboard.md         # Task status overview
├── Company_Handbook.md  # AI context reference
├── errors.md            # Error log
├── Inbox/               # User drops tasks here
├── Needs_Action/        # Watcher copies files here
├── Plans/               # AI writes plans here
└── Done/                # Completed tasks archived here

.claude/                 # Claude Code configuration
└── commands/
    ├── process-tasks.md # Command to process /Needs_Action
    └── complete-task.md # Command to mark task done
```

**Structure Decision**: Single project structure with two independent components: (1) Python watcher script in `/watcher` directory, and (2) Claude Code CLI commands in `.claude/commands`. The Obsidian vault is user-managed and can be located anywhere on the file system. The watcher is configured with the vault path and runs as a foreground process (not a daemon, per Bronze Tier constraints).

## Complexity Tracking

> **No violations** - All design decisions comply with Bronze Tier constitution.

## Phase 0: Research & Technology Decisions

See [research.md](./research.md) for detailed technology evaluation and decisions.

**Key Decisions**:
1. **File Watcher**: Python watchdog library (cross-platform, mature, event-driven)
2. **Markdown Parsing**: PyYAML for frontmatter, plain text for body (no heavy parsers)
3. **File Operations**: Python pathlib (standard library, cross-platform paths)
4. **AI Processing**: Claude Code CLI with custom commands (manual invocation)
5. **Configuration**: Simple Python config file (no YAML/JSON complexity)

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Core Entities**:
- Task File (user-created, AI-processed)
- Plan File (AI-generated)
- Dashboard (AI-maintained summary)
- Company Handbook (user-maintained context)
- Error Log (system-maintained audit trail)

### File Format Contracts

See [contracts/](./contracts/) for detailed schemas:
- `task-file.schema.md` - Task file format and frontmatter
- `plan-file.schema.md` - Plan file structure
- `dashboard.schema.md` - Dashboard layout

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup and usage instructions.

## Phase 2: Implementation Tasks

Tasks will be generated via `/sp.tasks` command after plan approval.

**Expected Task Categories**:
1. Setup: Vault structure, Python environment, Claude commands
2. Watcher: File monitoring, copy logic, collision handling
3. AI Commands: Task processing, plan generation, dashboard updates
4. Integration: End-to-end workflow validation

## Architecture Decisions

### Watcher Design

**Decision**: Foreground Python script using watchdog library
**Rationale**:
- Bronze Tier prohibits background daemons
- Watchdog provides cross-platform file system events
- User controls when watcher runs (manual start/stop)
- Simple, debuggable, no complex process management

**Alternatives Considered**:
- Node.js chokidar: Rejected (adds Node.js dependency)
- Bash inotify: Rejected (Linux-only, not cross-platform)
- Polling loop: Rejected (inefficient, higher CPU usage)

### AI Processing Design

**Decision**: Claude Code CLI with custom command files
**Rationale**:
- Manual trigger model (user invokes CLI)
- Claude Code already installed (per assumptions)
- Command files provide reusable workflows
- No additional infrastructure needed

**Alternatives Considered**:
- Python script calling Claude API: Rejected (violates Zero External Integration)
- Autonomous agent: Rejected (violates Manual Trigger Model)
- Scheduled cron jobs: Rejected (violates Manual Trigger Model)

### State Management Design

**Decision**: Folder location represents task state
**Rationale**:
- Visible in file explorer (no hidden state)
- User can manually intervene (move files)
- Simple, no database or state store needed
- Aligns with Folder-Based State Machine principle

**State Transitions**:
```
/Inbox → /Needs_Action (watcher)
/Needs_Action → /Plans (AI generates plan, task stays)
/Needs_Action → /Done (AI marks complete)
```

### Error Handling Design

**Decision**: Append-only errors.md file in vault root
**Rationale**:
- All errors visible in one place
- Markdown format (human-readable)
- Timestamped entries for audit trail
- No external logging service needed

**Error Categories**:
- Watcher errors (file copy failures, permission issues)
- AI processing errors (malformed markdown, missing files)
- Validation errors (empty tasks, unsupported formats)

## Non-Functional Requirements

### Performance
- File detection: <5 seconds (watchdog event-driven)
- Plan generation: <30 seconds (Claude Code processing)
- Dashboard update: <1 second (simple file write)

### Reliability
- Watcher continues on individual file errors
- AI processing continues if one task fails
- All errors logged to errors.md
- No silent failures

### Security
- All operations within vault boundaries
- No network access
- No external API calls
- File permissions respected (OS-level)

### Maintainability
- Simple Python scripts (no frameworks)
- Clear separation: watcher vs AI processing
- Markdown files (human-readable, editable)
- Minimal dependencies (watchdog, PyYAML, pathlib)

## Deployment Strategy

**Bronze Tier Deployment** (manual, local):
1. User installs Python 3.11+
2. User installs watcher dependencies: `pip install -r watcher/requirements.txt`
3. User configures vault path in `watcher/config.py`
4. User creates vault folder structure (Inbox, Needs_Action, Plans, Done)
5. User starts watcher: `python watcher/watcher.py` (foreground process)
6. User invokes Claude CLI commands as needed

**No automated deployment** - Bronze Tier is local-only, user-managed.

## Testing Strategy

**Manual Testing** (per Bronze Tier constraints):
1. File drop test: Create file in /Inbox, verify appears in /Needs_Action
2. Plan generation test: Run Claude command, verify plan in /Plans
3. Dashboard test: Verify Dashboard.md shows correct counts
4. Error handling test: Drop malformed file, verify error in errors.md
5. Collision test: Drop duplicate filename, verify numeric suffix added
6. Edge case tests: Empty file, missing handbook, concurrent execution

**No automated tests** - Bronze Tier focuses on manual validation.

## Migration & Rollback

**Not applicable** - Bronze Tier is initial implementation with no prior state.

## Monitoring & Observability

**Bronze Tier Monitoring** (manual):
- Watcher console output (file copy events)
- errors.md file (error log)
- Dashboard.md (task counts)
- Folder inspection (task lifecycle visibility)

**No automated monitoring** - User observes system through file system and console output.

## Open Questions

None - All requirements clear from specification and user input.

## Next Steps

1. Review and approve this plan
2. Run `/sp.tasks` to generate implementation tasks
3. Begin implementation with Setup phase (vault structure, Python environment)
4. Implement watcher component
5. Implement Claude CLI commands
6. Validate end-to-end workflow
