"""
Mobile Library for TOMBO Language
Mobile app development with UI, sensors, notifications, and native features
"""

from typing import Callable, List, Dict, Any, Optional, Tuple
from enum import Enum
from collections import deque


class Screen:
    """Represents mobile screen/activity"""
    
    def __init__(self, name: str = "Screen"):
        """Initialize screen"""
        self.name = name
        self.widgets: List['Widget'] = []
        self.background_color = "WHITE"
        self.is_visible = False
        self.title = ""
        self.listeners: Dict[str, List[Callable]] = {}
    
    def add_widget(self, widget: 'Widget') -> None:
        """Add widget to screen"""
        self.widgets.append(widget)
    
    def remove_widget(self, widget: 'Widget') -> None:
        """Remove widget from screen"""
        if widget in self.widgets:
            self.widgets.remove(widget)
    
    def find_widget(self, name: str) -> Optional['Widget']:
        """Find widget by name"""
        for widget in self.widgets:
            if widget.name == name:
                return widget
        return None
    
    def on_create(self) -> None:
        """Called when screen is created"""
        self.is_visible = True
    
    def on_destroy(self) -> None:
        """Called when screen is destroyed"""
        self.is_visible = False
    
    def on_pause(self) -> None:
        """Called when screen is paused"""
        self.is_visible = False
    
    def on_resume(self) -> None:
        """Called when screen is resumed"""
        self.is_visible = True
    
    def add_listener(self, event: str, callback: Callable) -> None:
        """Add event listener"""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    def trigger_event(self, event: str, data: Any = None) -> None:
        """Trigger event"""
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback(data)
    
    def get_widget_count(self) -> int:
        """Get number of widgets"""
        return len(self.widgets)


class Widget:
    """Base widget class"""
    
    def __init__(self, name: str = "Widget", widget_type: str = "view"):
        """Initialize widget"""
        self.name = name
        self.widget_type = widget_type
        self.enabled = True
        self.visible = True
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.background_color = "TRANSPARENT"
        self.children: List['Widget'] = []
        self.parent: Optional['Widget'] = None
        self.listeners: Dict[str, List[Callable]] = {}
    
    def add_child(self, widget: 'Widget') -> None:
        """Add child widget"""
        widget.parent = self
        self.children.append(widget)
    
    def remove_child(self, widget: 'Widget') -> None:
        """Remove child widget"""
        if widget in self.children:
            widget.parent = None
            self.children.remove(widget)
    
    def set_position(self, x: int, y: int) -> None:
        """Set widget position"""
        self.x = x
        self.y = y
    
    def set_size(self, width: int, height: int) -> None:
        """Set widget size"""
        self.width = width
        self.height = height
    
    def on_click(self, callback: Callable) -> None:
        """Register click listener"""
        self.add_listener("click", callback)
    
    def trigger_click(self) -> None:
        """Trigger click event"""
        if self.enabled:
            self.trigger_event("click")
    
    def add_listener(self, event: str, callback: Callable) -> None:
        """Add event listener"""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    def trigger_event(self, event: str, data: Any = None) -> None:
        """Trigger event"""
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback(data)


class Button(Widget):
    """Button widget"""
    
    def __init__(self, name: str = "Button", text: str = "Button"):
        """Initialize button"""
        super().__init__(name, "button")
        self.text = text
        self.background_color = "GRAY"
    
    def set_text(self, text: str) -> None:
        """Set button text"""
        self.text = text
    
    def click(self) -> None:
        """Simulate button click"""
        self.trigger_click()


class TextView(Widget):
    """Text view widget"""
    
    def __init__(self, name: str = "TextView", text: str = ""):
        """Initialize text view"""
        super().__init__(name, "textview")
        self.text = text
        self.text_color = "BLACK"
        self.text_size = 14
    
    def set_text(self, text: str) -> None:
        """Set text"""
        self.text = text
    
    def append_text(self, text: str) -> None:
        """Append text"""
        self.text += text


class EditText(Widget):
    """Edit text widget"""
    
    def __init__(self, name: str = "EditText", hint: str = ""):
        """Initialize edit text"""
        super().__init__(name, "edittext")
        self.text = ""
        self.hint = hint
        self.input_type = "text"
    
    def get_text(self) -> str:
        """Get text"""
        return self.text
    
    def set_text(self, text: str) -> None:
        """Set text"""
        self.text = text
    
    def clear(self) -> None:
        """Clear text"""
        self.text = ""


class ListView(Widget):
    """List view widget"""
    
    def __init__(self, name: str = "ListView"):
        """Initialize list view"""
        super().__init__(name, "listview")
        self.items: List[str] = []
        self.selected_index = -1
    
    def add_item(self, item: str) -> None:
        """Add item to list"""
        self.items.append(item)
    
    def remove_item(self, index: int) -> None:
        """Remove item from list"""
        if 0 <= index < len(self.items):
            self.items.pop(index)
    
    def clear(self) -> None:
        """Clear list"""
        self.items.clear()
        self.selected_index = -1
    
    def select_item(self, index: int) -> None:
        """Select item"""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self.trigger_event("item_selected", index)
    
    def get_item(self, index: int) -> Optional[str]:
        """Get item"""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    def get_selected_item(self) -> Optional[str]:
        """Get selected item"""
        if self.selected_index >= 0:
            return self.items[self.selected_index]
        return None


class Sensor:
    """Device sensor"""
    
    def __init__(self, sensor_type: str = "unknown"):
        """Initialize sensor"""
        self.sensor_type = sensor_type
        self.enabled = False
        self.values: List[float] = []
        self.listeners: List[Callable] = []
    
    def enable(self) -> None:
        """Enable sensor"""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable sensor"""
        self.enabled = False
    
    def read_value(self) -> float:
        """Read sensor value"""
        return self.values[-1] if self.values else 0.0
    
    def add_listener(self, callback: Callable) -> None:
        """Add value listener"""
        self.listeners.append(callback)
    
    def on_value_changed(self, value: float) -> None:
        """Trigger value change"""
        self.values.append(value)
        for listener in self.listeners:
            listener(value)
    
    def get_history(self) -> List[float]:
        """Get sensor value history"""
        return self.values.copy()


class Accelerometer(Sensor):
    """Accelerometer sensor"""
    
    def __init__(self):
        """Initialize accelerometer"""
        super().__init__("accelerometer")
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    
    def get_acceleration(self) -> Tuple[float, float, float]:
        """Get acceleration values"""
        return (self.x, self.y, self.z)
    
    def set_acceleration(self, x: float, y: float, z: float) -> None:
        """Set acceleration"""
        self.x = x
        self.y = y
        self.z = z
        self.on_value_changed((x + y + z) / 3)


class Gyroscope(Sensor):
    """Gyroscope sensor"""
    
    def __init__(self):
        """Initialize gyroscope"""
        super().__init__("gyroscope")
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    
    def get_rotation(self) -> Tuple[float, float, float]:
        """Get rotation values"""
        return (self.x, self.y, self.z)
    
    def set_rotation(self, x: float, y: float, z: float) -> None:
        """Set rotation"""
        self.x = x
        self.y = y
        self.z = z
        self.on_value_changed((x + y + z) / 3)


class GPS(Sensor):
    """GPS sensor"""
    
    def __init__(self):
        """Initialize GPS"""
        super().__init__("gps")
        self.latitude = 0.0
        self.longitude = 0.0
        self.accuracy = 0.0
    
    def get_location(self) -> Tuple[float, float]:
        """Get location"""
        return (self.latitude, self.longitude)
    
    def set_location(self, lat: float, lon: float, accuracy: float = 0.0) -> None:
        """Set location"""
        self.latitude = lat
        self.longitude = lon
        self.accuracy = accuracy
        self.on_value_changed(accuracy)
    
    def distance_to(self, lat: float, lon: float) -> float:
        """Calculate distance to coordinates"""
        import math
        dlat = (lat - self.latitude) * 111  # km per degree
        dlon = (lon - self.longitude) * 111
        return math.sqrt(dlat**2 + dlon**2)


class Notification:
    """Mobile notification"""
    
    def __init__(self, title: str = "", message: str = ""):
        """Initialize notification"""
        self.title = title
        self.message = message
        self.icon = ""
        self.priority = 0
        self.timestamp = 0
        self.is_read = False
        self.actions: List[str] = []
    
    def add_action(self, action: str) -> None:
        """Add notification action"""
        self.actions.append(action)
    
    def set_priority(self, priority: int) -> None:
        """Set notification priority"""
        self.priority = priority
    
    def mark_read(self) -> None:
        """Mark notification as read"""
        self.is_read = True


class NotificationManager:
    """Manage notifications"""
    
    def __init__(self):
        """Initialize notification manager"""
        self.notifications: deque = deque(maxlen=100)
        self.listeners: List[Callable] = []
    
    def send_notification(self, notification: Notification) -> None:
        """Send notification"""
        import time
        notification.timestamp = int(time.time())
        self.notifications.append(notification)
        for listener in self.listeners:
            listener(notification)
    
    def get_notifications(self) -> List[Notification]:
        """Get all notifications"""
        return list(self.notifications)
    
    def clear_notifications(self) -> None:
        """Clear notifications"""
        self.notifications.clear()
    
    def add_listener(self, callback: Callable) -> None:
        """Add notification listener"""
        self.listeners.append(callback)


class SharedPreferences:
    """Persistent key-value storage"""
    
    def __init__(self, name: str = "default"):
        """Initialize preferences"""
        self.name = name
        self.data: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Set value"""
        self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value"""
        return self.data.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer value"""
        return int(self.data.get(key, default))
    
    def get_string(self, key: str, default: str = "") -> str:
        """Get string value"""
        return str(self.data.get(key, default))
    
    def get_boolean(self, key: str, default: bool = False) -> bool:
        """Get boolean value"""
        val = self.data.get(key, default)
        if isinstance(val, bool):
            return val
        return val in [True, 1, "true", "True"]
    
    def remove(self, key: str) -> None:
        """Remove value"""
        if key in self.data:
            del self.data[key]
    
    def clear(self) -> None:
        """Clear all values"""
        self.data.clear()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all values"""
        return self.data.copy()


class Application:
    """Mobile application"""
    
    def __init__(self, name: str = "MobileApp"):
        """Initialize application"""
        self.name = name
        self.version = "1.0.0"
        self.screens: Dict[str, Screen] = {}
        self.current_screen: Optional[Screen] = None
        self.accelerometer = Accelerometer()
        self.gyroscope = Gyroscope()
        self.gps = GPS()
        self.notification_manager = NotificationManager()
        self.preferences = SharedPreferences()
        self.is_running = False
    
    def create_screen(self, name: str) -> Screen:
        """Create new screen"""
        screen = Screen(name)
        self.screens[name] = screen
        return screen
    
    def set_screen(self, name: str) -> bool:
        """Set active screen"""
        if name in self.screens:
            if self.current_screen:
                self.current_screen.on_pause()
            
            self.current_screen = self.screens[name]
            self.current_screen.on_resume()
            return True
        return False
    
    def get_screen(self, name: str) -> Optional[Screen]:
        """Get screen by name"""
        return self.screens.get(name)
    
    def start(self) -> None:
        """Start application"""
        self.is_running = True
        if self.current_screen:
            self.current_screen.on_create()
    
    def stop(self) -> None:
        """Stop application"""
        self.is_running = False
        if self.current_screen:
            self.current_screen.on_destroy()
    
    def send_notification(self, title: str, message: str) -> None:
        """Send notification"""
        notification = Notification(title, message)
        self.notification_manager.send_notification(notification)


class Intent:
    """Intent for starting activities/screens"""
    
    def __init__(self, target: str = ""):
        """Initialize intent"""
        self.target = target
        self.data: Dict[str, Any] = {}
        self.action = ""
    
    def put_extra(self, key: str, value: Any) -> None:
        """Put extra data"""
        self.data[key] = value
    
    def get_extra(self, key: str, default: Any = None) -> Any:
        """Get extra data"""
        return self.data.get(key, default)
    
    def set_action(self, action: str) -> None:
        """Set intent action"""
        self.action = action


class ActivityManager:
    """Manage app activities/screens"""
    
    def __init__(self, app: Application):
        """Initialize activity manager"""
        self.app = app
        self.back_stack: List[str] = []
    
    def start_activity(self, intent: Intent) -> bool:
        """Start activity"""
        if intent.target in self.app.screens:
            if self.app.current_screen:
                self.back_stack.append(self.app.current_screen.name)
            self.app.set_screen(intent.target)
            return True
        return False
    
    def finish_activity(self) -> bool:
        """Finish current activity"""
        if self.back_stack:
            prev_screen = self.back_stack.pop()
            return self.app.set_screen(prev_screen)
        return False
    
    def go_back(self) -> bool:
        """Go back in stack"""
        return self.finish_activity()


# Public API
__all__ = [
    'Screen',
    'Widget',
    'Button',
    'TextView',
    'EditText',
    'ListView',
    'Sensor',
    'Accelerometer',
    'Gyroscope',
    'GPS',
    'Notification',
    'NotificationManager',
    'SharedPreferences',
    'Application',
    'Intent',
    'ActivityManager'
]
