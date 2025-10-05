# 🧪 Scenario Test: Multi-Client Chat Exchange

## 📍 Type
Scenario Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Server running
- Two clients connected

## 🔄 Steps
1. Launch server
2. Launch Client A and B
3. Wait for `START` frame
4. Send chat from A to B

## ✅ Expected Result
- B receives message
- Logs show proper routing and delivery

## ❌ Failure Scenarios
- Message dropped
- Incorrect ID routing
