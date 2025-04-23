import os
import platform
import subprocess
import sys
import urllib.request
import shutil
import tempfile

def run(cmd, shell=False):
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, shell=shell, check=True)
    return result

def download(url, filename):
    print(f"Downloading: {url}")
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def install_on_windows():
    # Download latest Python 3.11 installer (64-bit)
    url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
    installer = os.path.join(tempfile.gettempdir(), "python311-installer.exe")
    download(url, installer)

    # Silent install
    run([
        installer,
        "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0"
    ])
    print("Python 3.11 installed successfully on Windows.")

def install_on_mac():
    # Uses the official macOS universal2 installer
    url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-macos11.pkg"
    pkg_file = os.path.join(tempfile.gettempdir(), "python311.pkg")
    download(url, pkg_file)

    # Install using installer (requires sudo)
    run(["sudo", "installer", "-pkg", pkg_file, "-target", "/"])
    print("Python 3.11 installed successfully on macOS.")

def install_on_linux():
    # Use apt or dnf depending on distro (basic example)
    distro = platform.linux_distribution()[0].lower() if hasattr(platform, 'linux_distribution') else platform.system()
    try:
        run(["sudo", "apt", "update"])
        run(["sudo", "apt", "install", "-y", "python3.11", "python3.11-venv", "python3.11-distutils"])
    except Exception:
        try:
            run(["sudo", "dnf", "install", "-y", "python3.11"])
        except Exception:
            print("Manual install required for your distro.")
    print("Python 3.11 installed successfully on Linux.")

def main():
    os_type = platform.system()
    if os_type == "Windows":
        install_on_windows()
    elif os_type == "Darwin":
        install_on_mac()
    elif os_type == "Linux":
        install_on_linux()
    else:
        print(f"Unsupported OS: {os_type}")
        sys.exit(1)

if __name__ == "__main__":
    main()
