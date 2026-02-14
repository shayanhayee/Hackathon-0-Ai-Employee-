# Data Model: Bronze Tier AI Employee

**Feature**: 001-bronze-ai-employee
**Date**: 2026-02-12
**Purpose**: Entity definitions and relationships for Bronze Tier system

## Overview

The Bronze Tier AI Employee system uses a file-based data model where entities are represented as Markdown files with optional YAML frontmatter. All relationships are implicit through naming conventions and folder location.

## Core Entities

### Task File

**Description**: User-created markdown file containing task description, requirements, and context.

**Location**:
- Created in: `/Inbox`
- Processed from: `/Needs_Action`
- Archived in: `/Done`

**Identifier**: Filename (e.g., `task-001.md`)

**Structure**:
```yaml
---
id: task-001
title: Research competitor pricing
priority: high
created: 2026-02-12T10:30:00Z
tags: [research, pricing, competitors]
---

# Task Description

Research and analyze competitor pricing strategies for our product category.

## Requirements
- Identify top 5 competitors
- Document pricing tiers
- Analyze value propositions

## Context
Company is preparing for Q2 pricing review.
```

**Attributes**:
- `id` (optional): Unique identifier, defaults to filename stem
- `title` (optional): Human-readable task title
- `priority` (optional): high, medium, low
- `created` (optional): ISO 8601 timestamp
- `tags` (optional): Array of classification tags
- Body (required): Markdown content with task description

**Validation Rules**:
- Filename must end with `.md`
- Body must not be empty or whitespace-only
- Frontmatter is optional but must be valid YAML if present
- No size limits (Bronze Tier assumes reasonable task descriptions)

**State Transitions**:
```
/Inbox → /Needs_Action (watcher copies)
/Needs_Action → /Done (AI marks complete)
```

**Relationships**:
- Has one Plan File (linked by naming convention: `plan-{task-id}.md`)
- Referenced in Dashboard (task count aggregation)
- May generate Error Log entries (if processing fails)

---

### Plan File

**Description**: AI-generated markdown file containing structured action plan, steps, resources, and timeline.

**Location**: `/Plans`

**Identifier**: Filename following convention `plan-{task-id}.md`

**Structure**:
```yaml
---
task_id: task-001
generated: 2026-02-12T10:35:00Z
status: draft
estimated_duration: 2 hours
---

# Plan: Research competitor pricing

## Objective
Research and analyze competitor pricing strategies for our product category.

## Steps

### 1. Identify Competitors
- Search industry reports for top competitors
- Review market analysis from Company_Handbook.md
- Create list of 5 primary competitors

**Duration**: 30 minutes

### 2. Document Pricing Tiers
- Visit competitor websites
- Screenshot pricing pages
- Create comparison table

**Duration**: 45 minutes

### 3. Analyze Value Propositions
- Compare features at each tier
- Identify pricing patterns
- Document competitive advantages

**Duration**: 45 minutes

## Resources
- Company_Handbook.md (market analysis section)
- Industry reports folder
- Competitor websites

## Assumptions
- Competitor pricing is publicly available
- Focus on direct competitors only
- Analysis covers current pricing (not historical)

## Next Steps
1. Execute research steps
2. Document findings
3. Mark task complete
```

**Attributes**:
- `task_id` (required): Links to source task file
- `generated` (required): ISO 8601 timestamp of plan creation
- `status` (optional): draft, in-progress, completed
- `estimated_duration` (optional): Human-readable time estimate
- Body (required): Structured plan with steps, resources, assumptions

**Validation Rules**:
- Filename must match pattern `plan-{task-id}.md`
- `task_id` in frontmatter must match filename
- Body must contain structured plan sections
- Generated timestamp must be valid ISO 8601

**State Transitions**:
- Created in `/Plans` (no movement, stays for reference)

**Relationships**:
- Belongs to one Task File (linked by `task_id`)
- Referenced in Dashboard (plan count aggregation)

---

### Dashboard

**Description**: Single markdown file displaying task counts across all folders, recent activity, and system status.

**Location**: `/Dashboard.md` (vault root)

**Identifier**: Fixed filename `Dashboard.md`

**Structure**:
```markdown
# AI Employee Dashboard

**Last Updated**: 2026-02-12T10:40:00Z

## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | 3 | New tasks awaiting watcher |
| Needs Action | 5 | Tasks ready for AI processing |
| Plans | 12 | Generated plans |
| Done | 47 | Completed tasks |

**Total Tasks**: 55

## Recent Activity

### 2026-02-12T10:35:00Z
- ✅ Generated plan for task-001.md
- 📝 Updated task counts

### 2026-02-12T09:15:00Z
- ✅ Completed task-042.md
- 📁 Moved to Done folder

### 2026-02-12T08:30:00Z
- 📥 New task detected: task-055.md
- 📋 Copied to Needs_Action

## System Status

- **Watcher**: Running
- **Last Error**: None
- **Vault Path**: /Users/username/Documents/ObsidianVault
```

**Attributes**:
- Last Updated (required): ISO 8601 timestamp
- Task counts (required): Count per folder
- Recent activity (optional): Chronological log of recent operations
- System status (optional): Watcher status, errors, configuration

**Validation Rules**:
- Must exist in vault root
- Task counts must be non-negative integers
- Last Updated must be valid ISO 8601 timestamp
- Created automatically if missing

**State Transitions**:
- Updated in place (no movement)
- Recreated if deleted

**Relationships**:
- Aggregates Task Files (counts per folder)
- Aggregates Plan Files (total count)
- References Error Log (last error status)

---

### Company Handbook

**Description**: User-maintained reference markdown file containing company policies, procedures, and context.

**Location**: `/Company_Handbook.md` (vault root)

**Identifier**: Fixed filename `Company_Handbook.md`

**Structure**:
```markdown
# Company Handbook

## Company Overview
[Company mission, vision, values]

## Policies
### Communication
[Communication guidelines]

### Project Management
[PM processes and tools]

## Market Context
### Competitors
[Competitor analysis]

### Target Audience
[Customer segments]

## Resources
### Tools
[Software and tools used]

### Templates
[Document templates]
```

**Attributes**:
- Freeform markdown content
- No required structure (user-defined)
- Sections organized by topic

**Validation Rules**:
- Must be valid markdown
- Optional (AI logs warning if missing)
- No size limits

**State Transitions**:
- User-maintained (no automatic updates)

**Relationships**:
- Referenced by AI during plan generation
- Not modified by system

---

### Error Log

**Description**: System-maintained markdown file containing timestamped error messages, warnings, and processing issues.

**Location**: `/errors.md` (vault root)

**Identifier**: Fixed filename `errors.md`

**Structure**:
```markdown
# Error Log

## 2026-02-12T10:45:00Z - File Copy Error

**Type**: Watcher Error
**Severity**: Warning

Failed to copy task-003.md from Inbox to Needs_Action.

**Reason**: Permission denied (file locked by another process)

**Action**: File will be retried on next watcher cycle. Check file permissions if error persists.

---

## 2026-02-12T09:20:00Z - Validation Error

**Type**: AI Processing Error
**Severity**: Error

Failed to process empty-task.md from Needs_Action.

**Reason**: Task file contains no content (empty or whitespace-only)

**Action**: Task remains in Needs_Action. Add task description and reprocess.

---

## 2026-02-12T08:15:00Z - Missing Reference

**Type**: AI Processing Warning
**Severity**: Warning

Company_Handbook.md not found in vault root.

**Reason**: File does not exist

**Action**: AI will process tasks without handbook context. Create Company_Handbook.md for better plan generation.
```

**Attributes**:
- Timestamp (required): ISO 8601 format
- Type (required): Error category (Watcher Error, AI Processing Error, Validation Error)
- Severity (required): Error, Warning, Info
- Reason (required): Technical explanation
- Action (required): User guidance for resolution

**Validation Rules**:
- Append-only (no deletions or edits)
- Entries in reverse chronological order (newest first)
- Created automatically if missing

**State Transitions**:
- Appended to (no movement)

**Relationships**:
- References Task Files (when processing fails)
- Referenced in Dashboard (last error status)

---

## Entity Relationships

```
Task File (1) ──────── (1) Plan File
    │                       │
    │                       │
    └───────────┬───────────┘
                │
                ▼
            Dashboard (aggregates counts)
                │
                ▼
            Error Log (logs failures)

Company Handbook ──(referenced by)──> AI Processing
```

**Relationship Rules**:
- Task File to Plan File: One-to-one, linked by naming convention
- Task File to Dashboard: Many-to-one, aggregated by folder location
- Task File to Error Log: One-to-many, logged when processing fails
- Company Handbook to AI Processing: Referenced during plan generation (optional)

---

## Naming Conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Task File | `{name}.md` | `task-001.md`, `urgent-bug-fix.md` |
| Plan File | `plan-{task-id}.md` | `plan-task-001.md`, `plan-urgent-bug-fix.md` |
| Dashboard | `Dashboard.md` | `Dashboard.md` (fixed) |
| Company Handbook | `Company_Handbook.md` | `Company_Handbook.md` (fixed) |
| Error Log | `errors.md` | `errors.md` (fixed) |

**Collision Handling**:
- Task files with duplicate names get numeric suffix: `task-001-1.md`, `task-001-2.md`
- Plan files follow task file naming: `plan-task-001-1.md`
- Fixed filenames (Dashboard, Handbook, errors) never collide

---

## Data Lifecycle

### Task File Lifecycle
```
1. User creates task in /Inbox
2. Watcher copies to /Needs_Action (original stays in /Inbox)
3. User triggers AI processing
4. AI reads task from /Needs_Action
5. AI generates plan in /Plans
6. User completes work
7. User triggers task completion
8. AI moves task from /Needs_Action to /Done
```

### Plan File Lifecycle
```
1. AI generates plan in /Plans
2. Plan remains in /Plans (never moved)
3. User references plan during work
4. Plan archived with task (stays in /Plans for reference)
```

### Dashboard Lifecycle
```
1. Created on first AI processing run (if missing)
2. Updated after each AI operation
3. User can view anytime
4. Recreated if manually deleted
```

### Error Log Lifecycle
```
1. Created on first error (if missing)
2. Appended to on each error
3. User reviews periodically
4. User can archive/clear manually (system recreates as needed)
```

---

## Storage Considerations

**File System Layout**:
```
vault/
├── Dashboard.md              # ~2 KB (updated frequently)
├── Company_Handbook.md       # ~10-50 KB (user-maintained)
├── errors.md                 # ~5-20 KB (grows over time)
├── Inbox/
│   └── *.md                  # Variable size, temporary
├── Needs_Action/
│   └── *.md                  # Variable size, active tasks
├── Plans/
│   └── plan-*.md             # ~2-5 KB each, permanent
└── Done/
    └── *.md                  # Variable size, archive
```

**Growth Estimates** (50 tasks/session, 1000 files in vault):
- Task files: ~1-5 KB each = 1-5 MB total
- Plan files: ~2-5 KB each = 2-5 MB total
- Dashboard: ~2 KB (constant)
- Error log: ~5-20 KB (grows slowly)
- **Total**: ~3-10 MB for 1000 tasks

**Bronze Tier Scope**: No size limits, no cleanup automation. User manages vault size manually.

---

## Constitutional Compliance

All entities comply with Bronze Tier constitution:

- ✅ **File System as Interface**: All entities are files
- ✅ **Markdown as Protocol**: All entities use Markdown format
- ✅ **Folder-Based State Machine**: Task state represented by folder location
- ✅ **Local-First Architecture**: All data stored locally in vault
- ✅ **No External Integration**: No databases, no external storage
