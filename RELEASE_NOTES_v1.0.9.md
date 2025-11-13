# Release Notes - Journey-Level Exam Generator v1.0.9

**Release Date:** November 13, 2025

## 🐛 Critical Bug Fix - Image Loading

Version 1.0.9 fixes a critical bug where images were not being found when running as a standalone executable.

## Issues Fixed

### Image Path Resolution
**Problem:** Images bundled in the executable or stored in the user's images folder were not being found, resulting in:
- Missing images in question dialogs
- Broken image references in generated PDFs
- "File not found" errors when displaying questions with images

**Root Cause:** The application was not correctly handling PyInstaller's temporary extraction directory (`sys._MEIPASS`). When PyInstaller creates a single-file executable, it extracts bundled resources to a temporary directory at runtime. The old code only looked in the executable's directory, not the temporary bundle location.

**Solution:** 
- ✅ Added new `get_resource_path()` function that correctly handles PyInstaller's `_MEIPASS` temporary directory
- ✅ Updated icon loading to use resource path function
- ✅ Enhanced `get_image_full_path()` to check bundled resources first, then user directory
- ✅ Images now load correctly from both bundled resources and user's images folder

## Technical Details

### New Function: `get_resource_path()`
```python
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not running as PyInstaller bundle, use regular path
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)
```

### Updated Image Resolution Logic
The `get_image_full_path()` method now:
1. Checks bundled resources in PyInstaller's temp directory (`sys._MEIPASS`) first
2. Falls back to user's working directory (where databases are stored)
3. Searches the `images/` subfolder if needed
4. Handles both absolute and relative paths correctly

### Two Types of Image Locations
- **Bundled Images**: Included in the executable during build, extracted to temp directory at runtime
- **User Images**: Stored in the `images/` folder next to the executable, where user adds new question images

## What This Fixes

✅ **Icon Display**: Application icon now loads correctly from bundled resources  
✅ **Question Images**: Images attached to questions display properly in dialogs  
✅ **PDF Generation**: Images render correctly in generated test PDFs  
✅ **User Images**: New images added by users load from `images/` folder  
✅ **Excel Import**: Images referenced in imported questions work correctly  

## All Features from v1.0.8 Preserved

- **Fixed Button Styling**: Custom tk.Button styling (blue, green, orange buttons)
- **Smart Auto-Updater**: Background update check after 5-second delay
- **Dual Database System**: JW and CW/CE question banks
- **Multi-Language Support**: English and Español
- **Complete Dependency Bundling**: All libraries included in standalone executable

## System Requirements

- **Operating System:** Windows 10 or later (64-bit)
- **Memory:** 4GB RAM recommended
- **Storage:** 150MB free disk space
- **Display:** 1024x768 minimum resolution
- **Additional Software:** **NONE** - Everything is included!

## Installation

1. Download `Journey-Level-Exam-Generator.exe` from the release assets
2. Double-click to run - **NO INSTALLATION OR PYTHON REQUIRED**
3. Program creates databases and `images/` folder automatically
4. All features work immediately out of the box

## Upgrade Notes

**From v1.0.8 or earlier:**
- Simply download the new executable and replace the old one
- All existing databases remain compatible
- Images in your `images/` folder are preserved
- No data loss or migration needed
- Settings preserved in `app_settings.json`

## Testing Performed

This release has been verified to:
- ✅ Load application icon from bundled resources
- ✅ Display images in question management dialogs
- ✅ Generate PDFs with embedded images
- ✅ Load user images from `images/` folder
- ✅ Handle both bundled and user-added images correctly
- ✅ Work on clean Windows installations without Python

## For Developers

### Key Changes
1. **New Function**: `get_resource_path(relative_path)` - Handles PyInstaller's `_MEIPASS`
2. **Updated**: Icon loading uses `get_resource_path()` instead of `get_application_path()`
3. **Enhanced**: `get_image_full_path()` checks bundled resources first, then user directory

### Build Configuration
- Images directory still bundled with `--add-data=images;images`
- Icon bundled with `--add-data=lightning_icon.ico;.`
- All resources correctly extracted to `sys._MEIPASS` at runtime

## Why This Update is Critical

**v1.0.8 Issue:** 
- Images not loading in executable
- Icon not displaying
- PDF generation failed with image questions
- Broken user experience for image-based questions

**v1.0.9 Solution:**
- ✅ Correct handling of PyInstaller's resource extraction
- ✅ Images load from both bundled and user locations
- ✅ Professional appearance with icon and images
- ✅ Full functionality for image-based questions

## Support

- **GitHub:** https://github.com/zerocool5878/Journey-Level-Exam-Generator
- **Issues:** Report bugs via GitHub Issues tab
- **Documentation:** See included README.txt

---

**Download:** Journey-Level-Exam-Generator.exe (52.8 MB)

**Previous Versions:** 
- [v1.0.8](https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases/tag/v1.0.8) - Fixed button styling, had image loading issue
- [v1.0.7](https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases/tag/v1.0.7) - Fixed dependencies
- [v1.0.6](https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases/tag/v1.0.6) - Had dependency issues

Built with 🔧 for reliable image handling!
