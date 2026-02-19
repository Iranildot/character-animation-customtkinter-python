# 📘 Character Library

A lightweight animation and movement library built on top of
**CustomTkinter**, designed to simplify animated character rendering
inside Tkinter-based applications.

This module provides:

-   🎞 Frame-based animation system\
-   🧍 Reusable animated character component\
-   🎮 Support for grid-based movement\
-   🕹 Support for free (pixel-based) movement

------------------------------------------------------------------------

## 📦 Module: `character.py`

### Overview

The `character.py` module contains three core components:

-   `AnimationFrame`
-   `Animation`
-   `Character`

These classes work together to provide a simple, extensible animation
system for GUI-based applications.

------------------------------------------------------------------------

## 🧱 Core Classes

### 1️⃣ AnimationFrame

Represents a single frame in an animation sequence.

**Parameters**

  Parameter      Type    Description
  -------------- ------- --------------------------------------------
  `image_path`   `str`   Filename of the image inside `images_path`
  `duration`     `int`   Duration in milliseconds (default varies)

**Example**

``` python
AnimationFrame("blue_square_blink_0001.png", duration=100)
```

------------------------------------------------------------------------

### 2️⃣ Animation

Represents a sequence of animation frames.

**Parameters**

  Parameter   Type                     Description
  ----------- ------------------------ ------------------------
  `name`      `str`                    Unique animation name
  `frames`    `list[AnimationFrame]`   Ordered list of frames

**Example**

``` python
Animation(
    name="blink",
    frames=[
        AnimationFrame("frame1.png"),
        AnimationFrame("frame2.png", duration=100),
    ],
)
```

------------------------------------------------------------------------

### 3️⃣ Character

Main component responsible for:

-   Rendering the character\
-   Managing animations\
-   Handling movement\
-   Updating position

**Constructor Parameters**

  ---------------------------------------------------------------------------------
  Parameter                Type                     Description
  ------------------------ ------------------------ -------------------------------
  `master`                 `Any`                    Parent widget

  `frame`                  `CTkFrame`               (Optional) Free movement
                                                    container

  `grid_cells`             `list[list[CTkFrame]]`   (Optional) Grid-based container

  `size`                   `int`                    Rendered character size

  `images_path`            `str`                    Path to image assets

  `bg_color`               `str`                    Background color

  `animations`             `list[Animation]`        List of available animations
  ---------------------------------------------------------------------------------

> ⚠️ Either `frame` (free mode) OR `grid_cells` (grid mode) must be
> provided.

------------------------------------------------------------------------

## 🔧 Main Methods

  Method                   Description
  ------------------------ ----------------------------
  `play_animation(name)`   Plays an animation by name
  `set_position((x, y))`   Sets character position
  `move((dx, dy))`         Moves character by offset
  `current_position`       Returns current position

------------------------------------------------------------------------

## 🎮 Examples

The repository includes three example applications demonstrating
different use cases.

------------------------------------------------------------------------

## 🧩 example1.py --- Grid Movement

Demonstrates grid-based movement.

**Features**

-   Movement constrained to a grid\
-   Arrow keys and WASD support\
-   Position feedback\
-   Invalid movement feedback

**Run**

``` bash
python example1.py
```

https://github.com/user-attachments/assets/749e16c1-95c6-4b91-bd3d-1a92a6901507

------------------------------------------------------------------------

## 🕹 example2.py --- Free Movement

Demonstrates pixel-based movement inside a frame.

**Features**

-   Free movement inside a play area\
-   Adjustable movement step\
-   Real-time position display

**Run**

``` bash
python example2.py
```

https://github.com/user-attachments/assets/7a12fa5f-a45e-4aff-a96d-34ee72bcc58a

------------------------------------------------------------------------

## 🎞 example3.py --- Animations Demo

UI-based animation preview tool.

**Features**

-   Multiple animation preview buttons\
-   Styled UI layout\
-   Centered character stage\
-   Isolated animation testing

**Run**

``` bash
python example3.py
```

https://github.com/user-attachments/assets/4fb2c0ec-818c-401f-b260-87acf9316bdb

------------------------------------------------------------------------

## 🗂 Recommended Project Structure

``` text
project/
│
├── character.py
├── example1.py
├── example2.py
├── example3.py
│
├── assets/
│   └── images/
│       ├── frame1.png
│       ├── frame2.png
│       └── ...
│
└── README.md
```

------------------------------------------------------------------------

## ⚙️ Movement Modes

### Grid Mode

``` python
grid_cells=matrix
```

Character movement is restricted to valid cells.

### Free Mode

``` python
frame=play_area
```

Character moves freely inside a container.

------------------------------------------------------------------------

## 🧠 Design Philosophy

This library focuses on:

-   Simplicity\
-   Readability\
-   Reusability\
-   Decoupled animation logic\
-   Clear separation between:
    -   Rendering\
    -   Animation\
    -   Movement\
    -   UI

------------------------------------------------------------------------
