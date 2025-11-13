#!/usr/bin/env python3
"""
Create GitHub Release for Journey-Level Exam Generator
"""
import requests
import json
import os
import sys
from pathlib import Path

def create_github_release():
    """Create a new GitHub release with executable upload"""
    
    # Configuration
    repo_owner = "zerocool5878"
    repo_name = "Journey-Level-Exam-Generator"
    version = "v1.0.7"
    
    # Read release notes
    release_notes_path = Path("RELEASE_NOTES_v1.0.7.md")
    if not release_notes_path.exists():
        print(f"❌ Release notes file not found: {release_notes_path}")
        return False
    
    with open(release_notes_path, 'r', encoding='utf-8') as f:
        release_body = f.read()
    
    # Executable path
    exe_path = Path("release/Journey-Level-Exam-Generator.exe")
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    print(f"📋 Creating GitHub release {version}...")
    print(f"📦 Executable: {exe_path} ({exe_path.stat().st_size / (1024*1024):.1f} MB)")
    
    # GitHub API token (you'll need to set this as environment variable)
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("💡 You can create one at: https://github.com/settings/tokens")
        print("💡 Then set it with: $env:GITHUB_TOKEN=\"your_token_here\"")
        return False
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    # Create release
    release_data = {
        'tag_name': version,
        'target_commitish': 'main',
        'name': f'Journey-Level Exam Generator {version}',
        'body': release_body,
        'draft': False,
        'prerelease': False
    }
    
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    
    try:
        print("🚀 Creating release...")
        response = requests.post(api_url, headers=headers, data=json.dumps(release_data))
        
        if response.status_code == 201:
            release_info = response.json()
            print(f"✅ Release created successfully!")
            print(f"🔗 Release URL: {release_info['html_url']}")
            
            # Upload executable as asset
            upload_url = release_info['upload_url'].replace('{?name,label}', '')
            
            print("📤 Uploading executable...")
            with open(exe_path, 'rb') as exe_file:
                upload_headers = {
                    'Authorization': f'token {token}',
                    'Content-Type': 'application/octet-stream'
                }
                upload_params = {
                    'name': 'Journey-Level-Exam-Generator.exe',
                    'label': 'Journey-Level Exam Generator v1.0.7 Executable'
                }
                
                upload_response = requests.post(
                    upload_url,
                    headers=upload_headers,
                    params=upload_params,
                    data=exe_file
                )
                
                if upload_response.status_code == 201:
                    print("✅ Executable uploaded successfully!")
                    print(f"📦 Asset URL: {upload_response.json()['browser_download_url']}")
                    return True
                else:
                    print(f"❌ Failed to upload executable: {upload_response.status_code}")
                    print(f"Response: {upload_response.text}")
                    return False
        else:
            print(f"❌ Failed to create release: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating release: {e}")
        return False

if __name__ == "__main__":
    success = create_github_release()
    if success:
        print("\n🎉 GitHub release created successfully!")
        print("🔄 Users can now update via the auto-updater!")
    else:
        print("\n💥 Failed to create GitHub release")
        sys.exit(1)