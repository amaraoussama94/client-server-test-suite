# /**
#  * @file test_smoke_local.py
#  * @brief Basic startup test: server + one client, validate launch and command handling.
#  *        Uses config files for both server and client.
#  *        Confirms connection and ID assignment by parsing server and client logs.
#  *        Ensures logs/ folder exists before writing output.
#  *        Stops parsing once expected behavior is confirmed.
#  *
#  *        Log assertions:
#  *        - Server: "Accepted connection", "Sent ID_ASSIGN"
#  *        - Client: "Connected to server", "Assigned client ID"
#  *
#  *        Logs are saved to logs/server.log and logs/client_local.log.
#  *        This test ensures local socket communication and validates protocol handshake.
#  *
#  * @author Oussama Amara
#  * @version 1.4
#  * @date 2025-10-12
#  */

import subprocess, time, logging, re, os
from utils import get_binary_path, get_config_path, clear_logs

logging.info("🧪 Starting test: smoke_local")

def run_smoke_local():
    try:
        clear_logs()
        os.makedirs("logs", exist_ok=True)  # ✅ Ensure logs/ exists

        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        server_log = open("logs/server.log", "w")
        client_log = open("logs/client_local.log", "w")

        server = subprocess.Popen(
            [server_bin, server_cfg],
            stdout=server_log,
            stderr=subprocess.STDOUT
        )
        print("✅ Server process started.")
        time.sleep(1)

        client = subprocess.Popen(
            [client_bin, client_cfg],
            stdin=subprocess.PIPE,
            stdout=client_log,
            stderr=subprocess.STDOUT
        )
        print("✅ Client process started.")
        time.sleep(2)

        client.stdin.write(b"ping\n")
        client.stdin.flush()
        time.sleep(1)

        server_log.flush()
        server_log.close()
        client_log.flush()
        client_log.close()
        print("📁 Server log closed.")
        print("📁 Client log closed.")

        # ✅ Log validation
        with open("logs/server.log") as s_log, open("logs/client_local.log") as c_log:
            s_content = s_log.read()
            c_content = c_log.read()

            print("🔍 Server log preview:\n", s_content[:300])
            print("🔍 Client log preview:\n", c_content[:300])

            assert "Accepted connection" in s_content
            assert "Sent ID_ASSIGN" in s_content
            assert "Connected to server" in c_content
            assert re.search(r"Assigned client ID: \d+", c_content)

        logging.info("✅ smoke_local test passed.")
    except Exception as e:
        logging.error(f"❌ smoke_local test failed: {e}")
    finally:
        try:
            server.terminate()
            client.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_smoke_local()
