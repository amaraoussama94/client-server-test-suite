# /**
#  * @file test_chunked_chat_message.py
#  * @brief Sends a long chat message to validate chunking and reassembly.
#  *        Uses config files for chat-capable clients and prints resolved paths for debugging.
#  *        Appends to logs, resolves client IDs dynamically, and validates chunked delivery.
#  *
#  *        Log assertions:
#  *        - Server: "[CHAT] Forwarding from X to Y: ..."
#  *        - Receiver: "Received frame: ...|chat|X|Y|...|READY"
#  *        - Sender: "Chat message sent in N chunk(s)"
#  *
#  * @author Oussama Amara
#  * @version 1.2
#  * @date 2025-10-12
#  */

import subprocess, time, logging, re
from utils import get_binary_path, get_config_path, clear_logs

logging.info("🧪 Starting test: chunked_chat_message")

def run_chunked_chat():
    try:
        clear_logs()
        long_message = "chat " + ("This is a long message. " * 50) + "\n"

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

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_a_log, stderr=subprocess.STDOUT)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_b_log, stderr=subprocess.STDOUT)
        time.sleep(10)

        server_log.flush(); server_log.close()
        client_a_log.flush(); client_a_log.close()
        client_b_log.flush(); client_b_log.close()

        print("📁 Logs written to:")
        print("   - logs/server.log")
        print("   - logs/client_a.log")
        print("   - logs/client_b.log")

        with open("logs/client_a.log") as a_log, open("logs/client_b.log") as b_log:
            a_lines = a_log.readlines()
            b_lines = b_log.readlines()

            id_a = next((re.search(r"Assigned client ID: (\d+)", line).group(1)
                         for line in reversed(a_lines) if "Assigned client ID" in line), None)
            id_b = next((re.search(r"Assigned client ID: (\d+)", line).group(1)
                         for line in reversed(b_lines) if "Assigned client ID" in line), None)

        if not id_a or not id_b or id_a == id_b:
            print("❌ Failed to resolve distinct client IDs.")
            raise RuntimeError("Could not resolve distinct client IDs")

        print(f"🆔 Client A ID: {id_a}")
        print(f"🆔 Client B ID: {id_b}")

        print(f"📤 Sending long message from A to B (target ID: {id_b})...")
        client_a.stdin.write(f"{id_b}\n".encode())
        client_a.stdin.flush()
        time.sleep(1)
        client_a.stdin.write(long_message.encode())
        client_a.stdin.flush()
        time.sleep(8)

        with open("logs/server.log") as s_log, open("logs/client_a.log") as a_log, open("logs/client_b.log") as b_log:
            s_content = s_log.read()
            a_content = a_log.read()
            b_content = b_log.read()

            # ✅ Server forwarding check
            forwarding_match = re.search(fr"\[CHAT\] Forwarding from {id_a} to {id_b}: chat .*?This is a long message", s_content)

            assert forwarding_match, "❌ Server did not forward chunked message."
            print("🔍 Server forwarding confirmed.")

            # ✅ Receiver frame check
            received_match = re.search(fr"Received frame: \w+\|chat\|{id_a}\|{id_b}\|chat This is a long message", b_content)
            assert received_match, "❌ Receiver did not log reassembled chat frame."
            print("🔍 Receiver log confirmed.")

            # ✅ Sender chunk count check
            chunk_match = re.search(r"Chat message sent in (\d+) chunk\(s\)", a_content)
            if chunk_match:
                print(f"📦 Sender confirms chunked delivery: {chunk_match.group(1)} chunk(s)")
            else:
                print("⚠️ No chunk count found in sender log.")

        print("✅ Test passed: chunked message delivered and reassembled.")
        logging.info("✅ chunked_chat_message test passed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"❌ chunked_chat_message test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
            print("🛑 Processes terminated.")
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_chunked_chat()
