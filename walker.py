#!/usr/bin/env python3
"""
Directory Walker Script

This script walks through a directory and its subdirectories,
prints a formatted list of all directories and files to the console,
and saves the output to pathlist.txt.
"""

import os
import sys
from datetime import datetime

def walk_directory(start_path, output_file):
    """
    Walk through directory and subdirectories, printing and saving the structure.
    
    Args:
        start_path (str): The directory path to start walking from
        output_file (file): An open file object to write the output to
    """
    # Check if the path exists
    if not os.path.exists(start_path):
        print(f"Error: Path '{start_path}' does not exist.")
        return
    
    # Print header information
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Get absolute full path including drive letter
    full_path = os.path.abspath(start_path)
    header = f"DIRECTORY WALKER REPORT\n"
    header += f"Full path: {full_path}\n"
    header += f"Generated on: {current_time}\n"
    header += "=" * 80 + "\n\n"
    
    print(header, end="")
    output_file.write(header)
    
    total_dirs = 0
    total_files = 0
    
    # Files to exclude
    excluded_files = ["walker.py", "walkerlist.txt"]
    
    # Walk through the directory
    for root, dirs, files in os.walk(start_path):
        # Calculate the relative level for indentation
        level = root.replace(start_path, '').count(os.sep)
        indent = '│   ' * level
        
        # Format and print directory name without full path
        dir_line = f"{indent}📁 {os.path.basename(root)}/\n"
        print(dir_line, end="")
        output_file.write(dir_line)
        total_dirs += 1
        
        # Add indentation for files
        sub_indent = '│   ' * (level + 1)
        
        # Sort files alphabetically and exclude specific files
        for file in sorted(files):
            # Skip excluded files
            if file in excluded_files:
                continue
                
            file_line = f"{sub_indent}📄 {file}\n"
            print(file_line, end="")
            output_file.write(file_line)
            total_files += 1
    
    # Print summary
    summary = f"\nSummary: Found {total_dirs} directories and {total_files} files.\n"
    print(summary)
    output_file.write(summary)

def main():
    # Get directory path from command line argument or use current directory
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    else:
        start_path = "."
    
    # Output file name
    output_filename = "walkerlist.txt"
    
    print(f"Walking directory: {os.path.abspath(start_path)}")
    print(f"Output will be saved to: {os.path.abspath(output_filename)}\n")
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            walk_directory(start_path, output_file)
        print(f"Successfully saved directory listing to {output_filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()