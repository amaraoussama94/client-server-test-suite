# 🧪 Scenario Test: Single Client Chat Attempt

## 📍 Type
Scenario Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Server running
- One client connected

## 🔄 Steps
1. Launch server
2. Launch one client
3. Send a chat message

## ✅ Expected Result
- Client receives `WAIT` frame
- Chat message is ignored or logged as warning

## ❌ Failure Scenarios
- Message sent without gating
- Server crashes on dispatch
