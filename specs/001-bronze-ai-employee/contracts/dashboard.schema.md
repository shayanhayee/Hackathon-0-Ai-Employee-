# Dashboard Schema

**Version**: 1.0.0
**Feature**: 001-bronze-ai-employee
**Purpose**: Define the structure and format for the Dashboard.md file

## Overview

Dashboard.md is an AI-maintained markdown file that provides a real-time overview of task status, recent activity, and system health. It serves as the primary interface for monitoring the Bronze Tier AI Employee system.

## File Format

**Extension**: `.md` (Markdown)
**Location**: `/Dashboard.md` (vault root)
**Encoding**: UTF-8
**Filename**: Fixed as `Dashboard.md`

## Structure

### Complete Example

```markdown
# AI Employee Dashboard

**Last Updated**: 2026-02-12T16:45:00Z

## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | 3 | New tasks awaiting watcher |
| Needs Action | 5 | Tasks ready for AI processing |
| Plans | 12 | Generated plans |
| Done | 47 | Completed tasks |

**Total Tasks**: 55

## Recent Activity

### 2026-02-12T16:45:00Z - Plan Generated
- ✅ Generated plan for `task-055.md`
- 📝 Plan saved to `/Plans/plan-task-055.md`
- 📊 Updated task counts

### 2026-02-12T15:30:00Z - Task Completed
- ✅ Completed `task-042.md`
- 📁 Moved from `/Needs_Action` to `/Done`
- 📊 Updated task counts

### 2026-02-12T14:15:00Z - File Detected
- 📥 New task detected: `urgent-bug-fix.md`
- 📋 Copied from `/Inbox` to `/Needs_Action`
- ⏱️ Detection time: 2.3 seconds

### 2026-02-12T13:00:00Z - Processing Session
- 🔄 Processed 3 tasks from `/Needs_Action`
- ✅ Generated 3 plans
- ⚠️ 1 warning (see errors.md)

### 2026-02-12T11:45:00Z - System Start
- 🚀 Watcher started
- 📂 Vault path: `/Users/username/Documents/ObsidianVault`
- ✅ All folders verified

## System Status

**Watcher**: ✅ Running
**Last Error**: None
**Vault Path**: `/Users/username/Documents/ObsidianVault`
**Python Version**: 3.11.5
**Watchdog Version**: 3.0.0

## Quick Stats

- **Tasks Today**: 8 created, 5 completed
- **Plans Generated**: 12 total, 3 today
- **Average Processing Time**: 18 seconds
- **Success Rate**: 95% (1 error in last 20 tasks)

## Health Indicators

| Indicator | Status | Details |
|-----------|--------|---------|
| File Detection | ✅ Healthy | Average 2.1s detection time |
| Plan Generation | ✅ Healthy | Average 18s generation time |
| Error Rate | ✅ Healthy | <5% error rate |
| Vault Access | ✅ Healthy | All folders accessible |
```

## Schema Definition

### Header Section

**Required**: Yes

```markdown
# AI Employee Dashboard

**Last Updated**: {ISO 8601 timestamp}
```

**Fields**:
- Title: Fixed as "AI Employee Dashboard"
- Last Updated: ISO 8601 timestamp of last dashboard update

### Task Status Section

**Required**: Yes

```markdown
## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | {count} | New tasks awaiting watcher |
| Needs Action | {count} | Tasks ready for AI processing |
| Plans | {count} | Generated plans |
| Done | {count} | Completed tasks |

**Total Tasks**: {sum of all counts}
```

**Fields**:
- Inbox count: Number of `.md` files in `/Inbox`
- Needs Action count: Number of `.md` files in `/Needs_Action`
- Plans count: Number of `.md` files in `/Plans`
- Done count: Number of `.md` files in `/Done`
- Total Tasks: Sum of all folder counts

**Validation**:
- All counts must be non-negative integers
- Total must equal sum of individual counts

### Recent Activity Section

**Required**: No (but recommended)

```markdown
## Recent Activity

### {ISO 8601 timestamp} - {Activity Type}
- {emoji} {Description line 1}
- {emoji} {Description line 2}
- {emoji} {Description line 3}
```

**Activity Types**:
- Plan Generated
- Task Completed
- File Detected
- Processing Session
- System Start
- Error Occurred

**Emoji Guide**:
- ✅ Success/completion
- 📥 Incoming/new
- 📋 Copy/move
- 📁 Folder operation
- 📊 Update/statistics
- 🔄 Processing
- ⚠️ Warning
- ❌ Error
- 🚀 System start

**Ordering**: Reverse chronological (newest first)
**Limit**: Last 10 activities (optional, can show more)

### System Status Section

**Required**: Yes

```markdown
## System Status

**Watcher**: {status emoji} {status text}
**Last Error**: {error summary or "None"}
**Vault Path**: {absolute path to vault}
**Python Version**: {version}
**Watchdog Version**: {version}
```

**Status Values**:
- Watcher: "✅ Running", "⏸️ Stopped", "❌ Error"
- Last Error: Error summary or "None"
- Vault Path: Absolute file system path
- Versions: Informational only

### Quick Stats Section

**Required**: No (optional)

```markdown
## Quick Stats

- **Tasks Today**: {created} created, {completed} completed
- **Plans Generated**: {total} total, {today} today
- **Average Processing Time**: {seconds} seconds
- **Success Rate**: {percentage}% ({errors} error in last {total} tasks)
```

**Calculations**:
- Tasks Today: Count of tasks created/completed since midnight
- Plans Generated: Total count and today's count
- Average Processing Time: Mean time for plan generation
- Success Rate: (successful tasks / total tasks) × 100

### Health Indicators Section

**Required**: No (optional)

```markdown
## Health Indicators

| Indicator | Status | Details |
|-----------|--------|---------|
| File Detection | {status} | {metric} |
| Plan Generation | {status} | {metric} |
| Error Rate | {status} | {metric} |
| Vault Access | {status} | {metric} |
```

**Status Values**:
- ✅ Healthy: Metric within normal range
- ⚠️ Warning: Metric approaching threshold
- ❌ Critical: Metric exceeds threshold

**Thresholds**:
- File Detection: <5s healthy, 5-10s warning, >10s critical
- Plan Generation: <30s healthy, 30-60s warning, >60s critical
- Error Rate: <5% healthy, 5-10% warning, >10% critical
- Vault Access: All folders accessible = healthy

## Update Triggers

Dashboard.md is updated after these events:

1. **Plan Generation**: After AI generates a plan
2. **Task Completion**: After AI moves task to /Done
3. **File Detection**: After watcher copies file to /Needs_Action (optional)
4. **Processing Session**: After batch processing multiple tasks
5. **System Start**: When watcher starts
6. **Error Occurrence**: When any error is logged

## Update Procedure

```python
def update_dashboard(vault_path, activity_type, details):
    # 1. Count files in each folder
    inbox_count = count_md_files(vault_path / "Inbox")
    needs_action_count = count_md_files(vault_path / "Needs_Action")
    plans_count = count_md_files(vault_path / "Plans")
    done_count = count_md_files(vault_path / "Done")

    # 2. Generate timestamp
    timestamp = datetime.now().isoformat()

    # 3. Create activity entry
    activity = format_activity(timestamp, activity_type, details)

    # 4. Read existing dashboard (if exists)
    dashboard_path = vault_path / "Dashboard.md"
    if dashboard_path.exists():
        existing_content = dashboard_path.read_text()
        activities = extract_activities(existing_content)
    else:
        activities = []

    # 5. Prepend new activity (keep last 10)
    activities.insert(0, activity)
    activities = activities[:10]

    # 6. Generate new dashboard content
    content = generate_dashboard(
        timestamp=timestamp,
        counts={
            "inbox": inbox_count,
            "needs_action": needs_action_count,
            "plans": plans_count,
            "done": done_count
        },
        activities=activities
    )

    # 7. Write atomically (temp file + rename)
    temp_path = vault_path / ".Dashboard.md.tmp"
    temp_path.write_text(content)
    temp_path.rename(dashboard_path)
```

## Validation

### Required Validations

1. **File Location**: Must be in vault root
2. **Filename**: Must be exactly `Dashboard.md`
3. **Encoding**: Must be UTF-8
4. **Last Updated**: Must be valid ISO 8601 timestamp
5. **Task Counts**: Must be non-negative integers

### Optional Validations

1. **Total Calculation**: Total should equal sum of folder counts
2. **Activity Timestamps**: Should be valid ISO 8601
3. **Activity Ordering**: Should be reverse chronological

### Error Handling

| Error | Severity | Action |
|-------|----------|--------|
| Missing dashboard | Info | Create new dashboard |
| Corrupted content | Warning | Recreate from scratch |
| Invalid counts | Error | Recount files, log error |
| Write failure | Error | Log to errors.md, retry |

## Examples

### Minimal Dashboard (Required Sections Only)

```markdown
# AI Employee Dashboard

**Last Updated**: 2026-02-12T10:00:00Z

## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | 0 | New tasks awaiting watcher |
| Needs Action | 0 | Tasks ready for AI processing |
| Plans | 0 | Generated plans |
| Done | 0 | Completed tasks |

**Total Tasks**: 0

## System Status

**Watcher**: ✅ Running
**Last Error**: None
**Vault Path**: `/Users/username/Documents/ObsidianVault`
**Python Version**: 3.11.5
**Watchdog Version**: 3.0.0
```

### Dashboard After First Task

```markdown
# AI Employee Dashboard

**Last Updated**: 2026-02-12T10:35:00Z

## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | 1 | New tasks awaiting watcher |
| Needs Action | 1 | Tasks ready for AI processing |
| Plans | 1 | Generated plans |
| Done | 0 | Completed tasks |

**Total Tasks**: 3

## Recent Activity

### 2026-02-12T10:35:00Z - Plan Generated
- ✅ Generated plan for `task-001.md`
- 📝 Plan saved to `/Plans/plan-task-001.md`
- 📊 Updated task counts

### 2026-02-12T10:30:00Z - File Detected
- 📥 New task detected: `task-001.md`
- 📋 Copied from `/Inbox` to `/Needs_Action`
- ⏱️ Detection time: 1.8 seconds

## System Status

**Watcher**: ✅ Running
**Last Error**: None
**Vault Path**: `/Users/username/Documents/ObsidianVault`
**Python Version**: 3.11.5
**Watchdog Version**: 3.0.0
```

## Lifecycle

```
1. Dashboard created on first AI processing run (if missing)
2. Updated after each AI operation (plan generation, task completion)
3. Optionally updated after watcher events (file detection)
4. User can view anytime in Obsidian
5. If manually deleted, recreated on next update
6. Never moved or archived
```

## Performance Considerations

- **File Counting**: Use efficient directory listing (not recursive search)
- **Atomic Writes**: Write to temp file, then rename (prevents corruption)
- **Activity Limit**: Keep only last 10 activities (prevents unbounded growth)
- **Update Frequency**: Update only on significant events (not every second)

## Constitutional Compliance

- ✅ **File System as Interface**: Dashboard is a file
- ✅ **Markdown as Protocol**: Dashboard uses Markdown format
- ✅ **Local-First Architecture**: Stored locally in vault
- ✅ **No External Integration**: No external services

## Version History

- **1.0.0** (2026-02-12): Initial schema definition
