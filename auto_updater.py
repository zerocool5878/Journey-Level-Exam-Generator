#!/usr/bin/env python3
"""
Auto-updater for Journey-Level Exam Generator
Checks GitHub releases for updates and handles automatic updating
"""

import os
import sys
import json
import requests
import subprocess
import shutil
import zipfile
import tempfile
from pathlib import Path
from tkinter import messagebox, Tk
import tkinter as tk
from threading import Thread
import time

class AutoUpdater:
    def __init__(self):
        self.current_version = "1.0.1"
        self.repo_owner = "zerocool5878"
        self.repo_name = "Journey-Level-Exam-Generator"
        self.github_api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.exe_name = "Journey-Level-Exam-Generator.exe"
        
    def get_current_version(self):
        """Get the current version of the application"""
        return self.current_version
    
    def check_for_updates(self, silent=False):
        """Check GitHub for newer releases"""
        try:
            response = requests.get(self.github_api_url, timeout=10)
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name'].lstrip('v')
                
                if self.is_newer_version(latest_version, self.current_version):
                    if not silent:
                        self.show_update_dialog(release_data)
                    return True, release_data
                else:
                    if not silent:
                        messagebox.showinfo("No Updates", 
                                          f"You're running the latest version ({self.current_version})")
                    return False, None
            else:
                if not silent:
                    messagebox.showwarning("Update Check Failed", 
                                         "Could not check for updates. Please try again later.")
                return False, None
                
        except requests.exceptions.RequestException as e:
            if not silent:
                messagebox.showwarning("Update Check Failed", 
                                     f"Network error: {str(e)}")
            return False, None
        except Exception as e:
            if not silent:
                messagebox.showerror("Update Check Failed", 
                                   f"Error checking for updates: {str(e)}")
            return False, None
    
    def is_newer_version(self, latest, current):
        """Compare version strings to see if latest is newer than current"""
        def version_tuple(v):
            return tuple(map(int, (v.split("."))))
        return version_tuple(latest) > version_tuple(current)
    
    def show_update_dialog(self, release_data):
        """Show update dialog with release information"""
        latest_version = release_data['tag_name'].lstrip('v')
        release_notes = release_data.get('body', 'No release notes available.')
        
        # Create update dialog
        dialog = tk.Toplevel()
        dialog.title("Update Available")
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        dialog.transient()
        dialog.grab_set()
        
        # Configure icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'lightning_icon.ico')
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
        except:
            pass
        
        # Main frame
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text=f"Update Available: v{latest_version}", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Current version info
        current_label = tk.Label(main_frame, 
                               text=f"Current version: v{self.current_version}")
        current_label.pack()
        
        # Release notes
        notes_label = tk.Label(main_frame, text="Release Notes:", font=("Arial", 12, "bold"))
        notes_label.pack(pady=(20, 5), anchor=tk.W)
        
        # Scrollable text widget for release notes
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(tk.END, release_notes)
        text_widget.config(state=tk.DISABLED)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Progress bar frame (initially hidden)
        progress_frame = tk.Frame(main_frame)
        progress_label = tk.Label(progress_frame, text="Downloading update...")
        progress_label.pack()
        
        def update_now():
            # Disable buttons
            update_btn.config(state=tk.DISABLED)
            skip_btn.config(state=tk.DISABLED)
            
            # Show progress
            progress_frame.pack(fill=tk.X, pady=(10, 0))
            
            # Start download in separate thread
            Thread(target=lambda: self.download_and_install_update(release_data, dialog), 
                  daemon=True).start()
        
        def skip_update():
            dialog.destroy()
        
        update_btn = tk.Button(button_frame, text="Update Now", command=update_now,
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        update_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        skip_btn = tk.Button(button_frame, text="Skip This Version", command=skip_update)
        skip_btn.pack(side=tk.RIGHT)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
    
    def download_and_install_update(self, release_data, dialog):
        """Download and install the update"""
        try:
            # Find the executable in release assets
            exe_asset = None
            for asset in release_data.get('assets', []):
                if asset['name'].endswith('.exe'):
                    exe_asset = asset
                    break
            
            if not exe_asset:
                messagebox.showerror("Update Failed", 
                                   "Could not find executable in release assets.")
                dialog.destroy()
                return
            
            # Download the new executable
            download_url = exe_asset['browser_download_url']
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.exe') as temp_file:
                temp_path = temp_file.name
            
            # Download with progress
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            # Get current executable path
            current_exe = sys.executable if getattr(sys, 'frozen', False) else __file__
            current_dir = os.path.dirname(os.path.abspath(current_exe))
            new_exe_path = os.path.join(current_dir, self.exe_name)
            backup_path = new_exe_path + ".backup"
            
            # Create backup of current version
            if os.path.exists(new_exe_path):
                shutil.copy2(new_exe_path, backup_path)
            
            # Replace with new version
            shutil.move(temp_path, new_exe_path)
            
            # Close current application and start new one
            dialog.destroy()
            messagebox.showinfo("Update Complete", 
                              "Update installed successfully! The application will now restart.")
            
            # Start new version and exit current
            subprocess.Popen([new_exe_path])
            sys.exit(0)
            
        except Exception as e:
            # Restore backup if something went wrong
            if 'backup_path' in locals() and os.path.exists(backup_path):
                if 'new_exe_path' in locals() and os.path.exists(new_exe_path):
                    os.remove(new_exe_path)
                shutil.move(backup_path, new_exe_path)
            
            messagebox.showerror("Update Failed", 
                               f"Error installing update: {str(e)}")
            dialog.destroy()
    
    def check_for_updates_on_startup(self):
        """Check for updates silently on startup"""
        Thread(target=lambda: self.check_for_updates(silent=True), daemon=True).start()

def manual_check_for_updates():
    """Function to be called from main application for manual update check"""
    updater = AutoUpdater()
    updater.check_for_updates(silent=False)

def startup_update_check():
    """Function to be called on application startup"""
    updater = AutoUpdater()
    updater.check_for_updates_on_startup()

if __name__ == "__main__":
    # Test the updater
    root = Tk()
    root.withdraw()  # Hide main window
    
    updater = AutoUpdater()
    updater.check_for_updates(silent=False)
    
    root.mainloop()