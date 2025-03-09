"""Entity class for the Entity Component System."""
from typing import Dict, Optional, Type, TypeVar
from uuid import uuid4

from .component import Component

T = TypeVar("T", bound=Component)


class Entity:
    """Base class for all game entities.

    An entity is a container for components that define its behavior and data.
    Each entity has a unique ID and can be part of a parent-child hierarchy.
    """

    def __init__(self, name: str = "") -> None:
        """Initialize the entity.

        Args:
            name: Optional name for the entity (default: auto-generated)
        """
        self.id = str(uuid4())
        self.name = name or f"Entity_{self.id[:8]}"
        self._components: Dict[Type[Component], Component] = {}
        self._children: Dict[str, "Entity"] = {}
        self._parent: Optional["Entity"] = None
        self._enabled = True

    @property
    def enabled(self) -> bool:
        """Get whether the entity is enabled.

        Returns:
            True if the entity is enabled
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether the entity is enabled.

        Args:
            value: True to enable, False to disable
        """
        self._enabled = value

    @property
    def components(self) -> Dict[Type[Component], Component]:
        """Get the components dictionary.

        Returns:
            Dictionary mapping component types to component instances
        """
        return self._components

    @property
    def children(self) -> Dict[str, "Entity"]:
        """Get the children dictionary.

        Returns:
            Dictionary mapping child IDs to child entities
        """
        return self._children

    @property
    def parent(self) -> Optional["Entity"]:
        """Get the parent entity.

        Returns:
            Parent entity or None if this is a root entity
        """
        return self._parent

    def _set_parent(self, parent: Optional["Entity"]) -> None:
        """Internal method to set the parent entity.

        Args:
            parent: Entity to set as parent, or None to remove parent
        """
        self._parent = parent

    def set_parent(self, parent: Optional["Entity"]) -> None:
        """Set the parent of this entity.

        Args:
            parent: Entity to set as parent, or None to remove parent
        """
        if self._parent == parent:
            return

        # Remove from old parent
        if self._parent:
            self._parent.remove_child(self)

        # Set new parent
        self._parent = parent
        if parent:
            parent.add_child(self)

    def add_child(self, child: "Entity") -> None:
        """Add a child entity.

        Args:
            child: Entity to add as a child
        """
        if child.parent:
            child.parent.remove_child(child)
        child._set_parent(self)
        self._children[child.id] = child

    def remove_child(self, child: "Entity") -> None:
        """Remove a child entity.

        Args:
            child: Entity to remove
        """
        if child.id in self._children:
            child._set_parent(None)
            del self._children[child.id]

    def add_component(self, component: Component) -> None:
        """Add a component to the entity.

        Args:
            component: Component to add

        Raises:
            ValueError: If a component of the same type already exists
        """
        component_type = type(component)
        if component_type in self._components:
            raise ValueError(
                f"Entity '{self.name}' already has a {component_type.__name__}"
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
        """Get a component by type.

        Args:
            component_type: Type of component to get

        Returns:
            The component if found, None otherwise
        """
        return self._components.get(component_type)  # type: ignore

    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if the entity has a component of the given type.

        Args:
            component_type: Type of component to check for

        Returns:
            True if the entity has the component, False otherwise
        """
        return component_type in self._components

    def __repr__(self) -> str:
        """Get string representation of the entity.

        Returns:
            String representation of the entity
        """
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"id='{self.id}', "
            f"enabled={self._enabled})"
        )
