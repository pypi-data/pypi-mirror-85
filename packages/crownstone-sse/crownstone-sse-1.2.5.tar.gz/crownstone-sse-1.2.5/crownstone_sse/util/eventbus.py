import asyncio
import logging
from typing import Awaitable, Callable, Dict, List

_LOGGER = logging.getLogger(__name__)


class EventBus:
    """Event bus that listens and fires system or SSE events"""

    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        """Init the event bus"""
        self.event_listeners: Dict[str, List[Callable or Awaitable]] = {}
        self.loop = loop

    def get_event_listeners(self) -> Dict[str, int]:
        """Return all current event listeners and amount of events"""

        return {key: len(self.event_listeners[key]) for key in self.event_listeners}

    def add_event_listener(self, event_type: str, event_listener: Callable or Awaitable) -> Callable or Awaitable:
        """Listen to events of a specific type"""
        if event_type in self.event_listeners:
            self.event_listeners[event_type].append(event_listener)
        else:
            self.event_listeners[event_type] = [event_listener]

        # Return listener so it can be removed again, if necessary
        return event_listener

    def fire(self, event_type: str, event=None) -> None:
        """Fire an event. Can be listened for."""
        for listener in self.event_listeners.get(event_type, []):
            if asyncio.iscoroutinefunction(listener):
                asyncio.run_coroutine_threadsafe(
                    listener(event),
                    self.loop if self.loop is not None else asyncio.get_running_loop()
                )
            else:
                listener(event)

    def remove_event_listener(self, event_type: str, listener: Callable or Awaitable) -> None:
        """Remove a listener for an event type"""
        try:
            self.event_listeners[event_type].remove(listener)
        except ValueError:
            _LOGGER.warning("Error removing listener, it does not exist.")
