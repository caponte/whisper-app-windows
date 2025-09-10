def is_python_installed():
    """Check if Python is installed on the system."""
    try:
        subprocess.run(["python", "--version"], capture_output=True, text=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def get_python_version():
    """Get the installed Python version."""
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception:
        return None