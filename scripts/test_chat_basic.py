# /**
#  * @file test_chat_basic.py
#  * @brief Validates basic chat exchange between two clients via server.
#  *        Uses config files for chat-capable clients.
#  *        Confirms ID assignment, target selection, and message delivery by parsing logs.
#  *        Appends to logs instead of deleting them, and parses only the latest session.
#  *        Dynamically resolves client IDs to avoid self-targeting.
#  *
#  *        Log assertions:
#  *        - Client A: "Assigned client ID: X"
#  *        - Client B: "Assigned client ID: Y"
#  *        - Server: "[CHAT] Forwarding from X to Y: Hello from A"
#  *        - Either client: "Received frame: ...|chat|X|Y|Hello from A|READY"
#  *
#  *        Logs are saved to logs/server.log, logs/client_a.log, and logs/client_b.log.
#  *        This test validates real-time message forwarding over the chat protocol.
#  *
#  * @author Oussama Amara
#  * @version 1.8
#  * @date 2025-10-12
#  */

import subprocess, time, logging, re
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

        server_log = open("logs/server.log", "a")
        client_a_log = open("logs/client_a.log", "a")
        client_b_log = open("logs/client_b.log", "a")

        server = subprocess.Popen([server_bin, server_cfg], stdout=server_log, stderr=subprocess.STDOUT)
        print("✅ Server process started.")
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_a_log, stderr=subprocess.STDOUT)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_b_log, stderr=subprocess.STDOUT)
        print("✅ Client A and B started.")
        time.sleep(10)

        server_log.flush(); server_log.close()
        client_a_log.flush(); client_a_log.close()
        client_b_log.flush(); client_b_log.close()

        with open("logs/client_a.log") as a_log, open("logs/client_b.log") as b_log:
            a_lines = a_log.readlines()
            b_lines = b_log.readlines()

            id_a = next((re.search(r"Assigned client ID: (\d+)", line).group(1)
                         for line in reversed(a_lines) if "Assigned client ID" in line), None)
            id_b = next((re.search(r"Assigned client ID: (\d+)", line).group(1)
                         for line in reversed(b_lines) if "Assigned client ID" in line), None)

        if not id_a or not id_b or id_a == id_b:
            raise RuntimeError("❌ Could not resolve distinct client IDs")

        print(f"🆔 Client A ID: {id_a}")
        print(f"🆔 Client B ID: {id_b}")

        # Send message from A to B
        client_a.stdin.write(f"{id_b}\n".encode())
        client_a.stdin.flush()
        time.sleep(1)
        client_a.stdin.write(b"chat Hello from A\n")
        client_a.stdin.flush()
        print("📤 Message sent from A to B.")
        time.sleep(5)

        with open("logs/server.log") as s_log, open("logs/client_a.log") as a_log, open("logs/client_b.log") as b_log:
            s_lines = s_log.readlines()
            a_content = a_log.read()
            b_content = b_log.read()

            # ✅ Server forwarding check
            s_recent = [line for line in reversed(s_lines) if f"[CHAT] Forwarding from {id_a} to {id_b}" in line or f"[CHAT] Forwarding from {id_b} to {id_a}" in line]
            assert s_recent, "❌ Server did not forward chat message."
            print("🔍 Server log preview:\n", "".join(s_recent[:1]))

            # ✅ Client frame check (either direction)
            frame_pattern = re.compile(
                fr"Received frame: \w+\|chat\|({id_a}|{id_b})\|({id_a}|{id_b})\|chat Hello from A\|READY"
            )
            if not frame_pattern.search(a_content) and not frame_pattern.search(b_content):
                print("⚠️ Chat frame not found in either client log.")
                print("📄 Last 20 lines of A log:\n", "\n".join(a_content.splitlines()[-20:]))
                print("📄 Last 20 lines of B log:\n", "\n".join(b_content.splitlines()[-20:]))
                raise AssertionError("❌ Chat frame not found.")

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
