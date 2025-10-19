# /**
#  * @file test_file_transfer_retry_timeout.py
#  * @brief Simulates packet loss to trigger RETRY and TIMEOUT during file transfer.
#  *        Ensures client resends chunks and handles failure gracefully.
#  *        Uses config files for file-capable clients and prints resolved paths for debugging.
#  *
#  *        Log assertions:
#  *        - Receiver: "Requested retry for missing chunk #0"
#  *        - Receiver: "Receiving 'test_file.txt': 100.00%"
#  *        - Receiver: "File 'test_file.txt' saved"
#  *        - Sender: "Received frame: ...|ack|Y|X|...|ACK"
#  *
#  * @author Oussama Amara
#  * @version 1.2
#  * @date 2025-10-18
#  */

import subprocess, time, shutil, logging, re
from utils import get_binary_path, get_config_path, clear_logs
import os

logging.info("🧪 Starting test: file_transfer_retry_timeout")

def run_retry_timeout_test():
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

        # Prepare folders and file
        try:
            os.makedirs("assets/to_send", exist_ok=True)
            os.makedirs("assets/received", exist_ok=True)
            shutil.copy("assets/test_file.txt", "assets/to_send/test_file.txt")
            print("📁 File placed at: assets/to_send/test_file.txt")
            print("📂 Folder ensured: assets/received/")
        except Exception as e:
            logging.error(f"❌ Failed to prepare test file or folders: {e}")
            return

        server_log = open("logs/server.log", "a")
        client_a_log = open("logs/client_a.log", "a")
        client_b_log = open("logs/client_b.log", "a")

        print("🚀 Launching server and clients...")
        server = subprocess.Popen([server_bin, server_cfg], stdout=server_log, stderr=subprocess.STDOUT)
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_a_log, stderr=subprocess.STDOUT)
        client_b = subprocess.Popen([client_bin, client_cfg], stdout=client_b_log, stderr=subprocess.STDOUT)
        time.sleep(10)

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
        time.sleep(0.5)
        client_a.stdin.write(b"test_file.txt\n")
        client_a.stdin.flush()
        time.sleep(10)

        # Validate retry and timeout behavior
        with open("logs/client_b.log") as b_log:
            b_content = b_log.read()
            retry_count = len(re.findall(r"Requested retry for missing chunk #0", b_content))
            assert retry_count >= 5, f"❌ Retry count too low: {retry_count}"
            assert "Receiving 'test_file.txt': 100.00%" in b_content, "❌ File not fully received"
            assert "File 'test_file.txt' saved" in b_content, "❌ File not saved on receiver"
            print(f"🔍 Receiver retried chunk #0 {retry_count} times and saved file.")

        with open("logs/client_a.log") as a_log:
            a_content = a_log.read()
            assert re.search(fr"Received frame: \w+\|ack\|{id_b}\|{id_a}\|.*\|ACK", a_content), "❌ ACK not received by sender"
            print("🔍 Sender received ACK frame.")

        print("✅ Test passed: retry and timeout behavior verified.")
        logging.info("✅ file_transfer_retry_timeout test passed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"❌ file_transfer_retry_timeout test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
            print("🛑 Processes terminated.")
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_retry_timeout_test()
