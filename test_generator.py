import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import random
from datetime import datetime
import os
import shutil
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageTk
import shutil
from reportlab.lib.units import inch
from threading import Thread

# Import auto-updater functions
try:
    from auto_updater import manual_check_for_updates, startup_update_check
    AUTO_UPDATE_AVAILABLE = True
except ImportError:
    print("Auto-updater not available")
    AUTO_UPDATE_AVAILABLE = False

class TestGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Generator - Question Bank Manager")
        self.root.geometry("1100x750")
        
        # Set the lightning bolt icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'lightning_icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Create menu bar
        self.create_menu()
        
        # Initialize database
        self.init_database()
        
        # Create main interface
        self.create_widgets()
        
        # Load default category settings
        self.load_category_settings()
        
        # Fix existing image paths in database
        self.fix_image_paths()
        
        # Check for updates on startup (after a delay to let UI load)
        if AUTO_UPDATE_AVAILABLE:
            self.root.after(3000, self.startup_update_check)  # Check after 3 seconds
    
    def startup_update_check(self):
        """Check for updates on startup"""
        Thread(target=startup_update_check, daemon=True).start()
    
    def fix_image_paths(self):
        """Fix image paths in database to include images/ prefix"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, image_path FROM questions WHERE image_path IS NOT NULL AND image_path != ''")
            rows = cursor.fetchall()
            
            for question_id, image_path in rows:
                if image_path and not image_path.startswith('images/') and not image_path.startswith('images\\'):
                    # Check if file exists in images directory
                    images_file_path = os.path.join(self.images_dir, image_path)
                    if os.path.exists(images_file_path):
                        # Update database with proper path
                        new_path = f"images/{image_path}".replace('\\', '/')
                        cursor.execute("UPDATE questions SET image_path = ? WHERE id = ?", (new_path, question_id))
                        print(f"Fixed image path for question {question_id}: {image_path} -> {new_path}")
            
            self.conn.commit()
        except Exception as e:
            print(f"Error fixing image paths: {e}")
    
    def get_image_full_path(self, relative_path):
        """Convert relative image path to full path"""
        if not relative_path:
            return None
        if os.path.isabs(relative_path):
            return relative_path
        
        # First try the path as given
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        if os.path.exists(full_path):
            return full_path
        
        # If not found, try looking in the images folder
        if not relative_path.startswith('images/') and not relative_path.startswith('images\\'):
            images_path = os.path.join(self.images_dir, relative_path)
            if os.path.exists(images_path):
                return images_path
        
        # Return the original attempt if nothing else works
        return full_path
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Backup Database", command=self.backup_database)
        tools_menu.add_command(label="Import from Excel", command=self.import_from_excel)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        if AUTO_UPDATE_AVAILABLE:
            help_menu.add_command(label="Check for Updates", command=self.check_for_updates)
            help_menu.add_separator()
        
        help_menu.add_command(label="About", command=self.show_about)
    
    def check_for_updates(self):
        """Check for application updates"""
        if AUTO_UPDATE_AVAILABLE:
            Thread(target=manual_check_for_updates, daemon=True).start()
        else:
            messagebox.showinfo("Updates", "Auto-update feature not available.")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Journey-Level Exam Generator v1.0.1

Professional desktop application for generating journey-level proficiency exams.

Features:
• Manage up to 250 questions with categories
• Image support for questions
• Multiple choice format (2-4 options)
• Professional PDF generation
• Excel import functionality
• Configurable category distribution

Built with ⚡ for professional exam generation.

© 2025 - Licensed under MIT License
GitHub: github.com/zerocool5878/Journey-Level-Exam-Generator"""
        
        messagebox.showinfo("About Journey-Level Exam Generator", about_text)
    
    def backup_database(self):
        """Create a backup of the current database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"test_questions_backup_{timestamp}.db"
            
            # Choose backup location
            backup_path = filedialog.asksaveasfilename(
                title="Save Database Backup",
                defaultextension=".db",
                initialfilename=backup_filename,
                filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
            )
            
            if backup_path:
                shutil.copy2('test_questions.db', backup_path)
                messagebox.showinfo("Backup Complete", 
                                  f"Database backed up successfully to:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Error creating backup: {str(e)}")
    
    def init_database(self):
        """Initialize SQLite database with required tables and create images folder"""
        self.conn = sqlite3.connect('test_questions.db')
        cursor = self.conn.cursor()
        
        # Create images directory if it doesn't exist
        self.images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            messagebox.showinfo("Images Folder Created", 
                              f"Created 'images' folder at:\n{self.images_dir}\n\n" + 
                              "All question images will be automatically copied here when you select them.")
            print(f"Created images directory: {self.images_dir}")
        
        # Questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT NOT NULL,
                choice_a TEXT DEFAULT NULL,
                choice_b TEXT DEFAULT NULL,
                choice_c TEXT DEFAULT NULL,
                choice_d TEXT DEFAULT NULL,
                image_path TEXT DEFAULT NULL,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add new columns if they don't exist (for existing databases)
        new_columns = ['image_path', 'choice_a', 'choice_b', 'choice_c', 'choice_d']
        for column in new_columns:
            try:
                cursor.execute(f'ALTER TABLE questions ADD COLUMN {column} TEXT DEFAULT NULL')
            except sqlite3.OperationalError:
                pass  # Column already exists
        
        # Category settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_settings (
                category TEXT PRIMARY KEY,
                percentage INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def configure_modern_style(self):
        """Configure modern, polished styling for the application"""
        style = ttk.Style()
        
        # Set a modern theme
        try:
            style.theme_use('clam')  # Modern, clean theme
        except:
            pass
        
        # Define color scheme
        colors = {
            'primary': '#2E86AB',      # Professional blue
            'secondary': '#A23B72',    # Accent purple
            'success': '#2E8B57',      # Success green
            'warning': '#FF8C42',      # Warning orange
            'danger': '#DC3545',       # Danger red
            'light': '#F8F9FA',        # Light background
            'dark': '#343A40',         # Dark text
            'white': '#FFFFFF'         # White
        }
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=colors['primary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        style.map('Primary.TButton',
                  background=[('active', '#1F5F79'),
                             ('pressed', '#1A4F6B')])
        
        style.configure('Success.TButton',
                       background=colors['success'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(12, 6))
        style.map('Success.TButton',
                  background=[('active', '#256B47'),
                             ('pressed', '#1F5A3B')])
        
        style.configure('Warning.TButton',
                       background=colors['warning'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(12, 6))
        style.map('Warning.TButton',
                  background=[('active', '#E6732A'),
                             ('pressed', '#CC5A12')])
        
        style.configure('Danger.TButton',
                       background=colors['danger'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(12, 6))
        style.map('Danger.TButton',
                  background=[('active', '#C82333'),
                             ('pressed', '#A71E2A')])
        
        # Configure notebook style
        style.configure('TNotebook',
                       background=colors['light'],
                       tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab',
                       background='#E9ECEF',
                       foreground=colors['dark'],
                       font=('Segoe UI', 11, 'bold'),
                       padding=[20, 12])
        style.map('TNotebook.Tab',
                  background=[('selected', colors['primary']),
                             ('active', '#DEE2E6')],
                  foreground=[('selected', 'white')])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure label styles
        style.configure('Heading.TLabel',
                       background=colors['light'],
                       foreground=colors['dark'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Subheading.TLabel',
                       background=colors['light'],
                       foreground=colors['dark'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 11),
                       padding=8)
    
    def create_widgets(self):
        """Create the main GUI interface"""
        # Configure modern styling
        self.configure_modern_style()
        
        # Set main window background
        self.root.configure(bg='#f0f0f0')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Generate Test
        self.create_test_tab()
        
        # Tab 2: Manage Questions
        self.create_questions_tab()
        
        # Tab 3: Category Settings
        self.create_settings_tab()
        
        # Tab 4: Import from Excel
        self.create_import_tab()
    
    def create_test_tab(self):
        """Create the test generation tab"""
        test_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(test_frame, text="⚡ Generate Test")
        
        # Main content frame with reduced padding
        content_frame = ttk.Frame(test_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Header
        header_label = ttk.Label(content_frame, text="📝 Test Generator", style='Heading.TLabel')
        header_label.pack(pady=(0, 10))
        
        # Test taker name section
        name_frame = ttk.Frame(content_frame, style='Card.TFrame')
        name_frame.pack(fill=tk.X, pady=(0, 10), padx=5, ipady=8)
        
        ttk.Label(name_frame, text="Test Taker Name:", style='Subheading.TLabel').pack(pady=(5, 3))
        self.name_entry = ttk.Entry(name_frame, style='Modern.TEntry', width=40, justify='center')
        self.name_entry.pack(pady=(0, 5))
        
        # Generate test button
        ttk.Button(content_frame, text="🎯 Generate Test (50 Questions)", 
                  command=self.generate_test, style="Primary.TButton").pack(pady=10)
        
        # Test preview section
        preview_section = ttk.Frame(content_frame, style='Card.TFrame')
        preview_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=5)
        
        ttk.Label(preview_section, text="📋 Test Preview", style='Subheading.TLabel').pack(anchor="w", pady=8, padx=10)
        
        # Preview text area with modern styling
        preview_frame = ttk.Frame(preview_section)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.test_preview = tk.Text(preview_frame, height=10, width=80, 
                                   font=("Segoe UI", 10), 
                                   bg='#FFFFFF', fg='#343A40',
                                   relief='flat', borderwidth=2,
                                   selectbackground='#2E86AB',
                                   selectforeground='white')
        scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.test_preview.yview)
        self.test_preview.configure(yscrollcommand=scrollbar.set)
        
        self.test_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export buttons with modern styling - positioned at bottom
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="📄 Export Test to PDF", 
                  command=self.export_to_pdf, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Export Answer Key", 
                  command=self.export_answer_key, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Clear Preview", 
                  command=self.clear_preview, style="Warning.TButton").pack(side=tk.LEFT, padx=5)
    
    def create_questions_tab(self):
        """Create the question management tab"""
        questions_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(questions_frame, text="📚 Manage Questions")
        
        # Main content with minimal padding
        content_frame = ttk.Frame(questions_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Header and action buttons
        header_frame = ttk.Frame(content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="🎓 Question Database", style='Heading.TLabel').pack(side=tk.LEFT)
        
        # Action buttons on the right
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="➕ Add Question", 
                  command=self.open_add_question_dialog, style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.load_questions, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        
        # Search functionality
        search_frame = ttk.Frame(content_frame, style='Card.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        ttk.Label(search_frame, text="🔍 Search:", style='Subheading.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        self.search_entry = ttk.Entry(search_frame, style='Modern.TEntry', width=35)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="🔍 Search", command=self.search_questions, style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="📋 Show All", command=self.load_questions, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        
        # Database table
        database_frame = ttk.Frame(content_frame, style='Card.TFrame')
        database_frame.pack(fill=tk.BOTH, expand=True, ipady=10)
        
        # Questions treeview
        columns = ('ID', 'Question', 'Answer', 'Category', 'Image', 'Date')
        tree_frame = ttk.Frame(database_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.questions_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configure columns with icons
        column_headers = {
            'ID': '🆔 ID',
            'Question': '❓ Question', 
            'Answer': '✅ Answer',
            'Category': '📁 Category',
            'Image': '🖼️ Image',
            'Date': '📅 Date'
        }
        
        for col in columns:
            self.questions_tree.heading(col, text=column_headers[col])
            if col == 'Question':
                self.questions_tree.column(col, width=300)  # Reduced to make room for image column
            elif col == 'Answer':
                self.questions_tree.column(col, width=80)
            elif col == 'Category':
                self.questions_tree.column(col, width=120)
            elif col == 'Image':
                self.questions_tree.column(col, width=70)  # New image column
            elif col == 'Date':
                self.questions_tree.column(col, width=100)
            else:
                self.questions_tree.column(col, width=60)  # ID column
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.questions_tree.yview)
        self.questions_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.questions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Management buttons at bottom
        mgmt_frame = ttk.Frame(content_frame)
        mgmt_frame.pack(pady=10)
        
        ttk.Button(mgmt_frame, text="✏️ Edit Selected", command=self.edit_question, 
                  style="Primary.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(mgmt_frame, text="🗑️ Delete Selected", command=self.delete_question, 
                  style="Danger.TButton").pack(side=tk.LEFT, padx=8)
        
        # Load initial questions
        self.load_questions()
    
    def create_settings_tab(self):
        """Create the category settings tab"""
        settings_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(settings_frame, text="⚙️ Category Settings")
        
        # Main content with padding
        content_frame = ttk.Frame(settings_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = ttk.Label(content_frame, text="⚙️ Category Configuration", style='Heading.TLabel')
        header_label.pack(pady=(0, 20))
        
        # Instructions with modern styling
        instructions_frame = ttk.Frame(content_frame, style='Card.TFrame')
        instructions_frame.pack(fill=tk.X, pady=(0, 20), ipady=15)
        
        instructions = """💡 Configure the percentage distribution of questions for each category in generated tests.
        
📊 Total percentages should equal 100%
🎯 Each test contains 50 questions distributed according to these percentages
📈 Values are rounded to the nearest whole number for question count"""
        
        ttk.Label(instructions_frame, text=instructions, font=("Segoe UI", 10), 
                 justify='left', foreground='#495057').pack(padx=20, pady=10)
        
        # Category settings frame with modern styling
        self.settings_frame = ttk.LabelFrame(content_frame, text="📊 Category Percentages", padding=20)
        self.settings_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save Settings", command=self.save_category_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Default", command=self.reset_category_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh Categories", command=self.load_category_settings).pack(side=tk.LEFT, padx=5)
        
        # Danger zone - Database wipe button
        danger_frame = ttk.LabelFrame(content_frame, text="⚠️ DANGER ZONE", padding=10)
        danger_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(danger_frame, text="WARNING: This will permanently delete ALL questions and data!", 
                 foreground="red", font=("Arial", 10, "bold")).pack(pady=5)
        ttk.Button(danger_frame, text="🗑️ WIPE DATABASE", command=self.wipe_database, 
                  style="Danger.TButton").pack(pady=5)
        
        # Load categories
        self.load_category_settings()
    
    def create_import_tab(self):
        """Create the Excel import tab"""
        import_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(import_frame, text="📊 Import from Excel")
        
        # Main content with padding
        content_frame = ttk.Frame(import_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = ttk.Label(content_frame, text="📊 Excel Import Wizard", style='Heading.TLabel')
        header_label.pack(pady=(0, 20))
        
        # Instructions with modern styling
        instructions_frame = ttk.Frame(content_frame, style='Card.TFrame')
        instructions_frame.pack(fill=tk.X, pady=(0, 20), ipady=15)
        
        instructions = """📋 Required Excel Columns (first row should contain these headers):

📝 Question - The question text
✅ Answer - Correct answer (A, B, C, or D)  
📁 Category - Question category
🅰️ ChoiceA - First multiple choice option
🅱️ ChoiceB - Second multiple choice option  
🅲️ ChoiceC - Third multiple choice option (optional)
🅳️ ChoiceD - Fourth multiple choice option (optional)
🖼️ ImagePath - Path to image file (optional)

💡 Images should be placed in the 'images' folder of the application."""
        
        ttk.Label(instructions_frame, text=instructions, font=("Segoe UI", 10), 
                 justify=tk.LEFT, foreground='#495057').pack(padx=20, pady=10, anchor="w")
        
        # File selection with modern styling
        file_section = ttk.Frame(content_frame, style='Card.TFrame')
        file_section.pack(fill=tk.X, pady=(0, 20), ipady=15)
        
        ttk.Label(file_section, text="📂 Select Excel File", style='Subheading.TLabel').pack(anchor="w", padx=20, pady=(10, 5))
        
        file_frame = ttk.Frame(file_section)
        file_frame.pack(padx=20, pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        self.excel_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, style='Modern.TEntry', 
                                    width=60, state="readonly")
        self.excel_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="📁 Browse", command=self.select_excel_file, 
                  style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        
        # Import button
        import_btn_frame = ttk.Frame(content_frame)
        import_btn_frame.pack(pady=20)
        ttk.Button(import_btn_frame, text="📊 Import Questions", command=self.import_from_excel, 
                  style="Success.TButton").pack()
        
        # Import log with modern styling  
        log_section = ttk.Frame(content_frame, style='Card.TFrame')
        log_section.pack(fill=tk.BOTH, expand=True, ipady=10)
        
        ttk.Label(log_section, text="📜 Import Log", style='Subheading.TLabel').pack(anchor="w", padx=20, pady=(15, 10))
        
        log_frame = ttk.Frame(log_section)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.import_log = tk.Text(log_frame, height=12, width=80, font=("Segoe UI", 10),
                                 bg='#FFFFFF', fg='#343A40', relief='flat', borderwidth=2,
                                 selectbackground='#2E86AB', selectforeground='white')
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.import_log.yview)
        self.import_log.configure(yscrollcommand=log_scroll.set)
        
        self.import_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def generate_test(self):
        """Generate a random test based on category settings"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter the test taker's name")
            return
        
        # Get category settings
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, percentage FROM category_settings WHERE percentage > 0")
        category_settings = dict(cursor.fetchall())
        
        if not category_settings:
            messagebox.showerror("Error", "No category settings configured")
            return
        
        # Calculate questions per category
        questions_per_category = {}
        total_questions = 50
        
        for category, percentage in category_settings.items():
            count = round((percentage / 100) * total_questions)
            questions_per_category[category] = count
        
        # Adjust to exactly 50 questions
        current_total = sum(questions_per_category.values())
        if current_total != total_questions:
            # Adjust the largest category
            largest_cat = max(questions_per_category.keys(), key=lambda k: questions_per_category[k])
            questions_per_category[largest_cat] += (total_questions - current_total)
        
        # Select random questions for each category
        selected_questions = []
        for category, count in questions_per_category.items():
            if count > 0:
                cursor.execute("SELECT question, answer, image_path, choice_a, choice_b, choice_c, choice_d FROM questions WHERE category = ? ORDER BY RANDOM() LIMIT ?", 
                             (category, count))
                category_questions = cursor.fetchall()
                selected_questions.extend([(q, a, category, img, ca, cb, cc, cd) for q, a, img, ca, cb, cc, cd in category_questions])
        
        if len(selected_questions) < total_questions:
            messagebox.showwarning("Warning", f"Only {len(selected_questions)} questions available. Need {total_questions}")
        
        # Shuffle all questions
        random.shuffle(selected_questions)
        
        # Generate test content with unique ID
        test_id = str(uuid.uuid4())[:8].upper()  # Short 8-character ID
        self.current_test = {
            'name': name,
            'date': datetime.now().strftime("%B %d, %Y"),
            'id': test_id,
            'questions': selected_questions
        }
        
        # Display in preview
        self.display_test_preview()
    
    def display_test_preview(self):
        """Display the generated test in the preview area"""
        self.test_preview.delete(1.0, tk.END)
        
        test_content = f"""
Journey-Level Proficiency Exam
Name: {self.current_test['name']}
Date: {self.current_test['date']}                                          Test ID: {self.current_test['id']}

Directions: For the following questions, fill the circle next to the option
that best answers the question or completes the statement. Show all work.

{"="*60}

"""
        
        for i, (question, answer, category, image_path, choice_a, choice_b, choice_c, choice_d) in enumerate(self.current_test['questions'], 1):
            if image_path:
                test_content += f"{i}. [IMAGE: {os.path.basename(image_path)}]\n"
            test_content += f"{i}. {question}\n\n"
            
            # Only show choices that have content
            if choice_a: test_content += f"   A) {choice_a}\n"
            if choice_b: test_content += f"   B) {choice_b}\n"
            if choice_c: test_content += f"   C) {choice_c}\n"
            if choice_d: test_content += f"   D) {choice_d}\n"
            test_content += "\n"
        
        self.test_preview.insert(1.0, test_content)
    
    def export_to_pdf(self):
        """Export the current test to PDF"""
        if not hasattr(self, 'current_test'):
            messagebox.showerror("Error", "No test generated yet")
            return
        
        filename = f"Test_{self.current_test['name']}_ID{self.current_test['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=filename
        )
        
        if filepath:
            try:
                self.create_pdf(filepath)
                messagebox.showinfo("Success", f"Test exported to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create PDF: {str(e)}")
    
    def export_answer_key(self):
        """Export the answer key to PDF"""
        if not hasattr(self, 'current_test'):
            messagebox.showerror("Error", "No test generated yet")
            return
        
        filename = f"AnswerKey_{self.current_test['name']}_ID{self.current_test['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=filename
        )
        
        if filepath:
            try:
                self.create_answer_key_pdf(filepath)
                messagebox.showinfo("Success", f"Answer key exported to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create answer key: {str(e)}")
    
    def create_answer_key_pdf(self, filepath):
        """Create PDF answer key - same format as test but with correct answers filled in"""
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "ANSWER KEY")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Name: {self.current_test['name']}")
        c.drawString(50, height - 100, f"Date: {self.current_test['date']}")
        
        # Answer Key ID prominently displayed
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, height - 80, f"Test ID: {self.current_test['id']}")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 120, "Instructions: Correct answers are filled in.")
        
        # Questions
        y_position = height - 160
        c.setFont("Helvetica", 11)
        
        for i, (question, answer, category, image_path, choice_a, choice_b, choice_c, choice_d) in enumerate(self.current_test['questions'], 1):
            # Calculate space needed for this question
            choices_count = sum([1 for c in [choice_a, choice_b, choice_c, choice_d] if c])
            image_height = 0
            
            # Check image size if present
            if image_path:
                full_image_path = self.get_image_full_path(image_path)
                if full_image_path and os.path.exists(full_image_path):
                    try:
                        img = Image.open(full_image_path)
                        img_width, img_height = img.size
                        
                        # Calculate scaled height
                        max_img_width = 400
                        max_img_height = 150
                        scale_w = max_img_width / img_width
                        scale_h = max_img_height / img_height
                        scale = min(scale_w, scale_h, 1.0)
                        image_height = int(img_height * scale)
                    except:
                        image_height = 20  # Space for error message
            
            # Calculate total space needed
            space_needed = 40 + image_height + (choices_count * 18) + 40
            
            # Check if we need a new page
            if y_position < space_needed:
                c.showPage()
                y_position = height - 50
            # Question text
            question_text = f"{i}. {question}"
            # Handle long questions by wrapping text
            if len(question_text) > 80:
                lines = []
                words = question_text.split()
                current_line = words[0] if words else ""
                
                for word in words[1:]:
                    if len(current_line + " " + word) <= 80:
                        current_line += " " + word
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                
                for line in lines:
                    c.drawString(50, y_position, line)
                    y_position -= 15
            else:
                c.drawString(50, y_position, question_text)
                y_position -= 15
            
            # Draw image if present (after question, before choices)
            if image_path:
                full_image_path = self.get_image_full_path(image_path)
                if full_image_path and os.path.exists(full_image_path):
                    try:
                        # Load and resize image
                        img = Image.open(full_image_path)
                        img_width, img_height = img.size
                        
                        # Scale image to fit
                        max_img_width = 400
                        max_img_height = 150
                        
                        scale_w = max_img_width / img_width
                        scale_h = max_img_height / img_height
                        scale = min(scale_w, scale_h, 1.0)  # Don't upscale
                        
                        new_width = int(img_width * scale)
                        new_height = int(img_height * scale)
                        
                        # Center the image
                        img_x = 50 + (400 - new_width) // 2
                        img_y = y_position - new_height - 10
                        
                        c.drawInlineImage(full_image_path, img_x, img_y, width=new_width, height=new_height)
                        y_position = img_y - 15  # Move down past image with spacing
                        
                    except Exception as e:
                        # If image fails to load, show error
                        print(f"Debug (Answer Key): Failed to load image {full_image_path}: {str(e)}")
                        c.drawString(50, y_position - 15, f"[IMAGE: {os.path.basename(image_path)} - Could not load]")
                        y_position -= 30
                else:
                    # Image path exists but file not found
                    print(f"Debug (Answer Key): Image path '{image_path}' not found")
                    c.drawString(50, y_position - 15, f"[IMAGE: {os.path.basename(image_path)} - File not found]")
                    y_position -= 30
            
            # Multiple choice options - only show choices with content
            y_position -= 10
            choices = []
            if choice_a: choices.append(('A', choice_a))
            if choice_b: choices.append(('B', choice_b))
            if choice_c: choices.append(('C', choice_c))
            if choice_d: choices.append(('D', choice_d))
            
            for choice_letter, choice_text in choices:
                # Add circle - filled if it's the correct answer, empty otherwise
                if choice_letter == answer:
                    c.circle(70, y_position + 5, 6, fill=1)  # Filled circle for correct answer
                else:
                    c.circle(70, y_position + 5, 6, fill=0)  # Empty circle
                c.drawString(85, y_position, f"{choice_letter}) {choice_text}")
                y_position -= 18
            
            y_position -= 25  # More space between questions
        
        c.save()
    
    def create_pdf(self, filepath):
        """Create PDF file of the test"""
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # Header - Journey-Level Proficiency Exam
        c.setFont("Helvetica-Bold", 16)
        title_text = "Journey-Level Proficiency Exam"
        title_width = c.stringWidth(title_text, "Helvetica-Bold", 16)
        c.drawString((width - title_width) / 2, height - 40, title_text)
        
        # Test ID centered below title
        c.setFont("Helvetica-Bold", 12)
        id_text = f"Test ID: {self.current_test['id']}"
        id_width = c.stringWidth(id_text, "Helvetica-Bold", 12)
        c.drawString((width - id_width) / 2, height - 60, id_text)
        
        # Name and Date line
        c.setFont("Helvetica", 12)
        name_date_line = f"Name: {self.current_test['name']}                                          Date: {self.current_test['date']}"
        c.drawString(50, height - 90, name_date_line)
        
        # Draw line under name/date
        c.line(50, height - 95, width - 50, height - 95)
        
        # Total Points
        c.setFont("Helvetica", 12)
        total_points_text = f"Total Points: {len(self.current_test['questions'])}"
        total_width = c.stringWidth(total_points_text, "Helvetica", 12)
        c.drawString((width - total_width) / 2, height - 115, total_points_text)
        
        # Directions
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 145, "Directions:")
        c.setFont("Helvetica", 11)
        c.drawString(120, height - 145, "For the following questions, fill the circle")
        c.drawString(50, height - 160, "next to the option that BEST answers the question or")
        c.drawString(50, height - 175, "completes the statement. Show all work.")
        
        # Setup two-column layout with moderate spacing between columns
        left_column_x = 50
        right_column_x = width / 2 + 14  # 14 points spacing between columns
        column_width = width / 2 - 64    # Adjusted for 14-point spacing
        
        questions_start_y = height - 210
        left_y = questions_start_y
        right_y = questions_start_y
        
        c.setFont("Helvetica", 11)  # Regular font but larger size for darker appearance
        
        # Process questions in two columns
        for i, (question, answer, category, image_path, choice_a, choice_b, choice_c, choice_d) in enumerate(self.current_test['questions'], 1):
            # Determine which column to use (odd numbers left, even numbers right)
            is_left_column = (i % 2 == 1)
            
            if is_left_column:
                current_x = left_column_x
                current_y = left_y
            else:
                current_x = right_column_x
                current_y = right_y
            
            # Calculate space needed for this question
            choices_count = sum([1 for c in [choice_a, choice_b, choice_c, choice_d] if c])
            image_height = 0
            
            # Check image size if present
            if image_path:
                full_image_path = self.get_image_full_path(image_path)
                if full_image_path and os.path.exists(full_image_path):
                    try:
                        img = Image.open(full_image_path)
                        img_width, img_height = img.size
                        
                        # Scale image to fit column width
                        max_img_width = column_width - 20
                        max_img_height = 100
                        scale_w = max_img_width / img_width
                        scale_h = max_img_height / img_height
                        scale = min(scale_w, scale_h, 1.0)
                        image_height = int(img_height * scale)
                    except:
                        image_height = 20
            
            # Calculate total space needed (accounting for wrapped answers and new spacing)
            estimated_choice_lines = 0
            for choice_text in [choice_a, choice_b, choice_c, choice_d]:
                if choice_text:
                    choice_length = len(f"a. {choice_text}")
                    lines_needed = max(1, (choice_length // 40) + 1)  # Adjusted for balanced columns
                    estimated_choice_lines += lines_needed
            
            space_needed = 45 + image_height + (estimated_choice_lines * 14) + 35  # Updated for new font and spacing
            
            # Check if we need a new page
            if current_y < space_needed:
                c.showPage()
                # Reset header for new page
                c.setFont("Helvetica-Bold", 16)
                title_text = "Journey-Level Proficiency Exam (continued)"
                title_width = c.stringWidth(title_text, "Helvetica-Bold", 16)
                c.drawString((width - title_width) / 2, height - 40, title_text)
                
                # Add Test ID to continuation page
                c.setFont("Helvetica-Bold", 12)
                id_text = f"Test ID: {self.current_test['id']}"
                id_width = c.stringWidth(id_text, "Helvetica-Bold", 12)
                c.drawString((width - id_width) / 2, height - 60, id_text)
                
                left_y = height - 90  # Adjusted for Test ID
                right_y = height - 90  # Adjusted for Test ID
                current_y = height - 90  # Adjusted for Test ID
                c.setFont("Helvetica", 11)  # Match updated font - regular but larger
            
            # Draw question text
            question_text = f"{i}. {question}"
            
            # Word wrap for column width (adjusted for balanced columns)
            max_chars = 48 if column_width < 270 else 52
            if len(question_text) > max_chars:
                words = question_text.split()
                lines = []
                current_line = ""
                
                for word in words:
                    if len(current_line + " " + word) <= max_chars:
                        current_line += (" " if current_line else "") + word
                    else:
                        lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                
                for line in lines:
                    c.drawString(current_x, current_y, line)
                    current_y -= 14  # Increased for better spacing with bold font
            else:
                c.drawString(current_x, current_y, question_text)
                current_y -= 14  # Increased for better spacing with bold font
            
            # Draw image if present
            if image_path:
                full_image_path = self.get_image_full_path(image_path)
                if full_image_path and os.path.exists(full_image_path):
                    try:
                        img = Image.open(full_image_path)
                        img_width, img_height = img.size
                        
                        # Scale image to fit column
                        max_img_width = column_width - 20
                        max_img_height = 100
                        scale_w = max_img_width / img_width
                        scale_h = max_img_height / img_height
                        scale = min(scale_w, scale_h, 1.0)
                        
                        new_width = int(img_width * scale)
                        new_height = int(img_height * scale)
                        
                        img_x = current_x + 10
                        img_y = current_y - new_height - 5
                        
                        c.drawImage(full_image_path, img_x, img_y, width=new_width, height=new_height)
                        current_y = img_y - 10
                        
                    except Exception as e:
                        c.drawString(current_x, current_y - 10, f"[Image error]")
                        current_y -= 15
            
            # Draw multiple choice options with word wrapping
            current_y -= 5
            choices = []
            if choice_a: choices.append(('a', choice_a))
            if choice_b: choices.append(('b', choice_b))
            if choice_c: choices.append(('c', choice_c))
            if choice_d: choices.append(('d', choice_d))
            
            for choice_letter, choice_text in choices:
                # Add circle for students to fill in
                c.circle(current_x + 5, current_y + 3, 3, fill=0)
                
                # Word wrap the choice text
                choice_with_letter = f"{choice_letter}. {choice_text}"
                max_choice_chars = 40  # Adjusted for balanced column width
                
                if len(choice_with_letter) > max_choice_chars:
                    # Split into words and wrap
                    words = choice_with_letter.split()
                    lines = []
                    current_line = ""
                    
                    for word in words:
                        if len(current_line + " " + word) <= max_choice_chars:
                            current_line += (" " if current_line else "") + word
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = word
                    
                    if current_line:
                        lines.append(current_line)
                    
                    # Draw first line with circle
                    c.drawString(current_x + 15, current_y, lines[0])
                    current_y -= 14  # Increased line spacing
                    
                    # Draw remaining lines indented
                    for line in lines[1:]:
                        c.drawString(current_x + 15, current_y, line)
                        current_y -= 14  # Increased line spacing
                else:
                    # Choice fits on one line
                    c.drawString(current_x + 15, current_y, choice_with_letter)
                    current_y -= 14  # Increased line spacing to match bold font
            
            current_y -= 35  # Further increased space between questions to match example
            
            # Update column positions
            if is_left_column:
                left_y = current_y
            else:
                right_y = current_y
        
        c.save()
    
    def clear_preview(self):
        """Clear the test preview"""
        self.test_preview.delete(1.0, tk.END)
    
    def select_image(self):
        """Select an image file for the question"""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select Image for Question",
            filetypes=filetypes
        )
        
        if filepath:
            # Copy image to images directory
            # Create unique filename
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(filename)
            counter = 1
            new_filepath = os.path.join(self.images_dir, filename)
            
            while os.path.exists(new_filepath):
                new_filename = f"{name}_{counter}{ext}"
                new_filepath = os.path.join(self.images_dir, new_filename)
                counter += 1
            
            try:
                shutil.copy2(filepath, new_filepath)
                # Store relative path from program directory
                relative_path = os.path.relpath(new_filepath, os.path.dirname(os.path.abspath(__file__)))
                self.image_path_var.set(relative_path)
                messagebox.showinfo("Success", f"Image copied to: {relative_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy image: {str(e)}")
    
    def clear_image(self):
        """Clear the selected image"""
        self.image_path_var.set("")

    def open_add_question_dialog(self):
        """Open a popup dialog to add a new question"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Question")
        dialog.geometry("800x600")
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Configure the dialog icon to match the main window
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'lightning_icon.ico')
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
        except:
            pass
        
        # Main content frame
        content_frame = ttk.Frame(dialog)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        ttk.Label(content_frame, text="➕ Add New Question", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(content_frame, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20), ipady=15)
        
        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        
        # Question text
        ttk.Label(form_frame, text="📝 Question:", style='Subheading.TLabel').grid(row=0, column=0, sticky="nw", pady=8, padx=(15, 10))
        question_entry = tk.Text(form_frame, height=4, width=60, font=("Segoe UI", 10),
                                bg='#FFFFFF', fg='#343A40', relief='solid', borderwidth=1)
        question_entry.grid(row=0, column=1, columnspan=3, pady=8, padx=(5, 15), sticky="ew")
        
        # Answer
        ttk.Label(form_frame, text="✅ Answer:", style='Subheading.TLabel').grid(row=1, column=0, sticky="w", pady=8, padx=(15, 10))
        answer_entry = ttk.Entry(form_frame, style='Modern.TEntry', width=15, justify='center')
        answer_entry.grid(row=1, column=1, pady=8, padx=5, sticky="w")
        ttk.Label(form_frame, text="(A, B, C, or D)", font=("Segoe UI", 9), foreground='#6C757D').grid(row=1, column=2, sticky="w", padx=5)
        
        # Multiple choice options
        ttk.Label(form_frame, text="🅰️ Choice A:", style='Subheading.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=(15, 10))
        choice_a_entry = ttk.Entry(form_frame, style='Modern.TEntry', width=50)
        choice_a_entry.grid(row=2, column=1, columnspan=3, pady=5, padx=(5, 15), sticky="ew")
        
        ttk.Label(form_frame, text="🅱️ Choice B:", style='Subheading.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=(15, 10))
        choice_b_entry = ttk.Entry(form_frame, style='Modern.TEntry', width=50)
        choice_b_entry.grid(row=3, column=1, columnspan=3, pady=5, padx=(5, 15), sticky="ew")
        
        ttk.Label(form_frame, text="🅲️ Choice C:", style='Subheading.TLabel').grid(row=4, column=0, sticky="w", pady=5, padx=(15, 10))
        choice_c_entry = ttk.Entry(form_frame, style='Modern.TEntry', width=50)
        choice_c_entry.grid(row=4, column=1, columnspan=3, pady=5, padx=(5, 15), sticky="ew")
        
        ttk.Label(form_frame, text="🅳️ Choice D:", style='Subheading.TLabel').grid(row=5, column=0, sticky="w", pady=5, padx=(15, 10))
        choice_d_entry = ttk.Entry(form_frame, style='Modern.TEntry', width=50)
        choice_d_entry.grid(row=5, column=1, columnspan=3, pady=5, padx=(5, 15), sticky="ew")
        
        # Category
        ttk.Label(form_frame, text="📁 Category:", style='Subheading.TLabel').grid(row=6, column=0, sticky="w", pady=8, padx=(15, 10))
        category_entry = ttk.Entry(form_frame, style='Modern.TEntry', width=30)
        category_entry.grid(row=6, column=1, pady=8, padx=5, sticky="w")
        
        # Image
        ttk.Label(form_frame, text="🖼️ Image:", style='Subheading.TLabel').grid(row=7, column=0, sticky="w", pady=8, padx=(15, 10))
        image_var = tk.StringVar()
        image_entry = ttk.Entry(form_frame, textvariable=image_var, style='Modern.TEntry', width=40, state="readonly")
        image_entry.grid(row=7, column=1, pady=8, padx=5, sticky="ew")
        
        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
            )
            if file_path:
                # Convert to relative path for images folder
                if not file_path.startswith('images/') and not file_path.startswith('images\\'):
                    filename = os.path.basename(file_path)
                    # Copy to images directory
                    dest_path = os.path.join(self.images_dir, filename)
                    try:
                        import shutil
                        shutil.copy2(file_path, dest_path)
                        image_var.set(f"images/{filename}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not copy image: {e}")
                else:
                    image_var.set(file_path)
        
        def clear_image():
            image_var.set("")
        
        ttk.Button(form_frame, text="📁 Browse", command=browse_image, style="Primary.TButton").grid(row=7, column=2, pady=8, padx=5)
        ttk.Button(form_frame, text="🗑️ Clear", command=clear_image, style="Warning.TButton").grid(row=7, column=3, pady=8, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=10)
        
        def add_question_from_dialog():
            question = question_entry.get(1.0, tk.END).strip()
            answer = answer_entry.get().strip().upper()
            category = category_entry.get().strip()
            choice_a = choice_a_entry.get().strip()
            choice_b = choice_b_entry.get().strip()
            choice_c = choice_c_entry.get().strip()
            choice_d = choice_d_entry.get().strip()
            image_path = image_var.get().strip() or None
            
            # Validate
            if not all([question, answer, category, choice_a, choice_b]):
                messagebox.showerror("Error", "Please fill in Question, Answer, Category, Choice A, and Choice B (minimum required)")
                return
            
            # Validate answer corresponds to a provided choice
            valid_answers = []
            if choice_a: valid_answers.append('A')
            if choice_b: valid_answers.append('B')
            if choice_c: valid_answers.append('C')
            if choice_d: valid_answers.append('D')
            
            if answer not in valid_answers:
                messagebox.showerror("Error", f"Answer '{answer}' must correspond to a provided choice")
                return
            
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO questions (question, answer, category, choice_a, choice_b, choice_c, choice_d, image_path, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                ''', (question, answer, category, choice_a, choice_b, choice_c, choice_d, image_path))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Question added successfully!")
                self.load_questions()  # Refresh the main list
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add question: {e}")
        
        ttk.Button(button_frame, text="➕ Add Question", command=add_question_from_dialog, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=dialog.destroy, style="Warning.TButton").pack(side=tk.LEFT, padx=5)

    def add_question(self):
        """Add a new question to the database"""
        question = self.question_entry.get(1.0, tk.END).strip()
        answer = self.answer_entry.get().strip().upper()
        category = self.category_entry.get().strip()
        choice_a = self.choice_a_entry.get().strip()
        choice_b = self.choice_b_entry.get().strip()
        choice_c = self.choice_c_entry.get().strip()
        choice_d = self.choice_d_entry.get().strip()
        image_path = self.image_path_var.get().strip() or None
        
        # Validate required fields - at least Choice A and B must be provided
        if not all([question, answer, category, choice_a, choice_b]):
            messagebox.showerror("Error", "Please fill in Question, Answer, Category, Choice A, and Choice B (minimum required)")
            return
        
        # Validate that the answer corresponds to a choice that has content
        valid_answers = []
        if choice_a: valid_answers.append('A')
        if choice_b: valid_answers.append('B')
        if choice_c: valid_answers.append('C')
        if choice_d: valid_answers.append('D')
        
        if answer not in valid_answers:
            messagebox.showerror("Error", f"Answer must be one of the choices you provided: {', '.join(valid_answers)}")
            return
        
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO questions (question, answer, category, choice_a, choice_b, choice_c, choice_d, image_path) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                      (question, answer, category, choice_a, choice_b, choice_c, choice_d, image_path))
        self.conn.commit()
        
        # Clear form
        self.question_entry.delete(1.0, tk.END)
        self.answer_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.choice_a_entry.delete(0, tk.END)
        self.choice_b_entry.delete(0, tk.END)
        self.choice_c_entry.delete(0, tk.END)
        self.choice_d_entry.delete(0, tk.END)
        self.image_path_var.set("")
        
        # Refresh questions list
        self.load_questions()
        messagebox.showinfo("Success", "Question added successfully")
    
    def load_questions(self):
        """Load all questions into the treeview"""
        # Clear existing items
        for item in self.questions_tree.get_children():
            self.questions_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, question, answer, category, created_date, image_path FROM questions ORDER BY id DESC")
        
        for row in cursor.fetchall():
            # Truncate long text for display
            question_text = row[1][:60] + "..." if len(row[1]) > 60 else row[1]
            answer_text = f"({row[2]})"  # Show answer as (A), (B), etc.
            image_status = "✅" if row[5] and row[5].strip() else "❌"  # Check if image exists
            
            self.questions_tree.insert('', tk.END, values=(
                row[0], question_text, answer_text, row[3], image_status, row[4][:10]  # Include image status in separate column
            ))
    
    def search_questions(self):
        """Search questions by keyword"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_questions()
            return
        
        # Clear existing items
        for item in self.questions_tree.get_children():
            self.questions_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, question, answer, category, created_date, image_path 
            FROM questions 
            WHERE question LIKE ? OR answer LIKE ? OR category LIKE ? 
               OR choice_a LIKE ? OR choice_b LIKE ? OR choice_c LIKE ? OR choice_d LIKE ?
            ORDER BY id DESC
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", 
              f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        for row in cursor.fetchall():
            question_text = row[1][:60] + "..." if len(row[1]) > 60 else row[1]
            answer_text = f"({row[2]})"  # Show answer as (A), (B), etc.
            image_status = "✅" if row[5] and row[5].strip() else "❌"  # Check if image exists
            
            self.questions_tree.insert('', tk.END, values=(
                row[0], question_text, answer_text, row[3], image_status, row[4][:10]  # Include image status in separate column
            ))
    
    def edit_question(self):
        """Edit selected question"""
        selected = self.questions_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a question to edit")
            return
        
        item = self.questions_tree.item(selected[0])
        question_id = item['values'][0]
        
        # Get full question data
        cursor = self.conn.cursor()
        cursor.execute("SELECT question, answer, category, image_path FROM questions WHERE id = ?", (question_id,))
        data = cursor.fetchone()
        
        if data:
            # Create edit window
            self.create_edit_window(question_id, data)
    
    def create_edit_window(self, question_id, data):
        """Create edit question window"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Question")
        edit_window.geometry("600x400")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Question field
        ttk.Label(edit_window, text="Question:").pack(anchor="w", padx=10, pady=(10,2))
        question_text = tk.Text(edit_window, height=4, width=70)
        question_text.pack(padx=10, pady=2)
        question_text.insert(1.0, data[0])
        
        # Answer field
        ttk.Label(edit_window, text="Answer:").pack(anchor="w", padx=10, pady=(10,2))
        answer_text = tk.Text(edit_window, height=3, width=70)
        answer_text.pack(padx=10, pady=2)
        answer_text.insert(1.0, data[1])
        
        # Category field
        ttk.Label(edit_window, text="Category:").pack(anchor="w", padx=10, pady=(10,2))
        category_entry = ttk.Entry(edit_window, width=30)
        category_entry.pack(anchor="w", padx=10, pady=2)
        category_entry.insert(0, data[2])
        
        # Image field
        ttk.Label(edit_window, text="Image (optional):").pack(anchor="w", padx=10, pady=(10,2))
        image_frame = ttk.Frame(edit_window)
        image_frame.pack(fill=tk.X, padx=10, pady=2)
        
        image_path_var = tk.StringVar(value=data[3] or "")
        image_entry = ttk.Entry(image_frame, textvariable=image_path_var, width=40, state="readonly")
        image_entry.pack(side=tk.LEFT, padx=(0,5))
        
        def select_edit_image():
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
            filepath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
            if filepath:
                # Copy to images directory with unique filename
                filename = os.path.basename(filepath)
                name, ext = os.path.splitext(filename)
                counter = 1
                new_filepath = os.path.join(self.images_dir, filename)
                
                while os.path.exists(new_filepath):
                    new_filename = f"{name}_{counter}{ext}"
                    new_filepath = os.path.join(self.images_dir, new_filename)
                    counter += 1
                
                try:
                    if filepath != new_filepath:
                        shutil.copy2(filepath, new_filepath)
                    # Store relative path
                    relative_path = os.path.relpath(new_filepath, os.path.dirname(os.path.abspath(__file__)))
                    image_path_var.set(relative_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy image: {str(e)}")
        
        def clear_edit_image():
            image_path_var.set("")
        
        ttk.Button(image_frame, text="Browse", command=select_edit_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(image_frame, text="Clear", command=clear_edit_image).pack(side=tk.LEFT, padx=2)
        
        # Buttons
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(pady=20)
        
        def save_changes():
            new_question = question_text.get(1.0, tk.END).strip()
            new_answer = answer_text.get(1.0, tk.END).strip()
            new_category = category_entry.get().strip()
            new_image_path = image_path_var.get().strip() or None
            
            if not all([new_question, new_answer, new_category]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE questions 
                SET question = ?, answer = ?, category = ?, image_path = ? 
                WHERE id = ?
            """, (new_question, new_answer, new_category, new_image_path, question_id))
            self.conn.commit()
            
            edit_window.destroy()
            self.load_questions()
            messagebox.showinfo("Success", "Question updated successfully")
        
        ttk.Button(button_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_question(self):
        """Delete selected question"""
        selected = self.questions_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a question to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?"):
            item = self.questions_tree.item(selected[0])
            question_id = item['values'][0]
            
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            self.conn.commit()
            
            self.load_questions()
            messagebox.showinfo("Success", "Question deleted successfully")
    
    def load_category_settings(self):
        """Load category settings from database"""
        # Clear existing widgets
        for widget in self.settings_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        
        # Get unique categories from questions
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM questions ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        
        # Get existing settings
        cursor.execute("SELECT category, percentage FROM category_settings")
        settings = dict(cursor.fetchall())
        
        self.category_vars = {}
        
        if categories:
            for i, category in enumerate(categories):
                frame = ttk.Frame(self.settings_frame)
                frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(frame, text=f"{category}:", width=20).pack(side=tk.LEFT, padx=5)
                
                var = tk.IntVar(value=settings.get(category, 0))
                self.category_vars[category] = var
                
                spinbox = tk.Spinbox(frame, from_=0, to=100, width=10, textvariable=var)
                spinbox.pack(side=tk.LEFT, padx=5)
                
                ttk.Label(frame, text="%").pack(side=tk.LEFT, padx=2)
        else:
            ttk.Label(self.settings_frame, text="No categories found. Add some questions first.").pack(pady=20)
    
    def save_category_settings(self):
        """Save category percentage settings"""
        if not hasattr(self, 'category_vars'):
            return
        
        # Check total percentage
        total = sum(var.get() for var in self.category_vars.values())
        if total != 100:
            if not messagebox.askyesno("Warning", f"Total percentage is {total}%, not 100%. Save anyway?"):
                return
        
        cursor = self.conn.cursor()
        
        # Clear existing settings
        cursor.execute("DELETE FROM category_settings")
        
        # Insert new settings
        for category, var in self.category_vars.items():
            percentage = var.get()
            if percentage > 0:
                cursor.execute("INSERT INTO category_settings (category, percentage) VALUES (?, ?)",
                             (category, percentage))
        
        self.conn.commit()
        messagebox.showinfo("Success", "Category settings saved")
    
    def reset_category_settings(self):
        """Reset all category percentages to 0"""
        if hasattr(self, 'category_vars'):
            for var in self.category_vars.values():
                var.set(0)
    
    def select_excel_file(self):
        """Select Excel file for import"""
        filepath = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if filepath:
            self.file_path_var.set(filepath)
    
    def import_from_excel(self):
        """Import questions from Excel file"""
        filepath = self.file_path_var.get()
        if not filepath:
            messagebox.showerror("Error", "Please select an Excel file")
            return
        
        try:
            # Clear log
            self.import_log.delete(1.0, tk.END)
            self.import_log.insert(tk.END, f"Starting import from: {os.path.basename(filepath)}\n")
            
            # Read Excel file
            df = pd.read_excel(filepath)
            
            # Check required columns
            required_cols = ['Question', 'Answer', 'Category', 'ChoiceA', 'ChoiceB', 'ChoiceC', 'ChoiceD']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                error_msg = f"Missing required columns: {', '.join(missing_cols)}\nFound columns: {', '.join(df.columns)}"
                messagebox.showerror("Error", error_msg)
                self.import_log.insert(tk.END, f"ERROR: {error_msg}\n")
                return
            
            # Add ImagePath column if it doesn't exist
            if 'ImagePath' not in df.columns:
                df['ImagePath'] = None
            
            # Import questions
            cursor = self.conn.cursor()
            imported_count = 0
            skipped_count = 0
            
            for index, row in df.iterrows():
                question = str(row['Question']).strip()
                answer = str(row['Answer']).strip().upper()
                category = str(row['Category']).strip()
                choice_a = str(row['ChoiceA']).strip()
                choice_b = str(row['ChoiceB']).strip()
                choice_c = str(row['ChoiceC']).strip()
                choice_d = str(row['ChoiceD']).strip()
                image_path = str(row['ImagePath']).strip() if pd.notna(row['ImagePath']) else None
                
                # Validate required fields - at least Choice A and B must be provided
                required_fields = [question, answer, category, choice_a, choice_b]
                if not all(required_fields) or any(val == 'nan' for val in required_fields):
                    skipped_count += 1
                    self.import_log.insert(tk.END, f"Row {index + 2}: Skipped (missing required data - need at least Question, Answer, Category, Choice A, and Choice B)\n")
                    continue
                
                # Clean up empty choices (convert 'nan' strings to empty)
                if choice_c == 'nan': choice_c = ''
                if choice_d == 'nan': choice_d = ''
                
                # Validate that answer corresponds to a provided choice
                valid_answers = []
                if choice_a and choice_a != 'nan': valid_answers.append('A')
                if choice_b and choice_b != 'nan': valid_answers.append('B')
                if choice_c and choice_c != 'nan': valid_answers.append('C')
                if choice_d and choice_d != 'nan': valid_answers.append('D')
                
                if answer not in valid_answers:
                    skipped_count += 1
                    self.import_log.insert(tk.END, f"Row {index + 2}: Skipped (answer '{answer}' doesn't match any provided choice)\n")
                    continue
                
                try:
                    cursor.execute("""INSERT INTO questions (question, answer, category, choice_a, choice_b, choice_c, choice_d, image_path) 
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (question, answer, category, choice_a, choice_b, choice_c, choice_d, image_path))
                    imported_count += 1
                    img_note = " [with image]" if image_path else ""
                    self.import_log.insert(tk.END, f"Row {index + 2}: Imported - {category} (Answer: {answer}){img_note}\n")
                except Exception as e:
                    skipped_count += 1
                    self.import_log.insert(tk.END, f"Row {index + 2}: Error - {str(e)}\n")
            
            self.conn.commit()
            
            # Summary
            self.import_log.insert(tk.END, f"\nImport Complete:\n")
            self.import_log.insert(tk.END, f"Successfully imported: {imported_count} questions\n")
            self.import_log.insert(tk.END, f"Skipped: {skipped_count} rows\n")
            
            # Refresh questions and categories
            self.load_questions()
            self.load_category_settings()
            
            messagebox.showinfo("Import Complete", f"Imported {imported_count} questions successfully")
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Error reading Excel file: {str(e)}")
            self.import_log.insert(tk.END, f"ERROR: {str(e)}\n")
    
    def wipe_database(self):
        """Wipe all data from database with password protection"""
        # Password dialog
        password_window = tk.Toplevel(self.root)
        password_window.title("Database Wipe - Password Required")
        password_window.geometry("400x200")
        password_window.resizable(False, False)
        password_window.grab_set()  # Make it modal
        
        # Center the window
        password_window.update_idletasks()
        x = (password_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (password_window.winfo_screenheight() // 2) - (200 // 2)
        password_window.geometry(f"400x200+{x}+{y}")
        
        ttk.Label(password_window, text="⚠️ DATABASE WIPE WARNING ⚠️", 
                 font=("Arial", 14, "bold"), foreground="red").pack(pady=10)
        
        ttk.Label(password_window, text="This will permanently delete ALL questions and data!\nThis action CANNOT be undone!", 
                 font=("Arial", 10)).pack(pady=10)
        
        ttk.Label(password_window, text="Enter password to proceed:").pack(pady=5)
        
        password_var = tk.StringVar()
        password_entry = ttk.Entry(password_window, textvariable=password_var, show="*", width=20, font=("Arial", 12))
        password_entry.pack(pady=5)
        password_entry.focus()
        
        button_frame = ttk.Frame(password_window)
        button_frame.pack(pady=20)
        
        def confirm_wipe():
            if password_var.get() == "ibew379":
                password_window.destroy()
                
                # Final confirmation
                final_confirm = messagebox.askyesno(
                    "FINAL CONFIRMATION",
                    "Are you absolutely sure you want to delete ALL questions and data?\n\n" +
                    "This will:\n" +
                    "• Delete all questions from database\n" +
                    "• Clear all category settings\n" +
                    "• This action CANNOT be undone!\n\n" +
                    "Click YES to proceed with deletion."
                )
                
                if final_confirm:
                    try:
                        cursor = self.conn.cursor()
                        
                        # Delete all questions
                        cursor.execute("DELETE FROM questions")
                        
                        # Delete all category settings
                        cursor.execute("DELETE FROM category_settings")
                        
                        # Reset the AUTOINCREMENT counter to start IDs back at 1
                        cursor.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
                        
                        self.conn.commit()
                        
                        # Clear the questions display
                        if hasattr(self, 'questions_tree'):
                            for item in self.questions_tree.get_children():
                                self.questions_tree.delete(item)
                        
                        # Clear category settings display
                        self.load_category_settings()
                        
                        messagebox.showinfo("Database Wiped", 
                                          "Database has been completely wiped clean.\n" +
                                          "All questions and settings have been deleted.")
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to wipe database: {str(e)}")
            else:
                messagebox.showerror("Invalid Password", "Incorrect password. Database wipe cancelled.")
                password_window.destroy()
        
        def cancel_wipe():
            password_window.destroy()
        
        # Enter key binding
        password_entry.bind('<Return>', lambda e: confirm_wipe())
        
        ttk.Button(button_frame, text="WIPE DATABASE", command=confirm_wipe, style="Danger.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=cancel_wipe).pack(side=tk.LEFT, padx=10)
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = TestGeneratorApp(root)
    
    # Configure styles
    style = ttk.Style()
    style.configure("Generate.TButton", font=("Arial", 12, "bold"))
    
    root.mainloop()

if __name__ == "__main__":
    main()