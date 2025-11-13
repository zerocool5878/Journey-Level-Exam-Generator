# Release Notes - Version 1.1.2

## Bug Fixes
- **Auto-Updater Critical Fix**: Fixed updater to dynamically detect actual EXE filename instead of assuming hardcoded name
- **Update Process**: Batch script now correctly replaces the running executable regardless of its filename
- **Progress Display**: Progress label properly positioned above buttons in update dialog
- **Process Exit**: Improved exit mechanism prevents hanging during update installation

## Technical Improvements
- Auto-updater now uses `sys.executable` to detect its own filename dynamically
- Streamlined file replacement process using batch script
- Fixed GitHub upload method to prevent file corruption
- Added proper timing delays to prevent race conditions

## Notes
This release fixes critical issues where updates would fail if the executable was renamed or running from non-standard locations. The auto-updater is now more robust and reliable.
