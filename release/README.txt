# Journey-Level Exam Generator v1.0.11

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
- **Version**: 1.0.11
- **Build Date**: November 2025
- **Python Version**: 3.13
- **Architecture**: 64-bit Windows

## ⚖️ License
This software is provided as-is for educational and professional use.

---

**Enjoy managing your test question banks!** 🎓
