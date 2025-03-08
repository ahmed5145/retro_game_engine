"""Tests for the physics system."""
import pytest
from src.core.physics import Vector2D, PhysicsConfig, PhysicsState, PhysicsBody

def test_vector_operations() -> None:
    """Test vector arithmetic operations."""
    v1 = Vector2D(1.0, 2.0)
    v2 = Vector2D(3.0, 4.0)

    # Addition
    result = v1 + v2
    assert result.x == 4.0
    assert result.y == 6.0

    # Subtraction
    result = v2 - v1
    assert result.x == 2.0
    assert result.y == 2.0

    # Scalar multiplication
    result = v1 * 2.0
    assert result.x == 2.0
    assert result.y == 4.0

    # Division
    result = v2 / 2.0
    assert result.x == 1.5
    assert result.y == 2.0

    # Division by zero
    with pytest.raises(ValueError):
        v1 / 0.0

def test_vector_magnitude() -> None:
    """Test vector magnitude calculation."""
    v = Vector2D(3.0, 4.0)
    assert v.magnitude() == 5.0  # 3-4-5 triangle

def test_vector_normalize() -> None:
    """Test vector normalization."""
    v = Vector2D(3.0, 4.0)
    normalized = v.normalize()
    assert abs(normalized.magnitude() - 1.0) < 0.0001  # Account for floating point

    # Test normalizing zero vector
    v = Vector2D(0.0, 0.0)
    normalized = v.normalize()
    assert normalized.x == 0.0
    assert normalized.y == 0.0

def test_vector_clamp() -> None:
    """Test vector magnitude clamping."""
    v = Vector2D(3.0, 4.0)  # Magnitude 5
    clamped = v.clamp(2.5)  # Should halve the magnitude
    assert abs(clamped.magnitude() - 2.5) < 0.0001

    # Test clamping vector below max
    v = Vector2D(1.0, 0.0)
    clamped = v.clamp(2.0)
    assert clamped.x == 1.0
    assert clamped.y == 0.0

def test_physics_config() -> None:
    """Test physics configuration."""
    config = PhysicsConfig()
    assert config.gravity.y > 0  # Positive is down
    assert config.max_velocity.x > 0
    assert config.max_velocity.y > 0
    assert 0 <= config.friction <= 1
    assert config.bounce >= 0

def test_physics_state() -> None:
    """Test physics state initialization."""
    state = PhysicsState()
    assert state.position.x == 0.0
    assert state.position.y == 0.0
    assert state.velocity.x == 0.0
    assert state.velocity.y == 0.0
    assert state.acceleration.x == 0.0
    assert state.acceleration.y == 0.0
    assert not state.grounded

def test_physics_body_initialization() -> None:
    """Test physics body initialization."""
    config = PhysicsConfig()
    body = PhysicsBody(config)
    assert body.config == config
    assert isinstance(body.state, PhysicsState)

def test_physics_apply_force() -> None:
    """Test applying forces to physics body."""
    body = PhysicsBody(PhysicsConfig())
    force = Vector2D(10.0, -20.0)
    body.apply_force(force)
    assert body.state.acceleration.x == 10.0
    assert body.state.acceleration.y == -20.0

def test_physics_set_velocity() -> None:
    """Test setting velocity with clamping."""
    config = PhysicsConfig(max_velocity=Vector2D(100.0, 100.0))
    body = PhysicsBody(config)

    # Test within limits
    body.set_velocity(Vector2D(50.0, 50.0))
    assert body.state.velocity.x == 50.0
    assert body.state.velocity.y == 50.0

    # Test exceeding limits
    body.set_velocity(Vector2D(200.0, 200.0))
    assert body.state.velocity.x == 100.0  # Clamped to max
    assert body.state.velocity.y == 100.0  # Clamped to max

def test_physics_update() -> None:
    """Test physics update step."""
    config = PhysicsConfig(
        gravity=Vector2D(0.0, 10.0),
        max_velocity=Vector2D(100.0, 100.0),
        friction=0.5
    )
    body = PhysicsBody(config)

    # Test gravity
    body.update(1.0)  # 1 second
    assert body.state.velocity.y == 10.0
    assert abs(body.state.position.y - 5.0) < 0.0001  # Half acceleration * t^2

    # Test friction when grounded
    body.state.velocity = Vector2D(10.0, 0.0)
    body.state.grounded = True
    body.update(1.0)
    assert body.state.velocity.x < 10.0  # Should decrease due to friction

def test_physics_collision() -> None:
    """Test collision response."""
    config = PhysicsConfig(bounce=0.5)
    body = PhysicsBody(config)

    # Set up a collision with the ground
    body.state.velocity = Vector2D(0.0, 10.0)
    normal = Vector2D(0.0, -1.0)  # Ground normal
    penetration = 2.0

    body.handle_collision(normal, penetration)

    # Check position correction
    assert body.state.position.y == -2.0  # Moved up by penetration

    # Check bounce
    assert body.state.velocity.y == -5.0  # Should bounce upward with half velocity
    assert not body.state.grounded  # Should not be grounded during bounce

    # After bounce is complete (velocity is upward), object should not be grounded
    body.state.velocity = Vector2D(0.0, 0.0)  # Zero velocity
    body.handle_collision(normal, 0.0)  # Another collision with no penetration
    assert body.state.grounded  # Now should be grounded since not bouncing

def test_physics_integration() -> None:
    """Test complete physics integration."""
    config = PhysicsConfig(
        gravity=Vector2D(0.0, 10.0),
        max_velocity=Vector2D(100.0, 100.0),
        friction=0.5,
        bounce=0.5
    )
    body = PhysicsBody(config)

    # Apply initial velocity
    body.set_velocity(Vector2D(5.0, -10.0))

    # Simulate for a few frames
    for _ in range(10):
        body.update(0.016)  # 60 FPS

    # Object should have moved and been affected by gravity
    assert body.state.position.x > 0
    assert body.state.position.y != 0
    assert body.state.velocity.y > -10.0  # Should have slowed down upward velocity 