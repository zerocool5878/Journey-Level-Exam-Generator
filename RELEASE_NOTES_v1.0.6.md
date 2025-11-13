# Release Notes - Journey-Level Exam Generator v1.0.6

**Release Date:** November 13, 2025

## 🚀 What's New in v1.0.6

### 🎯 Revolutionary Dual-Toggle Database System
- **Mode Toggle:** Switch between JW and CW/CE exam types with visual green indicators
- **Language Toggle:** Switch between English and Español with dedicated language support
- **4 Independent Databases:** Complete separation for JW+English, JW+Spanish, CW/CE+English, CW/CE+Spanish
- **Seamless Switching:** Instant database switching without data loss or application restart

### 🌐 Multi-Language Support
- **Dynamic PDF Titles:** Automatically adjust based on mode and language selection
  - JW + English: "Journey-Level Proficiency Exam"
  - JW + Spanish: "Examen de Competencia de Nivel de Viaje"
  - CW/CE + English: "CW/CE Exam"
  - CW/CE + Spanish: "Examen CW/CE"
- **Spanish Interface Elements:** Native Spanish labels and terminology
- **Answer Keys:** Multi-language support with appropriate titles

### 🎮 Enhanced User Interface
- **Clean Dual Toggle Design:** Professional toggle switches on main interface
- **Visual Feedback:** Green highlighting for selected mode and language
- **Contextual Window Titles:** Shows current mode and language (e.g., "JW (EN)", "CW/CE (ES)")
- **Intuitive Layout:** Side-by-side toggles with clear labels

### 💾 Advanced Database Management
- **Automatic Database Creation:** New databases created seamlessly when switching modes
- **Independent Operations:** Each database operates completely separately
- **Safe Wipe Function:** Database wipe targets only currently selected database
- **Settings Persistence:** Mode and language selections saved between sessions

### 🔧 Technical Improvements
- **Enhanced Category Validation:** Real-time validation with maximum percentage guidance
- **Improved Edit Functionality:** Streamlined question editing using unified dialog
- **Better Offline Handling:** Robust auto-updater with adaptive timeouts
- **Performance Optimization:** Efficient database switching with proper connection management

## 🔄 Database File Structure
- `test_questions.db` - JW English (existing database preserved)
- `test_questions_spanish.db` - JW Spanish
- `cw_questions.db` - CW/CE English  
- `cw_questions_spanish.db` - CW/CE Spanish

## 🎯 Key Features from Previous Versions
- **Smart Auto-Update System:** Non-intrusive update notifications (v1.0.5)
- **Enhanced Category Settings:** Intelligent percentage validation with max recommendations
- **Professional PDF Layout:** Natural column flow with consistent formatting
- **Intelligent Question Selection:** Handles category shortages gracefully
- **Excel Import Support:** Works perfectly across all database modes

## 💡 Why This Update Matters

Version 1.0.6 represents a **major architectural enhancement** that transforms the application from a single-database tool into a comprehensive multi-mode, multi-language examination system. Users can now:

- **Manage Multiple Exam Types:** Separate JW and CW/CE question banks
- **Support Multiple Languages:** English and Spanish with native terminology
- **Maintain Complete Separation:** No cross-contamination between databases
- **Switch Instantly:** Real-time mode switching without losing work
- **Generate Localized Content:** PDFs with appropriate titles and formatting

This release maintains **100% backward compatibility** while adding powerful new capabilities that scale with organizational needs.

## 🔄 Upgrade Notes

- **From v1.0.5:** Dual database system + multi-language support + enhanced category validation
- **From v1.0.4:** All previous improvements + revolutionary database architecture
- **From v1.0.3:** Complete feature set + professional multi-mode interface
- **Existing Data:** Your current `test_questions.db` becomes the JW English database automatically

## 💾 Installation

1. Download `Journey-Level-Exam-Generator.exe` from the release assets
2. Run the executable - no installation required
3. **NEW:** Toggle between 4 different database modes seamlessly
4. **Preserved:** All existing questions and settings remain intact

## 📊 System Requirements

- **OS:** Windows 10 or later
- **Memory:** 4GB RAM recommended
- **Storage:** 150MB free space (increased for multiple databases)
- **Network:** Internet connection required for update checking
- **Display:** 1024x768 minimum resolution

## 🛠️ For Developers

This release demonstrates:
- **Advanced Database Architecture:** Multi-database management with seamless switching
- **Internationalization Best Practices:** Clean language switching with localized content
- **State Management:** Persistent settings across application sessions
- **UI/UX Excellence:** Intuitive toggle system with visual feedback
- **Backward Compatibility:** Seamless migration from single to multi-database architecture

## 🎯 Perfect For Organizations That Need:
- **Separate JW and CW/CE Question Banks**
- **English and Spanish Language Support**  
- **Independent Database Management**
- **Professional Multi-Language PDFs**
- **Scalable Examination Systems**

---

**Download:** Journey-Level-Exam-Generator.exe (52.3 MB)

**Previous Version:** [v1.0.5](https://github.com/zerocool5878/Journey-Level-Exam-Generator/releases/tag/v1.0.5)

Built with 🎯 for professional multi-language examination management!