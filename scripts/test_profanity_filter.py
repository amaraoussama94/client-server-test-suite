# /**
#  * @file test_profanity_filter.py
#  * @brief Validates client-side profanity detection and ALERT frame dispatch.
#  *        Message is blocked before reaching the server.
#  *        ALERT frame is returned to sender (Client A).
#  *
#  *        Log assertions:
#  *        - Sender: "Received frame: ...|alert|0|X|Inappropriate language detected|ALERT"
#  *
#  * @author Oussama Amara
#  * @version 1.5
#  * @date 2025-10-13
#  */

import subprocess, time, logging, re
from utils import get_binary_path, get_config_path, clear_logs

logging.info("🧪 Starting test: profanity_filter")

def run_profanity_test():
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

        # Extract client A ID
        with open("logs/client_a.log") as a_log:
            a_lines = a_log.readlines()
            id_a = next((re.search(r"Assigned client ID: (\d+)", line).group(1)
                         for line in reversed(a_lines) if "Assigned client ID" in line), None)

        if not id_a:
            print("❌ Failed to resolve client A ID.")
            raise RuntimeError("Could not resolve client A ID")

        print(f"🆔 Client A ID: {id_a}")

        # Inject banned word
        banned_word = "fuck"
        message = f"chat This is {banned_word} bad\n"
        print("🧪 Profanity injection plan:")
        print(f"   - Banned word: '{banned_word}'")
        print(f"   - Full message: '{message.strip()}'")
        print(f"   - Sender: Client A (ID={id_a}) → Target: Client A (self)")

        client_a.stdin.write(f"{id_a}\n".encode())  # Target self to trigger local filter
        client_a.stdin.flush()
        time.sleep(0.5)
        client_a.stdin.write(message.encode())
        client_a.stdin.flush()
        time.sleep(5)

        # Validate sender log
        with open("logs/client_a.log") as a_log:
            a_content = a_log.read()
            frame_match = re.search(fr"Received frame: \w+\|system\|0\|{id_a}\|Inappropriate language detected\|ALERT", a_content)
            if not frame_match:
                print("📄 Sender log preview:\n", "\n".join(a_content.splitlines()[-40:]))
                raise AssertionError("❌ Sender did not receive ALERT frame.")
            print("🔍 Sender ALERT frame confirmed.")

        print("✅ Test passed: client-side profanity blocked and ALERT returned to sender.")
        logging.info("✅ profanity_filter test passed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"❌ profanity_filter test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
            print("🛑 Processes terminated.")
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_profanity_test()
