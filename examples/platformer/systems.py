"""Systems for the platformer example."""
from typing import List, Optional, Tuple, TypeGuard, cast

import pygame

from examples.platformer.components import BoxCollider, Physics, PlayerController
from src.core.ecs.components import Transform
from src.core.ecs.world import Entity, World
from src.core.vector2d import Vector2D


def player_system(world: World, dt: float) -> None:
    """Handle player input and movement.

    Args:
        world: Game world instance
        dt: Delta time in seconds
    """
    keys = pygame.key.get_pressed()

    for entity in world.get_entities_with_component(PlayerController):
        controller = entity.get_component(PlayerController)
        physics = entity.get_component(Physics)

        if not controller or not physics:
            continue

        # Horizontal movement
        move_dir = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir -= 1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir += 1.0

        # Set horizontal velocity directly
        physics.velocity.x = move_dir * controller.move_speed

        # Jumping
        if controller.can_jump and (
            keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        ):
            physics.velocity.y = -controller.jump_force
            controller.can_jump = False


def is_static_box_collider(collider: Optional[BoxCollider]) -> TypeGuard[BoxCollider]:
    """Check if a value is a static BoxCollider.

    Args:
        collider: The value to check.

    Returns:
        bool: True if the value is a static BoxCollider, False otherwise.
    """
    return isinstance(collider, BoxCollider) and collider.is_static


def is_box_collider(collider: Optional[BoxCollider]) -> TypeGuard[BoxCollider]:
    """Check if a value is a BoxCollider.

    Args:
        collider: The value to check.

    Returns:
        bool: True if the value is a BoxCollider, False otherwise.
    """
    return isinstance(collider, BoxCollider)


class PhysicsSystem:
    def __init__(self, gravity: float = 9.81) -> None:
        self.gravity = gravity

    def update(self, world: World, delta_time: float) -> None:
        """Update the physics system."""
        # Update physics for each entity with a physics body
        for entity in world.get_entities_with_component(Physics):
            physics = entity.get_component(Physics)
            collider = entity.get_component(BoxCollider)
            transform = entity.get_component(Transform)

            if not physics or not collider or not transform:
                continue

            # Type narrowing
            if not is_box_collider(collider):
                continue

            # Apply gravity if not static
            if not collider.is_static:
                physics.velocity.y += self.gravity * delta_time

            # Update position based on velocity
            transform.position.x += physics.velocity.x * delta_time
            transform.position.y += physics.velocity.y * delta_time

            # Screen bounds checking
            SCREEN_WIDTH = 800  # Match the window size
            SCREEN_HEIGHT = 600
            half_width = collider.width / 2
            half_height = collider.height / 2

            # Left and right bounds
            if transform.position.x - half_width < 0:
                transform.position.x = half_width
                physics.velocity.x = 0
            elif transform.position.x + half_width > SCREEN_WIDTH:
                transform.position.x = SCREEN_WIDTH - half_width
                physics.velocity.x = 0

            # Top and bottom bounds
            if transform.position.y - half_height < 0:
                transform.position.y = half_height
                physics.velocity.y = 0
            elif transform.position.y + half_height > SCREEN_HEIGHT:
                transform.position.y = SCREEN_HEIGHT - half_height
                physics.velocity.y = 0

            # Check for collisions with static colliders
            for other in world.get_entities_with_component(BoxCollider):
                if entity == other:
                    continue

                other_collider = other.get_component(BoxCollider)
                if not other_collider:
                    continue

                # Type narrowing and static check
                if not is_static_box_collider(other_collider):
                    continue

                # Get collision info
                collision = self._check_collision(entity, other)
                if collision:
                    self._resolve_collision(entity, other, collision)

    def _check_collision(self, entity: Entity, other: Entity) -> Tuple[bool, Vector2D]:
        """Check for collision between two entities.

        Args:
            entity: The first entity.
            other: The second entity.

        Returns:
            Tuple[bool, Vector2D]: A tuple containing whether a collision occurred and the collision normal.
        """
        # Implement collision detection logic here
        return False, Vector2D(0, 0)

    def _resolve_collision(
        self, entity: Entity, other: Entity, collision: Tuple[bool, Vector2D]
    ) -> None:
        """Resolve collision between two entities.

        Args:
            entity: The first entity.
            other: The second entity.
            collision: The collision information.
        """
        # Implement collision resolution logic here
        pass


def get_dynamic_entities(world: World) -> List[Entity]:
    """Get all dynamic entities with box colliders.

    Args:
        world: Game world

    Returns:
        List of entities with dynamic box colliders
    """
    return [
        entity
        for entity in world.get_entities_with_component(BoxCollider)
        if (collider := entity.get_component(BoxCollider)) is not None
        and isinstance(collider, BoxCollider)
        and not collider.is_static
    ]


def get_static_entities(world: World) -> List[Entity]:
    """Get all static entities with box colliders.

    Args:
        world: Game world

    Returns:
        List of entities with static box colliders
    """
    return [
        entity
        for entity in world.get_entities_with_component(BoxCollider)
        if (collider := entity.get_component(BoxCollider)) is not None
        and isinstance(collider, BoxCollider)
        and collider.is_static
    ]


def collision_system(world: World, dt: float) -> None:
    """Handle collisions between entities.

    Args:
        world: Game world
        dt: Time delta in seconds
    """
    # Get dynamic and static entities
    dynamic_entities = get_dynamic_entities(world)
    static_entities = get_static_entities(world)

    # Check collisions between dynamic entities and static entities
    for dynamic in dynamic_entities:
        for static in static_entities:
            if dynamic == static:
                continue

            # Get colliders
            dynamic_collider = dynamic.get_component(BoxCollider)
            static_collider = static.get_component(BoxCollider)

            # Type guards ensure these are not None
            if not is_box_collider(dynamic_collider) or not is_static_box_collider(
                static_collider
            ):
                continue

            # Get transforms
            dynamic_transform = dynamic.get_component(Transform)
            static_transform = static.get_component(Transform)

            if not dynamic_transform or not static_transform:
                continue

            # Check for collision
            dynamic_rect = pygame.Rect(
                dynamic_transform.position.x - dynamic_collider.width / 2,
                dynamic_transform.position.y - dynamic_collider.height / 2,
                dynamic_collider.width,
                dynamic_collider.height,
            )

            static_rect = pygame.Rect(
                static_transform.position.x - static_collider.width / 2,
                static_transform.position.y - static_collider.height / 2,
                static_collider.width,
                static_collider.height,
            )

            if dynamic_rect.colliderect(static_rect):
                # Calculate collision normal and penetration
                dx = (dynamic_rect.centerx - static_rect.centerx) / (
                    static_collider.width / 2
                )
                dy = (dynamic_rect.centery - static_rect.centery) / (
                    static_collider.height / 2
                )

                if abs(dx) > abs(dy):
                    normal = Vector2D(1.0 if dx > 0 else -1.0, 0.0)
                    penetration = (
                        static_collider.width / 2
                        + dynamic_collider.width / 2
                        - abs(dynamic_rect.centerx - static_rect.centerx)
                    )
                else:
                    normal = Vector2D(0.0, 1.0 if dy > 0 else -1.0)
                    penetration = (
                        static_collider.height / 2
                        + dynamic_collider.height / 2
                        - abs(dynamic_rect.centery - static_rect.centery)
                    )

                # Get physics component
                physics = dynamic.get_component(Physics)
                if physics:
                    # Resolve collision
                    dynamic_transform.position += normal * penetration
                    if normal.y < 0:  # Hit from above
                        physics.velocity.y = 0
                        # Notify player controller if present
                        if controller := dynamic.get_component(PlayerController):
                            controller.can_jump = True
