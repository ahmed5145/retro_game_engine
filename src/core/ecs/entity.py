"""Entity class for the Entity Component System."""
from typing import Any, Dict, Optional, Type, TypeVar
from uuid import uuid4

from .component import Component

T = TypeVar("T", bound=Component)


class Entity:
    """An entity in the game world.

    Entities are containers for components that define their behavior and properties.
    They have no functionality of their own and serve primarily as an ID to group
    related components together.
    """

    def __init__(self, name: str = "") -> None:
        """Initialize the entity.

        Args:
            name: Optional name for the entity (default: "")
        """
        self.id = str(uuid4())  # Unique identifier
        self.name = name or f"Entity_{self.id[:8]}"
        self._components: Dict[Type[Component], Component] = {}
        self._enabled: bool = True
        self._parent: Optional["Entity"] = None
        self._children: Dict[str, "Entity"] = {}

    @property
    def enabled(self) -> bool:
        """Check if the entity is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable the entity."""
        self._enabled = value

    def add_component(self, component: Component) -> None:
        """Add a component to the entity.

        Args:
            component: Component instance to add

        Raises:
            ValueError: If component type is already attached
        """
        component_type = type(component)
        if component_type in self._components:
            raise ValueError(
                f"Entity already has component of type {component_type.__name__}"
            )

        self._components[component_type] = component
        component.entity = self
        component.on_attach()

    def remove_component(self, component_type: Type[T]) -> None:
        """Remove a component from the entity.

        Args:
            component_type: Type of component to remove
        """
        if component_type in self._components:
            component = self._components[component_type]
            component.on_detach()
            component.entity = None
            del self._components[component_type]

    def get_component(self, component_type: Type[T]) -> Optional[T]:
        """Get a component of the specified type.

        Args:
            component_type: Type of component to get

        Returns:
            Component instance if found, None otherwise
        """
        return self._components.get(component_type)  # type: ignore

    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if entity has a component of the specified type.

        Args:
            component_type: Type of component to check for

        Returns:
            True if entity has component, False otherwise
        """
        return component_type in self._components

    def set_parent(self, parent: Optional["Entity"]) -> None:
        """Set the parent entity.

        Args:
            parent: Parent entity or None to clear parent
        """
        if self._parent == parent:
            return

        # Remove from old parent
        if self._parent is not None:
            self._parent._children.pop(self.id, None)

        # Set new parent
        self._parent = parent
        if parent is not None:
            parent._children[self.id] = self

    def add_child(self, child: "Entity") -> None:
        """Add a child entity.

        Args:
            child: Entity to add as child
        """
        child.set_parent(self)

    def remove_child(self, child: "Entity") -> None:
        """Remove a child entity.

        Args:
            child: Entity to remove
        """
        if child.id in self._children:
            child.set_parent(None)

    @property
    def parent(self) -> Optional["Entity"]:
        """Get the parent entity."""
        return self._parent

    @property
    def children(self) -> Dict[str, "Entity"]:
        """Get all child entities."""
        return self._children.copy()

    def __repr__(self) -> str:
        """Get string representation of the entity."""
        components = ", ".join(c.__class__.__name__ for c in self._components.values())
        return f"Entity(name='{self.name}', components=[{components}])"
