"""
Bronze Tier AI Employee - File System Watcher

Monitors the /Inbox folder and automatically copies new markdown files
to /Needs_Action for AI processing.

Usage:
    python watcher.py

Configuration:
    Set VAULT_PATH in config.py or AI_EMPLOYEE_VAULT environment variable

Press Ctrl+C to stop the watcher.
"""

import sys
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import local modules
import config
from file_handler import copy_file, validate_vault_access, log_error


# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class TaskFileHandler(FileSystemEventHandler):
    """
    Handles file system events for the Inbox folder.

    Monitors for new file creation events and copies markdown files
    to the Needs_Action folder.
    """

    def __init__(self, vault_root: Path, inbox_path: Path, needs_action_path: Path):
        """
        Initialize the file handler.

        Args:
            vault_root: Root path of the vault
            inbox_path: Path to Inbox folder
            needs_action_path: Path to Needs_Action folder
        """
        self.vault_root = vault_root
        self.inbox_path = inbox_path
        self.needs_action_path = needs_action_path
        super().__init__()

    def on_created(self, event):
        """
        Handle file creation events.

        Args:
            event: FileSystemEvent object
        """
        # Ignore directory creation events
        if event.is_directory:
            return

        source_path = Path(event.src_path)

        # Filter: Only process markdown files
        if source_path.suffix not in config.WATCH_EXTENSIONS:
            logger.debug(f"Ignoring non-markdown file: {source_path.name}")
            return

        logger.info(f"File detected: {source_path.name}")

        # Small delay to ensure file is fully written
        time.sleep(config.DEBOUNCE_SECONDS)

        # Copy file to Needs_Action
        logger.info(f"Copying to {config.NEEDS_ACTION_FOLDER}...")

        target_path = copy_file(source_path, self.needs_action_path, self.vault_root)

        if target_path:
            logger.info(f"✓ Copy complete: {target_path.name}")
        else:
            logger.error(f"✗ Copy failed: {source_path.name} (see errors.md)")


def validate_startup(vault_root: Path, folders: dict) -> bool:
    """
    Validate that the vault and required folders exist.

    Args:
        vault_root: Root path of the vault
        folders: Dictionary of folder paths

    Returns:
        True if validation passes, False otherwise
    """
    logger.info("Validating vault configuration...")

    # Check vault access
    is_valid, error_msg = validate_vault_access(vault_root)
    if not is_valid:
        logger.error(f"Vault validation failed: {error_msg}")
        return False

    logger.info(f"✓ Vault path: {vault_root}")

    # Check required folders exist
    missing_folders = []
    for name, path in folders.items():
        if not path.exists():
            missing_folders.append(name)
        else:
            logger.info(f"✓ {name.capitalize()} folder: {path}")

    if missing_folders:
        logger.error(f"Missing folders: {', '.join(missing_folders)}")
        logger.error("Run 'python watcher/init_vault.py' to create folder structure")
        return False

    return True


def main():
    """
    Main entry point for the watcher.
    """
    logger.info("=" * 60)
    logger.info("Bronze Tier AI Employee - File Watcher")
    logger.info("=" * 60)

    # Load configuration
    try:
        vault_root = config.get_vault_path()
        folders = config.get_folder_paths()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please update watcher/config.py with your vault path")
        sys.exit(1)

    # Validate startup
    if not validate_startup(vault_root, folders):
        sys.exit(1)

    # Create event handler
    event_handler = TaskFileHandler(
        vault_root=vault_root,
        inbox_path=folders["inbox"],
        needs_action_path=folders["needs_action"]
    )

    # Create and configure observer
    observer = Observer()
    observer.schedule(
        event_handler,
        str(folders["inbox"]),
        recursive=False  # Don't watch subdirectories
    )

    # Start observer
    logger.info("")
    logger.info("Starting watcher...")
    logger.info(f"Monitoring: {folders['inbox']}")
    logger.info("Press Ctrl+C to stop")
    logger.info("")

    observer.start()

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        logger.info("")
        logger.info("Stopping watcher...")
        observer.stop()
        observer.join()
        logger.info("✓ Watcher stopped")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
