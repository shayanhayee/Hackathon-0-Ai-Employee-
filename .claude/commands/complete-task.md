# Complete Task

Mark a task as complete by moving it from Needs_Action to Done and updating the Dashboard.

## Command Description

This command moves a completed task file from `/Needs_Action` to `/Done` and updates `Dashboard.md` to reflect the current system state.

## Workflow

1. **Validate Input**: Check that task ID is provided
2. **Find Task File**: Locate the task file in `/Needs_Action`
3. **Move File**: Move task from `/Needs_Action` to `/Done`
4. **Update Dashboard**: Update task counts and log activity
5. **Report Success**: Confirm completion to user

## Implementation

Get vault path and task ID from command arguments:

```python
from pathlib import Path
import os
import sys
from datetime import datetime

vault_path = Path(os.getenv("AI_EMPLOYEE_VAULT", ""))

# Get task ID from command arguments
# Usage: claude complete-task task-001
if len(sys.argv) < 2:
    print("Error: Task ID required")
    print("Usage: claude complete-task <task-id>")
    sys.exit(1)

task_id = sys.argv[1]
```

Find and validate task file:

```python
needs_action_dir = vault_path / "Needs_Action"
done_dir = vault_path / "Done"

# Find task file (with or without .md extension)
task_filename = task_id if task_id.endswith(".md") else f"{task_id}.md"
task_file = needs_action_dir / task_filename

if not task_file.exists():
    print(f"Error: Task file not found: {task_filename}")
    print(f"Looked in: {needs_action_dir}")
    sys.exit(1)
```

Move task file to Done folder:

```python
# Ensure Done directory exists
done_dir.mkdir(parents=True, exist_ok=True)

# Move file
target_path = done_dir / task_filename
task_file.rename(target_path)

print(f"✓ Moved {task_filename} to Done")
```

Update Dashboard.md:

```python
dashboard_path = vault_path / "Dashboard.md"
timestamp = datetime.now().isoformat()
timestamp_readable = datetime.now().strftime("%Y-%m-%d %I:%M %p")

# Count files in each folder
inbox_count = len(list((vault_path / "Inbox").glob("*.md")))
needs_action_count = len(list((vault_path / "Needs_Action").glob("*.md")))
plans_count = len(list((vault_path / "Plans").glob("*.md")))
done_count = len(list((vault_path / "Done").glob("*.md")))
total_count = inbox_count + needs_action_count + plans_count + done_count

# Create or update Dashboard
dashboard_content = f"""# AI Employee Dashboard

**Last Updated**: {timestamp}

## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | {inbox_count} | New tasks awaiting watcher |
| Needs Action | {needs_action_count} | Tasks ready for AI processing |
| Plans | {plans_count} | Generated plans |
| Done | {done_count} | Completed tasks |

**Total Tasks**: {total_count}

## Recent Activity

### {timestamp} - Task Completed
- ✅ Completed `{task_filename}`
- 📁 Moved from `/Needs_Action` to `/Done`
- 📊 Updated task counts

"""

# If dashboard exists, preserve previous activities (keep last 10)
if dashboard_path.exists():
    existing_content = dashboard_path.read_text(encoding="utf-8")

    # Extract previous activities (simple approach: find "## Recent Activity" section)
    if "## Recent Activity" in existing_content:
        activity_section = existing_content.split("## Recent Activity")[1]
        # Get previous activity entries (lines starting with ###)
        previous_activities = []
        for line in activity_section.split("\n"):
            if line.startswith("###"):
                previous_activities.append(line)

        # Keep last 9 previous activities (we're adding 1 new one)
        if previous_activities:
            dashboard_content += "\n".join(previous_activities[:9]) + "\n"

# Write dashboard
dashboard_path.write_text(dashboard_content, encoding="utf-8")

print(f"✓ Updated Dashboard.md")
```

## Dashboard Update Logic

The Dashboard.md file should follow this structure:

```markdown
# AI Employee Dashboard

**Last Updated**: {ISO 8601 timestamp}

## Task Status

| Folder | Count | Description |
|--------|-------|-------------|
| Inbox | {count} | New tasks awaiting watcher |
| Needs Action | {count} | Tasks ready for AI processing |
| Plans | {count} | Generated plans |
| Done | {count} | Completed tasks |

**Total Tasks**: {sum}

## Recent Activity

### {timestamp} - Task Completed
- ✅ Completed `{filename}`
- 📁 Moved from `/Needs_Action` to `/Done`
- 📊 Updated task counts

### {timestamp} - Plan Generated
- ✅ Generated plan for `{filename}`
- 📝 Plan saved to `/Plans/{plan-filename}`
- 📊 Updated task counts

{... keep last 10 activities}
```

## Error Handling

If task file doesn't exist:
```python
print(f"Error: Task file not found: {task_filename}")
print(f"Available tasks in Needs_Action:")
for f in needs_action_dir.glob("*.md"):
    print(f"  - {f.name}")
sys.exit(1)
```

If Dashboard.md doesn't exist, create it:
```python
# Dashboard creation is handled in the update logic above
# If file doesn't exist, it will be created with initial content
```

## Usage

```bash
# Complete a single task
claude complete-task task-001

# Complete task with .md extension
claude complete-task task-001.md

# The command will:
# 1. Move task-001.md from /Needs_Action to /Done
# 2. Update Dashboard.md with new counts
# 3. Log activity in Dashboard.md
```

## Expected Output

```
✓ Moved task-001.md to Done
✓ Updated Dashboard.md
Task completed.
```

## Notes

- Task file must exist in `/Needs_Action` folder
- Plan file (if exists) remains in `/Plans` for reference
- Dashboard.md is created if it doesn't exist
- Recent activity limited to last 10 entries
- All operations are atomic (file moves are atomic on most file systems)
