"""
Game Library for TOMBO Language
Professional game development tools with graphics, physics, and input
"""

from typing import List, Tuple, Optional, Callable, Dict, Any
import math
import time


class Vector2:
    """2D vector for positions and velocities"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        """Initialize vector"""
        self.x = x
        self.y = y
    
    def add(self, other: 'Vector2') -> 'Vector2':
        """Add vectors"""
        return Vector2(self.x + other.x, self.y + other.y)
    
    def subtract(self, other: 'Vector2') -> 'Vector2':
        """Subtract vectors"""
        return Vector2(self.x - other.x, self.y - other.y)
    
    def multiply(self, scalar: float) -> 'Vector2':
        """Multiply by scalar"""
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self) -> float:
        """Get vector magnitude"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Vector2':
        """Normalize to unit vector"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def dot(self, other: 'Vector2') -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y
    
    def distance_to(self, other: 'Vector2') -> float:
        """Distance to another vector"""
        return self.subtract(other).magnitude()
    
    def __str__(self) -> str:
        return f"Vector2({self.x:.2f}, {self.y:.2f})"


class Transform:
    """Object transformation (position, rotation, scale)"""
    
    def __init__(self, pos: Optional[Vector2] = None, 
                 rotation: float = 0.0, 
                 scale: Optional[Vector2] = None):
        """Initialize transform"""
        self.position = pos if pos else Vector2(0, 0)
        self.rotation = rotation  # Degrees
        self.scale = scale if scale else Vector2(1, 1)
    
    def rotate(self, degrees: float) -> None:
        """Rotate object"""
        self.rotation = (self.rotation + degrees) % 360
    
    def move(self, delta: Vector2) -> None:
        """Move object"""
        self.position = self.position.add(delta)
    
    def set_position(self, pos: Vector2) -> None:
        """Set position"""
        self.position = pos
    
    def get_forward(self) -> Vector2:
        """Get forward direction based on rotation"""
        rad = math.radians(self.rotation)
        return Vector2(math.cos(rad), math.sin(rad))


class Sprite:
    """Visual representation of game object"""
    
    def __init__(self, width: int = 32, height: int = 32, 
                 color: str = "WHITE", char: str = "█"):
        """Initialize sprite"""
        self.width = width
        self.height = height
        self.color = color
        self.char = char
        self.pixels = [[self.char for _ in range(width)] for _ in range(height)]
    
    def fill(self, color: str) -> None:
        """Fill sprite with color"""
        self.color = color
    
    def set_pixel(self, x: int, y: int, char: str) -> None:
        """Set individual pixel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = char
    
    def get_pixel(self, x: int, y: int) -> str:
        """Get pixel character"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return " "
    
    def draw_rect(self, x: int, y: int, w: int, h: int, char: str = "█") -> None:
        """Draw rectangle on sprite"""
        for py in range(y, min(y + h, self.height)):
            for px in range(x, min(x + w, self.width)):
                self.set_pixel(px, py, char)
    
    def draw_circle(self, cx: int, cy: int, radius: int, char: str = "●") -> None:
        """Draw circle on sprite"""
        for py in range(self.height):
            for px in range(self.width):
                if (px - cx) ** 2 + (py - cy) ** 2 <= radius ** 2:
                    self.set_pixel(px, py, char)


class Collider:
    """Collision detection"""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        """Initialize collider (AABB)"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def overlaps(self, other: 'Collider') -> bool:
        """Check AABB collision"""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is inside collider"""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)
    
    def distance_to(self, other: 'Collider') -> float:
        """Distance to another collider"""
        cx1 = self.x + self.width / 2
        cy1 = self.y + self.height / 2
        cx2 = other.x + other.width / 2
        cy2 = other.y + other.height / 2
        
        return math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)


class RigidBody:
    """Physics component"""
    
    def __init__(self, mass: float = 1.0, is_static: bool = False):
        """Initialize rigid body"""
        self.mass = mass
        self.is_static = is_static
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.gravity = Vector2(0, 9.8)
        self.friction = 0.1
    
    def apply_force(self, force: Vector2) -> None:
        """Apply force (F = ma)"""
        if not self.is_static:
            self.acceleration = force.multiply(1 / self.mass)
    
    def apply_gravity(self) -> None:
        """Apply gravity"""
        if not self.is_static:
            self.apply_force(self.gravity.multiply(self.mass))
    
    def update(self, delta_time: float) -> None:
        """Update physics"""
        if self.is_static:
            return
        
        # Apply friction
        self.velocity = self.velocity.multiply(1 - self.friction)
        
        # Update velocity
        self.velocity = self.velocity.add(self.acceleration.multiply(delta_time))
    
    def set_velocity(self, vel: Vector2) -> None:
        """Set velocity"""
        self.velocity = vel


class GameObject:
    """Base game object"""
    
    def __init__(self, name: str = "GameObject"):
        """Initialize game object"""
        self.name = name
        self.transform = Transform()
        self.sprite = Sprite()
        self.collider = Collider(0, 0, 32, 32)
        self.rigidbody = RigidBody()
        self.active = True
        self.components: Dict[str, Any] = {}
    
    def add_component(self, name: str, component: Any) -> None:
        """Add component"""
        self.components[name] = component
    
    def get_component(self, name: str) -> Optional[Any]:
        """Get component"""
        return self.components.get(name)
    
    def update(self, delta_time: float) -> None:
        """Update game object"""
        if not self.active:
            return
        
        self.rigidbody.update(delta_time)
        self.transform.move(self.rigidbody.velocity.multiply(delta_time))
        
        # Update collider position
        self.collider.x = self.transform.position.x
        self.collider.y = self.transform.position.y
    
    def render(self) -> str:
        """Render object"""
        return f"{self.name} at ({self.transform.position.x:.1f}, {self.transform.position.y:.1f})"


class Camera:
    """Game camera"""
    
    def __init__(self, width: int = 80, height: int = 24):
        """Initialize camera"""
        self.width = width
        self.height = height
        self.position = Vector2(0, 0)
        self.zoom = 1.0
    
    def pan_to(self, target: Vector2) -> None:
        """Pan camera to target"""
        self.position = target.subtract(
            Vector2(self.width / 2, self.height / 2)
        )
    
    def pan_smooth(self, target: Vector2, smoothing: float = 0.1) -> None:
        """Smooth camera pan"""
        delta = target.subtract(self.position)
        self.position = self.position.add(delta.multiply(smoothing))
    
    def set_zoom(self, zoom: float) -> None:
        """Set zoom level"""
        self.zoom = max(0.1, zoom)
    
    def screen_to_world(self, screen_pos: Vector2) -> Vector2:
        """Convert screen position to world position"""
        return screen_pos.add(self.position).multiply(1 / self.zoom)
    
    def world_to_screen(self, world_pos: Vector2) -> Vector2:
        """Convert world position to screen position"""
        return world_pos.subtract(self.position).multiply(self.zoom)


class InputHandler:
    """Handle player input"""
    
    def __init__(self):
        """Initialize input handler"""
        self.keys_pressed: Dict[str, bool] = {}
        self.mouse_pos = Vector2(0, 0)
        self.mouse_buttons: Dict[str, bool] = {}
    
    def key_down(self, key: str) -> bool:
        """Check if key is pressed"""
        return self.keys_pressed.get(key, False)
    
    def key_up(self, key: str) -> bool:
        """Check if key is released"""
        return not self.key_down(key)
    
    def set_key(self, key: str, pressed: bool) -> None:
        """Set key state"""
        self.keys_pressed[key] = pressed
    
    def mouse_button_down(self, button: str) -> bool:
        """Check if mouse button pressed"""
        return self.mouse_buttons.get(button, False)
    
    def set_mouse(self, x: float, y: float) -> None:
        """Set mouse position"""
        self.mouse_pos = Vector2(x, y)
    
    def get_movement_input(self) -> Vector2:
        """Get WASD movement"""
        direction = Vector2(0, 0)
        if self.key_down("w"):
            direction.y -= 1
        if self.key_down("s"):
            direction.y += 1
        if self.key_down("a"):
            direction.x -= 1
        if self.key_down("d"):
            direction.x += 1
        return direction.normalize() if direction.magnitude() > 0 else Vector2(0, 0)


class GameScene:
    """Container for game objects"""
    
    def __init__(self, name: str = "Scene"):
        """Initialize scene"""
        self.name = name
        self.objects: List[GameObject] = []
        self.camera = Camera()
        self.ambient_color = "BLACK"
    
    def add_object(self, obj: GameObject) -> None:
        """Add object to scene"""
        self.objects.append(obj)
    
    def remove_object(self, obj: GameObject) -> None:
        """Remove object from scene"""
        if obj in self.objects:
            self.objects.remove(obj)
    
    def find_object(self, name: str) -> Optional[GameObject]:
        """Find object by name"""
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None
    
    def update(self, delta_time: float) -> None:
        """Update all objects"""
        for obj in self.objects:
            if obj.active:
                obj.update(delta_time)
    
    def get_objects_at(self, pos: Vector2) -> List[GameObject]:
        """Get objects at position"""
        return [obj for obj in self.objects 
                if obj.collider.contains_point(pos.x, pos.y)]
    
    def render(self) -> str:
        """Render scene"""
        output = f"Scene: {self.name}\n"
        for obj in self.objects:
            if obj.active:
                output += obj.render() + "\n"
        return output


class GameEngine:
    """Main game engine"""
    
    def __init__(self, width: int = 80, height: int = 24, 
                 target_fps: int = 60):
        """Initialize game engine"""
        self.width = width
        self.height = height
        self.target_fps = target_fps
        self.delta_time = 0.0
        self.running = False
        self.current_scene: Optional[GameScene] = None
        self.input = InputHandler()
        self.time_elapsed = 0.0
    
    def set_scene(self, scene: GameScene) -> None:
        """Set active scene"""
        self.current_scene = scene
    
    def start(self) -> None:
        """Start game engine"""
        self.running = True
        self.time_elapsed = 0.0
    
    def stop(self) -> None:
        """Stop game engine"""
        self.running = False
    
    def update(self) -> None:
        """Update game state"""
        if not self.current_scene:
            return
        
        self.current_scene.update(self.delta_time)
        self.time_elapsed += self.delta_time
    
    def render(self) -> str:
        """Render current scene"""
        if not self.current_scene:
            return "No active scene"
        return self.current_scene.render()
    
    def simulate_frame(self, delta: float) -> None:
        """Simulate one frame"""
        self.delta_time = delta
        self.update()


# Public API
__all__ = [
    'Vector2',
    'Transform',
    'Sprite',
    'Collider',
    'RigidBody',
    'GameObject',
    'Camera',
    'InputHandler',
    'GameScene',
    'GameEngine'
]
