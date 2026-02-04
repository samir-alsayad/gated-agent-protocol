# Diagnosis: Memory Leak in WebSocket Handler

## Issue Description
The production server is experiencing gradual memory growth, eventually causing OOM kills after ~48 hours of operation. Logs indicate the WebSocket handler is accumulating disconnected client references.

## Root Cause Analysis
- **Location**: `src/handlers/websocket.py`, lines 45-67
- **Issue**: Client objects are added to `active_clients` set on connect but never removed on disconnect due to exception swallowing in the cleanup path.

## Impact Assessment
~2MB per orphaned connection; at 1000 connections/hour, memory grows by ~48GB/day.

## Reproduction
```bash
# Simulate 100 rapid connect/disconnect cycles
python scripts/stress_ws.py --cycles=100
# Observe memory via: watch -n 1 'ps -o rss= -p $(pgrep -f server.py)'
```

## Repair Strategy
Add proper cleanup in the disconnect handler and wrap the existing logic in a `finally` block to ensure removal from `active_clients` regardless of exception state.

## Implementation Steps

- [ ] **STEP-01**: Add `finally` block to `handle_disconnect()` to ensure client removal. — *Trace: ISSUE-01*
- [ ] **STEP-02**: Add logging for client cleanup events. — *Trace: ISSUE-01*
- [ ] **STEP-03**: Write unit test for connect/disconnect lifecycle. — *Trace: ISSUE-01*
- [ ] **STEP-04**: Run stress test to verify memory stability over 1000 cycles. — *Trace: ISSUE-01*

## Access Control
```yaml
allow_write:
  - "src/handlers/websocket.py"
  - "tests/test_websocket_lifecycle.py"
allow_exec:
  - "pytest tests/test_websocket_lifecycle.py"
  - "python scripts/stress_ws.py"
```

---
*Trace: ISSUE-01*
