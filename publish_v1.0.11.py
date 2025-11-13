#!/usr/bin/env python3
import requests, os

TOKEN = "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"
TAG = "v1.0.11"

release_body = """## 🎨 UX Improvements - Auto-Updater

Version 1.0.11 improves the auto-updater user experience with better dialog sizing and real-time download progress.

### Issues Fixed

**Update Dialog**
- ✅ Increased dialog size from 600x500 to 650x600 - buttons now always visible
- ✅ Added real-time download progress (shows MB downloaded and percentage)
- ✅ Larger chunk size (80KB) for faster downloads
- ✅ Better status messages throughout update process

**Download Experience**
- Shows "Downloading: X.X/52.8 MB (XX%)" during download
- Shows "Installing update..." when replacing files
- Proper timeout handling (60 seconds)
- Clear visual feedback at every step

### All Features from v1.0.10
- Dynamic About dialog showing correct version
- Fixed image path resolution
- Smart background update checks
- Professional UI with custom styling

## Installation

Download `Journey-Level-Exam-Generator.exe` below and run!

**Built with ⚡ for smooth updates!**
"""

url = f"https://api.github.com/repos/zerocool5878/Journey-Level-Exam-Generator/releases"
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
data = {"tag_name": TAG, "name": f"{TAG} - Auto-Updater UX Fix", "body": release_body, "draft": False}

print(f"Creating release {TAG}...")
r = requests.post(url, headers=headers, json=data)
if r.status_code == 201:
    release = r.json()
    print(f"✅ Release created!")
    
    # Upload EXE
    upload_url = release['upload_url'].split('{')[0]
    exe_path = "release/Journey-Level-Exam-Generator.exe"
    print(f"Uploading {os.path.getsize(exe_path)/(1024*1024):.1f} MB...")
    
    with open(exe_path, 'rb') as f:
        r2 = requests.post(upload_url, headers={**headers, "Content-Type": "application/octet-stream"}, 
                          params={"name": "Journey-Level-Exam-Generator.exe"}, data=f)
    
    if r2.status_code == 201:
        print(f"✅ Upload complete!\n🎉 {release['html_url']}")
    else:
        print(f"❌ Upload failed: {r2.status_code}")
else:
    print(f"❌ Failed: {r.status_code}\n{r.text}")
