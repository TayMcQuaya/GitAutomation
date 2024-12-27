import os
import subprocess
import re
import shutil

def run_command(command):
    """
    Function to execute a shell command and print its output.
    Returns the CompletedProcess object.
    """
    try:
        print(f"\nRunning: {command}")
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {command}\n{e.stderr}")
        raise

def get_current_branch():
    """
    Function to get the name of the current Git branch.
    """
    try:
        result = subprocess.run(
            "git rev-parse --abbrev-ref HEAD",
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error while getting current branch:\n{e.stderr}")
        return None

def ensure_gitignore():
    """
    Function to ensure a .gitignore file exists and includes 'gitauto.py'.
    """
    gitignore_path = ".gitignore"
    entry = "gitauto.py"
    pattern = re.compile(rf"^\s*{re.escape(entry)}\s*$", re.IGNORECASE)

    try:
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as f:
                f.write(entry + "\n")
            print(f"Created .gitignore and added '{entry}'.")
        else:
            # Create a backup before modifying
            backup_path = gitignore_path + ".backup"
            shutil.copy(gitignore_path, backup_path)
            print(f"Backup of existing .gitignore created at '{backup_path}'.")

            with open(gitignore_path, "r") as f:
                lines = f.readlines()

            # Check if 'gitauto.py' is already present
            if not any(pattern.match(line) for line in lines):
                with open(gitignore_path, "a") as f:
                    f.write(entry + "\n")
                print(f"Added '{entry}' to .gitignore.")
            else:
                print(f"'{entry}' is already in .gitignore.")
    except Exception as e:
        print(f"Error ensuring .gitignore: {e}")

def confirm_action(prompt):
    """
    Function to ask for user confirmation with 'yes/y' or 'no/n'.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ['yes', 'y']:
            return True
        elif answer in ['no', 'n']:
            return False
        else:
            print("Please answer 'y' or 'n'.")

def is_git_initialized():
    """
    Function to check if the current directory is a Git repository.
    """
    try:
        subprocess.run(
            "git rev-parse --is-inside-work-tree",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False

def initialize_new_repo():
    """
    Function to initialize a new Git repository and push to GitHub.
    """
    print("\nInitializing a new Git repository...")

    # Initialize the repository
    run_command("git init")

    # Ensure .gitignore includes 'gitauto.py'
    ensure_gitignore()

    # Add all files
    run_command("git add .")

    # Commit with a default message
    run_command('git commit -m "first commit"')

    # Set the branch to 'main'
    run_command("git branch -M main")

    while True:
        username = input("Enter your GitHub username: ").strip()
        repo_name = input("Enter the name of your GitHub repository: ").strip()

        if not username or not repo_name:
            print("Username and repository name cannot be empty. Please try again.")
            continue

        remote_url = f"https://github.com/{username}/{repo_name}.git"

        # Check if 'origin' remote exists
        try:
            subprocess.run(
                "git remote get-url origin",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Remote exists, set-url
            run_command(f"git remote set-url origin {remote_url}")
            print(f"Updated 'origin' remote to {remote_url}")
        except subprocess.CalledProcessError:
            # Remote does not exist, add it
            run_command(f"git remote add origin {remote_url}")
            print(f"Added 'origin' remote as {remote_url}")

        try:
            run_command("git push -u origin main")
            print("Repository successfully pushed to GitHub.")
            break
        except subprocess.CalledProcessError as e:
            print("Failed to push to GitHub. This may be due to incorrect username or repository name, or authentication issues.")
            print(f"Error: {e.stderr}")
            retry = confirm_action("Do you want to try entering the GitHub details again? (yes/y to retry, no/n to cancel): ")
            if not retry:
                print("Operation canceled.")
                return

def automate_git():
    """
    Function to automate git commands.
    """
    # Check if the current directory is a Git repository
    if not is_git_initialized():
        print("No Git repository detected in this directory.")
        if confirm_action("Do you want to initialize a new Git repository? (yes/y/no/n): "):
            initialize_new_repo()
        else:
            print("Operation canceled.")
            return
    else:
        # Proceed with existing repository operations
        print("Git repository detected.")

        # Ensure .gitignore includes 'gitauto.py'
        ensure_gitignore()

        # Ask the user for a commit message
        commit_message = input("Enter your commit message (press Enter to use default 'Updated files'): ").strip()

        if not commit_message:
            commit_message = "Updated files"

        # Get the current branch name
        branch_name = get_current_branch()

        if not branch_name:
            print("Could not determine the current branch. Aborting.")
            return

        # Ask the user for confirmation before pushing
        if not confirm_action(f"Are you sure you want to push to the branch '{branch_name}'? (yes/y/no/n): "):
            print("Push operation canceled.")
            return

        # Run the git commands
        run_command("git add .")
        run_command(f'git commit -m "{commit_message}"')
        run_command(f"git push origin {branch_name}")

if __name__ == "__main__":
    print("\nGit Automation Script\n")
    print("This script automates the following steps:")
    print("1. Checks if a Git repository is initialized.")
    print("2. Initializes a new repository if needed or works with the existing one.")
    print("3. Ensures .gitignore includes 'gitauto.py'.")
    print("4. Stages all changes (git add .).")
    print("5. Commits with a custom or default message (git commit).")
    print("6. Pushes to the current branch or sets up a new remote for new repositories.\n")
    automate_git()
