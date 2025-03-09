"""Demo showcasing the UI system features."""
import os
import sys

import pygame

from src.core.ui import Button, ButtonStyle, Text, TextConfig, UIElement, UIRect
from src.core.window import Window, WindowConfig


class UIDemo:
    """Demo application for UI system."""

    def __init__(self) -> None:
        """Initialize the demo."""
        # Initialize window
        config = WindowConfig(
            title="UI System Demo", width=800, height=600, scale=1, vsync=True
        )
        self.window = Window(config)
        self.running = True
        self.clock = pygame.time.Clock()

        # Create UI root with full window size
        self.ui_root = UIElement(UIRect(width=800, height=600))

        # Add title
        title_config = TextConfig(
            font_size=48, color=(255, 255, 255), align="center", shadow_offset=(2, 2)
        )
        title = Text(
            "UI System Demo",
            rect=UIRect(
                x=0.5,  # Center horizontally
                y=50,  # Fixed pixels from top
                width=600,  # Fixed width in pixels
                height=60,  # Fixed height in pixels
                anchor_x=0.5,  # Center anchor point
                anchor_y=0.0,  # Top anchor
            ),
            config=title_config,
        )
        self.ui_root.add_child(title)

        # Add animated text
        text_config = TextConfig(
            font_size=24,
            color=(200, 200, 255),
            align="center",
            shadow_offset=(1, 1),
        )
        animated_text = Text(
            "This text appears character by character...",
            rect=UIRect(
                x=0.5,  # Center horizontally
                y=150,  # Fixed pixels from top
                width=600,  # Fixed width in pixels
                height=40,  # Fixed height in pixels
                anchor_x=0.5,  # Center anchor point
                anchor_y=0.0,  # Top anchor
            ),
            config=text_config,
        )
        # Set animation speed after creation
        text_config.animation_speed = 20  # 20 characters per second
        self.ui_root.add_child(animated_text)

        # Button style configuration
        button_style = ButtonStyle(
            background_color=(40, 40, 80),
            hover_color=(60, 60, 100),
            pressed_color=(30, 30, 60),
            border_color=(80, 80, 120),
            border_width=2,
            corner_radius=5,
            padding=(10, 5, 10, 5),
        )

        # Start button
        start_button = Button(
            "Start Game",
            rect=UIRect(
                x=0.5,  # Center horizontally
                y=300,  # Fixed pixels from top
                width=200,  # Fixed width in pixels
                height=40,  # Fixed height in pixels
                anchor_x=0.5,  # Center anchor point
                anchor_y=0.0,  # Top anchor
            ),
            style=button_style,
        )
        start_button.on_click = lambda: print("Start clicked!")
        self.ui_root.add_child(start_button)

        # Settings button
        settings_button = Button(
            "Settings",
            rect=UIRect(
                x=0.5,  # Center horizontally
                y=360,  # Fixed pixels from top
                width=200,  # Fixed width in pixels
                height=40,  # Fixed height in pixels
                anchor_x=0.5,  # Center anchor point
                anchor_y=0.0,  # Top anchor
            ),
            style=button_style,
        )
        settings_button.on_click = lambda: print("Settings clicked!")
        self.ui_root.add_child(settings_button)

        # Quit button
        quit_button = Button(
            "Quit",
            rect=UIRect(
                x=0.5,  # Center horizontally
                y=420,  # Fixed pixels from top
                width=200,  # Fixed width in pixels
                height=40,  # Fixed height in pixels
                anchor_x=0.5,  # Center anchor point
                anchor_y=0.0,  # Top anchor
            ),
            style=button_style,
        )
        quit_button.on_click = self.quit
        self.ui_root.add_child(quit_button)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            else:
                # Let UI handle the event
                self.ui_root.handle_event(event)

    def update(self) -> None:
        """Update game state."""
        dt = self.clock.tick(60) / 1000.0
        self.ui_root.update(dt)

    def render(self) -> None:
        """Render the demo."""
        # Clear window
        self.window.clear((40, 40, 60))  # Dark blue-gray background

        # Render UI
        self.ui_root.render(self.window.surface)

        # Present frame
        self.window.present()

    def quit(self) -> None:
        """Quit the demo."""
        self.running = False

    def run(self) -> None:
        """Run the demo loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    demo = UIDemo()
    demo.run()
