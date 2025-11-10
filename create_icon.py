from PIL import Image, ImageDraw
import os

def create_lightning_bolt_icon():
    # Create a new image with transparency
    size = 64
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Define lightning bolt shape points (scaled for 64x64)
    lightning_points = [
        (28, 5),   # Top
        (22, 25),  # Upper bend
        (35, 25),  # Upper right
        (20, 40),  # Middle left
        (30, 40),  # Middle right
        (15, 59),  # Bottom left
        (25, 35),  # Lower bend
        (18, 35),  # Lower left
        (32, 20),  # Upper middle
        (25, 20),  # Upper left return
        (28, 5)    # Close path
    ]
    
    # Draw the lightning bolt with a yellow/gold color
    draw.polygon(lightning_points, fill=(255, 215, 0, 255), outline=(255, 165, 0, 255))
    
    # Add a slight shadow/outline for better visibility
    shadow_points = [(x+1, y+1) for x, y in lightning_points]
    draw.polygon(shadow_points, fill=(200, 150, 0, 100))
    
    # Save as ICO file (Windows icon format)
    icon_path = os.path.join(os.path.dirname(__file__), 'lightning_icon.ico')
    
    # Create multiple sizes for the ICO file
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]
    icons = []
    
    for size in sizes:
        resized_icon = icon.resize(size, Image.Resampling.LANCZOS)
        icons.append(resized_icon)
    
    # Save the ICO file with multiple sizes
    icons[0].save(icon_path, format='ICO', sizes=[(img.width, img.height) for img in icons])
    
    print(f"Lightning bolt icon created: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_lightning_bolt_icon()