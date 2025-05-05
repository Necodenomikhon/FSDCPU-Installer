import os
import shutil
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
import urllib.request
import zipfile

import python3_11_installer

class InstallWizard:
    def __init__(self):
        self.repo_owner = "Necodenomikhon"
        self.repo_name = "fastsdcpu"
        self.branch = "main"
        self.downloaded_repo_path = None

        self.install_path = ""
        self.root_window = None
        self.install_python_window = None
        self.install_window = None

    def run(self):
        self.root_window = tk.Tk()
        self.root_window.title("FastSD CPU Install Wizard")
        self.root_window.geometry("450x250")

        tk.Label(self.root_window, text="Select a directory to download the repository:").pack(pady=10)

        self.directory_entry = tk.Entry(self.root_window, width=50)
        self.directory_entry.pack(pady=5)

        tk.Button(self.root_window, text="Browse", command=self.select_directory).pack(pady=5)
        tk.Button(self.root_window, text="Download Repository", command=self.start_download).pack(pady=15)
        tk.Button(self.root_window, text="Exit", command=self.root_window.quit).pack(pady=5)

        self.root_window.mainloop()

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)

    def start_download(self):
        self.install_path = self.directory_entry.get()
        if not os.path.isdir(self.install_path):
            messagebox.showerror("Error", "Please select a valid directory.")
            return
        if not self.has_write_permission(self.install_path):
            messagebox.showerror("Permission Denied", f"No write access to:\n{self.install_path}")
            return
        self.download_repo_zip()

    def has_write_permission(self, path):
        try:
            test_file = os.path.join(path, '.__permission_test__')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except Exception:
            return False

    def download_repo_zip(self):
        zip_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/archive/refs/heads/{self.branch}.zip"

        try:
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, f"{self.repo_name}.zip")

            messagebox.showinfo("Downloading", f"Downloading repository ZIP...\n{zip_url}", parent=self.root_window)
            urllib.request.urlretrieve(zip_url, zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            extracted_folder = os.path.join(temp_dir, f"{self.repo_name}-{self.branch}")
            self.downloaded_repo_path = os.path.join(self.install_path, self.repo_name)

            if os.path.exists(self.downloaded_repo_path):
                shutil.rmtree(self.downloaded_repo_path)
            shutil.move(extracted_folder, self.downloaded_repo_path)

            messagebox.showinfo("Success", f"Repository downloaded to:\n{self.downloaded_repo_path}", parent=self.root_window)
            self.root_window.destroy()
            self.open_install_python_window()

        except Exception as e:
            messagebox.showerror("Download Failed", f"Could not download the repository:\n{e}", parent=self.root_window)

    def open_install_python_window(self):
        self.install_python_window = tk.Tk()
        self.install_python_window.title("Start Python Installation")
        self.install_python_window.geometry("350x250")

        tk.Label(self.install_python_window, text=(
            "Repository downloaded.\n"
            "Python 3.11 is required to run FastSDCPU.\n"
            "If you have Python 3.11 already, Click Skip.\n"
            "Otherwise, Click Start Installation or Cancel."
        )).pack(pady=15)

        tk.Button(self.install_python_window, text="Start Python 3.11 Installation",
                  command=self.force_install_python311).pack(pady=5)
        tk.Button(self.install_python_window, text="Skip to FastSD CPU Installation",
                  command=self.open_install_window).pack(pady=5)
        tk.Button(self.install_python_window, text="Cancel",
                  command=self.install_python_window.quit).pack(pady=5)

        self.install_python_window.mainloop()

    def force_install_python311(self):
        try:
            python3_11_installer.install_python311()
            self.open_install_window()
        except Exception as e:
            messagebox.showerror("Error", f"Python 3.11 installation failed:\n{e}")

    def open_install_window(self):
        if self.install_python_window:
            self.install_python_window.destroy()

        self.install_window = tk.Tk()
        self.install_window.title("Start Installation")
        self.install_window.geometry("350x150")

        tk.Label(self.install_window, text="Repository downloaded.\nClick Start Installation or Cancel.").pack(pady=15)

        tk.Button(self.install_window, text="Start Installation", command=self.run_install_script).pack(pady=5)
        tk.Button(self.install_window, text="Cancel", command=self.install_window.quit).pack(pady=5)

        self.install_window.mainloop()

    def run_install_script(self):
        self.install_window.destroy()

        if not self.downloaded_repo_path:
            messagebox.showerror("Error", "Repository has not been downloaded yet.")
            return

        bat_path = os.path.join(self.downloaded_repo_path, "install.bat")
        if not os.path.exists(bat_path):
            messagebox.showerror("Error", f"install.bat not found at:\n{bat_path}")
            return

        try:
            subprocess.run([bat_path], check=True, cwd=self.downloaded_repo_path)
            messagebox.showinfo("Success", "Installation completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running install.bat:\n{e}")

if __name__ == "__main__":
    wizard = InstallWizard()
    wizard.run()
