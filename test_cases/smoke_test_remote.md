# 🧪 Smoke Test: Remote Setup (LAN or VM)

## 📍 Type
Smoke Test

## 📦 Associated Script
`scripts/run_remote_test.ps1`

## 🔧 Preconditions
- Server running on one device (or VM)
- Client running on another device (or VM)
- Bridged networking or LAN IPs configured

## 🔄 Steps
1. Launch server on IP `192.168.x.x`
2. Launch client with `client_remote.cfg` pointing to server IP
3. Send chat and file commands
4. Monitor logs and cross-device delivery

## ✅ Expected Result
- Client connects to server via real IP
- Chat and file commands are routed correctly
- Logs show proper dispatch and delivery

## ❌ Failure Scenarios
- NAT blocks connection
- IP mismatch in config
- Firewall prevents socket binding
