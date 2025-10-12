# /**
#  * @file utils.py
#  * @brief Shared utility functions for test scripts.
#  *        Handles OS detection, binary path resolution, dynamic versioning, config pathing, logging, and log cleanup.
#  *        Ensures clean test environments by clearing logs before each run.
#  *
#  *        Functions:
#  *        - get_latest_version(): Detects latest version folder in bins/
#  *        - get_binary_path(name): Resolves platform-specific binary path
#  *        - get_config_path(name): Resolves config file path by alias
#  *        - clear_logs(): Empties logs/ folder before each test
#  *
#  * @author Oussama Amara
#  * @version 2.3
#  * @date 2025-10-12
#  */

import platform, os, re, logging

# Setup logger
logging.basicConfig(
    filename="test_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_latest_version():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    bins_dir = os.path.join(SCRIPT_DIR, "..", "bins")
    versions = []

    logging.debug(f"Scanning bins directory: {bins_dir}")

    try:
        for entry in os.listdir(bins_dir):
            if re.match(r'^\d+\.\d+$', entry):
                versions.append(entry)
                logging.debug(f"Found version folder: {entry}")
    except FileNotFoundError:
        logging.error(f"Bins directory not found: {bins_dir}")
        raise

    if not versions:
        logging.error("No version folders found in bins/")
        raise FileNotFoundError("No version folders found in bins/")

    versions.sort(key=lambda v: [int(x) for x in v.split('.')])
    latest = versions[-1]
    logging.info(f"Latest version selected: {latest}")
    return latest

def get_binary_path(name):
    system = platform.system()
    version = get_latest_version()
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(SCRIPT_DIR, "..", "bins", version, "windows" if system == "Windows" else "linux")
    ext = ".exe" if system == "Windows" else ""
    binary_path = os.path.abspath(os.path.join(base, f"{name}{ext}"))

    logging.info(f"Resolved binary path for '{name}': {binary_path}")
    return binary_path

def get_config_path(name):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    config_map = {
        "server": "server.cfg",
        "client_local": "client_local.cfg",
        "client_remote": "client_remote.cfg",
        "client_remote_file": "client_remote_file.cfg",
        "client_local_file": "client_local_file.cfg",
    }
    filename = config_map.get(name)
    if not filename:
        raise ValueError(f"Unknown config name: {name}")
    config_path = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "configs", filename))
    logging.info(f"Resolved config path for '{name}': {config_path}")
    return config_path

def clear_logs():
    """
    Clears all files in the logs/ directory to ensure clean test output.
    Creates the folder if it doesn't exist.
    """
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(SCRIPT_DIR, "..", "logs")
    os.makedirs(logs_dir, exist_ok=True)

    for f in os.listdir(logs_dir):
        try:
            os.remove(os.path.join(logs_dir, f))
            logging.debug(f"Deleted log file: {f}")
        except Exception as e:
            logging.warning(f"⚠️ Could not delete log file {f}: {e}")
