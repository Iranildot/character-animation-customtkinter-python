"""
exemple2.py

Test application for free (pixel-based) character movement using CustomTkinter.

Structure:
- FreeMovementApp → main application window
- FreeMovementCharacter → controllable character inside a free-movement area
"""

from typing import Any
import customtkinter as ctk

from character import Character, Animation, AnimationFrame


# ─────────────────────────────────────────────
#  FreeMovementCharacter
# ─────────────────────────────────────────────

class FreeMovementCharacter(Character):
    """
    Controllable character that moves freely inside a frame (no grid constraints).

    Inherits from Character and defines:
    - Default size
    - Initial animation
    - Assets path
    """

    DEFAULT_SIZE = 54
    IMAGE_ASSETS_PATH = "./assets/images/"

    def __init__(self, master: Any, play_area: ctk.CTkFrame):
        """
        :param master: Parent widget
        :param play_area: Frame where the character can move freely
        """
        super().__init__(
            master=master,
            frame=play_area,
            size=self.DEFAULT_SIZE,
            images_path=self.IMAGE_ASSETS_PATH,
            bg_color="#1E2A3A",
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
#  FreeMovementApp (Main Application)
# ─────────────────────────────────────────────

class FreeMovementApp(ctk.CTk):
    """
    Main application window for free movement testing.

    Responsibilities:
    - Build UI
    - Create play area
    - Spawn character
    - Handle keyboard input
    """

    STEP_PIXELS = 15
    INITIAL_POSITION = (20, 20)

    MOVEMENT_KEYS = {
        "Up":    (0,  -STEP_PIXELS),
        "Down":  (0,   STEP_PIXELS),
        "Left":  (-STEP_PIXELS, 0),
        "Right": ( STEP_PIXELS, 0),
        "w":     (0,  -STEP_PIXELS),
        "s":     (0,   STEP_PIXELS),
        "a":     (-STEP_PIXELS, 0),
        "d":     ( STEP_PIXELS, 0),
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
        self.title("Free Movement Demo")
        self.geometry("640x640")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

    # ─────────────────────────────────────────
    # UI Construction
    # ─────────────────────────────────────────

    def _build_ui(self) -> None:
        """Build the main UI layout."""
        self._configure_layout()
        self._create_header()
        self._create_play_area()
        self._create_position_label()

    def _configure_layout(self) -> None:
        """Configure grid layout weights."""
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

    def _create_header(self) -> None:
        """Create header label with instructions."""
        self.header_label = ctk.CTkLabel(
            self,
            text="Use ← ↑ → ↓ or W A S D to move freely",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#A0C4FF",
        )
        self.header_label.grid(row=0, column=0, pady=(20, 4))

    def _create_play_area(self) -> None:
        """Create the play area frame where the character can move."""
        self.play_area = ctk.CTkFrame(
            self,
            fg_color="#1E2A3A",
            border_width=0,
            corner_radius=0,
            width=560,
            height=500,
        )
        self.play_area.grid(row=1, column=0, padx=40, pady=10)
        self.play_area.grid_propagate(False)

    def _create_position_label(self) -> None:
        """Create label that shows the current character position."""
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
        """Create the character and set its initial position."""
        self.player = FreeMovementCharacter(self, play_area=self.play_area)
        self.player.set_position(self.INITIAL_POSITION)
        self.player.play_animation("idle")

    # ─────────────────────────────────────────
    # Input Handling
    # ─────────────────────────────────────────

    def _bind_keys(self) -> None:
        """Bind keyboard events."""
        self.focus_set()
        self.bind("<KeyPress>", self._handle_keypress)

    def _handle_keypress(self, event) -> None:
        """Handle key press events and move the character."""
        movement_offset = self.MOVEMENT_KEYS.get(event.keysym)
        if movement_offset is None:
            return

        moved = self.player.move(movement_offset)

        if not moved:
            self._flash_invalid_move()
            return

        self._update_position_label()

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
    app = FreeMovementApp()
    app.mainloop()
