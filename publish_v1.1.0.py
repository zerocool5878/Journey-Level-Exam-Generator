import requests, os
T = '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'
h = {'Authorization': f'Bearer {T}', 'Accept': 'application/vnd.github+json'}
body = """# 🎉 v1.1.0 - Stable Release

**Major milestone!** Version 1.1.0 represents the first fully stable release with a complete, working auto-updater system.

## 🌟 What's New in v1.1.0

### Fully Working Auto-Updater
- ✅ **Smart background checks** - Detects updates 5 seconds after launch
- ✅ **Real-time progress** - Shows download progress with MB and percentage
- ✅ **Proper UI updates** - No freezing, smooth experience
- ✅ **Clean process management** - Old version exits completely after update
- ✅ **Automatic restart** - New version launches seamlessly

### All Core Features
- ✅ **Dual Database System** - JW and CW/CE question banks
- ✅ **Multi-Language Support** - Full English and Spanish interface/PDFs
- ✅ **4 Independent Databases** - Separate storage per mode and language
- ✅ **Image Support** - Questions with illustrations (fixed path resolution)
- ✅ **Professional PDFs** - Two-column layout with proper formatting
- ✅ **Excel Import** - Bulk question management
- ✅ **Custom UI Styling** - Professional blue, green, orange buttons
- ✅ **Dynamic About Dialog** - Shows correct version automatically
- ✅ **Smart Folder Creation** - No duplicate messages

## 🔧 Technical Highlights

### Auto-Updater Improvements (v1.0.9 → v1.1.0)
- Fixed image path resolution for PyInstaller bundles
- Fixed About dialog to show dynamic version
- Improved dialog sizing (650x600)
- Added progress callbacks for UI updates
- Fixed threading issues with Tkinter
- Implemented `os._exit(0)` for clean process termination

### Build System
- Complete PyInstaller dependency bundling
- Proper TCL/TK resource handling
- 52.8 MB standalone executable
- No external dependencies required

## 💻 System Requirements

- **Operating System:** Windows 10 or later (64-bit)
- **Memory:** 4GB RAM recommended
- **Storage:** 150MB free disk space
- **Additional Software:** **NONE!**

## 🚀 Installation

1. Download `Journey-Level-Exam-Generator.exe` below
2. Double-click to run - NO INSTALLATION REQUIRED
3. Program creates databases and folders automatically
4. Start using immediately!

## 📱 Support

- **GitHub:** https://github.com/zerocool5878/Journey-Level-Exam-Generator
- **Issues:** Report via GitHub Issues
- **Auto-Updates:** Built-in update notification system

## ⭐ Why v1.1.0?

This is the first version where **everything just works**:
- Download the EXE ✅
- Run it ✅
- Create questions ✅
- Generate tests ✅
- Get automatic updates ✅

No Python, no dependencies, no hassle!

---

**Built with ⚡ for professional exam generation!**
"""
r = requests.post('https://api.github.com/repos/zerocool5878/Journey-Level-Exam-Generator/releases', 
                 headers=h, json={'tag_name': 'v1.1.0', 'name': 'v1.1.0 - Stable Release 🎉', 'body': body, 'draft': False})
print('✅ Release created!' if r.status_code == 201 else f'❌ Failed: {r.status_code}\n{r.text}')
if r.status_code == 201:
    rel = r.json()
    print('Uploading 52.8 MB...')
    with open('release/Journey-Level-Exam-Generator.exe', 'rb') as f:
        r2 = requests.post(rel['upload_url'].split('{')[0], headers={**h, 'Content-Type': 'application/octet-stream'},
                          params={'name': 'Journey-Level-Exam-Generator.exe'}, data=f)
    print(f'✅ Done!\n{rel["html_url"]}' if r2.status_code == 201 else f'❌ Upload failed: {r2.status_code}')
