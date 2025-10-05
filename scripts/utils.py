# /**
#  * @file utils.py
#  * @brief Shared utility functions for test scripts.
#  *        Handles OS detection and binary path resolution.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import platform, os

def get_binary_path(name):
    system = platform.system()
    base = os.path.join("..", "bins", "1.6", "windows" if system == "Windows" else "linux")
    ext = ".exe" if system == "Windows" else ""
    return os.path.join(base, f"{name}{ext}")
