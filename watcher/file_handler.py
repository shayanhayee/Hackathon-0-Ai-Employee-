"""
File Handler Utilities

Provides file operations for the Bronze Tier AI Employee watcher:
- File copying with collision detection
- Error logging
- Vault boundary validation
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional


def copy_file(source: Path, target_dir: Path, vault_root: Path) -> Optional[Path]:
    """
    Copy a file from source to target directory with collision handling.

    Args:
        source: Source file path
        target_dir: Target directory path
        vault_root: Vault root path for boundary validation

    Returns:
        Path to the copied file, or None if copy failed
    """
    # Validate vault boundary
    if not is_within_vault(source, vault_root):
        log_error(vault_root, "Vault Boundary Violation",
                  f"Source file outside vault: {source}")
        return None

    if not is_within_vault(target_dir, vault_root):
        log_error(vault_root, "Vault Boundary Violation",
                  f"Target directory outside vault: {target_dir}")
        return None

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Get unique target path (handle collisions)
    target_path = get_unique_path(target_dir, source.name)

    try:
        # Copy file preserving metadata
        shutil.copy2(source, target_path)
        return target_path
    except Exception as e:
        log_error(vault_root, "File Copy Error",
                  f"Failed to copy {source.name} to {target_dir}\nReason: {str(e)}")
        return None


def get_unique_path(target_dir: Path, filename: str) -> Path:
    """
    Get a unique file path by appending numeric suffix if file exists.

    Args:
        target_dir: Target directory
        filename: Original filename

    Returns:
        Unique Path object

    Examples:
        task-001.md -> task-001.md (if doesn't exist)
        task-001.md -> task-001-1.md (if exists)
        task-001.md -> task-001-2.md (if task-001-1.md exists)
    """
    path = target_dir / filename

    if not path.exists():
        return path

    # Extract stem and suffix
    stem = path.stem
    suffix = path.suffix
    counter = 1

    while True:
        new_path = target_dir / f"{stem}-{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def log_error(vault_root: Path, error_type: str, message: str) -> None:
    """
    Log an error to errors.md in the vault root.

    Args:
        vault_root: Vault root path
        error_type: Type of error (e.g., "File Copy Error", "Validation Error")
        message: Error message
    """
    errors_file = vault_root / "errors.md"
    timestamp = datetime.now().isoformat()

    entry = f"\n## {timestamp} - {error_type}\n\n{message}\n"

    try:
        # Append to errors.md (create if doesn't exist)
        with errors_file.open('a', encoding='utf-8') as f:
            f.write(entry)
    except Exception as e:
        # If we can't log to file, print to console
        print(f"ERROR: Failed to log error to {errors_file}: {e}")
        print(f"Original error: {error_type} - {message}")


def is_within_vault(path: Path, vault_root: Path) -> bool:
    """
    Check if a path is within the vault boundaries.

    Args:
        path: Path to check
        vault_root: Vault root path

    Returns:
        True if path is within vault, False otherwise
    """
    try:
        # Resolve to absolute paths
        abs_path = path.resolve()
        abs_vault = vault_root.resolve()

        # Check if path is relative to vault root
        abs_path.relative_to(abs_vault)
        return True
    except ValueError:
        # relative_to raises ValueError if path is not relative to vault
        return False


def validate_vault_access(vault_root: Path) -> tuple[bool, str]:
    """
    Validate that the vault path exists and is accessible.

    Args:
        vault_root: Vault root path

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not vault_root.exists():
        return False, f"Vault path does not exist: {vault_root}"

    if not vault_root.is_dir():
        return False, f"Vault path is not a directory: {vault_root}"

    # Check if we can write to the vault
    test_file = vault_root / ".watcher_test"
    try:
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        return False, f"Vault is not writable: {e}"

    return True, ""
