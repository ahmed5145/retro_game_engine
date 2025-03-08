"""Core tilemap system implementation."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import pygame
from .sprite import SpriteSheet
from .vector2d import Vector2D

@dataclass
class TileConfig:
    """Configuration for a tile."""
    solid: bool = False  # Whether the tile blocks movement
    animated: bool = False  # Whether the tile is animated
    frames: List[int] = field(default_factory=list)  # Frame indices for animation
    frame_duration: float = 0.1  # Duration of each frame in seconds
    auto_tile: bool = False  # Whether the tile participates in auto-tiling
    auto_tile_group: str = ""  # Group for auto-tiling (e.g., "ground", "water")
    current_frame: int = 0
    frame_timer: float = 0.0

@dataclass
class TileLayerConfig:
    """Configuration for a tile layer."""
    z_index: int = 0  # Rendering order
    scroll_factor_x: float = 1.0  # Parallax scrolling factor
    scroll_factor_y: float = 1.0
    visible: bool = True
    opacity: int = 255
    parallax: Vector2D = field(default_factory=lambda: Vector2D(1.0, 1.0))

class TileLayer:
    """A single layer of tiles."""

    def __init__(self, width: int, height: int, config: Optional[TileLayerConfig] = None):
        """Initialize the tile layer.
        
        Args:
            width: Width of the layer in tiles
            height: Height of the layer in tiles
            config: Layer configuration (default: None)
        """
        self.width = width
        self.height = height
        self.config = config or TileLayerConfig()
        self.tiles: List[List[Optional[int]]] = [[None] * width for _ in range(height)]
        self.dirty = True  # Whether the layer needs to be redrawn
        self._cache: Optional[pygame.Surface] = None

    def set_tile(self, x: int, y: int, tile_id: Optional[int]) -> None:
        """Set a tile at the given position.
        
        Args:
            x: X coordinate in tiles
            y: Y coordinate in tiles
            tile_id: ID of the tile to set, or None to clear
            
        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Tile coordinates out of bounds")
        self.tiles[y][x] = tile_id
        self.dirty = True

    def get_tile(self, x: int, y: int) -> Optional[int]:
        """Get the tile at the given position.
        
        Args:
            x: X coordinate in tiles
            y: Y coordinate in tiles
            
        Returns:
            The tile ID, or None if empty
            
        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Tile coordinates out of bounds")
        return self.tiles[y][x]

    def clear(self) -> None:
        """Clear all tiles from the layer."""
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = None
        self.dirty = True

    def fill(self, tile_id: int) -> None:
        """Fill the entire layer with a tile.
        
        Args:
            tile_id: ID of the tile to fill with
        """
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = tile_id
        self.dirty = True

class Tilemap:
    """Manages multiple tile layers and provides efficient rendering."""

    def __init__(self, tile_width: int, tile_height: int, tileset: SpriteSheet):
        """Initialize the tilemap.
        
        Args:
            tile_width: Width of each tile in pixels
            tile_height: Height of each tile in pixels
            tileset: SpriteSheet containing the tiles
        """
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tileset = tileset
        self.layers: Dict[str, TileLayer] = {}
        self.tile_configs: Dict[int, TileConfig] = {}
        self.time = 0.0  # Time for animated tiles
        self._width = 0  # Maximum width of all layers
        self._height = 0  # Maximum height of all layers
        self.collision_layer: Optional[str] = None  # Name of layer to use for collisions

    @property
    def width(self) -> int:
        """Get the width of the tilemap in tiles."""
        return max((layer.width for layer in self.layers.values()), default=0)

    @property
    def height(self) -> int:
        """Get the height of the tilemap in tiles."""
        return max((layer.height for layer in self.layers.values()), default=0)

    def add_layer(self, name: str, width: int, height: int,
                 config: Optional[TileLayerConfig] = None) -> None:
        """Add a new tile layer.
        
        Args:
            name: Name of the layer
            width: Width of the layer in tiles
            height: Height of the layer in tiles
            config: Layer configuration (default: None)
            
        Raises:
            ValueError: If layer already exists
        """
        if name in self.layers:
            raise ValueError(f"Layer '{name}' already exists")
        self.layers[name] = TileLayer(width, height, config)

    def remove_layer(self, name: str) -> None:
        """Remove a tile layer.
        
        Args:
            name: Name of the layer to remove
        """
        if name in self.layers:
            del self.layers[name]

    def get_layer(self, name: str) -> TileLayer:
        """Get a tile layer by name.
        
        Args:
            name: Name of the layer
            
        Returns:
            The requested layer
            
        Raises:
            KeyError: If layer doesn't exist
        """
        if name not in self.layers:
            raise KeyError(f"Layer '{name}' not found")
        return self.layers[name]

    def set_tile_config(self, tile_id: int, config: TileConfig) -> None:
        """Set the configuration for a tile type.
        
        Args:
            tile_id: ID of the tile
            config: Configuration for the tile
        """
        self.tile_configs[tile_id] = config

    def get_tile_config(self, tile_id: int) -> Optional[TileConfig]:
        """Get the configuration for a tile type.
        
        Args:
            tile_id: ID of the tile
            
        Returns:
            The tile configuration, or None if not configured
        """
        return self.tile_configs.get(tile_id)

    def update(self, dt: float) -> None:
        """Update animated tiles.
        
        Args:
            dt: Time elapsed since last update in seconds
        """
        self.time += dt

        # Find the longest animation cycle
        max_duration = 0.0
        for config in self.tile_configs.values():
            if config.animated and config.frames:
                cycle_duration = config.frame_duration * len(config.frames)
                max_duration = max(max_duration, cycle_duration)

        # Wrap time around the longest cycle to prevent floating point issues
        if max_duration > 0:
            self.time = self.time % max_duration

    def _get_visible_range(self, camera_x: int, camera_y: int,
                        view_width: int, view_height: int) -> Tuple[int, int, int, int]:
        """Calculate the range of tiles visible in the view.
        
        Args:
            camera_x: Camera X position in pixels
            camera_y: Camera Y position in pixels
            view_width: Width of the view in pixels
            view_height: Height of the view in pixels
            
        Returns:
            Tuple of (start_x, start_y, end_x, end_y) tile coordinates
        """
        # Convert camera position to tile coordinates
        start_x = max(0, camera_x // self.tile_width)
        start_y = max(0, camera_y // self.tile_height)

        # Calculate end coordinates (add 1 to account for partial tiles)
        tiles_x = (view_width + (camera_x % self.tile_width) + self.tile_width - 1) // self.tile_width
        tiles_y = (view_height + (camera_y % self.tile_height) + self.tile_height - 1) // self.tile_height
        end_x = min(self.width, start_x + tiles_x)
        end_y = min(self.height, start_y + tiles_y)

        return start_x, start_y, end_x, end_y

    def render(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0) -> None:
        """Render the tilemap with culling of off-screen tiles.
        
        Args:
            surface: Surface to render to
            camera_x: Camera X position in pixels (default: 0)
            camera_y: Camera Y position in pixels (default: 0)
        """
        # Get visible range of tiles
        view_width = surface.get_width()
        view_height = surface.get_height()
        start_x, start_y, end_x, end_y = self._get_visible_range(
            camera_x, camera_y, view_width, view_height
        )

        # Sort layers by z-index
        sorted_layers = sorted(
            self.layers.items(),
            key=lambda x: x[1].config.z_index
        )

        # Render each layer
        for _, layer in sorted_layers:
            if not layer.config.visible:
                continue

            # Apply parallax scrolling
            scroll_x = int(camera_x * layer.config.parallax.x)
            scroll_y = int(camera_y * layer.config.parallax.y)

            # Render visible tiles
            for y in range(start_y, end_y):
                if y >= layer.height:
                    break

                for x in range(start_x, end_x):
                    if x >= layer.width:
                        break

                    tile_id = layer.tiles[y][x]
                    if tile_id is None:
                        continue

                    # Get current frame for animated tiles
                    config = self.tile_configs.get(tile_id)
                    if config and config.animated and config.frames:
                        frame_index = int(self.time / config.frame_duration) % len(config.frames)
                        tile_id = config.frames[frame_index]

                    # Skip invalid tile IDs
                    if tile_id >= len(self.tileset.frames):
                        continue

                    # Calculate screen position
                    screen_x = x * self.tile_width - scroll_x
                    screen_y = y * self.tile_height - scroll_y

                    # Get the frame rectangle
                    frame = self.tileset.frames[tile_id]

                    # Create temporary surface for the tile with alpha
                    tile_surface = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
                    tile_surface.blit(
                        self.tileset.texture,
                        (0, 0),
                        (frame.x, frame.y, frame.width, frame.height)
                    )

                    # Apply layer opacity
                    if layer.config.opacity < 255:
                        tile_surface.set_alpha(layer.config.opacity)

                    # Draw the tile
                    surface.blit(tile_surface, (screen_x, screen_y))

    def set_collision_layer(self, layer_name: str) -> None:
        """Set which layer to use for collision detection.
        
        Args:
            layer_name: Name of the layer to use for collisions
            
        Raises:
            KeyError: If layer doesn't exist
        """
        if layer_name not in self.layers:
            raise KeyError(f"Layer '{layer_name}' not found")
        self.collision_layer = layer_name

    def get_tile_at_position(self, x: float, y: float) -> Tuple[Optional[int], str]:
        """Get the tile at a world position.
        
        Args:
            x: X coordinate in pixels
            y: Y coordinate in pixels
            
        Returns:
            Tuple of (tile_id, layer_name) or (None, "") if no tile
        """
        # Convert to tile coordinates
        tile_x = int(x // self.tile_width)
        tile_y = int(y // self.tile_height)

        # Check each layer from top to bottom
        for name, layer in sorted(
            self.layers.items(),
            key=lambda x: x[1].config.z_index,
            reverse=True
        ):
            if not layer.config.visible:
                continue

            try:
                tile_id = layer.get_tile(tile_x, tile_y)
                if tile_id is not None:
                    return tile_id, name
            except IndexError:
                continue

        return None, ""

    def get_solid_tiles_in_rect(self, rect: pygame.Rect) -> List[Tuple[pygame.Rect, Vector2D]]:
        """Get all solid tiles that intersect with the given rectangle."""
        if not self.collision_layer:
            return []

        layer = self.layers[self.collision_layer]
        solid_tiles = []

        # Convert rect to tile coordinates
        start_x = max(0, rect.left // self.tile_width)
        start_y = max(0, rect.top // self.tile_height)
        end_x = min(layer.width, (rect.right + self.tile_width - 1) // self.tile_width)
        end_y = min(layer.height, (rect.bottom + self.tile_height - 1) // self.tile_height)

        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                tile = layer.get_tile(x, y)
                if tile is not None and self.tile_configs.get(tile, TileConfig()).solid:
                    tile_rect = pygame.Rect(x * self.tile_width, y * self.tile_height, 
                                          self.tile_width, self.tile_height)
                    if rect.colliderect(tile_rect):
                        # Calculate intersection
                        intersection = rect.clip(tile_rect)
                        
                        # Calculate the relative position of the rectangles' centers
                        dx = rect.centerx - tile_rect.centerx
                        dy = rect.centery - tile_rect.centery
                        
                        # For equal intersections, we want to prioritize horizontal collisions
                        # and use the relative position to determine the direction
                        if abs(dx) >= abs(dy):
                            # Horizontal collision - normal points in the opposite direction of dx
                            if dx > 0:
                                normal = Vector2D(-1.0, 0.0)  # Push left
                            else:
                                normal = Vector2D(1.0, 0.0)  # Push right
                        else:
                            # Vertical collision - normal points in the opposite direction of dy
                            if dy > 0:
                                normal = Vector2D(0.0, -1.0)  # Push up
                            else:
                                normal = Vector2D(0.0, 1.0)  # Push down
                        
                        solid_tiles.append((tile_rect, normal))

        return solid_tiles

    def check_collision(self, rect: pygame.Rect) -> Optional[Tuple[Vector2D, float]]:
        """Check for collision with solid tiles.
        
        Args:
            rect: Rectangle in world coordinates
            
        Returns:
            Tuple of (surface_normal, penetration) or None if no collision
        """
        solid_tiles = self.get_solid_tiles_in_rect(rect)
        if not solid_tiles:
            return None

        # Find the collision with the smallest penetration
        min_penetration = float('inf')
        collision_normal = Vector2D()

        for tile_rect, normal in solid_tiles:
            # Calculate penetration depth
            if normal.x != 0:  # Horizontal collision
                penetration = (rect.width + tile_rect.width) / 2 - abs(rect.centerx - tile_rect.centerx)
            else:  # Vertical collision
                penetration = (rect.height + tile_rect.height) / 2 - abs(rect.centery - tile_rect.centery)

            if penetration < min_penetration:
                min_penetration = penetration
                collision_normal = normal

        return (collision_normal, min_penetration) if min_penetration < float('inf') else None
