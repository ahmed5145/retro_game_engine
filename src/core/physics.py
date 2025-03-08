"""Core physics system implementation."""
from dataclasses import dataclass, field
from typing import Tuple, Optional
import pygame
from .vector2d import Vector2D

@dataclass
class PhysicsConfig:
    """Configuration for physics behavior."""
    gravity: Vector2D = field(default_factory=lambda: Vector2D(0.0, 980.0))
    max_velocity: Vector2D = field(default_factory=lambda: Vector2D(500.0, 1000.0))
    friction: float = 0.8  # Friction coefficient (0 to 1)
    bounce: float = 0.0  # Bounce coefficient (0 to 1)

@dataclass
class PhysicsState:
    """Current state of a physics object."""
    position: Vector2D = field(default_factory=Vector2D)
    velocity: Vector2D = field(default_factory=Vector2D)
    acceleration: Vector2D = field(default_factory=Vector2D)
    grounded: bool = False

class PhysicsBody:
    """A physical body with basic physics properties."""

    def __init__(self, config: PhysicsConfig):
        """Initialize the physics body.
        
        Args:
            config: Physics configuration
        """
        self.config = config
        self.state = PhysicsState()
        self.collision_rect = pygame.Rect(0, 0, 32, 32)  # Default size

    def apply_force(self, force: Vector2D) -> None:
        """Apply a force to the body.
        
        Args:
            force: Force vector to apply
        """
        self.state.acceleration += force

    def set_velocity(self, velocity: Vector2D) -> None:
        """Set the velocity directly.
        
        Args:
            velocity: New velocity vector
        """
        # Clamp each component separately
        self.state.velocity = Vector2D(
            min(abs(velocity.x), self.config.max_velocity.x) * (1 if velocity.x > 0 else -1),
            min(abs(velocity.y), self.config.max_velocity.y) * (1 if velocity.y > 0 else -1)
        )

    def update(self, dt: float) -> None:
        """Update physics state.
        
        Args:
            dt: Time step in seconds
        """
        # Store initial velocity for position update
        initial_velocity = Vector2D(self.state.velocity.x, self.state.velocity.y)

        # Apply gravity
        self.state.acceleration += self.config.gravity

        # Update velocity with acceleration
        self.state.velocity += self.state.acceleration * dt

        # Apply friction if grounded
        if self.state.grounded:
            friction = Vector2D(self.state.velocity.x * -self.config.friction, 0)
            self.state.velocity += friction * dt

        # Clamp velocity to maximum
        self.state.velocity = Vector2D(
            min(abs(self.state.velocity.x), self.config.max_velocity.x) * (1 if self.state.velocity.x > 0 else -1),
            min(abs(self.state.velocity.y), self.config.max_velocity.y) * (1 if self.state.velocity.y > 0 else -1)
        )

        # Update position using average velocity
        average_velocity = (initial_velocity + self.state.velocity) * 0.5
        self.state.position += average_velocity * dt

        # Update collision rect position
        self.collision_rect.x = int(self.state.position.x)
        self.collision_rect.y = int(self.state.position.y)

        # Reset acceleration (forces are accumulated each frame)
        self.state.acceleration = Vector2D()

    def handle_collision(self, normal: Vector2D, penetration: float) -> None:
        """Handle collision response.
        
        Args:
            normal: Surface normal of the collision
            penetration: Penetration depth
        """
        # Resolve penetration
        self.state.position += normal * penetration

        # Calculate bounce
        bounced = False
        if self.config.bounce > 0:
            # Project velocity onto normal
            dot = self.state.velocity.dot(normal)

            # Only bounce if moving into the surface
            if dot < 0:
                # Calculate normal component of velocity
                normal_velocity = normal * dot
                # Calculate parallel component of velocity
                parallel_velocity = self.state.velocity - normal_velocity
                # Reflect normal component and scale by bounce
                reflected_normal = normal_velocity * -self.config.bounce
                # Combine parallel and reflected normal components
                self.state.velocity = parallel_velocity + reflected_normal
                bounced = True

        # Check if this collision makes us grounded
        # Only ground if not bouncing
        if not bounced and normal.y < -0.7:  # About 45 degrees
            self.state.grounded = True
            self.state.velocity.y = 0  # Stop vertical movement
