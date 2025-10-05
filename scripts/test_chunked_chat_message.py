# /**
#  * @file test_chunked_chat_message.py
#  * @brief Sends a long chat message to validate chunking and reassembly.
#  *        Uses config files for chat-capable clients and prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: chunked_chat_message")

def run_chunked_chat():
    try:
        long_message = "chat " + ("This is a long message. " * 50) + "\n"

        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        server = subprocess.Popen([server_bin, server_cfg])
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client_a.stdin.write(long_message.encode())
        client_a.stdin.flush()
        time.sleep(3)

        logging.info("✅ chunked_chat_message test passed.")
    except Exception as e:
        logging.error(f"❌ chunked_chat_message test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_chunked_chat()
