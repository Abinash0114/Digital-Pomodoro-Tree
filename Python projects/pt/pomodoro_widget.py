"""
Binary Tree Pomodoro Widget
A visual Pomodoro timer with a growing Christmas tree visualization.
The tree displays timer value in binary format.
"""

import tkinter as tk
import math


class BinaryChristmasTree:
    """
    Christmas tree visualization with binary digits as leaves.
    Bottom row displays the timer value in binary (MSB on left).
    Upper rows are filled with zeros for visual balance.
    """
    
    def __init__(self, canvas, center_x, base_y, tree_height=180):
        self.canvas = canvas
        self.center_x = center_x
        self.base_y = base_y
        self.tree_height = tree_height
        
        # Colors - Retro green theme
        self.leaf_color = "#00ff41"      # Matrix green for digits
        self.leaf_glow = "#33ff66"       # Lighter green for highlights
        self.trunk_color = "#8B4513"     # Brown trunk
        self.trunk_dark = "#5D3A1A"      # Darker brown for depth
        
        self.leaf_items = []
        self.trunk_items = []
        
        # Christmas tree structure: rows from top to bottom
        # Taller tree with more rows for height > width
        # Row 0: 1 leaf (top/star)
        # Row 1: 2 leaves
        # Row 2: 3 leaves
        # Row 3: 4 leaves
        # Row 4: 5 leaves
        # Row 5: 6 leaves
        # Row 6: 7 leaves
        # Row 7: 8 leaves (bottom - holds binary value)
        self.rows = [1, 2, 3, 4, 5, 6, 7, 8]
        
        # Uniform leaf size for all leaves
        self.leaf_size = 14
        
    def _calculate_positions(self):
        """Calculate leaf positions in Christmas tree shape."""
        positions = []
        
        # Calculate vertical spacing
        num_rows = len(self.rows)
        row_spacing = self.tree_height / (num_rows + 1)
        
        # Start from top of tree
        start_y = self.base_y - self.tree_height
        
        for row_idx, num_leaves in enumerate(self.rows):
            y = start_y + (row_idx + 1) * row_spacing
            
            # Calculate horizontal spread (narrower for taller appearance)
            max_spread = 95  # Narrower max width for taller look
            spread = (max_spread * (row_idx + 1)) / num_rows
            
            # Use uniform leaf size for all leaves
            base_size = self.leaf_size
            
            for i in range(num_leaves):
                if num_leaves == 1:
                    x = self.center_x
                else:
                    # Evenly distribute leaves
                    x = self.center_x - spread + (i * (2 * spread / (num_leaves - 1)))
                
                positions.append({
                    "x": x,
                    "y": y,
                    "row": row_idx,
                    "col": i,
                    "size": base_size,
                    "is_binary_row": (row_idx == len(self.rows) - 1)
                })
        
        return positions
    
    def draw_trunk(self):
        """Draw the tree trunk."""
        for item in self.trunk_items:
            self.canvas.delete(item)
        self.trunk_items = []
        
        trunk_top = self.base_y - 15
        trunk_bottom = self.base_y + 25
        trunk_width = 12
        
        # Main trunk
        trunk = self.canvas.create_rectangle(
            self.center_x - trunk_width/2, trunk_top,
            self.center_x + trunk_width/2, trunk_bottom,
            fill=self.trunk_color,
            outline=self.trunk_dark,
            width=2
        )
        self.trunk_items.append(trunk)
        
        # Trunk detail lines
        for i in range(3):
            y = trunk_top + 8 + (i * 10)
            line = self.canvas.create_line(
                self.center_x - trunk_width/2 + 2, y,
                self.center_x + trunk_width/2 - 2, y,
                fill=self.trunk_dark,
                width=1
            )
            self.trunk_items.append(line)
    
    def draw_tree(self, binary_value, growth_percent):
        """
        Draw the Christmas tree with binary leaves.
        
        Args:
            binary_value: Integer value to display in binary (timer minutes)
            growth_percent: 0-100, how much of the tree has grown
        """
        # Clear existing leaves
        for item in self.leaf_items:
            self.canvas.delete(item)
        self.leaf_items = []
        
        # Draw trunk first
        self.draw_trunk()
        
        # Get binary string (8 bits for bottom row)
        binary_str = format(min(binary_value, 255), '08b')
        
        # Get all positions
        positions = self._calculate_positions()
        total_leaves = len(positions)
        
        # Calculate how many leaves to show based on growth
        # Grow from bottom to top
        visible_count = int((growth_percent / 100) * total_leaves)
        
        # Reverse positions so we grow from bottom
        positions_reversed = list(reversed(positions))
        
        for i, pos in enumerate(positions_reversed):
            if i >= visible_count:
                continue
            
            # Determine the digit to display
            if pos["is_binary_row"]:
                # Bottom row: show actual binary value (left to right = MSB to LSB)
                bit_idx = pos["col"]
                digit = binary_str[bit_idx] if bit_idx < len(binary_str) else "0"
            else:
                # Upper rows: always show 0
                digit = "0"
            
            self._draw_leaf(pos, digit, i / max(1, visible_count - 1) if visible_count > 1 else 1)
    
    def _draw_leaf(self, pos, digit, growth_factor):
        """Draw a single leaf as a clean digit (no circles)."""
        x, y = pos["x"], pos["y"]
        size = pos["size"]
        
        # Animate size based on growth
        animated_size = size * (0.7 + 0.3 * growth_factor)
        
        # Font size for clean, readable digits
        font_size = int(animated_size * 1.1)
        
        # Highlight '1' digits with brighter color for emphasis
        text_color = self.leaf_glow if digit == "1" else self.leaf_color
        
        # Draw just the digit - clean and readable
        leaf_text = self.canvas.create_text(
            x, y,
            text=digit,
            fill=text_color,
            font=("Consolas", font_size, "bold")
        )
        self.leaf_items.append(leaf_text)
    
    def clear(self):
        """Clear all tree elements."""
        for item in self.leaf_items:
            self.canvas.delete(item)
        self.leaf_items = []
        for item in self.trunk_items:
            self.canvas.delete(item)
        self.trunk_items = []


class PomodoroTimer:
    """Handles timer logic and state."""
    
    def __init__(self, initial_minutes=5):
        self.total_seconds = initial_minutes * 60
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        self.minutes = initial_minutes
        
    def set_minutes(self, minutes):
        """Set timer duration in minutes."""
        self.minutes = max(1, min(60, minutes))  # Clamp between 1-60
        self.total_seconds = self.minutes * 60
        self.remaining_seconds = self.total_seconds
        
    def start(self):
        """Start or resume the timer."""
        self.is_running = True
        
    def pause(self):
        """Pause the timer."""
        self.is_running = False
        
    def reset(self):
        """Reset timer to initial value."""
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        
    def tick(self):
        """Decrease timer by 1 second. Returns True if timer is still running."""
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.remaining_seconds <= 0:
                self.is_running = False
                return False
        return self.is_running
    
    def get_display_time(self):
        """Return formatted time string MM:SS."""
        mins = self.remaining_seconds // 60
        secs = self.remaining_seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def get_progress_percent(self):
        """Return progress as percentage (0-100)."""
        if self.total_seconds == 0:
            return 100
        elapsed = self.total_seconds - self.remaining_seconds
        return (elapsed / self.total_seconds) * 100
    
    def is_complete(self):
        """Check if timer has completed."""
        return self.remaining_seconds <= 0


class PomodoroWidget:
    """Main Pomodoro widget window."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Binary Pomodoro")
        
        # Window configuration
        self.width = 320
        self.height = 400
        
        # Remove window decorations and set always on top
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)
        
        # Set window size and position (bottom right corner initially)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.width - 50
        y = screen_height - self.height - 80
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Prevent resizing
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = "#0a1a0a"
        self.accent_color = "#2d5a2d"
        self.text_color = "#ffffff"
        self.highlight_color = "#00ff41"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize timer
        self.timer = PomodoroTimer(5)
        
        # Create UI
        self._create_ui()
        
        # Drag functionality
        self._drag_data = {"x": 0, "y": 0}
        self._setup_drag()
        
        # Start update loop
        self._update()
        
    def _create_ui(self):
        """Create the widget UI elements."""
        # Main frame with border
        self.main_frame = tk.Frame(
            self.root,
            bg=self.bg_color,
            highlightbackground=self.accent_color,
            highlightthickness=3,
            width=self.width,
            height=self.height
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)
        
        # Top control bar
        self.top_bar = tk.Frame(self.main_frame, bg=self.bg_color, height=40)
        self.top_bar.pack(fill=tk.X, padx=10, pady=(8, 5))
        self.top_bar.pack_propagate(False)
        
        # Close button (small X in top left)
        self.close_btn = tk.Label(
            self.top_bar,
            text="✕",
            fg="#555555",
            bg=self.bg_color,
            font=("Arial", 11),
            cursor="hand2"
        )
        self.close_btn.pack(side=tk.LEFT, padx=(5, 0))
        self.close_btn.bind("<Button-1>", lambda e: self.root.destroy())
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.configure(fg="#ff4444"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.configure(fg="#555555"))
        
        # Play/Pause button (top right)
        self.play_btn = tk.Canvas(
            self.top_bar,
            width=38,
            height=38,
            bg=self.bg_color,
            highlightthickness=0,
            cursor="hand2"
        )
        self.play_btn.pack(side=tk.RIGHT, padx=(0, 5))
        self._draw_play_button()
        self.play_btn.bind("<Button-1>", self._toggle_timer)
        
        # Canvas for tree (centered area)
        canvas_height = 260
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.width - 30,
            height=canvas_height,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=(5, 10))
        
        # Initialize Christmas tree
        self.tree = BinaryChristmasTree(
            self.canvas,
            center_x=(self.width - 30) // 2,
            base_y=canvas_height - 30,
            tree_height=200
        )
        
        # Bottom control bar
        self.bottom_bar = tk.Frame(self.main_frame, bg=self.bg_color, height=55)
        self.bottom_bar.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.bottom_bar.pack_propagate(False)
        
        # Timer controls container (centered)
        self.timer_controls = tk.Frame(self.bottom_bar, bg=self.bg_color)
        self.timer_controls.pack(expand=True, anchor=tk.CENTER)
        
        # Minus button
        self.minus_btn = tk.Canvas(
            self.timer_controls,
            width=40,
            height=40,
            bg=self.bg_color,
            highlightthickness=0,
            cursor="hand2"
        )
        self.minus_btn.pack(side=tk.LEFT, padx=8)
        self._draw_minus_button()
        self.minus_btn.bind("<Button-1>", self._decrease_time)
        
        # Timer display
        self.timer_label = tk.Label(
            self.timer_controls,
            text="05:00",
            fg=self.text_color,
            bg=self.bg_color,
            font=("Consolas", 26, "bold")
        )
        self.timer_label.pack(side=tk.LEFT, padx=12)
        
        # Plus button
        self.plus_btn = tk.Canvas(
            self.timer_controls,
            width=40,
            height=40,
            bg=self.bg_color,
            highlightthickness=0,
            cursor="hand2"
        )
        self.plus_btn.pack(side=tk.LEFT, padx=8)
        self._draw_plus_button()
        self.plus_btn.bind("<Button-1>", self._increase_time)
        
        # Initial tree draw
        self._update_tree()
        
    def _draw_play_button(self):
        """Draw play or pause icon on the play button."""
        self.play_btn.delete("all")
        
        # Draw circle border with glow effect
        self.play_btn.create_oval(
            2, 2, 36, 36,
            outline=self.accent_color,
            width=2
        )
        
        if self.timer.is_running:
            # Draw pause icon (two rectangles)
            self.play_btn.create_rectangle(
                12, 10, 16, 28,
                fill=self.text_color,
                outline=self.text_color
            )
            self.play_btn.create_rectangle(
                22, 10, 26, 28,
                fill=self.text_color,
                outline=self.text_color
            )
        else:
            # Draw play icon (triangle)
            self.play_btn.create_polygon(
                13, 10,
                13, 28,
                28, 19,
                fill=self.text_color,
                outline=self.text_color
            )
    
    def _draw_minus_button(self):
        """Draw minus button with clean design."""
        self.minus_btn.delete("all")
        self.minus_btn.create_oval(2, 2, 38, 38, outline=self.accent_color, width=2)
        self.minus_btn.create_line(10, 20, 30, 20, fill=self.accent_color, width=3)
        
    def _draw_plus_button(self):
        """Draw plus button with clean design."""
        self.plus_btn.delete("all")
        self.plus_btn.create_oval(2, 2, 38, 38, outline=self.accent_color, width=2)
        self.plus_btn.create_line(10, 20, 30, 20, fill=self.accent_color, width=3)
        self.plus_btn.create_line(20, 10, 20, 30, fill=self.accent_color, width=3)
        
    def _toggle_timer(self, event=None):
        """Toggle timer start/pause."""
        if self.timer.is_complete():
            self.timer.reset()
        
        if self.timer.is_running:
            self.timer.pause()
        else:
            self.timer.start()
        
        self._draw_play_button()
        
    def _increase_time(self, event=None):
        """Increase timer by 1 minute."""
        if not self.timer.is_running:
            self.timer.set_minutes(self.timer.minutes + 1)
            self._update_display()
            self._update_tree()
            
    def _decrease_time(self, event=None):
        """Decrease timer by 1 minute."""
        if not self.timer.is_running:
            self.timer.set_minutes(self.timer.minutes - 1)
            self._update_display()
            self._update_tree()
            
    def _update_display(self):
        """Update the timer display."""
        self.timer_label.config(text=self.timer.get_display_time())
        
    def _update_tree(self):
        """Update the tree visualization."""
        progress = self.timer.get_progress_percent()
        # Show tree based on progress (minimum 25% visibility)
        display_progress = max(25, progress)
        self.tree.draw_tree(self.timer.minutes, display_progress)
        
    def _setup_drag(self):
        """Setup window dragging."""
        for widget in [self.main_frame, self.canvas, self.top_bar]:
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)
        
    def _start_drag(self, event):
        """Record the starting position for drag."""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        
    def _do_drag(self, event):
        """Handle window dragging."""
        x = self.root.winfo_x() + (event.x - self._drag_data["x"])
        y = self.root.winfo_y() + (event.y - self._drag_data["y"])
        self.root.geometry(f"+{x}+{y}")
        
    def _update(self):
        """Main update loop - runs every second."""
        if self.timer.is_running:
            self.timer.tick()
            self._update_display()
            self._update_tree()
            self._draw_play_button()
            
            # Check if timer completed
            if self.timer.is_complete():
                self._on_timer_complete()
        
        # Schedule next update
        self.root.after(1000, self._update)
        
    def _on_timer_complete(self):
        """Handle timer completion."""
        # Flash the border green multiple times
        def flash(count):
            if count > 0:
                color = self.highlight_color if count % 2 == 1 else self.accent_color
                self.main_frame.configure(highlightbackground=color)
                self.root.after(400, lambda: flash(count - 1))
        flash(6)
        
    def run(self):
        """Start the widget."""
        self.root.mainloop()


if __name__ == "__main__":
    widget = PomodoroWidget()
    widget.run()
