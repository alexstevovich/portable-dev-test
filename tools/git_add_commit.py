import os
import subprocess
import sys

# ✅ Find the closest Git repository root
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

# Get script directory and change to Git root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
GIT_ROOT = find_git_root()
os.chdir(GIT_ROOT)

# ✅ Stage all changes
print("🔹 Staging all changes (`git add .`)...")
subprocess.run(["git", "add", "."], check=True)
print("✅ Changes staged.")

# ✅ Prompt for commit message
commit_message = input("\n📝 Enter commit message: ").strip()
if not commit_message:
    print("❌ No commit message entered. Exiting.")
    sys.exit(1)

# ✅ Commit changes
print(f"🔹 Committing with message: '{commit_message}'...")
result = subprocess.run(["git", "commit", "-m", commit_message], text=True)

if result.returncode == 0:
    print("✅ Commit successful!")
else:
    print("⚠️ Commit failed!")

print("\n🎉 Git add & commit completed!")
