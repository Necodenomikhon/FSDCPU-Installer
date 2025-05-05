# FastSD CPU Installer

[Fast SD CPU](https://github.com/rupeshs/fastsdcpu) is a free, open-source image generation tool that runs Stable Diffusion models entirely on CPUs, making it ideal for local use on lower-powered machines without the need for a GPU. It enables efficient, offline AI art generation using advanced optimizations like LCM and OpenVINO to deliver fast performance even on modest hardware.

**FastSDCPU Install Wizard** is a guided installer that simplifies environment setup, Python installation, and repository deployment for Fast SD CPU.

---

## 🧰 What the Install Wizard Does

The `FSDCPU_Install_Wizard.py` is a graphical installer that automates the setup process for FastSD CPU. It:

1. **Prompts for a target install directory** using a graphical file browser.
2. **Downloads** the FastSD CPU GitHub repository as a ZIP file.
3. **Extracts and installs** the project files into the selected directory.
4. **Ensures Python 3.11 is installed** (or installs it if missing).
5. **Executes the `install.bat` script** inside the repository to complete environment configuration.

---

## 📦 What the Install Wizard Uses

The wizard and installer depend on the following components:

- **Tkinter GUI**: Provides a cross-platform graphical interface.
- **Python Standard Library**: Handles networking, file operations, subprocess management, and ZIP extraction.
- **`python3_11_installer` module**:
  - Downloads and installs Python 3.11.8 using official installers or system package managers.
  - Used as an internal module, not a subprocess, for cleaner integration.

---

## 🖥 System Requirements

- Operating System: Windows
- Internet connection (for downloading Python and the GitHub repository)
- Admin/sudo privileges for installing Python (if not already present)

---

## 🚀 Getting Started

1. Download and Run [FSDCPU_Install_Wizard.exe](https://github.com/Necodenomikhon/FSDCPU-Installer/releases/tag/v1.0.0-beta-1)
2. In the fastsdcpu folder, double-click the start.bat file.
  - Alternatively, double-click the start-webui.bat file and search http://127.0.0.1:7860 in your browser.
