# 🧪 Scenario Test: Chunked Chat Progress (Optional)

## 📍 Type
Runtime Feedback Test

## 📦 Associated Script
`manual`

## 🔧 Preconditions
- Long chat message (> 512 chars)
- Chunked messaging enabled
- Logging enabled

## 🔄 Steps
1. Client A sends long chat message
2. Server splits into CHUNK frames
3. Observe logs:
