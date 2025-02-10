import os
import json
import subprocess
import requests
import re
import time  # ✅ Import time for delays
from urllib.parse import urlparse

# Prompt for user input
OWNER = input("Enter GitHub repository owner: ")
REPO = input("Enter GitHub repository name: ")
TOKEN = input("Enter your GitHub token: ")
LIMIT = input("Enter the number of issues to fetch (default 10): ") or "10"
STATE = input("Enter issue state (open, closed, all - default all): ") or "all"

HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Ensure the image download directory exists
IMAGE_DIR = "downloaded_images"
os.makedirs(IMAGE_DIR, exist_ok=True)


# Function to download an image and return the local path
def download_image(image_url):
    try:
        print(f"Attempting to download image from URL: {image_url}")

        image_name = os.path.basename(urlparse(image_url).path)
        local_image_path = os.path.join(IMAGE_DIR, image_name)

        if os.path.exists(local_image_path):
            print(f"Image already downloaded: {image_name}")
            return local_image_path

        headers = {"Authorization": f"token {TOKEN}"}
        img_data = requests.get(image_url, headers=headers)

        if img_data.status_code == 200:
            with open(local_image_path, 'wb') as f:
                f.write(img_data.content)
            print(f"Downloaded image: {image_name}")
            return local_image_path
        else:
            print(f"Failed to download image. HTTP Status: {img_data.status_code} for URL: {image_url}")
            return None

    except Exception as e:
        print(f"Failed to download image from {image_url}: {e}")
        return None


# Step 1: Get all issues (open and closed) using GitHub CLI
print("\nFetching issues...")
issues_json = subprocess.run(
    ["gh", "issue", "list", "--repo", f"{OWNER}/{REPO}", "--limit", LIMIT, "--state", STATE, "--json", "number,title,body,state"],
    capture_output=True,
    text=True
).stdout

issues = json.loads(issues_json)

# ✅ Add sleep to prevent hitting CLI request limits
time.sleep(2)

# Step 2: Fetch comments for each issue using GitHub API
for issue in issues:
    issue_number = issue["number"]
    print(f"Fetching comments for issue #{issue_number}...")

    comments_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"
    response = requests.get(comments_url, headers=HEADERS)

    if response.status_code == 200:
        comments = response.json()
        issue["comments"] = [{"author": c["user"]["login"], "body": c["body"], "date": c["created_at"]} for c in comments]
    else:
        print(f"Failed to fetch comments for issue #{issue_number} (HTTP {response.status_code})")
        issue["comments"] = []

    # ✅ Sleep after each comment fetch (prevents API rate limits)
    time.sleep(1.5)

    # Step 3: Download images from the issue body and comments (if any)
    body = issue.get("body", "")
    for comment in issue["comments"]:
        body += comment["body"]

    # Regex to find image URLs in Markdown and HTML formats
    img_urls = re.findall(r'!\[.*?\]\((https?://[^\)]+)\)', body)
    img_urls += re.findall(r'<img[^>]+src="(https?://[^\"]+)"', body)

    for img_url in img_urls:
        local_image_path = download_image(img_url)

        # ✅ Sleep after each image download (avoids too many requests)
        time.sleep(1)

    issue["body"] = body

# ✅ Final sleep before saving (ensures all requests complete safely)
time.sleep(2)

# Save the issues with comments and updated image paths to a JSON file
with open("issues_with_comments_and_images.json", "w", encoding="utf-8") as f:
    json.dump(issues, f, indent=4)

print("✅ Export completed! Data saved in issues_with_comments_and_images.json")
