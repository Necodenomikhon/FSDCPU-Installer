import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import messagebox, simpledialog

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", e.stderr)
        return None

def clone_repository():
    """Clone the GitHub repository."""
    repo_url = "https://github.com/Necodenomikhon/fastsdcpu"
    messagebox.showinfo("Cloning", f"Cloning repository from {repo_url}...")
    run_command(['git', 'clone', repo_url])
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    # Change path to repository directory for later operation
    os.chdir("fastsdcpu")
    return repo_name

def run_install_script(install_path):
    """Run the install.bat script."""
    try:
        # Change the working directory to the specified path
        os.chdir(install_path)
        # Clone repo to the specified path
        clone_repository()
        # Run the install.bat script
        subprocess.run(['install.bat'], check=True)
        messagebox.showinfo("Success", "Installation completed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_directory():
    """Open a dialog to select the directory for downloading the repository."""
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)  # Clear the entry field
        directory_entry.insert(0, directory)  # Insert the selected directory

def start_installation():
    """Start the installation process."""
    install_path = directory_entry.get()
    if os.path.isdir(install_path):
        run_install_script(install_path)
    else:
        messagebox.showerror("Error", "Please select a valid directory.")

def main():
    """Create the main application window."""
    global directory_entry  # Make the entry field accessible in other functions

    root = tk.Tk()
    root.title("Install Wizard")
    root.geometry("400x200")

    # Label
    label = tk.Label(root, text="Select the directory to download the repository:")
    label.pack(pady=10)

    # Entry field for directory
    directory_entry = tk.Entry(root, width=40)
    directory_entry.pack(pady=5)

    # Browse button
    browse_button = tk.Button(root, text="Browse", command=select_directory)
    browse_button.pack(pady=5)

    # Start Installation button
    start_button = tk.Button(root, text="Start Installation", command=start_installation)
    start_button.pack(pady=20)

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
