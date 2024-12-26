# Git Automation Script

This script simplifies your Git workflow by automating common commands like staging, committing, and pushing changes. It also ensures that the script itself (`gitauto.py`) is excluded from version control by managing a `.gitignore` file.

## Features

- Automatically stages all changes using `git add .`.
- Commits changes with a custom or default message.
- Pushes to the current branch automatically.
- Ensures a `.gitignore` file exists and excludes `gitauto.py`.
- Displays the full commands being executed for clarity.
- Confirmation prompts to avoid accidental actions.

## Requirements

- Python 3.x
- Git installed and configured

## How to Use

1. Place the `gitauto.py` script in the root directory of your Git project.
2. Run the script:
   ```bash
   python gitauto.py
   ```
3. Follow the prompts:
   - Enter a commit message or press Enter for the default message (`Update files`).
   - Confirm whether to push to the current branch (`yes/y` or `no/n`).

## Example

```plaintext
Git Automation Script

This script automates the following steps:
1. Ensures .gitignore includes 'gitauto.py'
2. Stages all changes (git add .)
3. Commits with a custom or default message (git commit)
4. Pushes to the current branch (git push)

Enter your commit message (press Enter to use default 'Update files'): Fixed README typos
Are you sure you want to push to the branch 'main'? (yes/y/no/n): y
Running: git add .
Running: git commit -m "Fixed README typos"
Running: git push origin main
```

## Notes

- If the `.gitignore` file doesn't exist, it will be created, and `gitauto.py` will be added to it.
- If `gitauto.py` is already listed in `.gitignore`, no duplicate entries will be added.
- Use this script cautiously to ensure it matches your workflow.
