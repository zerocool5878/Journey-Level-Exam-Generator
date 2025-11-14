"""
Publish Script for Journey-Level Exam Generator v1.1.3
Builds the application and creates a GitHub release with onedir distribution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import zipfile

# Configuration
VERSION = "1.1.3"
TAG = f"v{VERSION}"
# GitHub token not needed - using GitHub CLI (gh) which uses its own authentication
REPO_OWNER = "zerocool5878"
REPO_NAME = "Journey-Level-Exam-Generator"

def print_step(message):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {description} failed!")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    print(f"Success: {description}")
    return True

def clean_build():
    """Clean build directories"""
    print_step("Cleaning Build Directories")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"Removed: {dir_path}")
    print("Build directories cleaned!")

def build_application():
    """Build the application with PyInstaller"""
    print_step("Building Application with PyInstaller")
    
    # Use venv312 Python
    python_exe = Path("venv312/Scripts/python.exe")
    if not python_exe.exists():
        print("ERROR: venv312 not found!")
        return False
    
    spec_file = Path("Journey-Level-Exam-Generator.spec")
    if not spec_file.exists():
        print("ERROR: spec file not found!")
        return False
    
    # Build with PyInstaller
    cmd = f'"{python_exe}" -m PyInstaller --noconfirm "{spec_file}"'
    if not run_command(cmd, "PyInstaller build"):
        return False
    
    # Verify build output (single-file mode)
    exe_path = Path("dist/Journey-Level-Exam-Generator.exe")
    if not exe_path.exists():
        print("ERROR: Built executable not found!")
        return False
    
    exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"✓ Executable built: {exe_path} ({exe_size_mb:.1f} MB)")
    return True

def create_zip_package():
    """Create ZIP package with single-file EXE"""
    print_step("Creating ZIP Package")
    
    exe_file = Path("dist/Journey-Level-Exam-Generator.exe")
    if not exe_file.exists():
        print("ERROR: Executable file not found!")
        return None
    
    # Create README for the package
    readme_content = """# Journey-Level Exam Generator - Installation Instructions

## Installation

1. **Extract the EXE**: Extract the executable from this ZIP file to your desired location
   - Right-click the ZIP file
   - Select "Extract All..."
   - Choose your destination folder

2. **Run the Application**: 
   - Navigate to the extracted location
   - Double-click `Journey-Level-Exam-Generator.exe`

## Important Notes

- **Single file**: This is a standalone executable - no additional files needed
- **First run**: Windows Defender may scan the application - this is normal
- **Startup time**: First launch may take a few seconds as the app extracts dependencies

## Updating

- The application will check for updates automatically on startup
- When an update is available, click "Update Now"
- After update downloads, the application will close
- **Manually reopen the application** to use the new version
- Your data (questions, settings, images) will be preserved

## System Requirements

- Windows 10 or later
- 100 MB free disk space
- Internet connection for updates

## Troubleshooting

If the application doesn't start:
1. Make sure the file is extracted from the ZIP
2. Try running as Administrator (right-click → Run as administrator)
3. Check Windows Defender hasn't quarantined the file

## Data Location

Your exam data is stored in the same folder as the executable:
- Questions: 4 database files (.db)
- Custom images: `images` subfolder (created automatically)
- Settings: `app_settings.json` (created automatically)

For support, visit: https://github.com/zerocool5878/Journey-Level-Exam-Generator
"""
    
    readme_path = Path("dist/README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Created: {readme_path}")
    
    # Create ZIP file with just the EXE and README
    zip_name = f"Journey-Level-Exam-Generator-v{VERSION}-Windows.zip"
    zip_path = Path("dist") / zip_name
    
    print(f"Creating ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(exe_file, exe_file.name)
        print(f"  Added: {exe_file.name}")
        zipf.write(readme_path, readme_path.name)
        print(f"  Added: {readme_path.name}")
    
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n✓ ZIP created: {zip_path} ({zip_size_mb:.1f} MB)")
    return zip_path

def git_operations():
    """Perform git operations"""
    print_step("Git Operations")
    
    # Add all changes
    if not run_command("git add .", "Stage changes"):
        return False
    
    # Commit
    commit_msg = f"Release v{VERSION} - Simplified auto-updater with manual restart"
    if not run_command(f'git commit -m "{commit_msg}"', "Commit changes"):
        print("Note: No changes to commit (this might be okay)")
    
    # Create tag
    tag_msg = f"Version {VERSION} - Improved auto-updater reliability"
    if not run_command(f'git tag -a {TAG} -m "{tag_msg}"', "Create tag"):
        print("Warning: Tag might already exist")
    
    # Push changes
    if not run_command("git push origin main", "Push to main"):
        return False
    
    # Push tag
    if not run_command(f"git push origin {TAG}", "Push tag"):
        return False
    
    print("✓ Git operations completed!")
    return True

def create_github_release(zip_path):
    """Create GitHub release and upload assets"""
    print_step("Creating GitHub Release")
    
    # Read release notes
    release_notes_path = Path(f"RELEASE_NOTES_v{VERSION}.md")
    if release_notes_path.exists():
        with open(release_notes_path, 'r', encoding='utf-8') as f:
            release_body = f.read()
    else:
        release_body = f"Release version {VERSION}"
    
    # Create release using GitHub CLI
    release_name = f"Journey-Level Exam Generator v{VERSION}"
    
    # Escape quotes in release body for command line
    release_body_escaped = release_body.replace('"', '\\"').replace('\n', '\\n')
    
    cmd = f'gh release create {TAG} "{zip_path}" --title "{release_name}" --notes "{release_body_escaped}" --repo {REPO_OWNER}/{REPO_NAME}'
    
    if not run_command(cmd, "Create GitHub release"):
        print("ERROR: Failed to create release!")
        print("You may need to install GitHub CLI: https://cli.github.com/")
        return False
    
    print(f"✓ Release created: {TAG}")
    print(f"✓ Asset uploaded: {zip_path.name}")
    return True

def main():
    """Main execution function"""
    print_step(f"Building and Publishing Journey-Level Exam Generator v{VERSION}")
    
    # Check if we're in the right directory
    if not Path("test_generator.py").exists():
        print("ERROR: Must run from project root directory!")
        return 1
    
    try:
        # Step 1: Clean
        clean_build()
        
        # Step 2: Build
        if not build_application():
            print("\n❌ Build failed!")
            return 1
        
        # Step 3: Create ZIP
        zip_path = create_zip_package()
        if not zip_path:
            print("\n❌ ZIP creation failed!")
            return 1
        
        # Step 4: Git operations
        if not git_operations():
            print("\n❌ Git operations failed!")
            return 1
        
        # Step 5: Create GitHub release
        if not create_github_release(zip_path):
            print("\n❌ GitHub release failed!")
            return 1
        
        # Success!
        print_step("✓ RELEASE SUCCESSFUL!")
        print(f"Version: {VERSION}")
        print(f"Tag: {TAG}")
        print(f"Package: {zip_path.name}")
        print(f"\nRelease URL: https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/{TAG}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
