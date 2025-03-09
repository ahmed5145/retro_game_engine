# Vector2D

A 2D vector implementation for handling positions, velocities, and other 2D quantities.

## Vector2D

```python
@dataclass
class Vector2D:
    x: float = 0.0
    y: float = 0.0
```

### Methods

#### __add__()
```python
def __add__(self, other: Vector2D) -> Vector2D
```
Add two vectors together.

#### __sub__()
```python
def __sub__(self, other: Vector2D) -> Vector2D
```
Subtract one vector from another.

#### __mul__()
```python
def __mul__(self, scalar: float) -> Vector2D
```
Multiply vector by a scalar.

#### __truediv__()
```python
def __truediv__(self, scalar: float) -> Vector2D
```
Divide vector by a scalar.

#### magnitude()
```python
def magnitude(self) -> float
```
Calculate the magnitude (length) of the vector.

#### normalize()
```python
def normalize(self) -> Vector2D
```
Return a normalized copy of this vector.

#### clamp()
```python
def clamp(self, max_magnitude: float) -> Vector2D
```
Clamp the vector's magnitude to a maximum value.

#### dot()
```python
def dot(self, other: Vector2D) -> float
```
Calculate dot product with another vector.

## Example Usage

```python
# Create vectors
pos = Vector2D(100.0, 200.0)
velocity = Vector2D(5.0, -3.0)

# Vector arithmetic
new_pos = pos + velocity * dt

# Normalization
direction = velocity.normalize()

# Magnitude
speed = velocity.magnitude()

# Clamping
clamped_velocity = velocity.clamp(max_speed)

# Dot product
angle_cos = direction.dot(Vector2D(1.0, 0.0))
```

## Best Practices

1. **Performance**:
   - Cache vector calculations when possible
   - Use in-place operations for frequent updates
   - Consider using integers for pixel-perfect positioning

2. **Precision**:
   - Be aware of floating-point precision issues
   - Use appropriate epsilon values for comparisons
   - Consider rounding for pixel alignment

3. **Memory**:
   - Reuse vector objects when possible
   - Use pooling for frequently created/destroyed vectors
   - Clear vector references when no longer needed

## Common Issues

### Precision
- Floating-point rounding errors
- Integer vs. float position mismatches
- Accumulating errors in physics calculations

### Performance
- Unnecessary vector allocations
- Frequent magnitude calculations
- Redundant normalizations

### Logic
- Division by zero in normalization
- Incorrect vector math operations
- Missing vector cleanup
