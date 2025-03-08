"""2D vector implementation."""
from dataclasses import dataclass
from typing import cast

@dataclass
class Vector2D:
    """2D vector with basic operations."""
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'Vector2D':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector."""
        return cast(float, (self.x * self.x + self.y * self.y) ** 0.5)

    def normalize(self) -> 'Vector2D':
        """Return a normalized copy of this vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D()
        return self / mag

    def clamp(self, max_magnitude: float) -> 'Vector2D':
        """Clamp the vector's magnitude to a maximum value."""
        mag = self.magnitude()
        if mag > max_magnitude:
            return self * (max_magnitude / mag)
        return Vector2D(self.x, self.y)

    def dot(self, other: 'Vector2D') -> float:
        """Calculate dot product with another vector."""
        return self.x * other.x + self.y * other.y
