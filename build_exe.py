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
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller command with proper options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable
        "--windowed",                   # No console window
        "--icon=lightning_icon.ico",    # Use our custom icon
        "--name=Journey-Level-Exam-Generator",  # Executable name
        "--add-data=lightning_icon.ico;.",      # Include icon in bundle
        "--hidden-import=tkinter",              # Ensure tkinter is included
        "--hidden-import=PIL",                  # Ensure Pillow is included
        "--hidden-import=reportlab",            # Ensure reportlab is included
        "--hidden-import=pandas",               # Ensure pandas is included
        "--hidden-import=openpyxl",             # Ensure openpyxl is included
        "--clean",                              # Clean cache
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
            shutil.copy2(exe_path, release_dir / "Journey-Level-Exam-Generator.exe")
            print(f"📦 Executable created: {release_dir}/Journey-Level-Exam-Generator.exe")
            
            # Get file size
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📏 File size: {size_mb:.1f} MB")
        else:
            print("❌ Executable not found in dist directory")
            return False
        
        # Create README for release
        readme_content = """# Journey-Level Exam Generator v1.0.0

## Installation
1. Download `Journey-Level-Exam-Generator.exe`
2. Run the executable - no installation required!
3. The program will create its database and folders automatically

## Features
- Manage up to 250 questions with categories
- Support for images in questions
- Multiple choice format (2-4 options per question)
- Excel import for bulk question management
- Professional PDF generation with two-column layout
- Configurable category distribution
- Password-protected database management

## System Requirements
- Windows 10 or later
- No additional software required

## Usage
1. Launch the application
2. Use "Manage Questions" to add your questions
3. Configure category percentages in "Settings"
4. Generate tests with "Generate Test"
5. Print the professional PDF output

## Data Security
- All data is stored locally on your computer
- No internet connection required
- Your question pool remains private

## Support
For issues or questions, visit: https://github.com/zerocool5878/Journey-Level-Exam-Generator
"""
        
        with open(release_dir / "README.txt", "w") as f:
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