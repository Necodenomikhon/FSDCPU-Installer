import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import tempfile
import shutil
import zipfile
import urllib.request

repo_owner = "Necodenomikhon"
repo_name = "fastsdcpu"
branch = "main"
downloaded_repo_path = None  # Will hold full path once downloaded

import subprocess
import sys
import os

def force_install_python311():
    python_installer = os.path.join(os.path.dirname(__file__), "python3-11_installer.py")
    print("Running python3-11_installer.py with current interpreter...")

    subprocess.run([sys.executable, python_installer], check=True)

def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", e.stderr or str(e))
        return None

def has_write_permission(path):
    try:
        test_file = os.path.join(path, '.__permission_test__')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except Exception:
        return False


def download_repo_zip(install_path, root_window):
    zip_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{branch}.zip"

    try:
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"{repo_name}.zip")

        messagebox.showinfo("Downloading", f"Downloading repository ZIP...\n{zip_url}", parent=root_window)
        urllib.request.urlretrieve(zip_url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        extracted_folder = os.path.join(temp_dir, f"{repo_name}-{branch}")
        downloaded_repo_path = os.path.join(install_path, repo_name)

        # Ensure clean target
        if os.path.exists(downloaded_repo_path):
            shutil.rmtree(downloaded_repo_path)

        shutil.move(extracted_folder, downloaded_repo_path)

        messagebox.showinfo("Success", f"Repository downloaded to:\n{downloaded_repo_path}", parent=root_window)

    except Exception as e:
        messagebox.showerror("Download Failed", f"Could not download the repository:\n{e}", parent=root_window)
    
    root_window.destroy()
    open_install_window()


def run_install_script():
    force_install_python311()
    if not downloaded_repo_path:
        messagebox.showerror("Error", "Repository has not been downloaded yet.")
        return

    bat_path = os.path.join(downloaded_repo_path, "install.bat")

    if not os.path.exists(bat_path):
        messagebox.showerror("Error", f"install.bat not found at:\n{bat_path}")
        return

    try:
        subprocess.run([bat_path], check=True, cwd=downloaded_repo_path)
        messagebox.showinfo("Success", "Installation completed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running install.bat:\n{e}")

def open_install_window():
    install_win = tk.Tk()
    install_win.title("Start Installation")
    install_win.geometry("350x150")

    tk.Label(install_win, text="Repository downloaded.\nClick Start Installation or Cancel.").pack(pady=15)

    tk.Button(install_win, text="Start Installation", command=run_install_script).pack(pady=5)
    tk.Button(install_win, text="Cancel", command=install_win.quit).pack(pady=5)

    install_win.mainloop()

def select_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

def start_download(entry_widget, root_window):
    install_path = entry_widget.get()
    if not os.path.isdir(install_path):
        messagebox.showerror("Error", "Please select a valid directory.")
        return
    if not has_write_permission(install_path):
        messagebox.showerror("Permission Denied", f"No write access to:\n{install_path}")
        return
    download_repo_zip(install_path, root_window)

def main():
    root = tk.Tk()
    root.title("FastSD CPU Install Wizard")
    root.geometry("450x250")

    tk.Label(root, text="Select a directory to download the repository:").pack(pady=10)

    directory_entry = tk.Entry(root, width=50)
    directory_entry.pack(pady=5)

    tk.Button(root, text="Browse", command=lambda: select_directory(directory_entry)).pack(pady=5)
    tk.Button(root, text="Download Repository", command=lambda: start_download(directory_entry, root)).pack(pady=15)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
