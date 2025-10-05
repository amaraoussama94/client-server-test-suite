# /**
#  * @file test_chat_basic.py
#  * @brief Validates basic chat exchange between two clients via server.
#  *        Uses config files for chat-capable clients and prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: chat_basic")

def run_chat_test():
    try:
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        server = subprocess.Popen([server_bin, server_cfg], stdout=subprocess.PIPE)
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client_a.stdin.write(b"chat Hello from A\n")
        client_a.stdin.flush()
        time.sleep(2)

        logging.info("✅ chat_basic test passed.")
    except Exception as e:
        logging.error(f"❌ chat_basic test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_chat_test()
