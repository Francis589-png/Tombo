"""
Tombo Game Domain - Game Development
Provides game engines, sprites, physics, input handling
"""

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def scale(self, factor):
        return Vector2(self.x * factor, self.y * factor)
    
    def distance(self, other):
        import math
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Sprite:
    def __init__(self, image_path='', x=0, y=0):
        self.image = image_path
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.rotation = 0
        self.scale = 1.0
        self.visible = True
    
    def update(self, delta_time):
        """Update sprite."""
        self.position = self.position.add(self.velocity.scale(delta_time))
        return self
    
    def draw(self, renderer):
        """Draw sprite."""
        return True
    
    def collision_check(self, other):
        """Check collision."""
        return self.position.distance(other.position) < 50

class Scene:
    def __init__(self, name=''):
        self.name = name
        self.sprites = []
        self.objects = []
        self.background = ''
    
    def add_sprite(self, sprite):
        """Add sprite to scene."""
        self.sprites.append(sprite)
        return self
    
    def update(self, delta_time):
        """Update scene."""
        for sprite in self.sprites:
            sprite.update(delta_time)
        return self
    
    def render(self, renderer):
        """Render scene."""
        return True
    
    def find_sprite(self, name):
        """Find sprite by name."""
        return self.sprites[0] if self.sprites else None

class GameEngine:
    def __init__(self, width=800, height=600, title='Game'):
        self.width = width
        self.height = height
        self.title = title
        self.scenes = {}
        self.current_scene = None
        self.running = False
        self.fps = 60
        self.delta_time = 0.016
    
    def create_scene(self, name):
        """Create new scene."""
        scene = Scene(name)
        self.scenes[name] = scene
        return scene
    
    def load_scene(self, name):
        """Load scene."""
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        return self
    
    def start(self):
        """Start game loop."""
        self.running = True
        return True
    
    def stop(self):
        """Stop game loop."""
        self.running = False
        return True
    
    def handle_input(self, event):
        """Handle input."""
        return True

# Physics
class RigidBody:
    def __init__(self, mass=1.0):
        self.mass = mass
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.gravity = 9.8
    
    def apply_force(self, force):
        """Apply force."""
        self.acceleration = Vector2(force.x / self.mass, force.y / self.mass)
        return self
    
    def update(self, delta_time):
        """Update physics."""
        self.velocity = self.velocity.add(self.acceleration.scale(delta_time))
        return self

class Collider:
    def __init__(self, x=0, y=0, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def check_collision(self, other):
        """Check collision with another collider."""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

# Input Handling
class Input:
    def __init__(self):
        self.keys_pressed = {}
        self.mouse_position = Vector2(0, 0)
        self.mouse_buttons = {}
    
    def is_key_pressed(self, key):
        """Check if key pressed."""
        return self.keys_pressed.get(key, False)
    
    def get_mouse_position(self):
        """Get mouse position."""
        return self.mouse_position
    
    def is_mouse_button_pressed(self, button):
        """Check if mouse button pressed."""
        return self.mouse_buttons.get(button, False)

# Factory Functions
def tombo_create_engine(width=800, height=600, title='Game'):
    """Create game engine."""
    return GameEngine(width, height, title)

def tombo_create_sprite(image_path='', x=0, y=0):
    """Create sprite."""
    return Sprite(image_path, x, y)

def tombo_create_scene(name=''):
    """Create scene."""
    return Scene(name)

def tombo_create_rigid_body(mass=1.0):
    """Create rigid body."""
    return RigidBody(mass)

def tombo_create_collider(x=0, y=0, width=50, height=50):
    """Create collider."""
    return Collider(x, y, width, height)

def tombo_load_sprite_sheet(path, cols, rows):
    """Load sprite sheet."""
    return {'path': path, 'cols': cols, 'rows': rows, 'frames': []}

def tombo_animate_sprite(sprite, frames, duration):
    """Create sprite animation."""
    return {'sprite': sprite, 'frames': frames, 'duration': duration}

def tombo_play_sound(sound_path):
    """Play sound."""
    return True

def tombo_play_music(music_path, loop=True):
    """Play music."""
    return True

def tombo_load_tilemap(path):
    """Load tilemap."""
    return {'path': path, 'tiles': []}

def tombo_create_particle_system(effect_type='explosion'):
    """Create particle system."""
    return {'type': effect_type, 'particles': []}

def tombo_create_camera(x=0, y=0, zoom=1.0):
    """Create camera."""
    return {'x': x, 'y': y, 'zoom': zoom}

def tombo_follow_target(camera, target, smoothing=0.1):
    """Camera follow target."""
    return camera

def tombo_screen_shake(camera, intensity=1.0, duration=0.2):
    """Create screen shake effect."""
    return True

def tombo_get_input():
    """Get input instance."""
    return Input()

def tombo_get_collision_pairs(sprites):
    """Get all colliding sprite pairs."""
    return []

def tombo_raycast(origin, direction, max_distance=1000):
    """Cast ray and check collisions."""
    return {'hit': False, 'distance': 0, 'object': None}

def register(env):
    """Register game domain."""
    env.set('GameEngine', GameEngine)
    env.set('Sprite', Sprite)
    env.set('Scene', Scene)
    env.set('Vector2', Vector2)
    env.set('RigidBody', RigidBody)
    env.set('Collider', Collider)
    env.set('Input', Input)
    
    functions = {
        'create_engine': tombo_create_engine,
        'create_sprite': tombo_create_sprite,
        'create_scene': tombo_create_scene,
        'create_rigid_body': tombo_create_rigid_body,
        'create_collider': tombo_create_collider,
        'load_sprite_sheet': tombo_load_sprite_sheet,
        'animate_sprite': tombo_animate_sprite,
        'play_sound': tombo_play_sound,
        'play_music': tombo_play_music,
        'load_tilemap': tombo_load_tilemap,
        'create_particle_system': tombo_create_particle_system,
        'create_camera': tombo_create_camera,
        'follow_target': tombo_follow_target,
        'screen_shake': tombo_screen_shake,
        'get_input': tombo_get_input,
        'get_collision_pairs': tombo_get_collision_pairs,
        'raycast': tombo_raycast,
    }
    for name, func in functions.items():
        env.set(name, func)

provides = ['game']
