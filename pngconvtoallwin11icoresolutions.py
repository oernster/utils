#!/usr/bin/env python3
"""
PNG to ICO Converter using ImageMagick

This script converts a PNG image to an ICO file with multiple sizes
suitable for Windows 11 applications using ImageMagick.

Usage:
    python png_to_ico.py input.png output.ico
"""

import sys
import os
import subprocess
import tempfile
import shutil


def check_imagemagick():
    """Check if ImageMagick is installed."""
    try:
        subprocess.run(['magick', '--version'], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False


def convert_png_to_ico(input_path, output_path):
    """
    Convert a PNG file to an ICO file with multiple sizes using ImageMagick.
    
    Args:
        input_path (str): Path to the input PNG file.
        output_path (str): Path to save the output ICO file.
    """
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.")
        return False
        
    # Check if ImageMagick is installed
    if not check_imagemagick():
        print("Error: ImageMagick is not installed or not in PATH.")
        print("Please install ImageMagick from https://imagemagick.org/script/download.php")
        return False
    
    try:
        # Create a temporary directory to store resized images
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define the sizes required for a Windows 11 ICO
            # Windows 11 typically uses: 16, 20, 24, 28, 32, 40, 48, 56, 64, 96, 128, 256
            sizes = [16, 20, 24, 28, 32, 40, 48, 56, 64, 96, 128, 256]
            resized_images = []
            
            # Resize the image to each size using ImageMagick
            for size in sizes:
                output_temp = os.path.join(temp_dir, f"icon_{size}x{size}.png")
                
                # Use ImageMagick to resize the image with high quality
                subprocess.run([
                    'magick',
                    'convert',
                    input_path,
                    '-resize', f"{size}x{size}",
                    '-background', 'transparent',
                    '-gravity', 'center',
                    '-extent', f"{size}x{size}",
                    output_temp
                ], check=True)
                
                resized_images.append(output_temp)
            
            # Combine all resized images into a single ICO file
            convert_cmd = ['magick', 'convert']
            convert_cmd.extend(resized_images)
            convert_cmd.append(output_path)
            
            # Run the ImageMagick command to create the ICO file
            subprocess.run(convert_cmd, check=True)
            
            print(f"Successfully converted '{input_path}' to '{output_path}' with sizes: {sizes}")
            return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing ImageMagick command: {e}")
        return False
    except Exception as e:
        print(f"Error converting PNG to ICO: {e}")
        return False


def main():
    """Main entry point of the script."""
    # Check arguments
    if len(sys.argv) != 3:
        print("Usage: python png_to_ico.py input.png output.ico")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Ensure output path ends with .ico
    if not output_path.lower().endswith('.ico'):
        output_path += '.ico'
    
    # Convert the PNG to ICO
    success = convert_png_to_ico(input_path, output_path)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()