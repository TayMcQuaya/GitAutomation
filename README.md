# Git Automation Script

This script simplifies your Git workflow by automating common commands like staging, committing, and pushing changes. It also ensures that the script itself (`gitauto.py`) is excluded from version control by managing a `.gitignore` file. Additionally, it can initialize a new Git repository for entirely new projects and connect it to a remote GitHub repository.

## Features

- **Existing Repositories**:
  - Automatically stages all changes using `git add .`.
  - Commits changes with a custom or default message.
  - Pushes to the current branch automatically.
  - Ensures a `.gitignore` file exists and excludes `gitauto.py`.
  - Displays the full commands being executed for clarity.
  - Confirmation prompts to avoid accidental actions.

- **New Repositories**:
  - Checks if a repository has been initialized (`git init`).
  - Initializes a new Git repository if needed.
  - Commits the initial changes with a default message (`first commit`).
  - Sets the branch to `main`.
  - Prompts the user for the GitHub repository name and adds the remote origin.
  - Pushes the initial commit to the remote `main` branch.

## Requirements

- Python 3.x
- Git installed and configured
- A GitHub account for new repository initialization

## How to Use

1. Place the `gitauto.py` script in the root directory of your project.
2. Run the script:
   ```bash
   python gitauto.py
   ```
3. Follow the prompts:
   - For existing repositories:
     - Enter a commit message or press Enter for the default message (`Updated files`).
     - Confirm whether to push to the current branch (`yes/y` or `no/n`).
   - For new repositories:
     - Confirm whether to initialize a new Git repository (`yes/y` or `no/n`).
     - Enter your GitHub username (if not fetched automatically) and repository name.
     - The script will handle the rest, including adding the remote origin and pushing the initial commit.

## Example

### Existing Repository
```plaintext
Git Automation Script

This script automates the following steps:
1. Ensures .gitignore includes 'gitauto.py'
2. Stages all changes (git add .)
3. Commits with a custom or default message (git commit)
4. Pushes to the current branch (git push)

Enter your commit message (press Enter to use default 'Updated files'): Fixed README typos
Are you sure you want to push to the branch 'main'? (yes/y/no/n): y
Running: git add .
Running: git commit -m "Fixed README typos"
Running: git push origin main
```

### New Repository
```plaintext
Git Automation Script

No Git repository detected in this directory.
Do you want to initialize a new Git repository? (yes/y/no/n): y
Initializing a new Git repository...
Running: git init
Created .gitignore and added 'gitauto.py'.
Running: git add .
Running: git commit -m "first commit"
Running: git branch -M main
Enter your GitHub username (leave blank to fetch automatically): myusername
Enter the name of your GitHub repository: my-new-repo
Running: git remote add origin https://github.com/myusername/my-new-repo.git
Running: git push -u origin main
```

## Notes

- If the `.gitignore` file doesn't exist, it will be created, and `gitauto.py` will be added to it.
- If `gitauto.py` is already listed in `.gitignore`, no duplicate entries will be added.
- For new repositories:
  - Make sure you have a valid GitHub account and access to create a new repository.
  - The remote repository should already exist on GitHub before adding it to your local project.
- Use this script cautiously to ensure it matches your workflow.
