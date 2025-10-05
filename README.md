# 🧪 Client-Server Protocol Test Suite

This repository validates the behavior of a modular, cross-platform client-server system written in C. It covers chat, file transfer, game commands, and protocol integrity across both localhost and real network setups.

---

## 📦 Folder Structure

```text
client-server-test-suite/
├── README.md
├── configs/                  # Sample config files for client/server
│   ├── client_local.cfg
│   ├── client_remote.cfg
│   └── server.cfg
├── scripts/                  # PowerShell scripts to automate test runs
│   ├── test_smoke_test_local.py
│   ├── test_smoke_test_remote.py
│   ├──  test_single_client_chat.py
│   ├──  test_multi_client_chat.py
│   ├──  test_file_transfer_basic.py
│   ├── test_file_transfer_retry_timeout.py
│   ├──  test_profanity_filter_chat.py
│   ├── test_client_list_broadcast.py
│   ├──  test_interaction_gating.py
│   ├── test_progress_bar_chunked.py
│   ├──  test_progress_bar.py
│   └── test_runner.py #to start all the test
├── test_cases/               # Markdown test plans (see below)
│   ├── smoke_test_local.md
│   ├── smoke_test_remote.md
│   ├──  single_client_chat.md
│   ├──  multi_client_chat.md
│   ├──  file_transfer_basic.md
│   ├── file_transfer_retry_timeout.md
│   ├──  profanity_filter_chat.md
│   ├── client_list_broadcast.md
│   ├──  interaction_gating.md
│   ├── progress_bar_chunked.md
│   └── progress_bar.md
├── chunked_chat_message.md
├── assets/                   # Sample files used in tests
│   ├── test_file.txt
│   └── profanity_trigger.txt
└── results/                  # Logs and output from test runs
    └── logs/
```

## 🧪 Test Goals

- ✅ Validate chat messaging (READY, ALERT, START, WAIT)

- ✅ Confirm file transfer integrity (CHUNK, DONE, ACK, RETRY, TIMEOUT)

- ✅ Test client list broadcasting and interaction gating

- ✅ Simulate real network latency and packet loss

- ✅ Inspect CRC integrity and frame structure

- ✅ Confirm multi-client routing and ID assignment

- ✅ Trigger and verify profanity filter behavior

##  🛠 Setup Instructions

### Localhost Test (Single PC)

``` powershell
.\scripts\run_local_test.ps1
```
Launches server and two clients using 127.0.0.1

Validates chat and file transfer with progress tracking

### Remote Test (LAN or VM)

```powershell
.\scripts\run_remote_test.ps1
```
Uses real IPs across devices or VMs

Requires bridged networking or LAN setup