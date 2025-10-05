# 🧪 Scenario Test: File Transfer Progress Bar

## 📍 Type
Runtime Feedback Test

## 📦 Associated Script
`manual` or `scripts/run_local_test.ps1`

## 🔧 Preconditions
- Server and clients running
- File size ≥ 3 chunks (e.g., ≥ 768 bytes)
- Logging enabled

## 🔄 Steps
1. Client A requests file transfer
2. Server sends CHUNK frames
3. Observe sender-side logs:
[FILE] Sent chunk #2 (50.00%)
4. Observe receiver-side logs:
[FILE] Receiving 'test_file.txt': 66.67% (2/3)

## ✅ Expected Result
- Sender logs progress after each chunk
- Receiver logs progress during reassembly
- Percentages match chunk count and sequence

## ❌ Failure Scenarios
- No progress logged
- Incorrect percentage calculation
- Final chunk not marked as 100%

## 🧪 Notes
Validates:
- Real-time feedback for sender and receiver
- Accurate progress calculation
- Contributor visibility during transfer
