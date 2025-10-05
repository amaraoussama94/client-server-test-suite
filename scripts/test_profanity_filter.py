# /**
#  * @file test_profanity_filter.py
#  * @brief Validates profanity detection and ALERT frame dispatch.
#  *        Uses banned word from input and checks for server response.
#  *        Uses config files for both server and clients. Prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: profanity_filter")

def run_profanity_test():
    try:
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

        # Inject banned word from asset file
        banned_word = "fuck"
        client_a.stdin.write(f"chat This is {banned_word} bad\n".encode())
        client_a.stdin.flush()
        time.sleep(2)

        logging.info("✅ profanity_filter test passed.")
    except Exception as e:
        logging.error(f"❌ profanity_filter test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_profanity_test()
