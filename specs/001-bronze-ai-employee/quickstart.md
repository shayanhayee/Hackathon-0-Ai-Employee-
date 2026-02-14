# Quickstart Guide: Bronze Tier AI Employee

**Feature**: 001-bronze-ai-employee
**Version**: 1.0.0
**Last Updated**: 2026-02-12

## Overview

This guide will help you set up and use the Bronze Tier AI Employee system. The system consists of two components:
1. **File Watcher**: Python script that monitors /Inbox and copies files to /Needs_Action
2. **Claude CLI Commands**: Manual commands to process tasks, generate plans, and update dashboard

**Time to Setup**: ~15 minutes
**Prerequisites**: Python 3.11+, Claude Code CLI, Obsidian (optional but recommended)

## Prerequisites

### Required Software

1. **Python 3.11 or higher**
   - Check version: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Claude Code CLI**
   - Check installation: `claude --version`
   - Already installed per Bronze Tier assumptions

3. **Git** (recommended for version control)
   - Check version: `git --version`
   - Download: https://git-scm.com/downloads

### Optional Software

4. **Obsidian** (recommended for viewing vault)
   - Download: https://obsidian.md/download
   - Not required (can use any text editor)

## Installation

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd AI_Employee_Vault

# Verify you're on the correct branch
git branch --show-current
# Should show: 001-bronze-ai-employee
```

### Step 2: Install Python Dependencies

```bash
# Navigate to watcher directory
cd watcher

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import watchdog; print(watchdog.__version__)"
# Should print: 3.0.0 or higher
```

**Dependencies installed**:
- `watchdog>=3.0.0` - File system monitoring
- `PyYAML>=6.0` - YAML frontmatter parsing

### Step 3: Configure Vault Path

Edit `watcher/config.py` to set your vault location:

```python
# watcher/config.py

# REQUIRED: Set absolute path to your Obsidian vault
VAULT_PATH = "/Users/username/Documents/ObsidianVault"  # macOS/Linux
# VAULT_PATH = "C:/Users/username/Documents/ObsidianVault"  # Windows

# Folder names (relative to vault root)
INBOX_FOLDER = "Inbox"
NEEDS_ACTION_FOLDER = "Needs_Action"
PLANS_FOLDER = "Plans"
DONE_FOLDER = "Done"

# Watcher settings
WATCH_EXTENSIONS = [".md"]
LOG_LEVEL = "INFO"
```

**Important**: Use absolute paths, not relative paths.

### Step 4: Initialize Vault Structure

```bash
# Return to repository root
cd ..

# Run initialization script (creates folders)
python watcher/init_vault.py

# Verify folders were created
ls -la /path/to/your/vault/
# Should show: Inbox/, Needs_Action/, Plans/, Done/
```

**Manual alternative** (if script doesn't exist):
```bash
cd /path/to/your/vault
mkdir -p Inbox Needs_Action Plans Done
touch Dashboard.md Company_Handbook.md errors.md
```

### Step 5: Create Company Handbook (Optional)

Create `/path/to/your/vault/Company_Handbook.md`:

```markdown
# Company Handbook

## Company Overview
[Your company mission, vision, values]

## Policies
### Communication
[Communication guidelines]

### Project Management
[PM processes and tools]

## Market Context
### Competitors
[Competitor information]

### Target Audience
[Customer segments]

## Resources
### Tools
[Software and tools used]

### Templates
[Document templates]
```

This file provides context for AI plan generation. It's optional but recommended.

## Usage

### Starting the Watcher

The watcher monitors /Inbox for new files and copies them to /Needs_Action.

```bash
# Start watcher (foreground process)
cd watcher
python watcher.py

# You should see:
# [INFO] Watcher started
# [INFO] Monitoring: /path/to/vault/Inbox
# [INFO] Press Ctrl+C to stop
```

**Keep this terminal open** - the watcher runs in the foreground per Bronze Tier constraints.

**To stop**: Press `Ctrl+C`

### Creating a Task

1. **Create a markdown file** in `/Inbox`:

```bash
# Example: Create a task file
cat > /path/to/vault/Inbox/task-001.md << 'EOF'
---
title: Research competitor pricing
priority: high
tags: [research, pricing]
---

# Task Description

Research and analyze competitor pricing strategies for our product category.

## Requirements
- Identify top 5 competitors
- Document pricing tiers
- Analyze value propositions

## Context
Company is preparing for Q2 pricing review.
EOF
```

2. **Watcher automatically copies** to `/Needs_Action` within 5 seconds:

```
[INFO] File detected: task-001.md
[INFO] Copying to Needs_Action...
[INFO] Copy complete: task-001.md
```

3. **Verify the copy**:

```bash
ls /path/to/vault/Needs_Action/
# Should show: task-001.md
```

### Processing Tasks (Generate Plans)

**Manual trigger** - User invokes Claude CLI:

```bash
# Navigate to vault directory
cd /path/to/vault

# Process all tasks in Needs_Action
claude process-tasks

# Or process specific task
claude process-task task-001.md
```

**What happens**:
1. Claude reads all `.md` files in `/Needs_Action`
2. Claude reads `Company_Handbook.md` for context
3. Claude generates structured plan for each task
4. Claude writes plans to `/Plans/plan-{task-id}.md`
5. Claude updates `Dashboard.md` with task counts
6. Any errors logged to `errors.md`

**Verify plan was created**:

```bash
ls /path/to/vault/Plans/
# Should show: plan-task-001.md

cat /path/to/vault/Plans/plan-task-001.md
# Should show structured plan with steps, resources, etc.
```

### Viewing Dashboard

```bash
# View dashboard in terminal
cat /path/to/vault/Dashboard.md

# Or open in Obsidian
# File -> Open vault -> Select your vault
# Navigate to Dashboard.md
```

**Dashboard shows**:
- Task counts per folder
- Recent activity
- System status
- Quick stats

### Completing a Task

After you've completed the work described in a plan:

```bash
# Mark task as complete
claude complete-task task-001

# Or mark multiple tasks
claude complete-tasks task-001 task-002 task-003
```

**What happens**:
1. Claude moves task file from `/Needs_Action` to `/Done`
2. Claude updates `Dashboard.md`
3. Plan file remains in `/Plans` for reference

**Verify task was moved**:

```bash
ls /path/to/vault/Done/
# Should show: task-001.md

ls /path/to/vault/Needs_Action/
# task-001.md should be gone
```

### Viewing Errors

```bash
# View error log
cat /path/to/vault/errors.md

# Or tail for recent errors
tail -n 20 /path/to/vault/errors.md
```

## Typical Workflow

### Daily Usage Pattern

```bash
# Morning: Start watcher
cd /path/to/repo/watcher
python watcher.py
# Keep terminal open

# Throughout day: Create tasks
# Drop markdown files into /Inbox
# Watcher automatically copies to /Needs_Action

# When ready: Process tasks
cd /path/to/vault
claude process-tasks
# Review generated plans in /Plans

# Do the work
# Reference plans while working

# When done: Mark complete
claude complete-task <task-id>

# Evening: Check dashboard
cat Dashboard.md
# Review completed tasks, check for errors

# Stop watcher
# Press Ctrl+C in watcher terminal
```

### Example Session

```bash
# 1. Start watcher
$ cd watcher && python watcher.py
[INFO] Watcher started
[INFO] Monitoring: /Users/john/vault/Inbox

# 2. Create task (in another terminal)
$ cat > ~/vault/Inbox/research-pricing.md << 'EOF'
# Research competitor pricing
Analyze top 5 competitors' pricing strategies.
EOF

# Watcher output:
[INFO] File detected: research-pricing.md
[INFO] Copying to Needs_Action...
[INFO] Copy complete: research-pricing.md

# 3. Process task
$ cd ~/vault
$ claude process-tasks
Processing 1 task from Needs_Action...
✓ Generated plan for research-pricing.md
✓ Updated Dashboard.md
Done. 1 plan generated.

# 4. View plan
$ cat Plans/plan-research-pricing.md
# Plan: Research competitor pricing
[... structured plan ...]

# 5. Do the work
# [Work on the task using the plan]

# 6. Mark complete
$ claude complete-task research-pricing
✓ Moved research-pricing.md to Done
✓ Updated Dashboard.md
Task completed.

# 7. Check dashboard
$ cat Dashboard.md
# AI Employee Dashboard
Last Updated: 2026-02-12T16:30:00Z

Task Status:
- Inbox: 0
- Needs Action: 0
- Plans: 1
- Done: 1
```

## Troubleshooting

### Watcher Not Detecting Files

**Problem**: Files dropped in /Inbox don't appear in /Needs_Action

**Solutions**:
1. Check watcher is running: Look for "Watcher started" message
2. Verify vault path in `config.py` is correct (absolute path)
3. Check file extension is `.md`
4. Check file permissions (watcher needs read/write access)
5. Restart watcher: `Ctrl+C` then `python watcher.py`

### Claude Commands Not Found

**Problem**: `claude process-tasks` returns "command not found"

**Solutions**:
1. Verify Claude Code CLI is installed: `claude --version`
2. Check you're in the vault directory: `pwd`
3. Verify command files exist in `.claude/commands/`
4. Reinstall Claude Code CLI if needed

### Plans Not Generated

**Problem**: `claude process-tasks` runs but no plans appear in /Plans

**Solutions**:
1. Check errors.md for error messages
2. Verify task files are valid markdown
3. Check task files are not empty
4. Verify /Plans folder exists and is writable
5. Check Dashboard.md for processing status

### Permission Errors

**Problem**: "Permission denied" errors in watcher or errors.md

**Solutions**:
1. Check folder permissions: `ls -la /path/to/vault`
2. Ensure watcher has write access to vault
3. On macOS: Grant Terminal full disk access in System Preferences
4. On Windows: Run as administrator if needed

### Dashboard Not Updating

**Problem**: Dashboard.md shows old counts or doesn't update

**Solutions**:
1. Manually trigger update: `claude process-tasks` (even with no tasks)
2. Check Dashboard.md is not open in another program (file lock)
3. Delete Dashboard.md and let system recreate it
4. Check errors.md for write failures

## Advanced Usage

### Custom Task Templates

Create reusable task templates:

```bash
# Create templates directory
mkdir ~/vault/Templates

# Create bug report template
cat > ~/vault/Templates/bug-template.md << 'EOF'
---
title: [Bug Title]
priority: high
tags: [bug]
---

# Bug Description
[Describe the bug]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]
EOF

# Use template
cp ~/vault/Templates/bug-template.md ~/vault/Inbox/bug-login.md
# Edit bug-login.md with specific details
```

### Batch Task Creation

```bash
# Create multiple tasks at once
for i in {1..5}; do
  cat > ~/vault/Inbox/task-$i.md << EOF
# Task $i
Description for task $i
EOF
done

# Watcher will copy all 5 files to Needs_Action
```

### Filtering Tasks by Priority

```bash
# Process only high-priority tasks
cd ~/vault/Needs_Action
grep -l "priority: high" *.md | while read file; do
  claude process-task "$file"
done
```

### Archiving Old Tasks

```bash
# Move tasks older than 30 days from Done to Archive
mkdir -p ~/vault/Archive
find ~/vault/Done -name "*.md" -mtime +30 -exec mv {} ~/vault/Archive/ \;
```

## Configuration Reference

### watcher/config.py

```python
# Vault location (REQUIRED)
VAULT_PATH = "/absolute/path/to/vault"

# Folder names (relative to vault root)
INBOX_FOLDER = "Inbox"              # Where users drop tasks
NEEDS_ACTION_FOLDER = "Needs_Action"  # Where watcher copies tasks
PLANS_FOLDER = "Plans"              # Where AI writes plans
DONE_FOLDER = "Done"                # Where completed tasks go

# Watcher settings
WATCH_EXTENSIONS = [".md"]          # File types to watch
LOG_LEVEL = "INFO"                  # INFO, DEBUG, WARNING, ERROR

# Performance tuning (optional)
DEBOUNCE_SECONDS = 1                # Wait time before processing file
MAX_RETRIES = 3                     # Retry count for failed copies
```

### Environment Variables (Optional)

```bash
# Set vault path via environment variable
export AI_EMPLOYEE_VAULT="/path/to/vault"

# Set log level
export AI_EMPLOYEE_LOG_LEVEL="DEBUG"

# Use in config.py
import os
VAULT_PATH = os.getenv("AI_EMPLOYEE_VAULT", "/default/path")
```

## Best Practices

### Task File Naming

- ✅ **Good**: `research-pricing.md`, `bug-login-mobile.md`, `task-001.md`
- ❌ **Avoid**: `task.md`, `todo.md`, `my task.md` (spaces)

### Task Descriptions

- Be specific and actionable
- Include context and requirements
- Reference Company_Handbook.md sections when relevant
- Use markdown formatting for readability

### Folder Organization

- Keep /Inbox clean (files are copied, not moved)
- Archive old tasks from /Done periodically
- Review /Plans regularly for reference
- Check errors.md weekly

### Performance Tips

- Process tasks in batches (not one at a time)
- Keep Company_Handbook.md concise (<50 KB)
- Archive completed tasks older than 30 days
- Restart watcher weekly to clear memory

## Next Steps

1. **Complete setup** following installation steps above
2. **Create your first task** in /Inbox
3. **Process the task** with `claude process-tasks`
4. **Review the plan** in /Plans
5. **Complete the task** and mark it done
6. **Check Dashboard.md** to see your progress

## Getting Help

- **Errors**: Check `errors.md` in vault root
- **Logs**: Check watcher console output
- **Status**: View `Dashboard.md`
- **Documentation**: See `/specs/001-bronze-ai-employee/` for detailed docs

## Version History

- **1.0.0** (2026-02-12): Initial quickstart guide
