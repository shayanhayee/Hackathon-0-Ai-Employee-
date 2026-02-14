# Research: Bronze Tier AI Employee

**Feature**: 001-bronze-ai-employee
**Date**: 2026-02-12
**Purpose**: Technology evaluation and decision rationale for Bronze Tier implementation

## Overview

This document captures research findings and technology decisions for the Bronze Tier AI Employee system. All decisions prioritize simplicity, local-first operation, and constitutional compliance.

## Decision 1: File Watcher Technology

### Requirement
Monitor /Inbox folder for new file creation events and copy files to /Needs_Action within 5 seconds.

### Options Evaluated

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Python watchdog | Cross-platform, event-driven, mature library (10+ years), 6k+ stars | Requires Python runtime | ✅ **SELECTED** |
| Node.js chokidar | Popular, well-maintained, good performance | Adds Node.js dependency, JavaScript complexity | ❌ Rejected |
| Bash inotify-tools | Native Linux, zero dependencies, very fast | Linux-only, not cross-platform | ❌ Rejected |
| Python polling loop | No external dependencies, simple | Inefficient, high CPU usage, slower detection | ❌ Rejected |

### Decision: Python watchdog 3.0+

**Rationale**:
- Cross-platform support (Windows, macOS, Linux) aligns with target platform requirements
- Event-driven architecture provides <5s detection time without polling overhead
- Mature library with stable API and active maintenance
- Simple Python API: `Observer`, `FileSystemEventHandler` pattern
- Bronze Tier allows Python dependencies for watcher component

**Implementation Notes**:
- Use `watchdog.observers.Observer` for cross-platform file system monitoring
- Implement custom `FileSystemEventHandler` subclass for file creation events
- Filter for `.md` files only (markdown requirement)
- Run as foreground process (no daemon mode per Bronze Tier constraints)

**References**:
- watchdog documentation: https://python-watchdog.readthedocs.io/
- PyPI package: https://pypi.org/project/watchdog/

---

## Decision 2: Markdown Parsing

### Requirement
Parse task files with YAML frontmatter and markdown body. Extract metadata and content for AI processing.

### Options Evaluated

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| PyYAML + plain text | Lightweight, standard library compatible, simple | Manual frontmatter splitting | ✅ **SELECTED** |
| python-frontmatter | Purpose-built for frontmatter, clean API | Additional dependency, overkill for simple parsing | ❌ Rejected |
| markdown library | Full markdown parsing, AST generation | Heavy, unnecessary for Bronze Tier, complex | ❌ Rejected |
| Regex parsing | Zero dependencies | Fragile, error-prone, hard to maintain | ❌ Rejected |

### Decision: PyYAML + plain text splitting

**Rationale**:
- PyYAML is widely used, stable, and handles YAML frontmatter parsing
- Plain text splitting for frontmatter/body is simple and sufficient
- No need for full markdown AST (AI processes raw markdown)
- Minimal dependencies align with Bronze Tier simplicity

**Implementation Notes**:
- Split file on `---` delimiters to extract frontmatter
- Use `yaml.safe_load()` for frontmatter parsing
- Keep body as plain text (no markdown-to-HTML conversion needed)
- Handle missing frontmatter gracefully (optional metadata)

**Example Code Pattern**:
```python
import yaml

def parse_task_file(content):
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
    else:
        frontmatter = {}
        body = content.strip()
    return frontmatter, body
```

---

## Decision 3: File Operations

### Requirement
Copy files from /Inbox to /Needs_Action, handle collisions, move files between folders, atomic writes.

### Options Evaluated

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Python pathlib | Standard library, cross-platform, modern API | None significant | ✅ **SELECTED** |
| shutil | Standard library, high-level operations | Less modern API than pathlib | ❌ Rejected (pathlib preferred) |
| os module | Standard library, low-level control | Verbose, platform-specific path handling | ❌ Rejected |

### Decision: Python pathlib (standard library)

**Rationale**:
- Standard library (no external dependencies)
- Cross-platform path handling (Windows vs Unix paths)
- Modern, readable API: `Path.read_text()`, `Path.write_text()`, `Path.rename()`
- Built-in existence checks, directory creation, file iteration

**Implementation Notes**:
- Use `Path.read_text()` for reading markdown files
- Use `Path.write_text()` for atomic writes (write to temp, then rename)
- Use `Path.rename()` for moving files between folders
- Use `Path.exists()` for collision detection
- Use `Path.mkdir(parents=True, exist_ok=True)` for folder creation

**Collision Handling Strategy**:
```python
def get_unique_path(target_dir, filename):
    path = target_dir / filename
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 1
    while True:
        new_path = target_dir / f"{stem}-{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1
```

---

## Decision 4: AI Processing Interface

### Requirement
Manual Claude CLI invocation to process tasks, generate plans, update dashboard.

### Options Evaluated

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Claude Code CLI commands | Manual trigger, already installed, reusable workflows | Requires user invocation | ✅ **SELECTED** |
| Python script calling Claude API | Programmatic control | Violates Zero External Integration (API calls) | ❌ Rejected |
| Autonomous agent loop | Fully automated | Violates Manual Trigger Model | ❌ Rejected |
| Bash scripts | Simple, no dependencies | Less readable, harder to maintain | ❌ Rejected |

### Decision: Claude Code CLI with custom command files

**Rationale**:
- Manual trigger model (user runs `claude <command>`)
- Claude Code already installed per assumptions
- Command files in `.claude/commands/` provide reusable workflows
- No external API calls (CLI operates locally)
- Aligns with Manual Trigger Model principle

**Implementation Notes**:
- Create `.claude/commands/process-tasks.md` for task processing workflow
- Create `.claude/commands/complete-task.md` for task completion workflow
- Commands read from /Needs_Action, write to /Plans, update Dashboard.md
- User invokes: `claude process-tasks` or `claude complete-task <task-id>`

**Command File Structure**:
```markdown
# Process Tasks

Read all markdown files in /Needs_Action folder.
For each task file:
1. Read task content and Company_Handbook.md
2. Generate structured plan
3. Write plan to /Plans/plan-{task-id}.md
4. Update Dashboard.md with task counts
5. Log any errors to errors.md
```

---

## Decision 5: Configuration Management

### Requirement
Configure vault path, folder names, watcher settings.

### Options Evaluated

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Python config.py | Simple, no parsing, direct import | Requires Python knowledge to edit | ✅ **SELECTED** |
| YAML config file | Human-readable, standard format | Adds parsing complexity, YAML dependency | ❌ Rejected |
| JSON config file | Standard format, widely supported | Less human-readable than YAML | ❌ Rejected |
| Environment variables | Standard, no files | Harder to discover, no validation | ❌ Rejected |

### Decision: Simple Python config.py file

**Rationale**:
- Bronze Tier prioritizes simplicity over flexibility
- Python config file is directly imported (no parsing needed)
- Easy to validate (Python syntax checking)
- Clear structure with comments

**Implementation Notes**:
```python
# watcher/config.py

# Absolute path to Obsidian vault
VAULT_PATH = "/Users/username/Documents/ObsidianVault"

# Folder names (relative to vault root)
INBOX_FOLDER = "Inbox"
NEEDS_ACTION_FOLDER = "Needs_Action"
PLANS_FOLDER = "Plans"
DONE_FOLDER = "Done"

# Watcher settings
WATCH_EXTENSIONS = [".md"]  # Only watch markdown files
LOG_LEVEL = "INFO"  # INFO, DEBUG, WARNING, ERROR
```

---

## Decision 6: Error Logging

### Requirement
Log all errors to errors.md with timestamps and actionable descriptions.

### Options Evaluated

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Append to errors.md | Simple, human-readable, Markdown format | No log rotation, could grow large | ✅ **SELECTED** |
| Python logging module | Structured, configurable, standard | Adds complexity, not Markdown format | ❌ Rejected |
| Separate log files per day | Automatic rotation | More complex, harder to search | ❌ Rejected |

### Decision: Append-only errors.md file

**Rationale**:
- Markdown format aligns with Markdown as Protocol principle
- Single file is easy to find and search
- Append-only ensures audit trail
- Timestamps provide chronological order
- Bronze Tier scope (50 tasks/session) won't cause excessive growth

**Implementation Notes**:
```python
def log_error(vault_path, error_type, message):
    errors_file = vault_path / "errors.md"
    timestamp = datetime.now().isoformat()
    entry = f"\n## {timestamp} - {error_type}\n\n{message}\n"

    with errors_file.open('a', encoding='utf-8') as f:
        f.write(entry)
```

**Error Entry Format**:
```markdown
## 2026-02-12T14:30:45 - File Copy Error

Failed to copy task-001.md from Inbox to Needs_Action.
Reason: Permission denied
Action: Check file permissions and try again.
```

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| File Watcher | Python watchdog | 3.0+ | Cross-platform, event-driven, mature |
| Markdown Parsing | PyYAML | 6.0+ | Standard YAML parsing, lightweight |
| File Operations | Python pathlib | stdlib | Cross-platform, modern API |
| AI Processing | Claude Code CLI | current | Manual trigger, already installed |
| Configuration | Python config.py | N/A | Simple, no parsing needed |
| Error Logging | Markdown append | N/A | Human-readable, audit trail |

**Total External Dependencies**: 2 (watchdog, PyYAML)

---

## Constitutional Compliance Review

All technology decisions comply with Bronze Tier constitution:

- ✅ **Local-First Architecture**: No cloud services, all local Python libraries
- ✅ **File System as Interface**: All I/O through file operations
- ✅ **Manual Trigger Model**: Watcher only copies files, AI invoked manually
- ✅ **Folder-Based State Machine**: State represented by file location
- ✅ **Zero External Integration**: No APIs, no network calls
- ✅ **Markdown as Protocol**: All data in Markdown format

---

## Performance Expectations

Based on technology choices:

| Metric | Expected Performance | Technology Factor |
|--------|---------------------|-------------------|
| File detection | <2 seconds | watchdog event-driven (faster than 5s requirement) |
| File copy | <100ms | pathlib native operations |
| Plan generation | 10-30 seconds | Claude Code processing time |
| Dashboard update | <500ms | Simple file write operation |
| Error logging | <100ms | Append operation |

All performance expectations meet or exceed success criteria from specification.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Watcher crashes | Low | Medium | User restarts (foreground process) |
| File permission errors | Medium | Low | Log error, continue processing |
| Vault path misconfigured | Medium | High | Validation on startup, clear error message |
| Concurrent file access | Low | Low | OS-level file locking |
| Large file processing | Low | Medium | No size limits in Bronze Tier (manual validation) |

No high-risk items identified. All risks have clear mitigation strategies.

---

## Open Questions

None - All technology decisions finalized and documented.

---

## References

- Python watchdog: https://python-watchdog.readthedocs.io/
- PyYAML: https://pyyaml.org/
- Python pathlib: https://docs.python.org/3/library/pathlib.html
- Claude Code CLI: https://claude.com/claude-code
