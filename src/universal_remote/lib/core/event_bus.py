class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name: str, callback) -> None:
        """Subscribe a callback function to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []

        for handler in self._subscribers[event_name]:
            if handler is callback:
                return

        self._subscribers[event_name].append(callback)

    def publish(self, event_name: str, *args, **kwargs) -> None:
        """Publish an event to all subscribed callbacks."""
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)

    def unsubscribe(self, event_name: str, callback) -> None:
        """Unsubscribe a callback function from an event."""
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(callback)
            if not self._subscribers[event_name]:
                del self._subscribers[event_name]
