#!/usr/bin/env python3
import requests, os
T = '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'
h = {'Authorization': f'Bearer {T}', 'Accept': 'application/vnd.github+json'}
body = """## 🔧 Fixed Auto-Updater UI Freezing

Version 1.0.12 fixes critical threading issues that caused the update dialog to freeze.

### Issues Fixed
- ✅ Fixed Tkinter threading issues causing UI freeze
- ✅ Progress updates now display properly
- ✅ Download completes and installs successfully
- ✅ Smoother, more reliable update experience
- ✅ Updates every 1MB to avoid UI lag

### Technical Changes
- Used thread-safe callback function for UI updates
- Replaced `dialog.update()` with `update_idletasks()`
- Added try/except to handle dialog closure gracefully
- Reduced update frequency to improve performance

**Built with ⚡ for rock-solid updates!**
"""
r = requests.post('https://api.github.com/repos/zerocool5878/Journey-Level-Exam-Generator/releases', 
                 headers=h, json={'tag_name': 'v1.0.12', 'name': 'v1.0.12 - Auto-Updater Threading Fix', 
                                 'body': body, 'draft': False})
print('✅ Release created!' if r.status_code == 201 else f'❌ Failed: {r.status_code}')
if r.status_code == 201:
    rel = r.json()
    print('Uploading 52.8 MB...')
    with open('release/Journey-Level-Exam-Generator.exe', 'rb') as f:
        r2 = requests.post(rel['upload_url'].split('{')[0], headers={**h, 'Content-Type': 'application/octet-stream'},
                          params={'name': 'Journey-Level-Exam-Generator.exe'}, data=f)
    print(f'✅ Done!\n{rel["html_url"]}' if r2.status_code == 201 else f'❌ Upload failed: {r2.status_code}')
