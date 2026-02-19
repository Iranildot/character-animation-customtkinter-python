"""
exemple3.py

UI demo for previewing character animations using CustomTkinter.

Structure:
- AnimationsDemoApp → main application window
- Character → animated character rendered on a stage
"""

from typing import Any
import customtkinter as ctk

from character import Character, Animation, AnimationFrame


# ─────────────────────────────────────────────
#  Animations Demo App
# ─────────────────────────────────────────────

class AnimationsDemoApp(ctk.CTk):
    """
    Application for previewing character animations.

    Responsibilities:
    - Build styled UI
    - Create animation preview stage
    - Spawn character
    - Provide buttons to trigger animations
    """

    WINDOW_SIZE = "560x620"
    CHARACTER_SIZE = 120

    # Theme colors
    BG_MAIN = "#0B1020"
    BG_CARD = "#0F172A"
    BG_STAGE = "#020617"
    BTN_MAIN = "#1F2937"
    BTN_HOVER = "#374151"
    TEXT_MAIN = "#E5E7EB"
    TEXT_MUTED = "#9CA3AF"
    ACCENT = "#38BDF8"

    def __init__(self):
        super().__init__()

        self._configure_window()
        self._build_ui()
        self._spawn_character()

    # ─────────────────────────────────────────
    # Window Setup
    # ─────────────────────────────────────────

    def _configure_window(self) -> None:
        """Configure main window settings and theme."""
        self.title("Character Animations")
        self.geometry(self.WINDOW_SIZE)
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.BG_MAIN)

    # ─────────────────────────────────────────
    # UI Construction
    # ─────────────────────────────────────────

    def _build_ui(self) -> None:
        """Build the main UI layout."""
        self.grid_columnconfigure(0, weight=1)

        self._create_card_container()
        self._create_header()
        self._create_stage()
        self._create_divider()
        self._create_controls()

    def _create_card_container(self) -> None:
        """Create the main card container."""
        self.card_container = ctk.CTkFrame(
            self,
            fg_color=self.BG_CARD,
            corner_radius=24,
        )
        self.card_container.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        self.card_container.grid_columnconfigure(0, weight=1)

    def _create_header(self) -> None:
        """Create title and subtitle."""
        self.title_label = ctk.CTkLabel(
            self.card_container,
            text="Animation Preview",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.TEXT_MAIN,
        )
        self.title_label.grid(row=0, column=0, pady=(20, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.card_container,
            text="Click a button to preview each animation",
            font=ctk.CTkFont(size=13),
            text_color=self.TEXT_MUTED,
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 16))

    def _create_stage(self) -> None:
        """Create the stage where the character is rendered."""
        self.stage = ctk.CTkFrame(
            self.card_container,
            fg_color=self.BG_STAGE,
            corner_radius=18,
            width=320,
            height=260,
            border_width=1,
            border_color="#1E293B",
        )
        self.stage.grid(row=2, column=0, padx=20, pady=12)
        self.stage.grid_propagate(False)

    def _create_divider(self) -> None:
        """Create a visual divider."""
        self.divider = ctk.CTkFrame(self.card_container, fg_color="#1E293B", height=1)
        self.divider.grid(row=3, column=0, sticky="ew", padx=32, pady=(16, 12))

    def _create_controls(self) -> None:
        """Create animation control buttons."""
        self.controls_container = ctk.CTkFrame(self.card_container, fg_color="transparent")
        self.controls_container.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.controls_container.grid_columnconfigure((0, 1), weight=1)

        self._create_animation_buttons()

    def _create_animation_buttons(self) -> None:
        """Create buttons for triggering animations."""
        def make_button(text: str, command):
            return ctk.CTkButton(
                self.controls_container,
                text=text,
                height=44,
                corner_radius=22,
                fg_color=self.BTN_MAIN,
                hover_color=self.BTN_HOVER,
                text_color=self.TEXT_MAIN,
                font=ctk.CTkFont(size=13, weight="bold"),
                border_width=1,
                border_color="#1E293B",
                command=command,
            )

        self.blink_button = make_button("Blink", lambda: self.character.play_animation("blink"))
        self.blink_button.grid(row=0, column=0, padx=8, pady=8, sticky="ew")

        self.blink_eye_button = make_button("Blink One Eye", lambda: self.character.play_animation("blink_an_eye"))
        self.blink_eye_button.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        self.look_up_button = make_button("Look Up", lambda: self.character.play_animation("look_up"))
        self.look_up_button.grid(row=1, column=0, padx=8, pady=8, sticky="ew")

        self.eyebrow_button = make_button("Move Eyebrow", lambda: self.character.play_animation("move_eyebrow"))
        self.eyebrow_button.grid(row=1, column=1, padx=8, pady=8, sticky="ew")

    # ─────────────────────────────────────────
    # Character Setup
    # ─────────────────────────────────────────

    def _spawn_character(self) -> None:
        """Create the character and center it on the stage."""
        self.character = Character(
            master=self,
            frame=self.stage,
            size=self.CHARACTER_SIZE,
            images_path="./assets/images/",
            bg_color=self.BG_STAGE,
            animations=self._build_animations(),
        )

        self._center_character_on_stage()

    def _center_character_on_stage(self) -> None:
        """Center the character inside the stage frame."""
        self.stage.update_idletasks()

        stage_width = self.stage.winfo_width()
        stage_height = self.stage.winfo_height()

        x = (stage_width - self.CHARACTER_SIZE) // 2
        y = (stage_height - self.CHARACTER_SIZE) // 2

        self.character.set_position((x, y))

    def _build_animations(self) -> list[Animation]:
        """Build and return the list of animations used in the demo."""
        return [
            Animation(
                name="blink",
                frames=[
                    AnimationFrame("blue_square_blink_0001.png"),
                    AnimationFrame("blue_square_blink_0002.png", duration=100),
                    AnimationFrame("blue_square_blink_0003.png", duration=100),
                    AnimationFrame("blue_square_blink_0004.png"),
                    AnimationFrame("blue_square_blink_0001.png", duration=3000),
                ],
            ),
            Animation(
                name="blink_an_eye",
                frames=[
                    AnimationFrame("blue_square_blinkaneye_0001.png"),
                    AnimationFrame("blue_square_blinkaneye_0002.png", duration=100),
                    AnimationFrame("blue_square_blinkaneye_0003.png", duration=100),
                    AnimationFrame("blue_square_blinkaneye_0004.png"),
                    AnimationFrame("blue_square_blinkaneye_0001.png", duration=2000),
                ],
            ),
            Animation(
                name="look_up",
                frames=[
                    AnimationFrame("blue_square_lookup_0001.png"),
                    AnimationFrame("blue_square_lookup_0002.png", duration=100),
                    AnimationFrame("blue_square_lookup_0003.png", duration=2000),
                    AnimationFrame("blue_square_lookup_0004.png", duration=100),
                    AnimationFrame("blue_square_lookup_0001.png", duration=2000),
                ],
            ),
            Animation(
                name="move_eyebrow",
                frames=[
                    AnimationFrame("blue_square_moveuplefteyebrow_0001.png"),
                    AnimationFrame("blue_square_moveuplefteyebrow_0002.png", duration=100),
                    AnimationFrame("blue_square_moveuplefteyebrow_0003.png", duration=3000),
                    AnimationFrame("blue_square_moveuplefteyebrow_0004.png", duration=100),
                    AnimationFrame("blue_square_moveuplefteyebrow_0001.png", duration=2000),
                ],
            ),
        ]


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = AnimationsDemoApp()
    app.mainloop()
