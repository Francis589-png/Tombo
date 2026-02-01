"""
TOMBO Image Processing Library
Loading, Filtering, Analysis, Transformations
"""

import math
from typing import List, Tuple, Optional


class Pixel:
    """Single pixel representation"""
    
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, a))
    
    def __str__(self):
        return f"RGBA({self.r}, {self.g}, {self.b}, {self.a})"
    
    def grayscale(self) -> int:
        """Convert to grayscale (0-255)"""
        return int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
    
    def brightness(self) -> float:
        """Get brightness (0-1)"""
        return (self.r + self.g + self.b) / (3 * 255)
    
    def invert(self):
        """Invert colors"""
        return Pixel(255 - self.r, 255 - self.g, 255 - self.b, self.a)


class Image:
    """Image representation and operations"""
    
    def __init__(self, width: int, height: int, pixels: Optional[List[List[Pixel]]] = None):
        self.width = width
        self.height = height
        
        if pixels is None:
            # Create white image
            self.pixels = [[Pixel(255, 255, 255) for _ in range(width)] for _ in range(height)]
        else:
            self.pixels = pixels
    
    def get_pixel(self, x: int, y: int) -> Pixel:
        """Get pixel at coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return Pixel(0, 0, 0, 0)
    
    def set_pixel(self, x: int, y: int, pixel: Pixel):
        """Set pixel at coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = pixel
    
    def resize(self, new_width: int, new_height: int):
        """Resize image using nearest neighbor"""
        new_pixels = []
        
        for y in range(new_height):
            row = []
            for x in range(new_width):
                src_x = int(x * self.width / new_width)
                src_y = int(y * self.height / new_height)
                row.append(self.get_pixel(src_x, src_y))
            new_pixels.append(row)
        
        return Image(new_width, new_height, new_pixels)
    
    def crop(self, x1: int, y1: int, x2: int, y2: int):
        """Crop image to rectangular region"""
        width = x2 - x1
        height = y2 - y1
        
        new_pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(self.get_pixel(x1 + x, y1 + y))
            new_pixels.append(row)
        
        return Image(width, height, new_pixels)
    
    def rotate_90(self, clockwise: bool = True):
        """Rotate image 90 degrees"""
        if clockwise:
            new_pixels = []
            for x in range(self.width):
                row = []
                for y in range(self.height - 1, -1, -1):
                    row.append(self.get_pixel(x, y))
                new_pixels.append(row)
            return Image(self.height, self.width, new_pixels)
        else:
            new_pixels = []
            for x in range(self.width - 1, -1, -1):
                row = []
                for y in range(self.height):
                    row.append(self.get_pixel(x, y))
                new_pixels.append(row)
            return Image(self.height, self.width, new_pixels)
    
    def flip_horizontal(self):
        """Flip image horizontally"""
        new_pixels = []
        for row in self.pixels:
            new_pixels.append(list(reversed(row)))
        return Image(self.width, self.height, new_pixels)
    
    def flip_vertical(self):
        """Flip image vertically"""
        return Image(self.width, self.height, list(reversed(self.pixels)))
    
    def grayscale(self):
        """Convert to grayscale"""
        new_pixels = []
        for row in self.pixels:
            new_row = []
            for pixel in row:
                gray_val = pixel.grayscale()
                new_pixel = Pixel(gray_val, gray_val, gray_val, pixel.a)
                new_row.append(new_pixel)
            new_pixels.append(new_row)
        return Image(self.width, self.height, new_pixels)
    
    def to_sepia(self):
        """Convert to sepia tone"""
        new_pixels = []
        for row in self.pixels:
            new_row = []
            for pixel in row:
                r = int(pixel.r * 0.393 + pixel.g * 0.769 + pixel.b * 0.189)
                g = int(pixel.r * 0.349 + pixel.g * 0.686 + pixel.b * 0.168)
                b = int(pixel.r * 0.272 + pixel.g * 0.534 + pixel.b * 0.131)
                new_pixel = Pixel(r, g, b, pixel.a)
                new_row.append(new_pixel)
            new_pixels.append(new_row)
        return Image(self.width, self.height, new_pixels)
    
    def invert(self):
        """Invert all colors"""
        new_pixels = []
        for row in self.pixels:
            new_row = [pixel.invert() for pixel in row]
            new_pixels.append(new_row)
        return Image(self.width, self.height, new_pixels)
    
    def blur(self, kernel_size: int = 3):
        """Apply box blur filter"""
        new_pixels = []
        offset = kernel_size // 2
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                r_sum, g_sum, b_sum, count = 0, 0, 0, 0
                
                for ky in range(-offset, offset + 1):
                    for kx in range(-offset, offset + 1):
                        pixel = self.get_pixel(x + kx, y + ky)
                        r_sum += pixel.r
                        g_sum += pixel.g
                        b_sum += pixel.b
                        count += 1
                
                avg_r = r_sum // count
                avg_g = g_sum // count
                avg_b = b_sum // count
                row.append(Pixel(avg_r, avg_g, avg_b))
            
            new_pixels.append(row)
        
        return Image(self.width, self.height, new_pixels)
    
    def sharpen(self):
        """Apply sharpening filter"""
        new_pixels = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                center = self.get_pixel(x, y)
                top = self.get_pixel(x, y - 1)
                bottom = self.get_pixel(x, y + 1)
                left = self.get_pixel(x - 1, y)
                right = self.get_pixel(x + 1, y)
                
                r = int(center.r * 5 - (top.r + bottom.r + left.r + right.r))
                g = int(center.g * 5 - (top.g + bottom.g + left.g + right.g))
                b = int(center.b * 5 - (top.b + bottom.b + left.b + right.b))
                
                row.append(Pixel(r, g, b, center.a))
            
            new_pixels.append(row)
        
        return Image(self.width, self.height, new_pixels)
    
    def edge_detect(self):
        """Detect edges using Sobel operator"""
        gray = self.grayscale()
        new_pixels = []
        
        for y in range(gray.height):
            row = []
            for x in range(gray.width):
                # Sobel X kernel
                gx = (-1 * gray.get_pixel(x-1, y-1).grayscale() +
                      0 * gray.get_pixel(x, y-1).grayscale() +
                      1 * gray.get_pixel(x+1, y-1).grayscale() +
                      -2 * gray.get_pixel(x-1, y).grayscale() +
                      0 * gray.get_pixel(x, y).grayscale() +
                      2 * gray.get_pixel(x+1, y).grayscale() +
                      -1 * gray.get_pixel(x-1, y+1).grayscale() +
                      0 * gray.get_pixel(x, y+1).grayscale() +
                      1 * gray.get_pixel(x+1, y+1).grayscale())
                
                # Sobel Y kernel
                gy = (-1 * gray.get_pixel(x-1, y-1).grayscale() +
                      -2 * gray.get_pixel(x, y-1).grayscale() +
                      -1 * gray.get_pixel(x+1, y-1).grayscale() +
                      0 * gray.get_pixel(x-1, y).grayscale() +
                      0 * gray.get_pixel(x, y).grayscale() +
                      0 * gray.get_pixel(x+1, y).grayscale() +
                      1 * gray.get_pixel(x-1, y+1).grayscale() +
                      2 * gray.get_pixel(x, y+1).grayscale() +
                      1 * gray.get_pixel(x+1, y+1).grayscale())
                
                magnitude = int(math.sqrt(gx**2 + gy**2))
                magnitude = max(0, min(255, magnitude))
                row.append(Pixel(magnitude, magnitude, magnitude))
            
            new_pixels.append(row)
        
        return Image(gray.width, gray.height, new_pixels)
    
    def threshold(self, threshold_val: int = 128):
        """Convert to black and white based on threshold"""
        gray = self.grayscale()
        new_pixels = []
        
        for row in gray.pixels:
            new_row = []
            for pixel in row:
                val = 255 if pixel.grayscale() >= threshold_val else 0
                new_row.append(Pixel(val, val, val))
            new_pixels.append(new_row)
        
        return Image(gray.width, gray.height, new_pixels)
    
    def brightness_adjust(self, factor: float):
        """Adjust brightness"""
        new_pixels = []
        for row in self.pixels:
            new_row = []
            for pixel in row:
                r = int(pixel.r * factor)
                g = int(pixel.g * factor)
                b = int(pixel.b * factor)
                new_row.append(Pixel(r, g, b, pixel.a))
            new_pixels.append(new_row)
        return Image(self.width, self.height, new_pixels)
    
    def contrast_adjust(self, factor: float):
        """Adjust contrast"""
        center = 128
        new_pixels = []
        for row in self.pixels:
            new_row = []
            for pixel in row:
                r = int((pixel.r - center) * factor + center)
                g = int((pixel.g - center) * factor + center)
                b = int((pixel.b - center) * factor + center)
                new_row.append(Pixel(r, g, b, pixel.a))
            new_pixels.append(new_row)
        return Image(self.width, self.height, new_pixels)
    
    def histogram(self):
        """Calculate color histogram"""
        r_hist = [0] * 256
        g_hist = [0] * 256
        b_hist = [0] * 256
        
        for row in self.pixels:
            for pixel in row:
                r_hist[pixel.r] += 1
                g_hist[pixel.g] += 1
                b_hist[pixel.b] += 1
        
        return {
            'red': r_hist,
            'green': g_hist,
            'blue': b_hist
        }


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

def create_image(width: int, height: int, color: Tuple[int, int, int] = (255, 255, 255)) -> Image:
    """Create new image with specified dimensions"""
    pixel = Pixel(color[0], color[1], color[2])
    pixels = [[pixel for _ in range(width)] for _ in range(height)]
    return Image(width, height, pixels)

def create_pixel(r: int, g: int, b: int, a: int = 255) -> Pixel:
    """Create pixel"""
    return Pixel(r, g, b, a)

def load_image(path: str) -> Image:
    """Load image from file (simulated)"""
    # In real implementation, would use PIL or similar
    return create_image(800, 600)

def save_image(image: Image, path: str) -> bool:
    """Save image to file (simulated)"""
    return True

def resize_image(image: Image, width: int, height: int) -> Image:
    """Resize image"""
    return image.resize(width, height)

def crop_image(image: Image, x1: int, y1: int, x2: int, y2: int) -> Image:
    """Crop image"""
    return image.crop(x1, y1, x2, y2)

def rotate_image(image: Image, degrees: int) -> Image:
    """Rotate image (90 degree increments)"""
    steps = (degrees % 360) // 90
    result = image
    for _ in range(steps):
        result = result.rotate_90(True)
    return result

def flip_horizontal(image: Image) -> Image:
    """Flip image horizontally"""
    return image.flip_horizontal()

def flip_vertical(image: Image) -> Image:
    """Flip image vertically"""
    return image.flip_vertical()

def grayscale(image: Image) -> Image:
    """Convert image to grayscale"""
    return image.grayscale()

def sepia(image: Image) -> Image:
    """Apply sepia tone"""
    return image.to_sepia()

def invert(image: Image) -> Image:
    """Invert image colors"""
    return image.invert()

def blur(image: Image, kernel_size: int = 3) -> Image:
    """Apply blur filter"""
    return image.blur(kernel_size)

def sharpen(image: Image) -> Image:
    """Apply sharpening filter"""
    return image.sharpen()

def detect_edges(image: Image) -> Image:
    """Detect edges in image"""
    return image.edge_detect()

def threshold(image: Image, threshold_val: int = 128) -> Image:
    """Apply threshold to image"""
    return image.threshold(threshold_val)

def adjust_brightness(image: Image, factor: float) -> Image:
    """Adjust image brightness"""
    return image.brightness_adjust(factor)

def adjust_contrast(image: Image, factor: float) -> Image:
    """Adjust image contrast"""
    return image.contrast_adjust(factor)

def get_histogram(image: Image) -> dict:
    """Get color histogram"""
    return image.histogram()
