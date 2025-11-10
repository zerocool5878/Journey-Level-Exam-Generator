# Journey-Level Exam Generator ⚡

A professional desktop application for creating and managing electrical trade examination questions. This tool is specifically designed for generating Journey-Level Proficiency Exams with customizable question banks and professional PDF output.

## Features

### Core Functionality
- **Question Management**: Add, edit, delete up to 250 questions
- **Category System**: Organize questions by categories  
- **Test Generation**: Generate 50-question tests with configurable category distribution
- **Excel Import**: Bulk import questions from Excel files
- **PDF Export**: Generate printable test PDFs with test taker names

### User Interface
- **Generate Test Tab**: Create tests by entering test taker name
- **Manage Questions Tab**: Add questions manually and view database summary
- **Category Settings Tab**: Configure percentage distribution for each category
- **Import from Excel Tab**: Bulk import questions from spreadsheet files

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Required Python packages (see requirements.txt)

### Installation Steps
1. Clone or download this project
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python test_generator.py
   ```

## Usage Guide

### Getting Started
1. **Add Questions**: Use the "Manage Questions" tab to add questions manually
2. **Import Questions**: Use "Import from Excel" tab to bulk import from spreadsheet
3. **Configure Categories**: Set percentage distribution in "Category Settings" 
- **Generate Tests**: Enter test taker name and generate randomized 50-question tests

### Excel Import Format
Your Excel file should contain these columns:
- **Question**: The question text
- **Answer**: The correct answer
- **Category**: The question category

Example:
| Question | Answer | Category |
|----------|---------|----------|
| What is 2+2? | 4 | Math |
| Capital of France? | Paris | Geography |

### Category Distribution
- Set percentages for each category in the Category Settings tab
- Total should equal 100% for optimal test generation
- Tests contain exactly 50 questions distributed according to your settings

### Test Generation
- Each test contains 50 randomly selected questions
- Questions are distributed according to category percentages
- Tests can be previewed on screen and exported to PDF
- PDF includes test taker name, date, and formatted questions

## Technical Details

### Database
- Uses SQLite database (test_questions.db) for local storage
- Automatically created on first run
- Stores questions, answers, categories, and settings

### File Structure
```
test_generator.py     # Main application
requirements.txt      # Python dependencies  
test_questions.db     # SQLite database (created automatically)
.github/             # Project documentation
├── copilot-instructions.md
```

### Dependencies
- **tkinter**: GUI framework (built into Python)
- **pandas**: Excel file processing
- **openpyxl**: Excel file reading
- **reportlab**: PDF generation
- **sqlite3**: Database (built into Python)

## Troubleshooting

### Common Issues
1. **"Module not found" error**: Install requirements with `pip install -r requirements.txt`
2. **Excel import fails**: Check that your Excel file has the correct column headers
3. **PDF export fails**: Ensure you have write permissions in the selected directory
4. **Category settings not saving**: Make sure percentages add up to 100%

### Support
- Check that all required Python packages are installed
- Verify Excel file format matches the expected columns
- Ensure the application has file system permissions for database operations

## Development

This application was built with:
- Python 3.x
- tkinter for the GUI interface
- SQLite for data storage
- pandas for Excel processing
- reportlab for PDF generation

The application follows a modular design with separate methods for each major feature area.