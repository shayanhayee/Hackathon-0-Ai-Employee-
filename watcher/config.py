"""
Configuration for Bronze Tier AI Employee Watcher

This file contains configuration settings for the file system watcher.
Update VAULT_PATH to point to your Obsidian vault location.
"""

import os
from pathlib import Path

# REQUIRED: Set absolute path to your Obsidian vault
# Example Windows: "C:/Users/username/Documents/ObsidianVault"
# Example macOS/Linux: "/Users/username/Documents/ObsidianVault"
VAULT_PATH = r"D:\Spec-driven-dev\Hackathon_0\AI_Employee_Vault"

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


def get_vault_path():
    """Get vault path as Path object with validation."""
    if not VAULT_PATH:
        raise ValueError(
            "VAULT_PATH not configured. Please set VAULT_PATH in config.py "
            "or set AI_EMPLOYEE_VAULT environment variable."
        )

    path = Path(VAULT_PATH)
    if not path.is_absolute():
        raise ValueError(f"VAULT_PATH must be absolute, got: {VAULT_PATH}")

    return path


def get_folder_paths():
    """Get all folder paths as Path objects."""
    vault = get_vault_path()
    return {
        "inbox": vault / INBOX_FOLDER,
        "needs_action": vault / NEEDS_ACTION_FOLDER,
        "plans": vault / PLANS_FOLDER,
        "done": vault / DONE_FOLDER,
    }
