"""
Runtime hook for tkinter to ensure proper theme and styling initialization
"""
import os
import sys

# Set TCL/TK environment variables for PyInstaller
if hasattr(sys, '_MEIPASS'):
    # Running as PyInstaller bundle
    os.environ['TCL_LIBRARY'] = os.path.join(sys._MEIPASS, 'tcl')
    os.environ['TK_LIBRARY'] = os.path.join(sys._MEIPASS, 'tk')
    
    # Ensure tkinter can find its resources
    tcl_dir = os.path.join(sys._MEIPASS, 'tcl')
    tk_dir = os.path.join(sys._MEIPASS, 'tk')
    
    if os.path.exists(tcl_dir):
        os.environ['TCL_LIBRARY'] = tcl_dir
    if os.path.exists(tk_dir):
        os.environ['TK_LIBRARY'] = tk_dir
