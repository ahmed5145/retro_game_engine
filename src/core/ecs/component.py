"""Base component class for the Entity Component System."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entity import Entity


class Component:
    """Base class for all components in the ECS.

    Components are pure data containers that can be attached to entities.
    They should not contain any game logic, only data and properties.
    """

    def __init__(self) -> None:
        """Initialize the component."""
        self._entity: "Entity | None" = None
        self._enabled: bool = True

    @property
    def entity(self) -> "Entity | None":
        """Get the entity this component is attached to.

        Returns:
            The entity this component is attached to, or None if not attached
        """
        return self._entity

    @entity.setter
    def entity(self, value: "Entity | None") -> None:
        """Set the entity this component is attached to.

        Args:
            value: The entity to attach this component to
        """
        self._entity = value

    @property
    def enabled(self) -> bool:
        """Get whether the component is enabled.

        Returns:
            True if the component is enabled, False otherwise
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether the component is enabled.

        Args:
            value: True to enable the component, False to disable it
        """
        self._enabled = value

    def on_attach(self) -> None:
        """Called when the component is attached to an entity."""
        pass

    def on_detach(self) -> None:
        """Called when the component is detached from an entity."""
        pass

    def __repr__(self) -> str:
        """Get string representation of the component.

        Returns:
            String representation of the component
        """
        return f"{self.__class__.__name__}(enabled={self._enabled})"
