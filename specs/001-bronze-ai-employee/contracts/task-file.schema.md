# Task File Schema

**Version**: 1.0.0
**Feature**: 001-bronze-ai-employee
**Purpose**: Define the structure and format for task files

## Overview

Task files are user-created markdown documents that describe work to be done. They are the primary input to the Bronze Tier AI Employee system.

## File Format

**Extension**: `.md` (Markdown)
**Location**: Created in `/Inbox`, processed from `/Needs_Action`, archived in `/Done`
**Encoding**: UTF-8

## Structure

### Complete Example

```markdown
---
id: task-001
title: Research competitor pricing
priority: high
created: 2026-02-12T10:30:00Z
tags: [research, pricing, competitors]
assignee: john-doe
due_date: 2026-02-15
---

# Task Description

Research and analyze competitor pricing strategies for our product category.

## Requirements
- Identify top 5 competitors
- Document pricing tiers
- Analyze value propositions

## Context
Company is preparing for Q2 pricing review. Focus on SaaS competitors in the project management space.

## Success Criteria
- Comparison table with 5 competitors
- Analysis document with recommendations
- Presentation slides for leadership team
```

## Frontmatter Schema

**Format**: YAML
**Delimiters**: `---` (three hyphens)
**Required**: No (frontmatter is optional)

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | string | No | Unique identifier, defaults to filename stem | `task-001` |
| `title` | string | No | Human-readable task title | `Research competitor pricing` |
| `priority` | enum | No | Task priority: `high`, `medium`, `low` | `high` |
| `created` | datetime | No | ISO 8601 timestamp of task creation | `2026-02-12T10:30:00Z` |
| `tags` | array | No | Classification tags | `[research, pricing]` |
| `assignee` | string | No | Person responsible (informational only) | `john-doe` |
| `due_date` | date | No | Target completion date | `2026-02-15` |

### Validation Rules

- All fields are optional
- If present, `priority` must be one of: `high`, `medium`, `low`
- If present, `created` must be valid ISO 8601 datetime
- If present, `due_date` must be valid ISO 8601 date
- If present, `tags` must be array of strings
- Unknown fields are ignored (forward compatibility)

## Body Schema

**Format**: Markdown
**Required**: Yes (must not be empty or whitespace-only)

### Recommended Sections

While the body is freeform markdown, these sections are recommended for clarity:

1. **Task Description** (required): What needs to be done
2. **Requirements** (optional): Specific deliverables or constraints
3. **Context** (optional): Background information, why this matters
4. **Success Criteria** (optional): How to know when task is complete

### Markdown Features Supported

- Headings (`#`, `##`, `###`)
- Lists (ordered and unordered)
- Bold and italic text
- Code blocks
- Links
- Blockquotes
- Tables

### Content Guidelines

- Be specific and actionable
- Include enough context for AI to generate useful plan
- Reference Company_Handbook.md sections if relevant
- Avoid implementation details (focus on what, not how)

## Validation

### Required Validations

1. **File Extension**: Must be `.md`
2. **Encoding**: Must be UTF-8
3. **Body Content**: Must not be empty or whitespace-only
4. **Frontmatter Format**: If present, must be valid YAML between `---` delimiters

### Optional Validations

1. **Frontmatter Fields**: If present, must match schema types
2. **Markdown Syntax**: Should be valid markdown (warnings only)

### Error Handling

| Error | Severity | Action |
|-------|----------|--------|
| Empty body | Error | Log to errors.md, leave in /Needs_Action |
| Invalid frontmatter YAML | Warning | Ignore frontmatter, process body only |
| Invalid field types | Warning | Ignore invalid fields, use valid ones |
| Non-UTF-8 encoding | Error | Log to errors.md, skip processing |

## Examples

### Minimal Task (No Frontmatter)

```markdown
# Fix login bug

Users are reporting that the login button doesn't work on mobile devices. Investigate and fix.
```

### Task with Frontmatter

```markdown
---
id: bug-042
title: Fix mobile login button
priority: high
created: 2026-02-12T14:00:00Z
tags: [bug, mobile, login]
---

# Bug Description

Users are reporting that the login button doesn't work on mobile devices (iOS Safari and Android Chrome).

## Steps to Reproduce
1. Open app on mobile browser
2. Navigate to login page
3. Tap login button
4. Nothing happens

## Expected Behavior
Login form should submit and user should be authenticated.

## Context
Reported by 5 users in the last 24 hours. Blocking new user signups.
```

### Research Task

```markdown
---
title: Market research for new feature
priority: medium
tags: [research, market-analysis]
due_date: 2026-02-20
---

# Research Objective

Conduct market research to validate demand for proposed analytics dashboard feature.

## Research Questions
- What analytics features do competitors offer?
- What are users asking for in support tickets?
- What is the market size for analytics tools?

## Deliverables
- Competitive analysis document
- User survey results
- Market size estimate
```

## Naming Conventions

### Recommended Patterns

- **Descriptive**: `research-competitor-pricing.md`
- **ID-based**: `task-001.md`, `task-042.md`
- **Category-prefix**: `bug-login-mobile.md`, `feature-analytics-dashboard.md`

### Avoid

- Generic names: `task.md`, `todo.md`
- Special characters: `task#1.md`, `task@home.md`
- Spaces (use hyphens): `my task.md` → `my-task.md`

### Collision Handling

If a task file with the same name already exists in /Needs_Action, the watcher will append a numeric suffix:
- `task-001.md` → `task-001-1.md`
- `task-001-1.md` → `task-001-2.md`

## Lifecycle

```
1. User creates task file in /Inbox
2. Watcher detects new file
3. Watcher copies to /Needs_Action (original stays in /Inbox)
4. User triggers AI processing
5. AI reads task from /Needs_Action
6. AI validates task file format
7. AI generates plan in /Plans
8. User completes work
9. User triggers task completion
10. AI moves task from /Needs_Action to /Done
```

## Version History

- **1.0.0** (2026-02-12): Initial schema definition
