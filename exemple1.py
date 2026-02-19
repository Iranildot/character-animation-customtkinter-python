"""
exemple1.py

Test application for grid-based character movement using CustomTkinter.

Structure:
- GridGameApp → main application window
- GridCharacter → controllable character inside a grid
"""

from typing import Any
import customtkinter as ctk

from character import Character, Animation, AnimationFrame
from cells_grid import CellsGrid


# ─────────────────────────────────────────────
#  GridCharacter
# ─────────────────────────────────────────────

class GridCharacter(Character):
    """
    Controllable character that moves inside a grid of cells.

    Inherits from Character and defines:
    - Default size
    - Initial animation
    - Assets path
    """

    DEFAULT_SIZE = 54
    IMAGE_ASSETS_PATH = "./assets/images/"

    def __init__(self, master: Any, grid_matrix: list[list[ctk.CTkFrame]]):
        """
        :param master: Parent widget
        :param grid_matrix: Matrix of grid cells
        """
        super().__init__(
            master=master,
            bg_color="#1E2A3A",
            grid_cells=grid_matrix,
            size=self.DEFAULT_SIZE,
            images_path=self.IMAGE_ASSETS_PATH,
            animations=[
                Animation(
                    name="idle",
                    frames=[
                        AnimationFrame("blue_square_blink_0001.png"),
                    ],
                )
            ],
        )


# ─────────────────────────────────────────────
#  GridGameApp (Main Application)
# ─────────────────────────────────────────────

class GridGameApp(ctk.CTk):
    """
    Main application window.

    Responsibilities:
    - Build UI
    - Initialize grid
    - Spawn character
    - Handle keyboard input
    """

    GRID_DIMENSION = 6
    CELL_SIZE = 80
    CELL_GAP = 8
    INITIAL_POSITION = (1, 0)

    MOVEMENT_KEYS = {
        "Up":    (-1,  0),
        "Down":  ( 1,  0),
        "Left":  ( 0, -1),
        "Right": ( 0,  1),
        "w":     (-1,  0),
        "s":     ( 1,  0),
        "a":     ( 0, -1),
        "d":     ( 0,  1),
    }

    def __init__(self):
        super().__init__()

        self._configure_window()
        self._build_ui()
        self._spawn_character()
        self._bind_keys()

    # ─────────────────────────────────────────
    # Window Setup
    # ─────────────────────────────────────────

    def _configure_window(self) -> None:
        """Configure main window settings."""
        self.title("Grid Movement Demo")
        self.geometry("640x720")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

    # ─────────────────────────────────────────
    # UI Construction
    # ─────────────────────────────────────────

    def _build_ui(self) -> None:
        """Build the main UI layout."""
        self._configure_layout()
        self._create_header()
        self._create_cells_grid()
        self._create_position_label()

    def _configure_layout(self) -> None:
        """Configure grid layout weights."""
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _create_header(self) -> None:
        """Create header label with instructions."""
        self.header_label = ctk.CTkLabel(
            self,
            text="Use ← ↑ → ↓ or W A S D to move",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#A0C4FF",
        )
        self.header_label.grid(row=0, column=0, pady=(20, 4))

    def _create_cells_grid(self) -> None:
        """Create and configure the cells grid widget."""
        self.grid_widget = CellsGrid(
            self,
            width=self.GRID_DIMENSION * (self.CELL_SIZE + self.CELL_GAP),
            height=self.GRID_DIMENSION * (self.CELL_SIZE + self.CELL_GAP),
            margin=20,
            padding=10,
        )
        self.grid_widget.grid(row=1, column=0)

        self.grid_widget.load_cells(
            array=self.GRID_DIMENSION,
            cells_size=self.CELL_SIZE,
            cells_spacing=self.CELL_GAP,
            cells_corner_radius=10,
            cells_fg_color="#1E2A3A",
            cells_border_color="#2E4A6A",
            cells_border_width=2,
        )

    def _create_position_label(self) -> None:
        """Create label that shows the current position."""
        self.position_label = ctk.CTkLabel(
            self,
            text=f"Position: {self.INITIAL_POSITION}",
            font=ctk.CTkFont(size=13),
            text_color="#7FBADC",
        )
        self.position_label.grid(row=2, column=0, pady=(4, 16))

    # ─────────────────────────────────────────
    # Character Setup
    # ─────────────────────────────────────────

    def _spawn_character(self) -> None:
        """Create character and set its initial position."""
        grid_matrix = self.grid_widget.get_cells_grid()
        self.player = GridCharacter(self, grid_matrix=grid_matrix)
        self.player.set_position(self.INITIAL_POSITION)
        self.player.play_animation("idle")

    # ─────────────────────────────────────────
    # Input Handling
    # ─────────────────────────────────────────

    def _bind_keys(self) -> None:
        """Bind keyboard events."""
        self.focus_set()
        self.bind("<KeyPress>", self._on_keypress)

    def _on_keypress(self, event) -> None:
        """Handle key press events and move the character."""
        movement_offset = self.MOVEMENT_KEYS.get(event.keysym)
        if movement_offset is None:
            return

        previous_position = self.player.position
        self.player.move(movement_offset)

        self.after(200, self._update_position_label)

        if self.player.position == previous_position:
            self._flash_invalid_move()

    # ─────────────────────────────────────────
    # UI Feedback
    # ─────────────────────────────────────────

    def _update_position_label(self) -> None:
        """Update the position label text."""
        self.position_label.configure(
            text=f"Position: {self.player.current_position}"
        )

    def _flash_invalid_move(self) -> None:
        """Visual feedback for invalid moves."""
        default_color = "#7FBADC"
        self.position_label.configure(text_color="#FF6B6B")
        self.after(200, lambda: self.position_label.configure(text_color=default_color))


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = GridGameApp()
    app.mainloop()
