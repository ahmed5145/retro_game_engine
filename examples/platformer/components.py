"""Custom components for the platformer example."""
from dataclasses import dataclass, field

from src.core.ecs import Component
from src.core.vector2d import Vector2D


@dataclass
class PlayerController(Component):
    """Component for handling player input and movement."""

    move_speed: float = 200.0
    jump_force: float = 400.0
    can_jump: bool = True


@dataclass
class Physics(Component):
    """Component for handling physics simulation."""

    velocity: Vector2D = field(default_factory=Vector2D)
    gravity: float = 800.0


@dataclass
class BoxCollider(Component):
    """Component for handling collision detection."""

    width: float
    height: float
    is_static: bool = False
    is_trigger: bool = False
