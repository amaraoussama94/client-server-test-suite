# 🧪 Scenario Test: Basic File Transfer

## 📍 Type
Scenario Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Server running
- Two clients connected
- `test_file.txt` present in `assets/to_send/`

## 🔄 Steps
1. Client A requests file transfer
2. Server sends INCOMING to B
3. B replies READY
4. Server sends CHUNKs
5. B reassembles and sends ACK

## ✅ Expected Result
- All chunks received
- File saved in `assets/received/`
- ACK sent to sender

## ❌ Failure Scenarios
- Missing READY
- Incomplete reassembly
- ERR frame sent
