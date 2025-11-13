import requests, os
T = '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'
h = {'Authorization': f'Bearer {T}', 'Accept': 'application/vnd.github+json'}
body = """## 🔧 Fixed Old Version Not Closing After Update

Version 1.0.13 ensures the old version properly exits after launching the new one.

### Issue Fixed
- ✅ Old version now properly closes after update
- ✅ Uses `os._exit(0)` to force process termination
- ✅ Launches new version immediately
- ✅ No more duplicate processes running
- ✅ Cleaner, professional update experience

**Built with ⚡ for seamless updates!**
"""
r = requests.post('https://api.github.com/repos/zerocool5878/Journey-Level-Exam-Generator/releases', 
                 headers=h, json={'tag_name': 'v1.0.13', 'name': 'v1.0.13 - Process Exit Fix', 'body': body, 'draft': False})
print('✅ Release created!' if r.status_code == 201 else f'❌ Failed: {r.status_code}\n{r.text}')
if r.status_code == 201:
    rel = r.json()
    print('Uploading 52.8 MB...')
    with open('release/Journey-Level-Exam-Generator.exe', 'rb') as f:
        r2 = requests.post(rel['upload_url'].split('{')[0], headers={**h, 'Content-Type': 'application/octet-stream'},
                          params={'name': 'Journey-Level-Exam-Generator.exe'}, data=f)
    print(f'✅ Done!\n{rel["html_url"]}' if r2.status_code == 201 else f'❌ Upload failed: {r2.status_code}')
