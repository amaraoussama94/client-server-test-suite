# 🧪 Scenario Test: Profanity Filter

## 📍 Type
Scenario Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Profanity filter enabled
- Two clients connected

## 🔄 Steps
1. Client A sends message with banned word (e.g., "fuck")
2. Server detects and logs profanity
3. ALERT frame sent to A

## ✅ Expected Result
- Message blocked or masked
- ALERT sent to sender
- Warning logged

## ❌ Failure Scenarios
- Message delivered unfiltered
- No ALERT sent
