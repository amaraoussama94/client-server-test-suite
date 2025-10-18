# /**
#  * @file test_client_list_broadcast.py
#  * @brief Validates LIST frame broadcast when clients connect/disconnect.
#  *        Ensures server updates all clients with active list.
#  *        Uses config files for chat-capable clients and prints resolved paths for debugging.
#  *
#  *        Log assertions:
#  *        - Client A: "Received frame: ...|system|0|X|Y,Client|LIST"
#  *        - Client A: "Received frame: ...|system|0|X|Y|LIST" (after disconnect)
#  *
#  * @author Oussama Amara
#  * @version 1.2
#  * @date 2025-10-13
#  */

import subprocess, time, logging, re
from utils import get_binary_path, get_config_path, clear_logs

logging.info("🧪 Starting test: client_list_broadcast")

def run_list_broadcast():
    try:
        clear_logs()
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local")

        print("🔧 Paths resolved:")
        print("   - Server bin :", server_bin)
        print("   - Client bin :", client_bin)
        print("   - Server cfg :", server_cfg)
        print("   - Client cfg :", client_cfg)

        server_log = open("logs/server.log", "a")
        client_a_log = open("logs/client_a.log", "a")
        client_b_log = open("logs/client_b.log", "a")

        print("🚀 Launching server and clients...")
        server = subprocess.Popen([server_bin, server_cfg], stdout=server_log, stderr=subprocess.STDOUT)
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdout=client_a_log, stderr=subprocess.STDOUT)
        time.sleep(1)

        client_b = subprocess.Popen([client_bin, client_cfg], stdout=client_b_log, stderr=subprocess.STDOUT)
        time.sleep(15)

        client_b.terminate()
        time.sleep(5)

        server_log.flush(); server_log.close()
        client_a_log.flush(); client_a_log.close()
        client_b_log.flush(); client_b_log.close()

        print("📁 Logs written to:")
        print("   - logs/server.log")
        print("   - logs/client_a.log")
        print("   - logs/client_b.log")

        # Validate LIST frames in client A log
        with open("logs/client_a.log") as a_log:
            content = a_log.read()
            connect_match = re.search(r"Received frame: \w+\|system\|0\|\d+\|.*,Client\|LIST", content)
            disconnect_match = re.search(r"Received frame: \w+\|system\|0\|\d+\|\d+,Client\|LIST", content)

            if not connect_match or not disconnect_match:
                print("📄 Client A log preview:\n", "\n".join(content.splitlines()[-40:]))
                raise AssertionError("❌ Client A did not receive LIST frame updates.")

            print("🔍 LIST frame on connect confirmed.")
            print("🔍 LIST frame on disconnect confirmed.")

        print("✅ Test passed: LIST frame broadcast verified.")
        logging.info("✅ client_list_broadcast test passed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"❌ client_list_broadcast test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            print("🛑 Processes terminated.")
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_list_broadcast()