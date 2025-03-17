# ---------- SCRIPT
# version: 1.0.0

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def find_git_root():
    """Find the closest .git root directory from the current script location."""
    try:
        git_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
        ).stdout.strip()
        return git_root
    except subprocess.CalledProcessError:
        print("❌ No Git repository found. Please run this script inside a Git repository.")
        sys.exit(1)

GIT_ROOT = find_git_root()
os.chdir(GIT_ROOT)

def get_git_remotes():
    """Retrieve all remotes configured in Git."""
    remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.strip().split("\n")
    return [r for r in remotes if r]  # Remove empty entries

remotes = get_git_remotes()
if not remotes:
    print("❌ No remotes found in this repository.")
    sys.exit(1)

branch = input("Enter the branch to push to all remotes: ").strip()
if not branch:
    print("❌ No branch entered. Exiting.")
    sys.exit(1)

for remote in remotes:
    print(f"\n🚀 Pushing branch '{branch}' to remote '{remote}'...")
    result = subprocess.run(["git", "push", remote, branch], text=True)
    if result.returncode == 0:
        print(f"✅ Successfully pushed to {remote}")
    else:
        print(f"⚠️ Failed to push to {remote}")

print("\n🎉 Push to all remotes completed!")
