"""Transform component for positioning entities in the game world."""
import math
from dataclasses import dataclass, field

from src.core.ecs import Component
from src.core.vector2d import Vector2D


@dataclass
class Transform(Component):
    """Component for handling entity position, rotation, and scale in 2D space.

    The Transform component defines where an entity is in the game world and
    how it is oriented. It supports basic 2D transformations including position,
    rotation (in degrees), and scale.
    """

    position: Vector2D = field(default_factory=Vector2D)
    rotation: float = 0.0  # Degrees, clockwise
    scale: Vector2D = field(default_factory=lambda: Vector2D(1.0, 1.0))
    local_position: Vector2D = field(default_factory=Vector2D)
    local_rotation: float = 0.0
    local_scale: Vector2D = field(default_factory=lambda: Vector2D(1.0, 1.0))

    def translate(self, offset: Vector2D) -> None:
        """Move the entity by the given offset.

        Args:
            offset: Vector to add to current position
        """
        self.position += offset

    def rotate(self, degrees: float) -> None:
        """Rotate the entity by the given angle.

        Args:
            degrees: Angle to add to current rotation (clockwise)
        """
        self.rotation = (self.rotation + degrees) % 360.0

    def set_scale(self, x: float, y: float) -> None:
        """Set the entity's scale.

        Args:
            x: Horizontal scale factor
            y: Vertical scale factor
        """
        self.scale = Vector2D(x, y)

    def get_world_position(self) -> Vector2D:
        """Calculate the world position considering parent transforms.

        Returns:
            World space position
        """
        if not self.entity or not self.entity.parent:
            return self.position + self.local_position

        parent_transform = self.entity.parent.get_component(Transform)
        if not parent_transform:
            return self.position + self.local_position

        # Get parent's world transform
        parent_pos = parent_transform.get_world_position()
        parent_rot = math.radians(parent_transform.get_world_rotation())
        parent_scale = parent_transform.get_world_scale()

        # Calculate rotated and scaled local position
        local_x = self.local_position.x * math.cos(
            parent_rot
        ) - self.local_position.y * math.sin(parent_rot)
        local_y = self.local_position.x * math.sin(
            parent_rot
        ) + self.local_position.y * math.cos(parent_rot)
        local_pos = Vector2D(local_x, local_y)

        # Apply parent scale to local position
        local_pos = Vector2D(local_pos.x * parent_scale.x, local_pos.y * parent_scale.y)

        # Calculate final position
        return parent_pos + local_pos + self.position

    def get_world_rotation(self) -> float:
        """Calculate the world rotation considering parent transforms.

        Returns:
            World space rotation in degrees
        """
        if not self.entity or not self.entity.parent:
            return self.rotation + self.local_rotation

        parent_transform = self.entity.parent.get_component(Transform)
        if not parent_transform:
            return self.rotation + self.local_rotation

        return (
            parent_transform.get_world_rotation() + self.rotation + self.local_rotation
        ) % 360.0

    def get_world_scale(self) -> Vector2D:
        """Calculate the world scale considering parent transforms.

        Returns:
            World space scale
        """
        if not self.entity or not self.entity.parent:
            return Vector2D(
                self.scale.x * self.local_scale.x, self.scale.y * self.local_scale.y
            )

        parent_transform = self.entity.parent.get_component(Transform)
        if not parent_transform:
            return Vector2D(
                self.scale.x * self.local_scale.x, self.scale.y * self.local_scale.y
            )

        parent_scale = parent_transform.get_world_scale()
        return Vector2D(
            parent_scale.x * self.scale.x * self.local_scale.x,
            parent_scale.y * self.scale.y * self.local_scale.y,
        )
