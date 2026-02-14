# Bronze Tier AI Employee - Watcher Component

File system watcher that monitors the Inbox folder and automatically copies new markdown files to Needs_Action for AI processing.

## Overview

The watcher is a Python script that runs in the foreground and monitors your Obsidian vault's `/Inbox` folder. When you drop a new markdown file into `/Inbox`, the watcher automatically copies it to `/Needs_Action` within 5 seconds, making it ready for AI processing.

## Features

- **Automatic file detection**: Monitors `/Inbox` for new `.md` files
- **Fast copying**: Files appear in `/Needs_Action` within 5 seconds
- **Collision handling**: Duplicate filenames get numeric suffixes (task-001-1.md)
- **Error logging**: All errors logged to `errors.md` with timestamps
- **Vault boundary validation**: Ensures all operations stay within vault
- **Graceful shutdown**: Clean stop with Ctrl+C

## Prerequisites

- Python 3.11 or higher
- Obsidian vault (or any folder structure)
- pip (Python package manager)

## Installation

1. **Install Python dependencies**:

```bash
cd watcher
pip install -r requirements.txt
```

This installs:
- `watchdog>=3.0.0` - File system monitoring
- `PyYAML>=6.0` - YAML frontmatter parsing

2. **Configure vault path**:

Edit `watcher/config.py` and set your vault path:

```python
VAULT_PATH = "/absolute/path/to/your/vault"
```

Or set environment variable:

```bash
export AI_EMPLOYEE_VAULT="/absolute/path/to/your/vault"
```

3. **Initialize vault structure**:

```bash
python watcher/init_vault.py /path/to/your/vault
```

This creates:
- `/Inbox` - Drop tasks here
- `/Needs_Action` - Watcher copies files here
- `/Plans` - AI writes plans here
- `/Done` - Completed tasks archived here
- `Dashboard.md` - Task status overview
- `Company_Handbook.md` - AI context reference
- `errors.md` - Error log

## Usage

### Starting the Watcher

```bash
cd watcher
python watcher.py
```

You should see:

```
============================================================
Bronze Tier AI Employee - File Watcher
============================================================
[INFO] Validating vault configuration...
[INFO] ✓ Vault path: /path/to/vault
[INFO] ✓ Inbox folder: /path/to/vault/Inbox
[INFO] ✓ Needs_action folder: /path/to/vault/Needs_Action
[INFO] ✓ Plans folder: /path/to/vault/Plans
[INFO] ✓ Done folder: /path/to/vault/Done

[INFO] Starting watcher...
[INFO] Monitoring: /path/to/vault/Inbox
[INFO] Press Ctrl+C to stop
```

### Stopping the Watcher

Press `Ctrl+C` to stop:

```
[INFO] Stopping watcher...
[INFO] ✓ Watcher stopped
============================================================
```

### Creating Tasks

Drop a markdown file into `/Inbox`:

```bash
echo "# Research competitor pricing" > vault/Inbox/task-001.md
```

The watcher will automatically:
1. Detect the new file
2. Copy it to `/Needs_Action`
3. Log the operation

Console output:

```
[INFO] File detected: task-001.md
[INFO] Copying to Needs_Action...
[INFO] ✓ Copy complete: task-001.md
```

## Configuration

### config.py

```python
# Vault path (required)
VAULT_PATH = "/absolute/path/to/vault"

# Folder names (relative to vault root)
INBOX_FOLDER = "Inbox"
NEEDS_ACTION_FOLDER = "Needs_Action"
PLANS_FOLDER = "Plans"
DONE_FOLDER = "Done"

# Watcher settings
WATCH_EXTENSIONS = [".md"]  # Only watch markdown files
LOG_LEVEL = "INFO"  # INFO, DEBUG, WARNING, ERROR

# Performance tuning
DEBOUNCE_SECONDS = 1  # Wait time before processing file
MAX_RETRIES = 3  # Retry count for failed copies
```

### Environment Variables

```bash
# Set vault path via environment variable
export AI_EMPLOYEE_VAULT="/path/to/vault"

# Set log level
export AI_EMPLOYEE_LOG_LEVEL="DEBUG"
```

## File Structure

```
watcher/
├── watcher.py          # Main watcher script
├── config.py           # Configuration
├── file_handler.py     # File operations utilities
├── init_vault.py       # Vault initialization script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## How It Works

1. **Startup**: Validates vault path and folder structure
2. **Monitoring**: Uses watchdog library to monitor `/Inbox`
3. **Detection**: Detects new `.md` file creation events
4. **Filtering**: Ignores non-markdown files
5. **Copying**: Copies file to `/Needs_Action` with collision handling
6. **Logging**: Logs all operations to console and errors to `errors.md`

## Collision Handling

If a file with the same name already exists in `/Needs_Action`:

```
task-001.md → task-001-1.md
task-001.md → task-001-2.md (if task-001-1.md exists)
```

## Error Handling

All errors are logged to `vault/errors.md`:

```markdown
## 2026-02-12T14:30:00Z - File Copy Error

Failed to copy task-001.md from Inbox to Needs_Action.
Reason: Permission denied
Action: Check file permissions and try again.
```

## Troubleshooting

### Watcher won't start

**Error**: `Configuration error: VAULT_PATH not configured`

**Solution**: Set `VAULT_PATH` in `config.py` or `AI_EMPLOYEE_VAULT` environment variable

---

**Error**: `Vault validation failed: Vault path does not exist`

**Solution**: Create the vault directory or fix the path in `config.py`

---

**Error**: `Missing folders: inbox, needs_action`

**Solution**: Run `python watcher/init_vault.py /path/to/vault`

### Files not being copied

**Problem**: Files dropped in `/Inbox` don't appear in `/Needs_Action`

**Solutions**:
1. Check watcher is running (look for "Monitoring" message)
2. Verify file extension is `.md`
3. Check console for error messages
4. Check `errors.md` for logged errors
5. Verify vault path is correct

### Permission errors

**Problem**: "Permission denied" errors

**Solutions**:
1. Check folder permissions: `ls -la /path/to/vault`
2. Ensure watcher has write access to vault
3. On macOS: Grant Terminal full disk access in System Preferences
4. On Windows: Run as administrator if needed

## Bronze Tier Constraints

This watcher follows Bronze Tier constitutional constraints:

- ✅ **Local-First**: All operations within vault boundaries
- ✅ **File System Interface**: Uses only file operations
- ✅ **Manual Trigger**: Watcher only copies files, doesn't process them
- ✅ **No External Integration**: No APIs, no network calls
- ✅ **Foreground Process**: Runs in foreground, not as daemon

## Next Steps

After starting the watcher:

1. **Create tasks**: Drop markdown files in `/Inbox`
2. **Process tasks**: Run `claude process-tasks` to generate plans
3. **Complete tasks**: Run `claude complete-task <task-id>` when done
4. **Check dashboard**: View `Dashboard.md` for system status

## License

Part of the Bronze Tier AI Employee project.
