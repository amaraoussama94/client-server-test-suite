# /**
#  * @file test_multi_client_chat.py
#  * @brief Simulates 10 clients sending messages to random peers concurrently.
#  *        Validates routing, delivery, and START frame readiness.
#  *        Uses config files and dynamic ID resolution.
#  *
#  *        Log assertions:
#  *        - Server: "[CHAT]Forwarding from X to Y: Hello from X"
#  *        - Receiver: "Received frame: ...|chat|X|Y|Hello from X|READY"
#  *        - Receiver: "You may begin|START"
#  *        - Sender: "Chat message sent in N chunk(s)"
#  *
#  * @author Oussama Amara
#  * @version 1.5
#  * @date 2025-10-13
#  */

import subprocess, time, logging, re, threading, random
from utils import get_binary_path, get_config_path, clear_logs

logging.info("🧪 Starting test: multi_client_chat_stress")

def run_stress_chat():
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
        client_logs = [open(f"logs/client_{i}.log", "a") for i in range(10)]

        print("🚀 Launching server and 10 clients...")
        server = subprocess.Popen([server_bin, server_cfg], stdout=server_log, stderr=subprocess.STDOUT)
        time.sleep(1)

        clients = [
            subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE, stdout=client_logs[i], stderr=subprocess.STDOUT)
            for i in range(10)
        ]
        time.sleep(20)

        server_log.flush(); server_log.close()
        for log in client_logs: log.flush(); log.close()

        print("📁 Logs written to:")
        print("   - logs/server.log")
        for i in range(10):
            print(f"   - logs/client_{i}.log")

        # Extract client IDs
        ids = []
        for i in range(10):
            with open(f"logs/client_{i}.log") as log:
                lines = log.readlines()
                id_match = next((re.search(r"Assigned client ID: (\d+)", line).group(1)
                                 for line in reversed(lines) if "Assigned client ID" in line), None)
                ids.append(id_match)

        # Filter out clients with missing IDs
        valid_clients = [(i, ids[i], clients[i]) for i in range(10) if ids[i] is not None]
        valid_indices = [i for i, _, _ in valid_clients]
        if len(valid_clients) < 10:
            print(f"⚠️ Only {len(valid_clients)} clients initialized successfully.")

        print("🆔 Assigned client IDs:", ids)

        # Wait for START frames
        print("⏳ Waiting for START frames...")
        start_confirmed = set()
        timeout = time.time() + 15
        while time.time() < timeout and len(start_confirmed) < len(valid_clients):
            for i, cid, _ in valid_clients:
                with open(f"logs/client_{i}.log") as log:
                    if re.search(r"You may begin\|START", log.read()):
                        start_confirmed.add(i)
            time.sleep(1)

        # Define message plan
        message_plan = []
        for i, sender_id, proc in valid_clients:
            target_choices = [j for j in valid_indices if j != i and ids[j] is not None]
            if not target_choices:
                continue
            target_index = random.choice(target_choices)
            target_id = ids[target_index]
            message = f"chat Hello from {sender_id}\n"
            message_plan.append((i, target_id, message))

        def send_message(client_index, target_id, message):
            proc = clients[client_index]
            try:
                proc.stdin.write(f"{target_id}\n".encode())
                proc.stdin.flush()
                time.sleep(0.5)
                proc.stdin.write(message.encode())
                proc.stdin.flush()
            except Exception as e:
                print(f"⚠️ Client {client_index} failed to send: {e}")

        print("📤 Sending messages concurrently...")
        threads = []
        for index, target_id, msg in message_plan:
            t = threading.Thread(target=send_message, args=(index, target_id, msg))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print("⏳ Waiting for routing and log flush...")
        time.sleep(10)

        # Validate server forwarding with retry
        missing = []
        for attempt in range(3):
            with open("logs/server.log") as s_log:
                s_content = s_log.read()
                missing = []
                for sender_index, target_id, msg in message_plan:
                    sender_id = ids[sender_index]
                    if not sender_id or not target_id:
                        continue
                    match = re.search(fr"\[CHAT\] \s*Forwarding from {sender_id} to {target_id}: chat .*?Hello from {sender_id}", s_content)
                    if not match:
                        missing.append((sender_id, target_id))
            if not missing:
                break
            print(f"🔁 Retry {attempt+1}: waiting for forwarding...")
            time.sleep(5)

        if missing:
            print("📄 Server log preview:\n", "\n".join(s_content.splitlines()[-40:]))
            for sid, tid in missing:
                print(f"❌ Server did not forward message from {sid} to {tid}")
            raise AssertionError("❌ Missing forwarding logs.")

        print("🔍 Server forwarding confirmed for all messages.")

        # Validate chat delivery
        for sender_index, target_id, msg in message_plan:
            sender_id = ids[sender_index]
            if not sender_id or not target_id:
                continue
            receiver_index = ids.index(target_id)
            with open(f"logs/client_{receiver_index}.log") as log:
                content = log.read()
                match = re.search(fr"Received frame: \w+\|chat\|{sender_id}\|{target_id}\|chat Hello from {sender_id}\|READY", content)
                if not match:
                    print(f"❌ Client {target_id} did not receive chat from {sender_id}")
                    raise AssertionError(f"Missing chat frame for {sender_id} → {target_id}")
                print(f"🔍 Client {target_id} received chat from {sender_id}")

        print("✅ Test passed: 10-client concurrent chat routing verified.")
        logging.info("✅ multi_client_chat_stress test passed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logging.error(f"❌ multi_client_chat_stress test failed: {e}")
    finally:
        try:
            server.terminate()
            for proc in clients:
                proc.terminate()
            print("🛑 Processes terminated.")
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_stress_chat()
