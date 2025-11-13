#!/usr/bin/env python3
"""
Test script to demonstrate the auto-updater functionality
Shows the update checking and installation process
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_updater import AutoUpdater
from version import VERSION

def show_demo_window():
    """Create a demo window showing the auto-updater in action"""
    root = tk.Tk()
    root.title("Auto-Updater Demonstration")
    root.geometry("700x600")
    
    # Main frame
    main_frame = tk.Frame(root, padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, 
                          text="Journey-Level Exam Generator\nAuto-Updater Demo",
                          font=("Arial", 18, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Current version info
    version_frame = tk.Frame(main_frame, relief=tk.RIDGE, borderwidth=2, bg="#e8f4f8", padx=20, pady=15)
    version_frame.pack(fill=tk.X, pady=(0, 30))
    
    current_version_label = tk.Label(version_frame, 
                                    text=f"Current Version: {VERSION}",
                                    font=("Arial", 14, "bold"),
                                    bg="#e8f4f8")
    current_version_label.pack()
    
    repo_label = tk.Label(version_frame,
                         text="Repository: zerocool5878/Journey-Level-Exam-Generator",
                         font=("Arial", 10),
                         bg="#e8f4f8")
    repo_label.pack()
    
    # Info text
    info_frame = tk.Frame(main_frame)
    info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    info_text = tk.Text(info_frame, wrap=tk.WORD, height=15, font=("Arial", 10))
    info_text.pack(fill=tk.BOTH, expand=True)
    
    info_content = f"""How the Auto-Updater Works:

1. CHECK FOR UPDATES
   • Connects to GitHub API: https://api.github.com/repos/zerocool5878/Journey-Level-Exam-Generator/releases/latest
   • Compares latest release version with current version ({VERSION})
   • Happens automatically 5 seconds after app starts (non-blocking)
   • Can also be triggered manually from Help menu

2. UPDATE NOTIFICATION
   • IF newer version found:
     - Shows dialog with release notes
     - "Update Now" or "Skip This Version" buttons
   • IF same version or older:
     - No dialog shown (silent check)
     - Manual check shows "You're up to date" message

3. DOWNLOAD & INSTALL (when user clicks "Update Now"):
   • Downloads new .exe from GitHub release assets
   • Creates backup of current version (.backup file)
   • Replaces old executable with new version
   • Launches new version: subprocess.Popen([new_exe_path])
   • Exits current process: sys.exit(0)

4. AUTOMATIC RESTART
   • New version starts immediately
   • Old process exits cleanly
   • User continues working seamlessly

5. ERROR HANDLING
   • If download fails: restores backup
   • If offline: silent check fails gracefully (no popup)
   • If no .exe asset found: shows error message

Current Status: The app is running version {VERSION}
Next GitHub release will be detected automatically!
"""
    
    info_text.insert(tk.END, info_content)
    info_text.config(state=tk.DISABLED)
    
    # Button frame
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))
    
    # Status label
    status_label = tk.Label(button_frame, text="", font=("Arial", 9), fg="green")
    status_label.pack(pady=(0, 10))
    
    def check_now():
        """Check for updates manually"""
        status_label.config(text="Checking for updates...", fg="blue")
        button_frame.update()
        
        updater = AutoUpdater()
        has_update, release_data = updater.check_for_updates(silent=False)
        
        if has_update:
            status_label.config(text="✓ Update available! Dialog shown.", fg="green")
        else:
            status_label.config(text="✓ You're running the latest version.", fg="green")
    
    def simulate_startup_check():
        """Simulate the startup check behavior"""
        status_label.config(text="Simulating startup check (5 second delay)...", fg="blue")
        button_frame.update()
        
        import time
        import threading
        
        def delayed_check():
            time.sleep(5)
            updater = AutoUpdater()
            has_update, release_data = updater.check_for_updates(silent=True)
            
            if has_update:
                status_label.config(text="✓ Update found on startup! Dialog shown.", fg="green")
                updater.show_update_dialog(release_data)
            else:
                status_label.config(text="✓ Startup check complete - no update needed.", fg="green")
        
        threading.Thread(target=delayed_check, daemon=True).start()
    
    # Buttons
    check_btn = tk.Button(button_frame, 
                         text="Check for Updates Now",
                         command=check_now,
                         bg="#2E86AB", fg="white",
                         font=("Arial", 11, "bold"),
                         padx=20, pady=10)
    check_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    simulate_btn = tk.Button(button_frame,
                            text="Simulate Startup Check",
                            command=simulate_startup_check,
                            bg="#2E8B57", fg="white",
                            font=("Arial", 11, "bold"),
                            padx=20, pady=10)
    simulate_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    close_btn = tk.Button(button_frame,
                         text="Close",
                         command=root.destroy,
                         bg="#DC3545", fg="white",
                         font=("Arial", 11, "bold"),
                         padx=20, pady=10)
    close_btn.pack(side=tk.RIGHT)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    show_demo_window()
