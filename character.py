from PIL import Image
from typing import Any
import customtkinter as ctk

class AnimationFrame:
    """
    Represents a single frame of an animation sequence.

    Attributes:
        filename (str): Image filename relative to the images directory.
        duration (int): Duration (in milliseconds) that this frame is displayed.
    """

    def __init__(self, filename: str, duration: int = 250):
        """
        Args:
            filename (str): Image filename relative to the images directory.
            duration (int, optional): Duration of the frame in milliseconds. Defaults to 250.
        """
        self.filename = filename
        self.duration = duration


class Animation:
    """
    Represents a named animation composed of multiple frames.

    Attributes:
        name (str): Unique name of the animation.
        frames (list[AnimationFrame]): Ordered list of frames for the animation.
    """

    def __init__(self, name: str, frames: list[AnimationFrame]):
        """
        Args:
            name (str): Name of the animation.
            frames (list[AnimationFrame]): List of animation frames.

        Raises:
            ValueError: If the animation is created with an empty list of frames.
        """
        if not frames:
            raise ValueError(f"The animation '{name}' cannot be empty.")
        self.name = name
        self.frames = frames


class Character(ctk.CTkLabel):
    """
    UI component representing an animated character.

    The character can be positioned in two different layout modes:
    - Absolute positioning inside a single frame (`frame`)
    - Cell-based positioning inside a grid of frames (`grid_cells`)

    The character supports multiple named animations and frame-based playback.
    """

    def __init__(
        self,
        master: Any,
        animations: list[Animation] | None = None,
        position: tuple[int, int] = (0, 0),
        images_path: str = "./assets/images/",
        size: int = 100,
        bg_color: str = "transparent",
        frame: ctk.CTkFrame | None = None,
        grid_cells: list[list[ctk.CTkFrame]] | None = None,
    ):
        """
        Initializes a Character instance.

        Args:
            master (Any): Parent widget.
            animations (list[Animation] | None): List of animations to register.
            position (tuple[int, int]): Initial position of the character.
                - (row, col) when using grid_cells
                - (x, y) when using frame
            images_path (str): Directory containing animation images.
            size (int): Width and height of the character in pixels.
            bg_color (str): Background color of the wrapper frame.
            frame (ctk.CTkFrame | None): Frame used for absolute positioning.
            grid_cells (list[list[ctk.CTkFrame]] | None): Grid used for matrix-based positioning.

        Raises:
            RuntimeError: If neither frame nor grid_cells is provided when positioning is applied.
        """

        self._background_color = bg_color

        self._wrapper = ctk.CTkFrame(
            master,
            fg_color=bg_color,
            width=size,
            height=size,
        )

        super().__init__(self._wrapper, text="", fg_color=bg_color, width=size, height=size)
        self.grid(row=0, column=0, sticky="nsew")
        self._wrapper.rowconfigure(0, weight=1)
        self._wrapper.columnconfigure(0, weight=1)

        self.animations: dict[str, list[AnimationFrame]] = {}
        self.position = position
        self.current_frame_index = 0
        self.images_path = images_path
        self.size = size
        self.frame = frame
        self.grid_cells = grid_cells
        self._active_animation_name: str | None = None
        self._active_image: ctk.CTkImage | None = None

        if animations:
            self._register_animations(*animations)

    def play_animation(self, name: str):
        """
        Plays an animation by name.

        Args:
            name (str): Name of the registered animation.

        Notes:
            Frames are displayed sequentially using the Tkinter event loop (`after`).
        """
        self._active_animation_name = name
        frames = self.animations[name]

        def run(frame_index: int):
            """
            Renders a single frame and schedules the next one.
            """
            img = ctk.CTkImage(
                Image.open(self.images_path + frames[frame_index].filename),
                size=(self.size, self.size),
            )
            self._active_image = img
            self.configure(image=img)

            if frame_index < len(frames) - 1:
                self.after(frames[frame_index].duration, run, frame_index + 1)

        self.after(frames[0].duration, run, 0)

    def show(self, **kwargs):
        """
        Displays the character wrapper using the grid geometry manager.

        Args:
            **kwargs: Keyword arguments forwarded to `grid()`.
        """
        self._wrapper.grid(**kwargs)

    def set_position(self, position: tuple[int, int]) -> bool:
        """
        Sets the character position.

        Args:
            position (tuple[int, int]):
                - (row, col) when using grid_cells
                - (x, y) when using frame

        Returns:
            bool: True if the position was applied successfully,
                  False if the position exceeds layout bounds.
        """
        if self.grid_cells is not None:
            row, col = position
            rows = len(self.grid_cells)
            cols = len(self.grid_cells[0]) if rows else 0

            if not (0 <= row < rows and 0 <= col < cols):
                return False

        self.position = position
        self._update_position()
        return True

    def move(self, offset: tuple[int, int]) -> bool:
        """
        Moves the character relative to its current position.

        Args:
            offset (tuple[int, int]): (dx, dy) offset.

        Returns:
            bool: True if the movement was applied successfully,
                  False if the resulting position is out of bounds.
        """
        dx, dy = offset
        x, y = self.position
        return self.set_position((x + dx, y + dy))

    def _update_position(self):
        if self.grid_cells is not None:
            row, col = self.position

            if row < 0 or col < 0 or row >= len(self.grid_cells) or col >= len(self.grid_cells[row]):
                return

            target_cell = self.grid_cells[row][col]

            # 🔁 agora tudo relativo ao master (pai do wrapper)
            parent = self._wrapper.master
            parent.update_idletasks()

            cell_x = target_cell.winfo_rootx() - parent.winfo_rootx()
            cell_y = target_cell.winfo_rooty() - parent.winfo_rooty()

            offset_x = (target_cell.winfo_width() - self.size) // 2
            offset_y = (target_cell.winfo_height() - self.size) // 2

            self._wrapper.place(x=cell_x + offset_x, y=cell_y + offset_y)

        elif self.frame is not None:
            x, y = self.position
            self._wrapper.place_forget()
            self._wrapper.grid_forget()
            self._wrapper.place(in_=self.frame, x=x, y=y)

        else:
            raise RuntimeError("No frame or grid_cells was defined.")

    def _register_animations(self, *animations: Animation):
        """
        Registers one or more animations.

        Args:
            *animations (Animation): Animations to be registered.

        Raises:
            ValueError: If an animation with the same name already exists.
        """
        for animation in animations:
            if animation.name in self.animations:
                raise ValueError(f"Duplicate animation '{animation.name}'.")
            self.animations[animation.name] = animation.frames

    def get_animation_frames(self, name: str) -> list[AnimationFrame]:
        """
        Returns the frames of a registered animation.

        Args:
            name (str): Name of the animation.

        Returns:
            list[AnimationFrame]: Frames belonging to the animation.
        """
        return self.animations[name]

    @property
    def current_position(self) -> tuple[int, int]:
        """
        Returns the current position of the character.

        Returns:
            tuple[int, int]: Current coordinates.
        """
        return self.position