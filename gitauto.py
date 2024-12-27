import os
import subprocess

def run_command(command):
    """
    Function to execute a shell command and print its output.
    """
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {command}\n{e.stderr}")

def get_current_branch():
    """
    Function to get the name of the current Git branch.
    """
    try:
        result = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    try:
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as f:
                f.write(entry + "\n")
            print(f"Created .gitignore and added '{entry}'.")
        else:
            with open(gitignore_path, "r") as f:
                lines = f.readlines()
            if entry + "\n" not in lines:
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
        subprocess.run("git rev-parse --is-inside-work-tree", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def initialize_new_repo():
    """
    Function to initialize a new Git repository and push to GitHub.
    """
    print("Initializing a new Git repository...")

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

    # Get GitHub username and repo name
    username = input("Enter your GitHub username (leave blank to fetch automatically): ").strip()
    repo_name = input("Enter the name of your GitHub repository: ").strip()

    if username and repo_name:
        # Add the remote repository
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        run_command(f"git remote add origin {remote_url}")

        # Push to the main branch
        run_command("git push -u origin main")
    else:
        print("GitHub username or repository name not provided. Aborting.")
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
        run_command(f"git commit -m \"{commit_message}\"")
        run_command(f"git push origin {branch_name}")

if __name__ == "__main__":
    print("\nGit Automation Script\n")
    print("This script automates the following steps:")
    print("1. Checks if a Git repository is initialized.")
    print("2. Initializes a new repository if needed or works with the existing one.")
    print("3. Ensures .gitignore includes 'gitauto.py'.")
    print("4. Stages all changes (git add .).")
    print("5. Commits with a custom or default message (git commit).")
    print("6. Pushes to the current branch or sets up a new remote for new repositories.")
    automate_git()
