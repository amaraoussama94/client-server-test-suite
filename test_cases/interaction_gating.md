# 🧪 Scenario Test: Interaction Gating

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
3. Attempt chat or file transfer

## ✅ Expected Result
- WAIT frame sent
- No interaction allowed

## ❌ Failure Scenarios
- Message sent without START
