# 🎄 Binary Tree Pomodoro Widget

**A unique productivity companion that grows with your focus.**

The **Binary Tree Pomodoro Widget** is a custom visual timer for Windows that reimagines the Pomodoro Technique. Instead of a stressing countdown, watch a Christmas tree grow in real-time. The bottom leaves display the remaining time in **8-bit binary format**, combining a retro hacker aesthetic with a calming natural visualization. Perfect for developers, students, and anyone who wants to stay focused with style.

![Widget Preview](widget_preview.png)

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation Guide](#installation-guide)
4. [Usage](#usage)
5. [Project Architecture](#project-architecture)
6. [Libraries & Technologies](#libraries--technologies)
7. [Concepts & Ideation](#concepts--ideation)
8. [File Structure](#file-structure)
9. [Customization](#customization)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Binary Tree Pomodoro Widget is a productivity timer that combines the Pomodoro Technique with a unique visual representation. Instead of a standard countdown, this widget displays a growing Christmas tree where the bottom row of leaves shows the timer duration in **8-bit binary format** (MSB to LSB, left to right).

### Why Binary?

The binary representation serves as a subtle reminder of the computational nature of time management while providing an aesthetically pleasing, "retro hacker" visual style.

---

## Features

| Feature | Description |
|---------|-------------|
| **Tall Christmas Tree** | Taller-than-wide tree shape (8 rows) |
| **Uniform Leaf Size** | All leaves are the same size for clean appearance |
| **Binary Display** | Bottom leaves show timer in 8-bit binary |
| **Growth Animation** | Tree grows progressively as timer runs |
| **Always-on-Top** | Widget stays visible over all windows |
| **Draggable Window** | Move the widget anywhere on screen |
| **Frameless Design** | Clean, modern look without title bar |
| **Windows Startup** | Optional auto-start with Windows |
| **Retro Green Theme** | Matrix-style green on dark background |

---

## Installation Guide

### Prerequisites

- **Python 3.8+** (Download from [python.org](https://www.python.org/downloads/))
- **Windows 10/11** (for startup integration)

### Step 1: Clone or Download

```bash
# If using git:
git clone <repository-url>
cd pt

# Or simply download and extract the files to a folder
```

### Step 2: Verify Python Installation

```powershell
python --version
# Should output: Python 3.x.x
```

### Step 3: Install Dependencies (Optional)

The core widget uses only Tkinter (included with Python). For Windows startup integration:

```powershell
pip install -r requirements.txt
# Or manually:
pip install pywin32
```

### Step 4: Run the Widget

```powershell
cd "c:\Users\abina\Desktop\Python projects\pt"
python pomodoro_widget.py
```

### Step 5: Add to Windows Startup (Optional)

```powershell
python create_startup_shortcut.py
```

To remove from startup:
```powershell
python create_startup_shortcut.py --remove
```

---

## Usage

### Controls

| Control | Action |
|---------|--------|
| **▶ Button** | Start/Pause timer |
| **+ Button** | Increase time by 1 minute |
| **− Button** | Decrease time by 1 minute |
| **✕ Button** | Close widget |
| **Drag** | Click and drag anywhere to move |

### Timer Range

- **Minimum**: 1 minute
- **Maximum**: 60 minutes
- **Default**: 5 minutes

### Binary Display Example

| Timer | Binary (8-bit) | Bottom Row Display |
|-------|----------------|-------------------|
| 5 min | `00000101` | 0 0 0 0 0 1 0 1 |
| 10 min | `00001010` | 0 0 0 0 1 0 1 0 |
| 25 min | `00011001` | 0 0 0 1 1 0 0 1 |
| 45 min | `00101101` | 0 0 1 0 1 1 0 1 |

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PomodoroWidget                       │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │  PomodoroTimer  │  │    BinaryChristmasTree      │  │
│  │                 │  │                             │  │
│  │  - minutes      │  │  - leaf_positions[]        │  │
│  │  - remaining    │  │  - draw_tree()             │  │
│  │  - is_running   │  │  - draw_leaf()             │  │
│  │  - tick()       │  │  - binary conversion       │  │
│  │  - progress%    │  │                             │  │
│  └─────────────────┘  └─────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                 Tkinter Canvas                   │   │
│  │   - Tree visualization                          │   │
│  │   - Animation rendering                         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Class Descriptions

#### `BinaryChristmasTree`
Handles the visual representation of the binary tree:
- Calculates leaf positions in Christmas tree formation
- Renders leaves with binary digits
- Animates tree growth based on timer progress
- Bottom row displays actual binary value; upper rows show zeros

#### `PomodoroTimer`
Manages timer state and logic:
- Tracks total and remaining seconds
- Handles start, pause, and reset operations
- Calculates progress percentage for tree growth
- Provides formatted time display (MM:SS)

#### `PomodoroWidget`
Main application window:
- Creates frameless, always-on-top window
- Assembles UI components (buttons, canvas, labels)
- Handles user interactions (drag, click)
- Runs main update loop (1 second interval)

---

## Libraries & Technologies

### Tkinter (Built-in)

**What it is**: Python's standard GUI (Graphical User Interface) library, included with Python installation.

**Why we use it**:
- **Lightweight**: Minimal memory footprint, perfect for an always-on widget
- **Canvas widget**: Powerful drawing capabilities for custom shapes and animations
- **Cross-platform**: Works on Windows, macOS, and Linux
- **No installation**: Comes bundled with Python

**Key Tkinter features used**:
```python
# Frameless window
root.overrideredirect(True)

# Always on top
root.attributes("-topmost", True)

# Transparency
root.attributes("-alpha", 0.95)

# Canvas for custom drawing
canvas.create_oval(...)      # Leaf shapes
canvas.create_text(...)      # Binary digits
canvas.create_polygon(...)   # Button icons
```

### pywin32 (Optional)

**What it is**: Python extensions for Windows, providing access to Windows API.

**Why we use it**: Creating Windows startup shortcuts via COM automation.

```python
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(path)
```

### PyInstaller (Optional)

**What it is**: Converts Python scripts into standalone executables.

**Why we might use it**: Distribute the widget as a single .exe file without requiring Python installation.

```powershell
pyinstaller --onefile --windowed pomodoro_widget.py
```

---

## Concepts & Ideation

### The Pomodoro Technique

The Pomodoro Technique is a time management method developed by Francesco Cirillo:

1. **Choose a task** to work on
2. **Set a timer** (traditionally 25 minutes)
3. **Work** until the timer rings
4. **Take a short break** (5 minutes)
5. **Repeat** - after 4 pomodoros, take a longer break

### Binary Representation

Each minute value is converted to 8-bit binary:
```
Decimal 5 → Binary 00000101
         ↓
         MSB          LSB
         0 0 0 0 0 1 0 1
         ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
         128 64 32 16 8 4 2 1
         
         = 0 + 0 + 0 + 0 + 0 + 4 + 0 + 1 = 5
```

### Christmas Tree Design

The tree uses a tall, symmetrical structure with uniform leaf sizes:

```
        Row 0:    1 leaf     (top/star)
        Row 1:   2 leaves
        Row 2:   3 leaves
        Row 3:  4 leaves
        Row 4:  5 leaves
        Row 5:  6 leaves
        Row 6:  7 leaves
        Row 7: 8 leaves      (bottom - binary display)
                  │
               [trunk]
```

**Design choices:**
- **Taller than wide**: Height > width ratio for elegant appearance
- **Uniform leaf size**: All leaves are 14px for clean, consistent look
- **8 rows**: Creates a proper tall Christmas tree silhouette

### Growth Animation

As the timer progresses:
- **0%**: Only trunk visible
- **25%**: Bottom few leaves appear
- **50%**: Half the tree grown
- **100%**: Full tree with complete binary display

The animation creates a visual representation of time passing, similar to the Forest app concept where completing a focus session "grows" a tree.

### Color Theory

The "retro green" theme is inspired by:
- **Matrix digital rain**: The iconic green-on-black aesthetic
- **Old terminal screens**: Phosphor green monitors from the 80s/90s
- **Forest/nature**: Trees = productivity = growth

Color palette:
```
#0a1a0a - Background (very dark green-black)
#00ff41 - Primary text/leaves (Matrix green)
#33ff66 - Highlights for '1' digits
#2d5a2d - Borders and accents
#8B4513 - Tree trunk (natural brown)
```

---

## File Structure

```
pt/
├── pomodoro_widget.py         # Main application
├── create_startup_shortcut.py # Windows startup utility
├── requirements.txt           # Python dependencies
└── README.md                  # This documentation
```

---

## Customization

### Change Default Timer

In `pomodoro_widget.py`, line 185:
```python
self.timer = PomodoroTimer(5)  # Change 5 to your preferred default
```

### Modify Colors

In `BinaryChristmasTree.__init__`:
```python
self.leaf_color = "#00ff41"    # Change leaf color
self.leaf_glow = "#33ff66"     # Change highlight color
self.trunk_color = "#8B4513"   # Change trunk color
```

### Adjust Window Size

In `PomodoroWidget.__init__`:
```python
self.width = 320   # Change width
self.height = 400  # Change height
```

### Change Tree Shape

Modify the `self.rows` array in `BinaryChristmasTree`:
```python
# Current: Tall tree with 8 rows
self.rows = [1, 2, 3, 4, 5, 6, 7, 8]

# Alternative: Wider tree
self.rows = [1, 3, 5, 7, 8]
```

### Change Leaf Size

Modify `self.leaf_size` in `BinaryChristmasTree`:
```python
self.leaf_size = 14  # Uniform size for all leaves (default: 14px)
```

---

## Troubleshooting

### Widget doesn't appear

1. Check if Python is installed: `python --version`
2. Look for the widget in the bottom-right corner of your screen
3. Check taskbar for Python icon

### Widget appears behind other windows

The widget uses `attributes("-topmost", True)`. If this doesn't work:
- Try running as administrator
- Some fullscreen applications may override

### Startup shortcut fails

1. Ensure pywin32 is installed: `pip install pywin32`
2. Run with elevated permissions if needed
3. Check the Startup folder manually: `Win+R` → `shell:startup`

### Tree doesn't display correctly

- Ensure window is not minimized
- Try resizing your display scaling to 100%
- Check for Python/Tkinter version compatibility

---

## License

This project is open source. Feel free to modify and distribute.

---

## Contributing

Suggestions and improvements are welcome! Consider adding:
- Sound notifications
- Session tracking/statistics
- Customizable themes
- Break timer integration
- Multiple tree styles

---

*Created with 🌳 and Python*
