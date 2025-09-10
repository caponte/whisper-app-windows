import os
import subprocess
import sys
import platform
import urllib.request
import zipfile

def is_python_installed():
    """Check if Python is installed and return its version."""
    try:
        version = subprocess.check_output([sys.executable, '--version'], stderr=subprocess.STDOUT)
        return version.decode().strip()
    except Exception:
        return None

def download_python_installer():
    """Download the Python installer based on the OS."""
    os_type = platform.system()
    if os_type == "Windows":
        url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
        installer_name = "python_installer.exe"
    elif os_type == "Linux":
        url = "https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz"
        installer_name = "python_installer.tgz"
    elif os_type == "Darwin":  # macOS
        url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-macos11.pkg"
        installer_name = "python_installer.pkg"
    else:
        raise Exception("Unsupported operating system.")

    print(f"Downloading Python installer from {url}...")
    urllib.request.urlretrieve(url, installer_name)
    return installer_name

def install_python(installer_name):
    """Install Python using the downloaded installer."""
    os_type = platform.system()
    if os_type == "Windows":
        subprocess.run([installer_name, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'])
    elif os_type == "Linux":
        with zipfile.ZipFile(installer_name, 'r') as zip_ref:
            zip_ref.extractall("/tmp/python_install")
        os.chdir("/tmp/python_install/Python-3.10.0")
        subprocess.run(['./configure'])
        subprocess.run(['make'])
        subprocess.run(['make', 'install'])
    elif os_type == "Darwin":
        subprocess.run(['installer', '-pkg', installer_name, '-target', '/'])
    else:
        raise Exception("Unsupported operating system.")

def main():
    """Main function to check Python installation and install if necessary."""
    python_version = is_python_installed()
    if python_version:
        print(f"Python is already installed: {python_version}")
    else:
        print("Python is not installed. Proceeding with installation...")
        installer_name = download_python_installer()
        install_python(installer_name)
        print("Python installation completed.")

if __name__ == "__main__":
    main()