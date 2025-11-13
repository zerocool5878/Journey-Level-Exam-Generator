#!/usr/bin/env python3
"""
Script to publish GitHub release v1.0.10
"""

import requests
import json
import os

# GitHub API configuration
GITHUB_TOKEN = "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"
REPO_OWNER = "zerocool5878"
REPO_NAME = "Journey-Level-Exam-Generator"
TAG_NAME = "v1.0.10"

# Release notes
release_body = """## 🐛 Bug Fix - About Dialog Version

Version 1.0.10 fixes the About dialog to display the correct version number dynamically.

### Issue Fixed

**About Dialog Version**
- ✅ About dialog now reads version from `version.py` dynamically
- ✅ No more hardcoded version numbers
- ✅ Always shows the correct current version

### What Changed
- Updated `show_about()` method to import and use VERSION from version.py
- Changed from hardcoded "v1.0.6" to dynamic `f"v{VERSION}"`

### All Features from v1.0.9
- Fixed image path resolution with PyInstaller
- Fixed folder creation notifications
- Smart auto-updater with background checks
- Fixed button styling
- Dual database system (JW & CW/CE)
- Multi-language support (English & Español)

## Installation

1. Download `Journey-Level-Exam-Generator.exe` below
2. Double-click to run - NO INSTALLATION REQUIRED
3. Help → About will now show correct version!

**Built with ⚡ for accurate version reporting!**
"""

def create_release():
    """Create GitHub release"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    data = {
        "tag_name": TAG_NAME,
        "name": f"{TAG_NAME} - About Dialog Fix",
        "body": release_body,
        "draft": False,
        "prerelease": False
    }
    
    print(f"Creating release {TAG_NAME}...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        release_data = response.json()
        print(f"✅ Release created successfully!")
        print(f"   Upload URL: {release_data['upload_url']}")
        print(f"   Release ID: {release_data['id']}")
        return release_data
    else:
        print(f"❌ Failed to create release: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def upload_asset(release_data, file_path):
    """Upload executable to release"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Get upload URL and remove the {?name,label} template part
    upload_url = release_data['upload_url'].split('{')[0]
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
    
    print(f"\nUploading {file_name} ({file_size:.1f} MB)...")
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/octet-stream",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    params = {
        "name": file_name
    }
    
    with open(file_path, 'rb') as f:
        response = requests.post(upload_url, headers=headers, params=params, data=f)
    
    if response.status_code == 201:
        print(f"✅ Asset uploaded successfully!")
        return True
    else:
        print(f"❌ Failed to upload asset: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    # Create the release
    release_data = create_release()
    
    if release_data:
        # Upload the executable
        exe_path = "release/Journey-Level-Exam-Generator.exe"
        if upload_asset(release_data, exe_path):
            print(f"\n🎉 Release v1.0.10 published successfully!")
            print(f"   View at: {release_data['html_url']}")
        else:
            print(f"\n⚠️  Release created but asset upload failed")
            print(f"   You can manually upload the EXE at: {release_data['html_url']}")
    else:
        print("\n❌ Failed to create release")
