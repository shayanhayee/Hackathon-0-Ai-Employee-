"""
Vault Initialization Script

Creates the required folder structure for the Bronze Tier AI Employee system.
Run this script once to set up your vault.
"""

import sys
from pathlib import Path
from datetime import datetime


def create_vault_structure(vault_path):
    """
    Create the folder structure for the AI Employee vault.

    Args:
        vault_path: Path to the Obsidian vault (string or Path object)

    Returns:
        bool: True if successful, False otherwise
    """
    vault = Path(vault_path)

    # Validate vault path
    if not vault.exists():
        print(f"Error: Vault path does not exist: {vault}")
        return False

    if not vault.is_dir():
        print(f"Error: Vault path is not a directory: {vault}")
        return False

    # Define folders to create
    folders = {
        "Inbox": "User drops tasks here",
        "Needs_Action": "Watcher copies files here",
        "Plans": "AI writes plans here",
        "Done": "Completed tasks archived here",
    }

    print(f"Initializing vault structure in: {vault}")
    print("-" * 60)

    # Create folders
    for folder_name, description in folders.items():
        folder_path = vault / folder_name
        if folder_path.exists():
            print(f"✓ {folder_name:15} already exists")
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ {folder_name:15} created - {description}")

    # Create initial files if they don't exist
    files = {
        "Dashboard.md": "# AI Employee Dashboard\n\n**Last Updated**: {timestamp}\n\n## Task Status\n\n| Folder | Count | Description |\n|--------|-------|-------------|\n| Inbox | 0 | New tasks awaiting watcher |\n| Needs Action | 0 | Tasks ready for AI processing |\n| Plans | 0 | Generated plans |\n| Done | 0 | Completed tasks |\n\n**Total Tasks**: 0\n",
        "Company_Handbook.md": "# Company Handbook\n\n## Company Overview\n[Your company mission, vision, values]\n\n## Policies\n### Communication\n[Communication guidelines]\n\n### Project Management\n[PM processes and tools]\n\n## Market Context\n### Competitors\n[Competitor information]\n\n### Target Audience\n[Customer segments]\n\n## Resources\n### Tools\n[Software and tools used]\n\n### Templates\n[Document templates]\n",
        "errors.md": "# Error Log\n\n",
    }

    print()
    for filename, content in files.items():
        file_path = vault / filename
        if file_path.exists():
            print(f"✓ {filename:20} already exists")
        else:
            timestamp = datetime.now().isoformat()
            file_content = content.format(timestamp=timestamp)
            file_path.write_text(file_content, encoding="utf-8")
            print(f"✓ {filename:20} created")

    print()
    print("=" * 60)
    print("✅ Vault initialization complete!")
    print()
    print("Next steps:")
    print("1. Update watcher/config.py with your vault path")
    print("2. Install dependencies: pip install -r watcher/requirements.txt")
    print("3. Start watcher: python watcher/watcher.py")

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = input("Enter vault path: ").strip()

    if not vault_path:
        print("Error: Vault path is required")
        sys.exit(1)

    success = create_vault_structure(vault_path)
    sys.exit(0 if success else 1)
