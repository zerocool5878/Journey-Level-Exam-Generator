# Release Notes - Version 1.1.1

## Bug Fixes
- **Auto-Updater UI**: Fixed progress label positioning - now displays above buttons in visible area
- **Auto-Updater Reliability**: Simplified update completion process to prevent hanging at "Installing update..." step
- **Update Process**: Removed blocking message boxes that could cause the updater to freeze
- **Process Exit**: Improved process termination with proper timing to ensure smooth transition to new version

## Technical Improvements
- Added progress status updates during file replacement ("Finalizing...", "Starting new version...")
- Implemented timing delays to prevent race conditions during file operations
- Streamlined exit mechanism for more reliable updates

## Notes
This release fixes the update process issues reported in v1.1.0, ensuring smooth automatic updates without UI freezing or hanging.
