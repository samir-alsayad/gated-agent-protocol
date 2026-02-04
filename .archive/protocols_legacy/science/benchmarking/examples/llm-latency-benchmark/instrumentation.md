# Instrumentation: LLM Latency Benchmark

## Instrumentation Strategy
- Use dedicated benchmarking server with fixed CPU governor (performance mode)
- Disable thermal throttling via BIOS
- Run from single geographic region to minimize network variance

## Telemetry Map
| Metric | Collection Point | Precision |
|:-------|:-----------------|:----------|
| Time-to-First-Token (TTFT) | Client-side | μs |
| Total Latency | Client-side | μs |
| Token Count | Response metadata | exact |
| HTTP Status | Response | exact |

## Hardware Bounds
- **CPU**: Pinned to cores 0-3, isolated from OS scheduler
- **Network**: Dedicated NIC with 1Gbps guaranteed bandwidth
- **Memory**: 32GB DDR5, no swap enabled

## Access Control
```yaml
allow_write:
  - "config/hardware_profile.json"
allow_exec:
  - "lscpu"
  - "uname -a"
  - "sysctl -w vm.swappiness=0"
```

---
*Trace: INST-01, INST-02*
