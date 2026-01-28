"""
Create Windows Startup Shortcut for Binary Pomodoro Widget
Run this script to add the widget to Windows startup.
"""

import os
import sys


def create_startup_shortcut():
    """Create a shortcut in the Windows Startup folder."""
    try:
        import win32com.client
    except ImportError:
        print("Error: pywin32 is required. Install with: pip install pywin32")
        print("After installing, you may need to run: python Scripts/pywin32_postinstall.py -install")
        return False
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    widget_script = os.path.join(script_dir, "pomodoro_widget.py")
    
    # Get Windows Startup folder
    startup_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )
    
    shortcut_path = os.path.join(startup_folder, "BinaryPomodoro.lnk")
    
    # Get Python executable
    python_exe = sys.executable
    
    # For pythonw.exe (no console window)
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    if os.path.exists(pythonw_exe):
        python_exe = pythonw_exe
    
    try:
        # Create shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{widget_script}"'
        shortcut.WorkingDirectory = script_dir
        shortcut.Description = "Binary Tree Pomodoro Widget"
        shortcut.save()
        
        print(f"✓ Startup shortcut created successfully!")
        print(f"  Location: {shortcut_path}")
        print(f"  The widget will now start automatically when Windows starts.")
        return True
        
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        return False


def remove_startup_shortcut():
    """Remove the startup shortcut."""
    startup_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )
    shortcut_path = os.path.join(startup_folder, "BinaryPomodoro.lnk")
    
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print(f"✓ Startup shortcut removed.")
        print(f"  The widget will no longer start automatically.")
        return True
    else:
        print("No startup shortcut found.")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Binary Pomodoro startup shortcut")
    parser.add_argument(
        "--remove", "-r",
        action="store_true",
        help="Remove the startup shortcut instead of creating it"
    )
    
    args = parser.parse_args()
    
    if args.remove:
        remove_startup_shortcut()
    else:
        create_startup_shortcut()
