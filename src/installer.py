import os
import subprocess
import sys
from src.utils.check_python import is_python_installed, get_python_version
from src.python_installer import install_python

def main():
    print("=== Python Installer ===")
    
    if is_python_installed():
        print(f"Python is already installed. Version: {get_python_version()}")
    else:
        print("Python is not installed. Starting installation process...")
        install_python()

if __name__ == "__main__":
    main()