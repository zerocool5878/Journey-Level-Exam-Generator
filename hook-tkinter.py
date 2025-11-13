"""
Runtime hook for tkinter to ensure proper theme and styling initialization
"""
import os
import sys

# Set TCL/TK environment variables for PyInstaller (both onefile and onedir modes)
if getattr(sys, 'frozen', False):
    # Determine base path based on PyInstaller mode
    if hasattr(sys, '_MEIPASS'):
        # onefile mode - temp extraction folder
        base_path = sys._MEIPASS
    else:
        # onedir mode - _internal subfolder next to executable
        base_path = os.path.join(os.path.dirname(sys.executable), '_internal')
        # Set _PYI_APPLICATION_HOME_DIR for onedir mode (required by some libraries)
        os.environ['_PYI_APPLICATION_HOME_DIR'] = os.path.dirname(sys.executable)
    
    # Set TCL/TK library paths
    tcl_dir = os.path.join(base_path, 'tcl')
    tk_dir = os.path.join(base_path, 'tk')
    
    if os.path.exists(tcl_dir):
        os.environ['TCL_LIBRARY'] = tcl_dir
    if os.path.exists(tk_dir):
        os.environ['TK_LIBRARY'] = tk_dir
