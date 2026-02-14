# Feature Specification: Bronze Tier AI Employee

**Feature Branch**: `001-bronze-ai-employee`
**Created**: 2026-02-12
**Status**: Draft
**Tier**: Bronze (Local file operations only, no external integrations)
**Input**: User description: "Create the Bronze Tier specification for the Personal AI Employee project. Build a minimal local AI Employee that can detect file drops, generate task plans, and mark tasks as completed using a local Obsidian vault."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Intake via File Drop (Priority: P1)

A user creates a new task by dropping a markdown file into the /Inbox folder. The file system watcher detects the new file and automatically copies it to /Needs_Action, making it ready for AI processing.

**Why this priority**: This is the entry point for all tasks. Without reliable task intake, the entire system is non-functional. This is the foundation that all other features depend on.

**Independent Test**: Can be fully tested by creating a file in /Inbox and verifying it appears in /Needs_Action within 5 seconds. Delivers immediate value by providing a simple, reliable task capture mechanism.

**Acceptance Scenarios**:

1. **Given** /Inbox folder is empty, **When** user creates "task-001.md" in /Inbox, **Then** "task-001.md" appears in /Needs_Action within 5 seconds
2. **Given** /Inbox contains "urgent-task.md", **When** watcher detects the file, **Then** file is copied (not moved) to /Needs_Action preserving original content
3. **Given** /Needs_Action already contains "task-001.md", **When** user drops another "task-001.md" in /Inbox, **Then** system creates "task-001-1.md" in /Needs_Action to avoid collision
4. **Given** user drops "empty-task.md" with no content in /Inbox, **When** watcher processes it, **Then** file is still copied to /Needs_Action (validation happens during AI processing)

---

### User Story 2 - AI Task Planning (Priority: P2)

A user manually triggers Claude Code to process tasks in /Needs_Action. The AI reads each task file, interprets the content using Company_Handbook.md as context, generates a detailed plan, and writes the plan to /Plans folder with a corresponding filename.

**Why this priority**: This is the core AI functionality that transforms raw tasks into actionable plans. Without this, the system is just a file mover. This delivers the primary value proposition of an "AI Employee."

**Independent Test**: Can be fully tested by placing a task file in /Needs_Action, running Claude CLI command, and verifying a plan file appears in /Plans. Delivers value by automating planning work.

**Acceptance Scenarios**:

1. **Given** "task-001.md" exists in /Needs_Action with content "Research competitor pricing", **When** user runs Claude CLI processing command, **Then** "plan-001.md" is created in /Plans with structured research steps
2. **Given** Company_Handbook.md contains company policies, **When** AI processes a task, **Then** generated plan references relevant handbook sections
3. **Given** task file contains ambiguous requirements, **When** AI processes it, **Then** plan includes clarifying questions and assumptions made
4. **Given** task file is malformed markdown, **When** AI attempts to process it, **Then** error is logged to "errors.md" and task remains in /Needs_Action
5. **Given** multiple tasks exist in /Needs_Action, **When** user triggers processing, **Then** AI processes each task sequentially and creates corresponding plans

---

### User Story 3 - Task Completion and Dashboard Updates (Priority: P3)

After a user completes work based on a plan, they manually trigger Claude Code to mark the task as done. The AI moves the task file from /Needs_Action to /Done and updates Dashboard.md to reflect current task status across all folders.

**Why this priority**: This provides closure and visibility. While less critical than intake and planning, it enables users to track progress and maintain a clean workspace.

**Independent Test**: Can be fully tested by marking a task complete via CLI command and verifying file movement and Dashboard update. Delivers value through progress tracking and workspace organization.

**Acceptance Scenarios**:

1. **Given** "task-001.md" exists in /Needs_Action and user marks it complete, **When** AI processes completion, **Then** "task-001.md" is moved to /Done folder
2. **Given** Dashboard.md exists, **When** AI completes task processing, **Then** Dashboard.md is updated with task counts: Inbox (N), Needs Action (N), Plans (N), Done (N)
3. **Given** Dashboard.md doesn't exist, **When** AI runs for first time, **Then** Dashboard.md is created with initial task summary
4. **Given** task file has corresponding plan in /Plans, **When** task is moved to /Done, **Then** plan file remains in /Plans for reference
5. **Given** multiple tasks are completed in one session, **When** AI processes completions, **Then** Dashboard.md shows accurate counts for all folders

---

### Edge Cases

- **What happens when a task file is deleted from /Needs_Action before AI processes it?** System logs a warning in errors.md and continues processing remaining tasks.
- **What happens when /Inbox contains a non-markdown file (e.g., .txt, .pdf)?** Watcher copies it to /Needs_Action, but AI logs an error during processing indicating unsupported format.
- **What happens when Dashboard.md is manually deleted?** AI recreates it on next processing run with current task counts.
- **What happens when required folders (/Inbox, /Needs_Action, /Plans, /Done) don't exist?** System initialization creates missing folders before any processing begins.
- **What happens when two users drop files with identical names simultaneously?** Watcher uses timestamp-based collision resolution (e.g., task-001-20260212-143022.md).
- **What happens when Company_Handbook.md is missing?** AI processes tasks without handbook context and logs a warning.
- **What happens when a task file is empty or contains only whitespace?** AI logs an error in errors.md indicating insufficient task description and leaves file in /Needs_Action.
- **What happens when AI is triggered while already processing?** System prevents concurrent execution and logs a message indicating processing is already in progress.

## Requirements *(mandatory)*

### Functional Requirements

**Bronze Tier Constraints** (apply to ALL requirements):
- Operations MUST be file-system based within vault boundaries
- NO external API calls, email, messaging, or network operations
- State changes MUST occur via folder transitions
- Processing MUST be manually triggered (no autonomous loops)

**Vault Structure:**

- **FR-001**: System MUST maintain a vault structure with folders: /Inbox, /Needs_Action, /Plans, /Done
- **FR-002**: System MUST create missing folders on initialization if they don't exist
- **FR-003**: System MUST maintain Dashboard.md in vault root for task status overview
- **FR-004**: System MUST maintain Company_Handbook.md in vault root as AI context reference

**File Watcher:**

- **FR-005**: System MUST monitor /Inbox folder for new file creation events
- **FR-006**: System MUST copy (not move) new files from /Inbox to /Needs_Action within 5 seconds of detection
- **FR-007**: System MUST handle filename collisions by appending numeric suffix (e.g., task-001-1.md)
- **FR-008**: System MUST preserve original file content and metadata during copy operations

**AI Processing (Manual Trigger):**

- **FR-009**: System MUST provide a CLI command to trigger AI processing of /Needs_Action folder
- **FR-010**: AI MUST read all markdown files in /Needs_Action when triggered
- **FR-011**: AI MUST interpret task content and generate structured plans
- **FR-012**: AI MUST reference Company_Handbook.md for context when generating plans
- **FR-013**: AI MUST write plan files to /Plans folder with naming convention: plan-{task-id}.md
- **FR-014**: AI MUST update Dashboard.md with current task counts after each processing run
- **FR-015**: AI MUST move completed tasks from /Needs_Action to /Done when user marks them complete

**Error Handling:**

- **FR-016**: System MUST log all errors to errors.md in vault root
- **FR-017**: System MUST continue processing remaining tasks if one task fails
- **FR-018**: System MUST validate markdown format and log errors for malformed files
- **FR-019**: System MUST handle missing Company_Handbook.md gracefully with warning log

**State Management:**

- **FR-020**: System MUST represent task lifecycle through folder location: Inbox → Needs_Action → Done
- **FR-021**: System MUST NOT use external databases or state stores
- **FR-022**: System MUST persist all state as markdown files within vault

### Key Entities

- **Task File**: Markdown file containing task description, requirements, and context. Created by user in /Inbox, processed from /Needs_Action, archived in /Done. Filename serves as unique identifier.

- **Plan File**: Markdown file containing AI-generated action plan, steps, resources, and timeline. Created by AI in /Plans folder. Linked to task file by naming convention (plan-{task-id}.md).

- **Dashboard**: Single markdown file (Dashboard.md) in vault root displaying task counts across all folders, recent activity, and system status. Updated by AI after each processing run.

- **Company Handbook**: Reference markdown file (Company_Handbook.md) containing company policies, procedures, and context. Used by AI to inform plan generation. Maintained by user.

- **Error Log**: Markdown file (errors.md) in vault root containing timestamped error messages, warnings, and processing issues. Append-only log maintained by system.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can drop a task file in /Inbox and see it appear in /Needs_Action within 5 seconds without manual intervention
- **SC-002**: AI can generate a plan from a task file within 30 seconds of manual CLI trigger
- **SC-003**: Dashboard.md accurately reflects task counts across all folders within 1 second of AI processing completion
- **SC-004**: 100% of valid markdown task files result in plan generation (no silent failures)
- **SC-005**: System operates entirely within vault boundaries with zero external network calls
- **SC-006**: User can process 50 tasks in a single session without system degradation or errors
- **SC-007**: All errors are logged to errors.md with timestamps and actionable descriptions
- **SC-008**: Task lifecycle (Inbox → Needs_Action → Done) is visible through folder structure without requiring special tools

## Assumptions

- Users have Obsidian installed and configured with a vault
- Users have Claude Code CLI installed and accessible
- File system watcher is a separate lightweight process (not part of Claude Code)
- Task files follow basic markdown format (no strict schema required)
- Users manually trigger AI processing via CLI (no scheduled automation)
- Single user environment (no concurrent multi-user access)
- Vault is stored on local file system (not network drive or cloud sync)
- Windows, macOS, or Linux operating system with standard file system operations
