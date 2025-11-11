# Release Notes - Journey-Level Exam Generator v1.0.1

**Release Date:** November 10, 2025

## 🚀 What's New in v1.0.1

### ⚡ Major Feature: Auto-Updater System
- **Automatic Update Notifications:** Users are now automatically notified when new versions are available
- **One-Click Updates:** Download and install updates with just a few clicks
- **Manual Update Check:** Help menu includes "Check for Updates" option
- **Safe Update Process:** Backup and restore functionality ensures safe updates
- **GitHub Integration:** Updates are delivered through GitHub releases

### 🔧 Improvements
- **Professional Menu System:** Added File, Tools, and Help menus for better organization
- **Database Backup Feature:** Tools → Backup Database for easy data protection
- **About Dialog:** Professional about dialog with version information and features list
- **Enhanced User Experience:** Better organization of features through menu system
- **Scrollable Category Settings:** Categories now display in a grid with scrollbars to handle unlimited categories without pushing buttons off-screen

### � Bug Fixes
- **Question Selection Algorithm:** Fixed issue where tests generated fewer than 50 questions (e.g., 48 instead of 50) when category percentages didn't divide evenly
- **Images Folder Location:** Fixed images folder being created in temporary directory instead of next to executable
- **Category UI Refresh:** Fixed category settings not refreshing properly after Excel import, eliminating duplicate "No categories found" messages
- **Scalable Category Layout:** Fixed categories pushing buttons off-screen by implementing scrollable grid layout that supports unlimited categories
- **Dialog Layout Optimization:** Fixed "Add Question" dialog and Category Settings page layout to ensure all elements fit properly on screen

### �📋 Technical Enhancements
- **Version Management:** Centralized version tracking system
- **Release Automation:** Automated release preparation and building tools
- **Error Handling:** Improved error handling for network operations
- **Thread Safety:** Background update checking doesn't block the UI
- **Intelligent Question Distribution:** Smart algorithm fills category shortages from other categories to ensure exactly 50 questions
- **Executable Path Resolution:** Proper detection of .exe vs .py environments for consistent file handling

## 💾 Installation

1. Download `Journey-Level-Exam-Generator.exe` from the release assets
2. Run the executable - no installation required
3. **NEW:** The application will automatically check for updates on startup
4. Existing databases will be automatically compatible

## 🔄 Upgrade Notes

- **For v1.0.0 users:** This version adds auto-update capability - future updates will be automatic!
- **Existing Data:** All your questions, categories, and settings are preserved
- **New Features:** Access new tools through the menu bar (File, Tools, Help)

## ⚡ Why This Update Matters

This release ensures that **all future updates** will be delivered automatically to users. Once you install v1.0.1, you'll never need to manually check for updates again - the application will notify you when new versions are available and help you update with just a few clicks.

## 📊 System Requirements

- **OS:** Windows 10 or later
- **Memory:** 4GB RAM recommended
- **Storage:** 100MB free space
- **Network:** Internet connection required for update checking
- **Display:** 1024x768 minimum resolution

## 🛠️ For Developers

This release includes:
- Complete auto-updater system with GitHub API integration
- Release management tools and scripts
- Version tracking and management system
- Professional menu system architecture

---

**Download:** Journey-Level-Exam-Generator.exe (48.1 MB)

**Previous Version:** [v1.0.0](https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases/tag/v1.0.0)

Built with ⚡ for professional exam generation and automatic updates!
