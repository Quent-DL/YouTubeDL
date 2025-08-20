import os
import winreg
import subprocess
from pathlib import Path
import platform

import tkinter


def get_output_folder_path() -> str:

    def windows_download_folder() -> str:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
            downloads, _ = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')
            return os.path.expandvars(downloads)
        
    def linux_macos_download_folder() -> str:
        path = subprocess.check_output(['xdg-user-dir', 'DOWNLOAD'], text=True).strip()
        return path
    

    try:
        if platform.system() == "Windows":
            dl_path = windows_download_folder()
        elif platform.system() in ("Linux", "Darwin"):
            dl_path = linux_macos_download_folder()
        else:
            dl_path = str(Path.home() / 'Downloads')  # fallback
    except:
        dl_path = str(Path.home() / 'Downloads')  # fallback

    return os.path.join(dl_path, "YouTubeDL")
