"""
Build portable distribution package
Creates onedir build and packages as ZIP for easy distribution
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    # Get project root
    project_root = Path(__file__).parent
    
    print("=" * 70)
    print("Building Portable Distribution Package")
    print("=" * 70)
    
    # Clean previous builds
    print("\n[1/4] Cleaning previous builds...")
    for dir_name in ['build', 'dist']:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  ✓ Removed {dir_name}/")
    
    # Build with PyInstaller
    print("\n[2/4] Building with PyInstaller (onedir mode)...")
    python_exe = project_root / 'venv312' / 'Scripts' / 'python.exe'
    spec_file = project_root / 'Journey-Level-Exam-Generator.spec'
    
    result = subprocess.run(
        [str(python_exe), '-m', 'PyInstaller', '--noconfirm', str(spec_file)],
        cwd=str(project_root),
        capture_output=False
    )
    
    if result.returncode != 0:
        print("  ✗ Build failed!")
        sys.exit(1)
    
    print("  ✓ Build completed successfully")
    
    # Create ZIP package
    print("\n[3/4] Creating ZIP distribution package...")
    dist_folder = project_root / 'dist' / 'Journey-Level-Exam-Generator'
    
    if not dist_folder.exists():
        print(f"  ✗ Distribution folder not found: {dist_folder}")
        sys.exit(1)
    
    # Create README for distribution
    readme_content = """# Journey-Level Exam Generator

## Installation Instructions

1. Extract this ZIP file to your desired location (e.g., C:\\Program Files\\Journey-Level-Exam-Generator)
2. Run Journey-Level-Exam-Generator.exe from the extracted folder
3. The application will create its database files in the same folder

## Important Notes

- **Do not move the .exe file separately** - the entire folder structure must stay together
- All DLL files in the _internal folder are required for the application to run
- Your exam data and settings are stored in the application folder

## System Requirements

- Windows 10 or later
- No Python installation required - everything is included

## Support

For issues or questions, please contact your administrator.
"""
    
    readme_path = dist_folder / 'README.txt'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✓ Created README.txt")
    
    # Create ZIP
    zip_path = project_root / 'dist' / 'Journey-Level-Exam-Generator-Portable'
    shutil.make_archive(str(zip_path), 'zip', str(dist_folder.parent), dist_folder.name)
    print(f"  ✓ Created {zip_path.name}.zip")
    
    # Get file size
    zip_file = Path(str(zip_path) + '.zip')
    size_mb = zip_file.stat().st_size / (1024 * 1024)
    
    print("\n[4/4] Build Summary")
    print(f"  Package: {zip_file.name}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Location: {zip_file}")
    
    print("\n" + "=" * 70)
    print("✓ Portable distribution package created successfully!")
    print("=" * 70)
    print("\nDistribution Instructions:")
    print("1. Share the ZIP file with users")
    print("2. Users extract the ZIP to any folder")
    print("3. Users run Journey-Level-Exam-Generator.exe from the extracted folder")

if __name__ == '__main__':
    main()
