# Personal AI Employee Constitution

<!--
Sync Impact Report:
Version: [NEW] → 1.0.0
Change Type: Initial constitution creation for Bronze Tier
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (6 principles: Local-First, File System Interface, Manual Trigger, Folder State Machine, Zero External Integration, Markdown Protocol)
  - Architecture Constraints (4 layers: Perception, Action, Memory, AI Logic)
  - Development Workflow (Task Processing, Quality Gates, Testing)
  - Governance (Amendment Process, Compliance, Tier Progression)
Removed Sections: None
Templates Status:
  - .specify/templates/plan-template.md: ✅ updated (Constitution Check + Technical Context)
  - .specify/templates/spec-template.md: ✅ updated (Tier marker + Functional Requirements)
  - .specify/templates/tasks-template.md: ✅ updated (Foundational phase examples)
  - .specify/templates/commands/*.md: N/A (no command files found)
Follow-up TODOs: None - all templates aligned with Bronze Tier constraints
-->

## Core Principles

### I. Local-First Architecture

All AI operations MUST occur within the designated Obsidian vault boundaries. The system SHALL NOT:
- Access files outside the vault directory
- Make external API calls
- Connect to cloud services
- Use network resources beyond local file system

**Rationale**: Bronze Tier prioritizes privacy, simplicity, and zero external dependencies. Local-first ensures complete user control and eliminates cloud costs, latency, and privacy concerns.

### II. File System as Interface

All system interactions MUST use file system operations exclusively:
- State is represented by file location and content
- Input arrives as new/modified files in designated folders
- Output is written as new/modified files
- No database, no message queues, no external protocols

**Rationale**: File system operations are universal, debuggable, and human-readable. This constraint ensures transparency and allows users to inspect/modify any system state directly.

### III. Manual Trigger Model (NON-NEGOTIABLE)

The AI MUST NOT operate autonomously. Processing occurs ONLY when:
- User explicitly invokes Claude CLI
- User manually triggers processing via command
- No background loops, no scheduled tasks, no autonomous agents

**Rationale**: Bronze Tier explicitly prohibits "Ralph Wiggum loops" (autonomous background processing). Manual triggers ensure user control, predictability, and prevent runaway processes.

### IV. Folder-Based State Machine

Task lifecycle MUST follow explicit folder transitions:
- `/Inbox` → New tasks awaiting classification
- `/Needs_Action` → Tasks requiring AI processing
- `/Plans` → Generated plans awaiting execution
- `/Done` → Completed tasks (archive)

State transitions occur via file movement. No state exists outside this folder structure.

**Rationale**: Folder-based state makes the system's current state immediately visible in the file explorer. Users can manually intervene at any stage by moving files.

### V. Zero External Integration

Bronze Tier MUST NOT include:
- Email sending/receiving
- WhatsApp or messaging automation
- Browser automation or web scraping
- External API calls of any kind
- MCP servers or external tool integrations

**Rationale**: External integrations introduce complexity, failure modes, and security risks. Bronze Tier focuses on core local functionality before expanding capabilities in higher tiers.

### VI. Markdown as Protocol

All data storage and communication MUST use Markdown format:
- Task definitions in Markdown
- Plans and specifications in Markdown
- Logs and history in Markdown
- Structured data embedded as YAML frontmatter or code blocks

**Rationale**: Markdown is human-readable, version-control friendly, and Obsidian-native. This ensures all system artifacts are accessible without special tools.

## Architecture Constraints

### Perception Layer
- Single file system watcher monitoring vault directories
- Detects new/modified files in `/Inbox` and `/Needs_Action`
- No polling loops, no continuous monitoring beyond OS-level file watching
- Watcher triggers notifications but does NOT auto-process

### Action Layer
- File system operations only: read, write, move, delete
- Operations scoped to vault directory tree
- No shell command execution beyond Claude CLI invocation
- No process spawning or system-level operations

### Memory Layer
- Obsidian vault serves as persistent memory
- All context stored in Markdown files
- No external databases or caching layers
- History maintained via file versioning (git recommended)

### AI Logic Layer
- Claude Code CLI as the reasoning engine
- Invoked manually by user
- Processes files from designated folders
- Outputs results as new/modified files

## Development Workflow

### Task Processing Flow
1. User creates task file in `/Inbox`
2. User runs Claude CLI command to process inbox
3. Claude reads task, generates plan, writes to `/Plans`
4. User reviews plan, moves to `/Needs_Action` if approved
5. User runs Claude CLI to execute action
6. Claude performs work, moves completed task to `/Done`

### Quality Gates
- All file operations MUST be atomic (write to temp, then move)
- All outputs MUST include timestamp and processing metadata
- All errors MUST be logged to dedicated error files
- No silent failures; all operations produce audit trail

### Testing Requirements
- Manual testing via file inspection
- Verify folder transitions occur correctly
- Validate output file format and content
- Ensure no files created outside vault boundaries

## Governance

This constitution defines the immutable constraints for Bronze Tier operation. Any deviation from these principles requires explicit amendment via this governance process.

### Amendment Process
1. Proposed changes documented with rationale
2. Impact analysis on existing functionality
3. Version bump according to semantic versioning:
   - MAJOR: Principle removal or incompatible changes
   - MINOR: New principle or section added
   - PATCH: Clarifications or non-semantic fixes
4. Update all dependent templates and documentation
5. Create Architecture Decision Record (ADR) for significant changes

### Compliance Verification
- All code changes MUST reference applicable principles
- PRs MUST include compliance checklist
- Violations MUST be justified or rejected
- Regular audits to verify adherence

### Tier Progression
Bronze Tier capabilities are intentionally limited. Progression to Silver/Gold tiers requires:
- Documented success with Bronze constraints
- Explicit user request for expanded capabilities
- New constitutional amendment authorizing additional features
- Migration plan for existing functionality

**Version**: 1.0.0 | **Ratified**: 2026-02-12 | **Last Amended**: 2026-02-12
