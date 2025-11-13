#!/usr/bin/env python3
"""
Build script for Journey-Level Exam Generator
Creates a standalone executable with proper configuration
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    print("🔨 Building Journey-Level Exam Generator executable...")
    
    # Verify required files exist
    if not os.path.exists("lightning_icon.ico"):
        print("❌ Error: lightning_icon.ico not found!")
        return False
    
    if not os.path.exists("images"):
        print("⚠️  Warning: images directory not found, creating it...")
        os.makedirs("images")
        # Create .gitkeep to preserve directory
        with open("images/.gitkeep", "w") as f:
            f.write("")
    
    print("✅ All required files verified")
    
    # Clean previous builds with error handling
    import time
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name, ignore_errors=True)
                time.sleep(0.5)  # Give Windows time to release locks
                if os.path.exists(dir_name):
                    # Try again if still exists
                    shutil.rmtree(dir_name, ignore_errors=True)
                print(f"🧹 Cleaned {dir_name} directory")
            except Exception as e:
                print(f"⚠️  Warning: Could not fully clean {dir_name}: {e}")
                print("   Continuing with build...")
    
    # Use spec file if it exists, otherwise use command-line args
    spec_file = "Journey-Level-Exam-Generator.spec"
    if os.path.exists(spec_file):
        print(f"📋 Using spec file: {spec_file}")
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--noconfirm",  # Overwrite without asking
            spec_file
        ]
    else:
        # PyInstaller command with proper options
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",                    # Single executable
            "--windowed",                   # No console window
            "--icon=lightning_icon.ico",    # Use our custom icon
            "--name=Journey-Level-Exam-Generator",  # Executable name
        "--add-data=lightning_icon.ico;.",      # Include icon in bundle
        "--add-data=images;images",             # Include images directory
        
        # Core GUI and system imports - CRITICAL FOR STYLING
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.font",
        "--hidden-import=tkinter.constants",
        "--collect-all=tkinter",                # Include ALL tkinter resources
        "--collect-all=_tkinter",               # Include C extension
        # Collect tcl/tk files (themes, styling, etc)
        "--collect-data=tkinter",
        
        # PIL/Pillow - complete image handling
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=PIL._tkinter_finder",
        "--collect-all=PIL",
        
        # ReportLab - complete PDF generation
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.pdfgen",
        "--hidden-import=reportlab.pdfgen.canvas",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=reportlab.lib.utils",
        "--hidden-import=reportlab.lib.units",
        "--hidden-import=reportlab.pdfbase",
        "--hidden-import=reportlab.pdfbase.pdfmetrics",
        "--hidden-import=reportlab.pdfbase._fontdata",
        "--collect-all=reportlab",
        
        # Pandas and data handling
        "--hidden-import=pandas",
        "--hidden-import=pandas.core",
        "--hidden-import=pandas.io",
        "--hidden-import=pandas.io.excel",
        "--hidden-import=pandas.io.formats",
        "--collect-submodules=pandas",
        
        # Excel file handling
        "--hidden-import=openpyxl",
        "--hidden-import=openpyxl.cell",
        "--hidden-import=openpyxl.styles",
        "--collect-all=openpyxl",
        
        # HTTP requests for auto-updater
        "--hidden-import=requests",
        "--hidden-import=urllib3",
        "--hidden-import=certifi",
        "--hidden-import=charset_normalizer",
        
        # Database
        "--hidden-import=sqlite3",
        
        # JSON and system modules
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=datetime",
        "--hidden-import=uuid",
        "--hidden-import=shutil",
        
        # Numpy (pandas dependency)
        "--hidden-import=numpy",
        "--hidden-import=numpy.core",
        "--hidden-import=numpy.core._multiarray_umath",
        
        # Additional data handling
        "--hidden-import=pytz",
        "--hidden-import=dateutil",
        "--hidden-import=dateutil.parser",
        
        # Critical: Don't compress tkinter DLLs - can break themes/styling
            "--noupx",
            
            # Note: --clean removed due to Windows file locking issues
            # Clean manually if needed before running
            "test_generator.py"
        ]
    
    print("Running PyInstaller...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Build successful!")
        
        # Create release directory
        release_dir = Path("release")
        release_dir.mkdir(exist_ok=True)
        
        # Copy executable to release directory
        exe_path = Path("dist/Journey-Level-Exam-Generator.exe")
        if exe_path.exists():
            dest_exe = release_dir / "Journey-Level-Exam-Generator.exe"
            shutil.copy2(exe_path, dest_exe)
            print(f"📦 Executable created: {release_dir}/Journey-Level-Exam-Generator.exe")
            
            # Get file size
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📏 File size: {size_mb:.1f} MB")
            
            # Verify executable
            if dest_exe.exists():
                print("✅ Executable verified in release directory")
            else:
                print("❌ Failed to copy executable to release directory")
                return False
        else:
            print("❌ Executable not found in dist directory")
            return False
        
        # Create README for release
        from version import VERSION
        readme_content = f"""# Journey-Level Exam Generator v{VERSION}

## 🚀 Quick Start
1. Download `Journey-Level-Exam-Generator.exe`
2. Double-click to run - **NO INSTALLATION REQUIRED!**
3. The program automatically creates its databases and folders
4. Start managing questions and generating tests immediately

## ✨ Key Features
- **Dual Database System**: Separate JW and CW/CE question banks
- **Multi-Language Support**: Full English and Spanish interface and PDFs
- **Manage up to 250 questions** with categories per database
- **Image Support**: Include diagrams and illustrations in questions
- **Multiple Choice Format**: 2-4 answer options per question
- **Excel Import**: Bulk question management via spreadsheet
- **Professional PDFs**: Two-column layout with automatic formatting
- **Smart Category Distribution**: Configurable percentage per category
- **Auto-Update System**: Automatic notification of new versions
- **Password Protection**: Secure database management functions

## 💻 System Requirements
- **Operating System**: Windows 10 or later (64-bit)
- **Memory**: 4GB RAM recommended
- **Storage**: 150MB free disk space
- **Display**: 1024x768 minimum resolution
- **Additional Software**: NONE - Everything is included!

## 📦 What's Included
The standalone executable contains:
✅ Complete GUI application
✅ SQLite database engine
✅ PDF generation engine (ReportLab)
✅ Excel file support (pandas, openpyxl)
✅ Image handling (Pillow/PIL)
✅ HTTP client for updates (requests)
✅ All fonts and resources
✅ Images directory structure

## 🎯 Usage Guide

### First Launch
- Program creates 4 databases automatically:
  - `test_questions.db` (JW English)
  - `test_questions_spanish.db` (JW Spanish)
  - `cw_questions.db` (CW/CE English)
  - `cw_questions_spanish.db` (CW/CE Spanish)
- Creates `images/` folder for question illustrations
- Creates `app_settings.json` for preferences

### Managing Questions
1. Click "Manage Questions" button
2. Add questions manually or import from Excel
3. Assign categories to organize questions
4. Add images if needed (stored in images folder)

### Generating Tests
1. Configure category percentages in "Settings"
2. Click "Generate Test"
3. Enter test taker name
4. Professional PDF is created automatically
5. Print or save the PDF

### Switching Modes
- Toggle between **JW** and **CW/CE** modes
- Toggle between **English** and **Español**
- Each combination uses its own database
- Switch instantly without losing data

## 🔒 Data Security
- ✅ All data stored **locally** on your computer
- ✅ No internet connection required (except for update checks)
- ✅ Your question banks remain completely **private**
- ✅ No data sent to external servers
- ✅ Password protection for sensitive operations

## 🆘 Troubleshooting

**"Windows protected your PC" message:**
- Click "More info"
- Click "Run anyway"
- This is normal for unsigned executables

**Excel import not working:**
- Ensure Excel file has columns: Question, Option1, Option2, Answer, Category
- Save file as .xlsx format (not .xls)

**Images not displaying:**
- Place image files in the `images/` folder
- Use relative paths in questions (e.g., "images/diagram1.png")
- Supported formats: PNG, JPG, GIF, BMP

**Program won't start:**
- Check Windows Event Viewer for specific errors
- Ensure you have Windows 10 or later
- Try running as Administrator (right-click → Run as administrator)

## 📱 Support & Updates
- **GitHub**: https://github.com/zerocool5878/Journey-Level-Exam-Generator
- **Issues**: Report bugs via GitHub Issues
- **Updates**: Program checks for updates automatically
- **Manual Updates**: Download new version and replace the EXE

## 📝 Version Information
- **Version**: {VERSION}
- **Build Date**: November 2025
- **Python Version**: 3.13
- **Architecture**: 64-bit Windows

## ⚖️ License
This software is provided as-is for educational and professional use.

---

**Enjoy managing your test question banks!** 🎓
"""
        
        with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("📝 Release README created")
        print(f"🎉 Release ready in: {release_dir.absolute()}")
        return True
        
    else:
        print("❌ Build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False

if __name__ == "__main__":
    main()