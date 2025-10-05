# 🧪 Scenario Test: Chunked Chat Messaging

## 📍 Type
Scenario Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Server and clients running
- Long message (>512 chars)

## 🔄 Steps
1. Client A sends long chat message
2. Server splits into CHUNK frames with SEQ=X
3. Server reassembles and dispatches to B

## ✅ Expected Result
- All chunks received
- Message reassembled correctly
- Delivered to B

## ❌ Failure Scenarios
- Missing chunk
- Incorrect SEQ order
- Message discarded
