import os

def list_python_files(directory='.', output_file='python_files.txt'):
    """
    Recursively find all Python files in the given directory, 
    excluding virtual environment directories.
    
    Args:
        directory (str): Directory to search (default: current directory)
        output_file (str): File to write Python file paths to
    """
    # Find all Python scripts
    python_scripts = []
    for root, dirs, files in os.walk(directory):
        # Skip virtual environment directories
        dirs[:] = [d for d in dirs if d not in {'venv', '.venv', 'env', '.env', 'virtualenv'}]
        
        # Find .py files
        python_scripts.extend([
            os.path.normpath(os.path.join(root, file)).replace(os.path.normpath(directory) + os.sep, '')
            for file in files 
            if file.endswith('.py')
        ])
    
    # Sort scripts alphabetically
    python_scripts.sort()
    
    # Write paths to output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for script in python_scripts:
            outfile.write(f"- {script}\n")
    
    # Print total number of Python files found
    print(f"Found {len(python_scripts)} Python files. List written to {output_file}")
    
    # Optionally, print to console as well
    for script in python_scripts:
        print(f"- {script}")

# Run the script when executed directly
if __name__ == "__main__":
    list_python_files()