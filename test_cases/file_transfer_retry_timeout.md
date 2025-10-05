# 🧪 Scenario Test: Retry & Timeout Logic

## 📍 Type
Scenario Test

## 📦 Associated Script
`simulate_loss.ps1`

## 🔧 Preconditions
- Server and clients running
- Retry and timeout logic enabled

## 🔄 Steps
1. Simulate packet loss or delay
2. Observe RETRY frames for missing chunks
3. Observe TIMEOUT if no chunk received

## ✅ Expected Result
- RETRY sent for missing chunks
- TIMEOUT sent if stalled
- Transfer aborted if retry limit exceeded

## ❌ Failure Scenarios
- RETRY spam (no throttling)
- No TIMEOUT triggered
