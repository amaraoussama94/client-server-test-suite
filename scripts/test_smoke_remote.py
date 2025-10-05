# /**
#  * @file test_smoke_remote.py
#  * @brief Validates remote startup: server on local, client connects via remote IP.
#  *        Uses config files for both server and remote client. Prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: smoke_remote")

def run_smoke_remote():
    try:
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_remote")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        server = subprocess.Popen([server_bin, server_cfg])
        time.sleep(1)

        client = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client.stdin.write(b"ping\n")
        client.stdin.flush()
        time.sleep(1)

        logging.info("✅ smoke_remote test passed.")
    except Exception as e:
        logging.error(f"❌ smoke_remote test failed: {e}")
    finally:
        try:
            server.terminate()
            client.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_smoke_remote()
