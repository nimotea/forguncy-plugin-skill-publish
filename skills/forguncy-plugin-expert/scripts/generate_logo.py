#!/usr/bin/env python3
"""
Logo Generation Script for Forguncy Plugins.
Designed to be AI-friendly: The implementation details (rendering) are fixed,
while the creative aspects (colors, text, styles) are injectable via configuration.

Dependencies:
    pip install Pillow

Usage:
    python generate_logo.py [--config config.json]
    python generate_logo.py --text "MyPlugin" --bg-color-start "#FF0000" --bg-color-end "#0000FF"
"""

import sys
import json
import argparse
import os
import platform
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
except ImportError:
    print("Error: Pillow is required. Please install it via 'pip install Pillow'")
    sys.exit(1)

def get_system_font_path():
    """Try to find a good sans-serif font on the system."""
    system = platform.system()
    if system == "Windows":
        fonts = ["arialbd.ttf", "arial.ttf", "msyhbd.ttc", "msyh.ttc", "seguiemj.ttf"]
        font_dir = Path("C:/Windows/Fonts")
        for font in fonts:
            if (font_dir / font).exists():
                return str(font_dir / font)
    elif system == "Darwin": # macOS
        fonts = ["Arial.ttf", "Helvetica.ttc", "PingFang.ttc"]
        font_dirs = [Path("/Library/Fonts"), Path("/System/Library/Fonts")]
        for fd in font_dirs:
            for font in fonts:
                if (fd / font).exists():
                    return str(fd / font)
    elif system == "Linux":
        # Common locations on Linux
        fonts = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                 "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"]
        for font in fonts:
            if Path(font).exists():
                return font
    
    return None

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(width, height, start_color, end_color, direction='vertical'):
    """Create a gradient image."""
    base = Image.new('RGBA', (width, height), start_color)
    top = Image.new('RGBA', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        for x in range(width):
            if direction == 'vertical':
                mask_data.append(int(255 * (y / height)))
            else:
                mask_data.append(int(255 * (x / width)))
                
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def generate_logo(config):
    """
    Generate a logo based on the provided configuration.
    
    Config Schema:
    {
        "output_path": str,         # Path to save the file
        "size": [width, height],    # Output size, e.g., [100, 100]
        "text": str,                # Text to display, e.g., "FP"
        "font_size_ratio": float,   # Font size relative to height, default 0.5
        "font_path": str,           # Optional path to .ttf file
        "bg_color_start": str,      # Gradient start hex, e.g., "#4E73DF"
        "bg_color_end": str,        # Gradient end hex, e.g., "#224ABE"
        "text_color": str,          # Text color hex, default "#FFFFFF"
        "border_radius_ratio": float, # Corner radius relative to size, default 0.2
        "padding_ratio": float      # Padding for content, default 0.1
    }
    """
    # 1. Parse Config & Defaults
    width, height = config.get("size", [100, 100])
    output_path = config.get("output_path", "logo.png")
    text = config.get("text", "FP")
    bg_start = config.get("bg_color_start", "#4E73DF")
    bg_end = config.get("bg_color_end", "#224ABE")
    text_color = config.get("text_color", "#FFFFFF")
    radius_ratio = config.get("border_radius_ratio", 0.2)
    font_ratio = config.get("font_size_ratio", 0.5)
    
    # 2. Setup High-Res Canvas (Antialiasing)
    scale = 4 # Super-sampling factor
    w, h = width * scale, height * scale
    
    # 3. Create Background
    # Draw gradient
    try:
        c1 = hex_to_rgb(bg_start)
        c2 = hex_to_rgb(bg_end)
        # Add alpha channel
        c1 = c1 + (255,)
        c2 = c2 + (255,)
    except Exception as e:
        print(f"Color parsing error: {e}. Using blue default.")
        c1 = (78, 115, 223, 255)
        c2 = (34, 74, 190, 255)

    img = create_gradient(w, h, c1, c2)
    
    # 4. Apply Rounded Corners Mask
    mask = Image.new('L', (w, h), 0)
    draw_mask = ImageDraw.Draw(mask)
    radius = int(min(w, h) * radius_ratio)
    draw_mask.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
    
    # Apply mask
    output = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    img = output
    draw = ImageDraw.Draw(img)

    # 5. Draw Text
    if text:
        font_path = config.get("font_path")
        if not font_path:
            font_path = get_system_font_path()
            
        font_size = int(h * font_ratio)
        
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Fallback to default (ugly but works)
                print("Warning: No system font found, using default.")
                font = ImageFont.load_default()
        except Exception as e:
            print(f"Font loading error: {e}. Using default.")
            font = ImageFont.load_default()

        # Center text
        # getbbox returns (left, top, right, bottom)
        left, top, right, bottom = font.getbbox(text)
        text_w = right - left
        text_h = bottom - top
        
        # Auto-fit logic: If text is too wide, reduce font size
        max_width = w * 0.9 # Leave 10% padding
        if text_w > max_width:
             while text_w > max_width and font_size > 5:
                 font_size -= 4 # Decrease step (in scale=4 coordinates, this is 1px)
                 font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
                 left, top, right, bottom = font.getbbox(text)
                 text_w = right - left
                 text_h = bottom - top

        # Adjust position to center
        # Note: text rendering often needs visual adjustment, especially vertically
        x = (w - text_w) / 2 - left
        y = (h - text_h) / 2 - top
        
        draw.text((x, y), text, font=font, fill=text_color)

    # 6. Downsample to target size
    final_img = img.resize((width, height), resample=Image.Resampling.LANCZOS)
    
    # 7. Save
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    final_img.save(output_path, "PNG")
    print(f"Generated: {output_path} ({width}x{height})")


def main():
    parser = argparse.ArgumentParser(description="Generate Logos for Forguncy Plugin")
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument("--text", help="Text to display on logo")
    parser.add_argument("--bg-start", help="Gradient start color (hex)")
    parser.add_argument("--bg-end", help="Gradient end color (hex)")
    
    args = parser.parse_args()
    
    # Base configuration for Plugin Logo (100x100)
    plugin_logo_config = {
        "output_path": "PluginLogo.png",
        "size": [100, 100],
        "text": "FP",
        "font_size_ratio": 0.5,
        "bg_color_start": "#4E73DF",
        "bg_color_end": "#224ABE",
        "text_color": "#FFFFFF",
        "border_radius_ratio": 0.2
    }
    
    # Base configuration for Command Icon (16x16)
    # 16x16 is very small, so we simplify: less radius, larger relative text
    command_icon_config = {
        "output_path": "CommandIcon.png",
        "size": [16, 16],
        "text": "FP",
        "font_size_ratio": 0.55, # Adjusted to avoid overflow
        "bg_color_start": "#4E73DF",
        "bg_color_end": "#224ABE",
        "text_color": "#FFFFFF",
        "border_radius_ratio": 0.2
    }

    # Override with arguments if provided
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            # If user provides a list of configs, process all
            if isinstance(user_config, list):
                for cfg in user_config:
                    generate_logo(cfg)
                return
            else:
                # Single config override
                plugin_logo_config.update(user_config)
                # For command icon, we might want to apply styles but keep size
                # Heuristic: if user config doesn't specify size/path, apply style to both
                if "size" not in user_config and "output_path" not in user_config:
                     command_icon_config.update(user_config)
                     # Restore specific sizes
                     command_icon_config["size"] = [16, 16]
                     command_icon_config["output_path"] = "CommandIcon.png"

    # Command line overrides (highest priority for style)
    if args.text:
        plugin_logo_config["text"] = args.text
        command_icon_config["text"] = args.text
    if args.bg_start:
        plugin_logo_config["bg_color_start"] = args.bg_start
        command_icon_config["bg_color_start"] = args.bg_start
    if args.bg_end:
        plugin_logo_config["bg_color_end"] = args.bg_end
        command_icon_config["bg_color_end"] = args.bg_end

    # Generate both
    print("Generating PluginLogo.png (100x100)...")
    generate_logo(plugin_logo_config)
    
    print("Generating CommandIcon.png (16x16)...")
    generate_logo(command_icon_config)

if __name__ == "__main__":
    main()
