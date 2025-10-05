# 🧪 Scenario Test: Client List Broadcasting

## 📍 Type
Scenario Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Server running
- Multiple clients connected

## 🔄 Steps
1. Observe LIST frames on connect
2. Disconnect one client
3. Observe updated LIST frames

## ✅ Expected Result
- LIST frames sent every 3 seconds
- START sent if ≥2 clients
- WAIT sent if only one

## ❌ Failure Scenarios
- LIST not updated
- START/WAIT logic broken
