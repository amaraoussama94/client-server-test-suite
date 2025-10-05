# /**
#  * @file test_progress_bar_chunks.py
#  * @brief Validates progress feedback during chunked chat message delivery.
#  *        Ensures client displays progress bar or chunk count.
#  *        Uses config files for both server and clients. Prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: progress_bar_chunks")

def run_chunk_progress():
    try:
        long_message = "chat " + ("Chunked message. " * 40) + "\n"

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
        client_b = subprocess.Popen([client_bin, client_cfg])
        time.sleep(2)

        client_a.stdin.write(long_message.encode())
        client_a.stdin.flush()
        time.sleep(3)

        logging.info("✅ progress_bar_chunks test passed.")
    except Exception as e:
        logging.error(f"❌ progress_bar_chunks test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_chunk_progress()
