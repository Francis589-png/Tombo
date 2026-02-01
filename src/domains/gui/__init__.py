"""
Tombo GUI Domain - Graphical User Interface
Provides windows, widgets, layouts, events, dialogs
"""

class Window:
    def __init__(self, title='', width=800, height=600):
        self.title = title
        self.width = width
        self.height = height
        self.widgets = []
        self.shown = False
        self.properties = {}
    
    def add_widget(self, widget):
        """Add widget to window."""
        self.widgets.append(widget)
        return self
    
    def show(self):
        """Show window."""
        self.shown = True
        return True
    
    def hide(self):
        """Hide window."""
        self.shown = False
        return True
    
    def close(self):
        """Close window."""
        self.shown = False
        return True
    
    def set_title(self, title):
        """Set window title."""
        self.title = title
        return self
    
    def set_size(self, width, height):
        """Set window size."""
        self.width = width
        self.height = height
        return self

class Widget:
    def __init__(self, label='', x=0, y=0, width=100, height=30):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = ''
        self.enabled = True
        self.visible = True
    
    def set_position(self, x, y):
        """Set widget position."""
        self.x = x
        self.y = y
        return self
    
    def set_size(self, width, height):
        """Set widget size."""
        self.width = width
        self.height = height
        return self
    
    def set_enabled(self, enabled):
        """Enable/disable widget."""
        self.enabled = enabled
        return self
    
    def set_visible(self, visible):
        """Show/hide widget."""
        self.visible = visible
        return self

class Button(Widget):
    def __init__(self, label='', callback=None):
        super().__init__(label)
        self.callback = callback
    
    def click(self):
        """Simulate button click."""
        if self.callback:
            return self.callback()
        return True

class Label(Widget):
    def __init__(self, text=''):
        super().__init__(text)
        self.text = text
    
    def set_text(self, text):
        """Set label text."""
        self.text = text
        self.label = text
        return self

class TextBox(Widget):
    def __init__(self, label='', value=''):
        super().__init__(label)
        self.value = value
    
    def get_value(self):
        """Get text value."""
        return self.value
    
    def set_value(self, value):
        """Set text value."""
        self.value = value
        return self

class CheckBox(Widget):
    def __init__(self, label='', checked=False):
        super().__init__(label)
        self.checked = checked
    
    def is_checked(self):
        """Check if checked."""
        return self.checked
    
    def set_checked(self, checked):
        """Set checked state."""
        self.checked = checked
        return self

class ComboBox(Widget):
    def __init__(self, label='', items=None):
        super().__init__(label)
        self.items = items or []
        self.selected_index = 0
    
    def add_item(self, item):
        """Add item to list."""
        self.items.append(item)
        return self
    
    def get_selected(self):
        """Get selected item."""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None
    
    def set_selected(self, index):
        """Set selected item."""
        self.selected_index = index
        return self

class ListBox(Widget):
    def __init__(self, label='', items=None):
        super().__init__(label)
        self.items = items or []
        self.selected = []
    
    def add_item(self, item):
        """Add item."""
        self.items.append(item)
        return self
    
    def get_selected(self):
        """Get selected items."""
        return self.selected
    
    def clear(self):
        """Clear items."""
        self.items = []
        return self

class Layout:
    def __init__(self, layout_type='vertical'):
        self.layout_type = layout_type
        self.widgets = []
        self.padding = 5
        self.spacing = 5
    
    def add_widget(self, widget):
        """Add widget to layout."""
        self.widgets.append(widget)
        return self
    
    def set_padding(self, padding):
        """Set padding."""
        self.padding = padding
        return self
    
    def set_spacing(self, spacing):
        """Set spacing."""
        self.spacing = spacing
        return self

class Menu:
    def __init__(self, label=''):
        self.label = label
        self.items = []
    
    def add_item(self, label, callback=None):
        """Add menu item."""
        self.items.append({'label': label, 'callback': callback})
        return self
    
    def add_separator(self):
        """Add separator."""
        self.items.append({'label': '---', 'separator': True})
        return self
    
    def add_submenu(self, submenu):
        """Add submenu."""
        self.items.append(submenu)
        return self

# Window Management
def tombo_create_window(title='', width=800, height=600):
    """Create new window."""
    return Window(title, width, height)

def tombo_window_fullscreen(window):
    """Set window to fullscreen."""
    window.width = 1920
    window.height = 1080
    return window

def tombo_window_maximize(window):
    """Maximize window."""
    window.width = 1366
    window.height = 768
    return window

def tombo_window_minimize(window):
    """Minimize window."""
    return window

# Widget Creation
def tombo_create_button(label='', callback=None):
    """Create button."""
    return Button(label, callback)

def tombo_create_label(text=''):
    """Create label."""
    return Label(text)

def tombo_create_textbox(label='', value=''):
    """Create text input."""
    return TextBox(label, value)

def tombo_create_checkbox(label='', checked=False):
    """Create checkbox."""
    return CheckBox(label, checked)

def tombo_create_combobox(label='', items=None):
    """Create dropdown."""
    return ComboBox(label, items)

def tombo_create_listbox(label='', items=None):
    """Create listbox."""
    return ListBox(label, items)

def tombo_create_layout(layout_type='vertical'):
    """Create layout."""
    return Layout(layout_type)

# Layout Management
def tombo_add_to_layout(layout, widget):
    """Add widget to layout."""
    layout.add_widget(widget)
    return layout

def tombo_layout_horizontal(widgets):
    """Create horizontal layout."""
    layout = Layout('horizontal')
    for widget in widgets:
        layout.add_widget(widget)
    return layout

def tombo_layout_vertical(widgets):
    """Create vertical layout."""
    layout = Layout('vertical')
    for widget in widgets:
        layout.add_widget(widget)
    return layout

def tombo_layout_grid(rows, cols):
    """Create grid layout."""
    return {'type': 'grid', 'rows': rows, 'cols': cols, 'widgets': []}

# Dialogs
def tombo_message_box(title, message, message_type='info'):
    """Show message box."""
    return {'title': title, 'message': message, 'type': message_type}

def tombo_input_dialog(title, prompt, default=''):
    """Show input dialog."""
    return {'title': title, 'prompt': prompt, 'default': default}

def tombo_file_open_dialog(title='Open File', filter_str='All Files'):
    """Show file open dialog."""
    return ''

def tombo_file_save_dialog(title='Save File', filter_str='All Files'):
    """Show file save dialog."""
    return ''

def tombo_color_picker(title='Choose Color'):
    """Show color picker."""
    return '#000000'

def tombo_confirm_dialog(title, message):
    """Show confirmation dialog."""
    return True

# Menu Management
def tombo_create_menu(label=''):
    """Create menu."""
    return Menu(label)

def tombo_add_menu_item(menu, label, callback=None):
    """Add menu item."""
    menu.add_item(label, callback)
    return menu

def tombo_add_menu_separator(menu):
    """Add menu separator."""
    menu.add_separator()
    return menu

# Event Handling
def tombo_connect_event(widget, event_type, callback):
    """Connect event handler."""
    return True

def tombo_emit_event(widget, event_type, data=None):
    """Emit event."""
    return True

# Drawing
class Canvas:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.items = []
    
    def draw_line(self, x1, y1, x2, y2, color='black'):
        """Draw line."""
        self.items.append({'type': 'line', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color})
        return self
    
    def draw_rect(self, x, y, width, height, color='black', fill=False):
        """Draw rectangle."""
        self.items.append({'type': 'rect', 'x': x, 'y': y, 'width': width, 'height': height, 'color': color, 'fill': fill})
        return self
    
    def draw_circle(self, x, y, radius, color='black', fill=False):
        """Draw circle."""
        self.items.append({'type': 'circle', 'x': x, 'y': y, 'radius': radius, 'color': color, 'fill': fill})
        return self
    
    def draw_text(self, x, y, text, color='black'):
        """Draw text."""
        self.items.append({'type': 'text', 'x': x, 'y': y, 'text': text, 'color': color})
        return self
    
    def clear(self):
        """Clear canvas."""
        self.items = []
        return self

def tombo_create_canvas(width=800, height=600):
    """Create canvas."""
    return Canvas(width, height)

def tombo_canvas_draw_line(canvas, x1, y1, x2, y2, color='black'):
    """Draw line on canvas."""
    canvas.draw_line(x1, y1, x2, y2, color)
    return canvas

def tombo_canvas_draw_rect(canvas, x, y, width, height, color='black', fill=False):
    """Draw rectangle on canvas."""
    canvas.draw_rect(x, y, width, height, color, fill)
    return canvas

def tombo_canvas_draw_circle(canvas, x, y, radius, color='black', fill=False):
    """Draw circle on canvas."""
    canvas.draw_circle(x, y, radius, color, fill)
    return canvas

def tombo_canvas_draw_text(canvas, x, y, text, color='black'):
    """Draw text on canvas."""
    canvas.draw_text(x, y, text, color)
    return canvas

# Styling
def tombo_set_style(widget, style_name, value):
    """Set widget style."""
    if not hasattr(widget, 'styles'):
        widget.styles = {}
    widget.styles[style_name] = value
    return widget

def tombo_create_stylesheet(rules):
    """Create stylesheet."""
    return rules

def register(env):
    """Register GUI domain."""
    env.set('Window', Window)
    env.set('Button', Button)
    env.set('Label', Label)
    env.set('TextBox', TextBox)
    env.set('CheckBox', CheckBox)
    env.set('ComboBox', ComboBox)
    env.set('ListBox', ListBox)
    env.set('Layout', Layout)
    env.set('Menu', Menu)
    env.set('Canvas', Canvas)
    
    functions = {
        'create_window': tombo_create_window,
        'window_fullscreen': tombo_window_fullscreen,
        'window_maximize': tombo_window_maximize,
        'window_minimize': tombo_window_minimize,
        'create_button': tombo_create_button,
        'create_label': tombo_create_label,
        'create_textbox': tombo_create_textbox,
        'create_checkbox': tombo_create_checkbox,
        'create_combobox': tombo_create_combobox,
        'create_listbox': tombo_create_listbox,
        'create_layout': tombo_create_layout,
        'add_to_layout': tombo_add_to_layout,
        'layout_horizontal': tombo_layout_horizontal,
        'layout_vertical': tombo_layout_vertical,
        'layout_grid': tombo_layout_grid,
        'message_box': tombo_message_box,
        'input_dialog': tombo_input_dialog,
        'file_open_dialog': tombo_file_open_dialog,
        'file_save_dialog': tombo_file_save_dialog,
        'color_picker': tombo_color_picker,
        'confirm_dialog': tombo_confirm_dialog,
        'create_menu': tombo_create_menu,
        'add_menu_item': tombo_add_menu_item,
        'add_menu_separator': tombo_add_menu_separator,
        'connect_event': tombo_connect_event,
        'emit_event': tombo_emit_event,
        'create_canvas': tombo_create_canvas,
        'canvas_draw_line': tombo_canvas_draw_line,
        'canvas_draw_rect': tombo_canvas_draw_rect,
        'canvas_draw_circle': tombo_canvas_draw_circle,
        'canvas_draw_text': tombo_canvas_draw_text,
        'set_style': tombo_set_style,
        'create_stylesheet': tombo_create_stylesheet,
    }
    for name, func in functions.items():
        env.set(name, func)

provides = ['gui']
