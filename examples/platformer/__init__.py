"""Platformer example game using the Entity Component System."""

from .components import BoxCollider, Physics, PlayerController
from .systems import PhysicsSystem, collision_system, player_system

__all__ = [
    "PlayerController",
    "Physics",
    "BoxCollider",
    "PhysicsSystem",
    "collision_system",
    "player_system",
]
