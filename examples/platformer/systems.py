"""Systems for the platformer example."""
import pygame

from examples.platformer.components import BoxCollider, Physics, PlayerController
from src.core.ecs import World
from src.core.ecs.components import Transform
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


def physics_system(world: World, dt: float) -> None:
    """Update physics for all entities with Physics component.

    Args:
        world: Game world instance
        dt: Delta time in seconds
    """
    SCREEN_WIDTH = 800  # Match the window size
    SCREEN_HEIGHT = 600

    for entity in world.get_entities_with_component(Physics):
        physics = entity.get_component(Physics)
        transform = entity.get_component(Transform)
        collider = entity.get_component(BoxCollider)

        if not physics or not transform or not collider:
            continue

        # Apply gravity
        physics.velocity.y += physics.gravity * dt

        # Update position
        transform.position.x += physics.velocity.x * dt
        transform.position.y += physics.velocity.y * dt

        # Screen bounds checking
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


def collision_system(world: World, dt: float) -> None:
    """Handle collision detection and response.

    Args:
        world: Game world instance
        dt: Delta time in seconds
    """
    # Get all dynamic colliders
    dynamic_entities = [
        entity
        for entity in world.get_entities_with_component(BoxCollider)
        if entity.get_component(BoxCollider)
        and not entity.get_component(BoxCollider).is_static
    ]

    # Get all static colliders
    static_entities = [
        entity
        for entity in world.get_entities_with_component(BoxCollider)
        if entity.get_component(BoxCollider)
        and entity.get_component(BoxCollider).is_static
    ]

    # Check collisions between dynamic and static entities
    for dynamic in dynamic_entities:
        d_transform = dynamic.get_component(Transform)
        d_collider = dynamic.get_component(BoxCollider)
        d_physics = dynamic.get_component(Physics)

        if not d_transform or not d_collider or not d_physics:
            continue

        # Create dynamic entity rect
        d_rect = pygame.Rect(
            d_transform.position.x - d_collider.width / 2,
            d_transform.position.y - d_collider.height / 2,
            d_collider.width,
            d_collider.height,
        )

        # Store initial position
        initial_pos = Vector2D(d_transform.position.x, d_transform.position.y)

        for static in static_entities:
            s_transform = static.get_component(Transform)
            s_collider = static.get_component(BoxCollider)

            if not s_transform or not s_collider:
                continue

            # Create static entity rect
            s_rect = pygame.Rect(
                s_transform.position.x - s_collider.width / 2,
                s_transform.position.y - s_collider.height / 2,
                s_collider.width,
                s_collider.height,
            )

            # Check collision
            if d_rect.colliderect(s_rect):
                # Calculate overlap
                dx = d_rect.centerx - s_rect.centerx
                dy = d_rect.centery - s_rect.centery

                if abs(dx) > abs(dy):
                    # Horizontal collision
                    if dx > 0:
                        d_transform.position.x = s_rect.right + d_collider.width / 2
                    else:
                        d_transform.position.x = s_rect.left - d_collider.width / 2
                    d_physics.velocity.x = 0
                else:
                    # Vertical collision
                    if dy > 0:
                        d_transform.position.y = s_rect.bottom + d_collider.height / 2
                        d_physics.velocity.y = 0
                    else:
                        d_transform.position.y = s_rect.top - d_collider.height / 2
                        d_physics.velocity.y = 0
                        # Allow jumping when on ground
                        controller = dynamic.get_component(PlayerController)
                        if controller:
                            controller.can_jump = True
