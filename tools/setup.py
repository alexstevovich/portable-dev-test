# ---------------------------------------------------
# This script is to configure the admin workspace.sys
# It should not be run by collaborators.
# ---------------------------------------------------

# ---------- CONFIG
PROJECT_NAME = "portable-dev-test"
USER_NAME = "Alex Stevovich"
USER_EMAIL = "alex.stevovich@gmail.com"

# ---------- SCRIPT
# version: 1.0.0

import os
import subprocess
import sys

# ✅ Prevent accidental execution with a simple confirmation
print("\n⚠️  WARNING: This script is for Admin Devs only.")
print("⚠️  If you're a collaborator, you should set up Git manually.\n")

confirm = input("Are you sure you want to continue? (y/N): ").strip().lower()
if confirm != "y":
    print("❌ Setup aborted.")
    sys.exit(1)

# Get script directory and change to it
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Utility function to run commands safely
def run(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"⚠️ Error running command: {cmd}\n{result.stderr.strip()}")
    return result.stdout.strip()

# 1️⃣ Ensure Git is installed
if not run("git --version"):
    print("❌ Git is not installed. Please install Git and rerun this script.")
    sys.exit(1)

# 2️⃣ Find the root of the Git repository (works even when run from tools/)
GIT_ROOT = run("git rev-parse --show-toplevel")
if not GIT_ROOT:
    print("❌ This is not a Git repository.")
    choice = input("Would you like to initialize a new Git repository here? (y/n): ").strip().lower()
    if choice == "y":
        run("git init")
        print("✅ Git repository initialized!")
        GIT_ROOT = os.getcwd()  # Assume it's the current working directory
    else:
        print("❌ Exiting. Please run this script inside a Git repository.")
        sys.exit(1)

# Change working directory to Git root
os.chdir(GIT_ROOT)

# 3️⃣ Set Git user details (unless `--no-user` is provided)
print("🔹 Configuring Git user settings...")
run(f'git config --local user.name "{USER_NAME}"')
run(f'git config --local user.email "{USER_EMAIL}"')

# 4️⃣ Clear existing remotes
print("🔹 Clearing existing Git remotes...")
existing_remotes = run("git remote").split("\n")
for remote in existing_remotes:
    if remote:
        run(f"git remote remove {remote}")

# 5️⃣ Add remotes
print("🔹 Adding Git remotes...")
run(f"git remote add github https://github.com/alexstevovich/{PROJECT_NAME}.git")
run(f"git remote add gitlab https://gitlab.com/alexstevovich/{PROJECT_NAME}.git")

# 6️⃣ Verify workspace
print("\n✅ Setup complete! Verifying workspace:")
print(f"🔹 User: {run('git config --local user.name')}")
print(f"🔹 Email: {run('git config --local user.email')}")
print("🔹 Remotes:")
print(run("git remote -v"))

print(f"\n🚀 Your workspace is now fully configured! (Git root: {GIT_ROOT})")
