# 🧪 Smoke Test: Localhost Setup

## 📍 Type
Smoke Test

## 📦 Associated Script
`scripts/run_local_test.ps1`

## 🔧 Preconditions
- Server and client binaries compiled
- `client_local.cfg` and `server.cfg` present
- Assets folder contains `test_file.txt`

## 🔄 Steps
1. Launch server on localhost
2. Launch one client
3. Send a chat message
4. Request a file transfer
5. Observe logs and terminal output

## ✅ Expected Result
- Server accepts connection
- Client receives `ID_ASSIGN`, `LIST`, `WAIT`
- Chat message is logged and ignored (only one client)
- File transfer request is logged but not executed

## ❌ Failure Scenarios
- Server crashes on startup
- Client fails to connect
- Unexpected frame format or missing logs

## 🧪 Notes
Validates basic startup, config parsing, and socket readiness.
