#!/usr/bin/env python3
"""
Release script for Journey-Level Exam Generator
Handles version updates, building, and release preparation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import re
from datetime import datetime

def get_current_version():
    """Get current version from version.py"""
    try:
        with open('version.py', 'r') as f:
            content = f.read()
            match = re.search(r'VERSION = "([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return "1.0.0"

def update_version_in_files(new_version):
    """Update version in all relevant files"""
    files_to_update = [
        ('version.py', r'VERSION = "[^"]+"', f'VERSION = "{new_version}"'),
        ('auto_updater.py', r'self\.current_version = "[^"]+"', f'self.current_version = "{new_version}"'),
        ('test_generator.py', r'Journey-Level Exam Generator v[0-9.]+', f'Journey-Level Exam Generator v{new_version}'),
        ('README.md', r'# Journey-Level Exam Generator v[0-9.]+', f'# Journey-Level Exam Generator v{new_version}'),
    ]
    
    for filename, pattern, replacement in files_to_update:
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                
                updated_content = re.sub(pattern, replacement, content)
                
                with open(filename, 'w') as f:
                    f.write(updated_content)
                
                print(f"✅ Updated version in {filename}")
            except Exception as e:
                print(f"❌ Error updating {filename}: {e}")

def create_release_notes(version):
    """Create release notes template"""
    notes_filename = f"RELEASE_NOTES_v{version}.md"
    
    if os.path.exists(notes_filename):
        print(f"⚠️  Release notes already exist: {notes_filename}")
        return notes_filename
    
    template = f"""# Release Notes - Journey-Level Exam Generator v{version}

**Release Date:** {datetime.now().strftime('%B %d, %Y')}

## 🚀 What's New in v{version}

### ✨ New Features
- [Add new features here]

### 🔧 Improvements
- [Add improvements here]

### 🐛 Bug Fixes
- [Add bug fixes here]

### 📋 Technical Changes
- [Add technical changes here]

## 💾 Installation

1. Download `Journey-Level-Exam-Generator.exe` from the release assets
2. Run the executable - no installation required
3. The application will automatically update its database schema if needed

## 🔄 Upgrade Notes

- Existing databases will be automatically upgraded
- No data loss expected during upgrade
- Backup recommended before upgrading

## 📊 System Requirements

- **OS:** Windows 10 or later
- **Memory:** 4GB RAM recommended
- **Storage:** 100MB free space
- **Display:** 1024x768 minimum resolution

---

**Download:** [Journey-Level-Exam-Generator.exe](https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases/tag/v{version})
"""
    
    with open(notes_filename, 'w') as f:
        f.write(template)
    
    print(f"📝 Created release notes template: {notes_filename}")
    return notes_filename

def build_executable():
    """Build the executable using the build script"""
    print("🔨 Building executable...")
    
    try:
        result = subprocess.run([sys.executable, "build_exe.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error building executable: {e}")
        return False

def create_git_tag(version):
    """Create and push git tag for the release"""
    tag_name = f"v{version}"
    
    try:
        # Check if tag already exists
        result = subprocess.run(["git", "tag", "-l", tag_name], 
                              capture_output=True, text=True)
        
        if tag_name in result.stdout:
            print(f"⚠️  Git tag {tag_name} already exists")
            return True
        
        # Create tag
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Release v{version}"], check=True)
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release v{version}"], check=True)
        subprocess.run(["git", "push"], check=True)
        subprocess.run(["git", "push", "origin", tag_name], check=True)
        
        print(f"✅ Created and pushed git tag: {tag_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error with git operations: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        current_version = get_current_version()
        print(f"Usage: python release.py <new_version>")
        print(f"Current version: {current_version}")
        print(f"Example: python release.py 1.0.1")
        sys.exit(1)
    
    new_version = sys.argv[1]
    current_version = get_current_version()
    
    print(f"🚀 Creating release {new_version} (current: {current_version})")
    
    # Update version in all files
    print("\n📝 Updating version numbers...")
    update_version_in_files(new_version)
    
    # Create release notes template
    print("\n📄 Creating release notes...")
    notes_file = create_release_notes(new_version)
    
    # Build executable
    print("\n🔨 Building executable...")
    if not build_executable():
        print("❌ Build failed. Aborting release.")
        sys.exit(1)
    
    # Create git tag
    print("\n🏷️  Creating git tag...")
    if not create_git_tag(new_version):
        print("❌ Git operations failed. Aborting release.")
        sys.exit(1)
    
    print(f"""
🎉 Release v{new_version} prepared successfully!

Next steps:
1. Edit the release notes in: {notes_file}
2. Go to: https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases
3. Create a new release using tag v{new_version}
4. Upload the executable from: release/Journey-Level-Exam-Generator.exe
5. Copy the release notes from: {notes_file}
6. Publish the release

The auto-updater will detect the new version automatically! 🚀
""")

if __name__ == "__main__":
    main()