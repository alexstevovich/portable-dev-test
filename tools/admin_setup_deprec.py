# ---------------------------------------------------
# This script configures the admin workspace.
# It should not be run by collaborators.
# ---------------------------------------------------

import os
import subprocess
import sys
import json

# 1️⃣ Get the script's directory and navigate to it
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Utility function to run shell commands safely
def run(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"⚠️ Error running command: {cmd}\n{result.stderr.strip()}")
    return result.stdout.strip()

# 2️⃣ Ensure Git is installed
if not run("git --version"):
    print("❌ Git is not installed. Please install Git and rerun this script.")
    sys.exit(1)

# 3️⃣ Find the root of the Git repository
GIT_ROOT = run("git rev-parse --show-toplevel")
if not GIT_ROOT:
    print("❌ This is not a Git repository.")
    choice = input("Would you like to initialize a new Git repository here? (y/n): ").strip().lower()
    if choice == "y":
        run("git init")
        print("✅ Git repository initialized!")
        GIT_ROOT = os.getcwd()  # Assume current working directory is root
    else:
        print("❌ Exiting. Please run this script inside a Git repository.")
        sys.exit(1)

# Change working directory to Git root
os.chdir(GIT_ROOT)

# 4️⃣ Load project.json
PROJECT_FILE = os.path.join(GIT_ROOT, "project.json")

if not os.path.exists(PROJECT_FILE):
    print(f"❌ Missing project.json at: {PROJECT_FILE}")
    sys.exit(1)

try:
    with open(PROJECT_FILE, "r", encoding="utf-8") as f:
        project_data = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Error parsing project.json: {e}")
    print("🛠️ Please validate your project.json at https://jsonlint.com/")
    sys.exit(1)

# 5️⃣ Extract user info & remotes from project.json
git_meta = project_data.get("git", {})
admin_meta = git_meta.get("admin", {})

USER_NAME = admin_meta.get("user", "")
USER_EMAIL = admin_meta.get("email", "")
REMOTES = admin_meta.get("remote", [])

if not USER_NAME or not USER_EMAIL:
    print("⚠️ Warning: No user info found in project.json. Skipping Git user config.")

if not REMOTES:
    print("❌ No remotes found in project.json! Exiting.")
    sys.exit(1)

# 6️⃣ Set Git user details (if available)
if USER_NAME and USER_EMAIL:
    print("🔹 Configuring Git user settings...")
    run(f'git config --local user.name "{USER_NAME}"')
    run(f'git config --local user.email "{USER_EMAIL}"')

# 7️⃣ Clear existing remotes
print("🔹 Clearing existing Git remotes...")
existing_remotes = run("git remote").split("\n")
for remote in existing_remotes:
    if remote:
        run(f"git remote remove {remote}")

# 8️⃣ Add remotes from project.json
print("🔹 Adding Git remotes from project.json...")

for remote in REMOTES:
    fetch_url = remote.get("url")
    proxy_urls = remote.get("proxy", [])

    if not fetch_url:
        print("⚠️ Warning: Remote entry missing 'url'. Skipping.")
        continue

    # Set origin fetch URL
    run(f"git remote add origin {fetch_url}")

    # Ensure `url` is added as the first push URL
    run(f"git remote set-url --add --push origin {fetch_url}")

    # Configure additional push URLs (proxies) if available
    for proxy_url in proxy_urls:
        run(f"git remote set-url --add --push origin {proxy_url}")

# 9️⃣ Verify workspace setup
print("\n✅ Setup complete! Verifying workspace:")
print(f"🔹 User: {run('git config --local user.name')}")
print(f"🔹 Email: {run('git config --local user.email')}")
print("🔹 Remotes:")
print(run("git remote -v"))

print(f"\n🚀 Your workspace is now fully configured! (Git root: {GIT_ROOT})")
