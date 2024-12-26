import os
import subprocess

def run_command(command):
    """
    Function to execute a shell command and print its output.
    """
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            # Create .gitignore if it doesn't exist
            with open(gitignore_path, "w") as f:
                f.write(entry + "\n")
            print(f"Created .gitignore and added '{entry}'.")
        else:
            # Check if the entry already exists
            with open(gitignore_path, "r") as f:
                lines = f.readlines()

            if entry + "\n" not in lines:
                # Add entry to .gitignore
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

def automate_git():
    """
    Function to automate git commands.
    """
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
    run_command("\nRunning git add .")

    run_command(f"\nRunning git commit -m \"{commit_message}\"")

    run_command(f"\nRunning git push origin {branch_name}")

if __name__ == "__main__":
    print("\nGit Automation Script\n")
    print("This script automates the following steps:\n1. Ensures .gitignore includes 'gitauto.py'\n2. Stages all changes (git add .)\n3. Commits with a custom or default message (git commit)\n4. Pushes to the current branch (git push)")
    automate_git()
