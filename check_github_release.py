import requests
import os

GITHUB_TOKEN = "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"
REPO_OWNER = "zerocool5878"
REPO_NAME = "Journey-Level-Exam-Generator"
VERSION = "v1.1.1"

# Get release info
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{VERSION}"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    release_data = response.json()
    assets = release_data.get("assets", [])
    
    for asset in assets:
        print(f"Asset: {asset['name']}")
        print(f"Size: {asset['size'] / (1024*1024):.2f} MB")
        print(f"Download URL: {asset['browser_download_url']}")
        print(f"State: {asset['state']}")
else:
    print(f"Failed to get release: {response.status_code}")
