# TOMBO LANGUAGE - SIMPLEST INSTALLATION

## ONE-COMMAND INSTALLATION

### Windows (Batch File)
```bash
cd c:\Users\FRANCIS JUSU\Documents\TOMBO
install.bat
```

### Windows (PowerShell)
```powershell
cd c:\Users\FRANCIS JUSU\Documents\TOMBO
.\install.ps1
```

### Manual Installation (if scripts don't work)
```bash
cd c:\Users\FRANCIS JUSU\Documents\TOMBO
pip install -e .
```

---

## DONE! NOW JUST USE IT

### In Python (Simplest)
```python
from src.core.interpreter import Interpreter
interp = Interpreter()

# Use any function
fn = interp.global_env.get('print')
fn("Hello Tombo!")
```

### From Command Line
```bash
python tombo.py
```

---

## WHAT YOU GET

✓ 39 Libraries (automatically loaded)
✓ 1,301 Functions (ready to use)
✓ Hardware Support (Camera, Audio, Sensors)
✓ Zero Configuration

---

## QUICK EXAMPLES

### Example 1: Print
```python
from src.core.interpreter import Interpreter
interp = Interpreter()
interp.global_env.get('print')("Hello!")
```

### Example 2: Vision
```python
from src.core.interpreter import Interpreter
interp = Interpreter()

load = interp.global_env.get('load_image')
detect = interp.global_env.get('detect_faces')

img = load('photo.jpg')
faces = detect(img)
```

### Example 3: Audio
```python
from src.core.interpreter import Interpreter
interp = Interpreter()

gen = interp.global_env.get('generate_tone')
tone = gen(440, 1.0)  # A4 for 1 second
```

### Example 4: Sensors
```python
from src.core.interpreter import Interpreter
interp = Interpreter()

read_hr = interp.global_env.get('read_heart_rate')
heart_rate = read_hr()
```

---

**That's it! Simple as that!**

Version: 1.0.0
Status: Ready to use
