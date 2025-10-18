# /**
#  * @file test_file_transfer.py
#  * @brief Validates file transfer between clients using INCOMING, CHUNK, DONE, ACK.
#  *        Uses test_file.txt from assets and config files for file-capable clients.
#  *        Prints resolved paths for debugging.
#  *
#  *        Log assertions:
#  *        - Server: "[FILE] Preparing to send ..."
#  *        - Server: "[FILE] Sent chunk #0"
#  *        - Server: "[FILE] Transfer complete ..."
#  *        - Receiver: "Received frame: ...|file|0|Y|...|INCOMING"
#  *        - Receiver: "Received frame: ...|file|0|Y|...|CHUNK"
#  *        - Receiver: "Received frame: ...|file|0|Y|...|DONE"
#  *        - Sender: "Received frame: ...|ack|Y|X|...|ACK"
#  *
#  * @author Oussama Amara
#  * @version 1.3
#  * @date 2025-10-18
#  */

import subprocess, time, shutil, logging, re
from utils import get_binary_path, get_config_path, clear_logs
import os

logging.info("🧪 Starting test: file_transfer")

def run_file_test():
    try:
        clear_logs()
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local_file")

        print("🔧 Paths resolved:")
        print("   - Server bin :", server_bin)
        print("   - Client bin :", client_bin)
        print("   - Server cfg :", server_cfg)
        print("   - Client cfg :", client_cfg)

        try:
            os.makedirs("assets/to_send", exist_ok=True)
            shutil.copy("assets/test_file.txt", "assets/to_send/test_file.txt")
            print("📁 Test file moved to: assets/to_send/test_file.txt")
        except Exception as e:
            logging.error(f"❌ Failed to prepare test file: {e}")
            return

        server_log = open("logs/server.log", "a")
        client_a_log = open("logs/client_a.log", "a")
        client_b_log = open("logs/client_b.log", "a")

        print("🚀 Launching server and clients...")
        server = subprocess.Popen([server_bin, server_cfg], stdout=server_log, stderr=subprocess.STDOUT)
        time.sleep(5)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_a_log, stderr=subprocess.STDOUT)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_b_log, stderr=subprocess.STDOUT)
        time.sleep(20)

        server_log.flush(); server_log.close()
        client_a_log.flush(); client_a_log.close()
        client_b_log.flush(); client_b_log.close()

        print("📁 Logs written to:")
        print("   - logs/server.log")
        print("   - logs/client_a.log")
        print("   - logs/client_b.log")

        # Extract client IDs
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

        # Send file from A to B
        print(f"📤 Sending file from Client A (ID={id_a}) → Client B (ID={id_b})")
        client_a.stdin.write(f"{id_b}\n".encode())
        client_a.stdin.flush()
        time.sleep(5)
        client_a.stdin.write(b"test_file.txt\n")
        client_a.stdin.flush()
        time.sleep(20)

        # Validate logs
        with open("logs/server.log") as s_log:
            s_content = s_log.read()
            assert re.search(fr"\[FILE\] \s*Preparing to send 'test_file.txt'", s_content), "❌ Server did not prepare file"
            assert re.search(fr"\[FILE\] \s*Sent chunk #0", s_content), "❌ Server did not send CHUNK"
            assert re.search(fr"\[FILE\] \s*Transfer complete", s_content), "❌ Server did not complete transfer"
            print("🔍 Server CHUNK and DONE confirmed.")

        with open("logs/client_b.log") as b_log:
            b_content = b_log.read()
            assert re.search(fr"Received frame: \w+\|file\|0\|{id_b}\|.*test_file.txt.*\|INCOMING", b_content), "❌ INCOMING frame missing"
            assert re.search(fr"Received frame: \w+\|file\|0\|{id_b}\|.*\|CHUNK", b_content), "❌ CHUNK frame not from server"
            assert re.search(fr"Received frame: \w+\|file\|0\|{id_b}\|.*\|DONE", b_content), "❌ DONE frame not from server"
            print("🔍 Client B received INCOMING, CHUNK, and DONE frames.")

        with open("logs/client_a.log") as a_log:
            a_content = a_log.read()
            assert re.search(fr"Received frame: \w+\|ack\|{id_b}\|{id_a}\|.*\|ACK", a_content), "❌ ACK not received by sender"
            print("🔍 Client A received ACK frame.")

        print("✅ Test passed: file transfer verified.")
        logging.info("✅ file_transfer test passed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"❌ file_transfer test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
            print("🛑 Processes terminated.")
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_file_test()
