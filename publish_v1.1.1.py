import requests
import os
from pathlib import Path

# Configuration
GITHUB_TOKEN = "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"
REPO_OWNER = "zerocool5878"
REPO_NAME = "Journey-Level-Exam-Generator"
VERSION = "v1.1.1"
EXE_PATH = "release/Journey-Level-Exam-Generator.exe"
RELEASE_NOTES_PATH = "RELEASE_NOTES_v1.1.1.md"

def create_release():
    """Create a new GitHub release"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Read release notes
    with open(RELEASE_NOTES_PATH, 'r', encoding='utf-8') as f:
        release_notes = f.read()
    
    data = {
        "tag_name": VERSION,
        "name": f"Journey-Level Exam Generator {VERSION}",
        "body": release_notes,
        "draft": False,
        "prerelease": False
    }
    
    print(f"Creating release {VERSION}...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ Release {VERSION} created successfully!")
        return response.json()
    else:
        print(f"❌ Failed to create release: {response.status_code}")
        print(response.json())
        return None

def upload_asset(release_id, file_path):
    """Upload an asset to the release"""
    url = f"https://uploads.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{release_id}/assets"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    
    file_name = os.path.basename(file_path)
    params = {"name": file_name}
    
    print(f"Uploading {file_name}...")
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size / (1024*1024):.2f} MB")
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    print(f"Data read: {len(file_data) / (1024*1024):.2f} MB")
    response = requests.post(url, headers=headers, params=params, data=file_data)
    
    if response.status_code == 201:
        print(f"✅ {file_name} uploaded successfully!")
        return True
    else:
        print(f"❌ Failed to upload {file_name}: {response.status_code}")
        print(response.json())
        return False

def main():
    # Verify files exist
    if not os.path.exists(EXE_PATH):
        print(f"❌ Executable not found: {EXE_PATH}")
        return
    
    if not os.path.exists(RELEASE_NOTES_PATH):
        print(f"❌ Release notes not found: {RELEASE_NOTES_PATH}")
        return
    
    # Create release
    release_data = create_release()
    if not release_data:
        return
    
    release_id = release_data["id"]
    
    # Upload executable
    if not upload_asset(release_id, EXE_PATH):
        return
    
    print(f"\n🎉 Release {VERSION} published successfully!")
    print(f"🔗 {release_data['html_url']}")

if __name__ == "__main__":
    main()
