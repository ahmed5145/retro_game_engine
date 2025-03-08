"""World class for the Entity Component System."""
from typing import Callable, Dict, List, Optional, Set, Type, TypeVar

from .component import Component
from .entity import Entity

T = TypeVar("T", bound=Component)


class World:
    """A container for all entities and systems in the game.

    The World class manages the lifecycle of entities and coordinates
    system updates. It provides methods for entity creation, querying,
    and cleanup.
    """

    def __init__(self) -> None:
        """Initialize the world."""
        self._entities: Dict[str, Entity] = {}
        self._systems: List[Callable[[float], None]] = []
        self._component_cache: Dict[Type[Component], Set[Entity]] = {}
        self._pending_removal: Set[str] = set()

    def create_entity(self, name: str = "") -> Entity:
        """Create a new entity in the world.

        Args:
            name: Optional name for the entity (default: "")

        Returns:
            The created entity
        """
        entity = Entity(name)
        self._entities[entity.id] = entity
        return entity

    def remove_entity(self, entity: Entity) -> None:
        """Mark an entity for removal.

        The entity will be actually removed during the next cleanup phase.

        Args:
            entity: Entity to remove
        """
        self._pending_removal.add(entity.id)

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by its ID.

        Args:
            entity_id: ID of the entity to get

        Returns:
            Entity if found, None otherwise
        """
        return self._entities.get(entity_id)

    def add_system(self, system: Callable[[float], None]) -> None:
        """Add a system to the world.

        Systems are functions that operate on entities and components
        during the update phase.

        Args:
            system: Function that takes delta time as argument
        """
        self._systems.append(system)

    def get_entities_with_component(self, component_type: Type[T]) -> Set[Entity]:
        """Get all entities that have a specific component type.

        Args:
            component_type: Type of component to query for

        Returns:
            Set of entities with the component
        """
        # Check cache first
        if component_type in self._component_cache:
            return self._component_cache[component_type]

        # Build cache
        entities = {
            entity
            for entity in self._entities.values()
            if entity.has_component(component_type)
        }
        self._component_cache[component_type] = entities
        return entities

    def _cleanup(self) -> None:
        """Remove pending entities and clear caches."""
        if not self._pending_removal:
            return

        # Remove entities
        for entity_id in self._pending_removal:
            if entity := self._entities.pop(entity_id, None):
                # Remove from parent if any
                if entity.parent:
                    entity.set_parent(None)

                # Detach all children
                for child in list(entity.children.values()):
                    child.set_parent(None)

        # Clear component cache as it might be invalid
        self._component_cache.clear()
        self._pending_removal.clear()

    def update(self, dt: float) -> None:
        """Update all systems.

        Args:
            dt: Delta time in seconds
        """
        # Run systems
        for system in self._systems:
            system(dt)

        # Cleanup removed entities
        self._cleanup()

    def clear(self) -> None:
        """Remove all entities from the world."""
        self._entities.clear()
        self._component_cache.clear()
        self._pending_removal.clear()
