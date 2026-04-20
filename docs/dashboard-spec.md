# Dashboard Spec

Required Layer-2 panels:
1. Latency P50/P95/P99
2. Traffic (request count or QPS)
3. Error rate with breakdown
4. Cost over time
5. Tokens in/out
6. Quality proxy (heuristic, thumbs, or regenerate rate)

Quality bar:
- default time range = 1 hour
- auto refresh every 15-30 seconds
- visible threshold/SLO line
- units clearly labeled
- no more than 6-8 panels on the main layer

---

## Layer 1: Main Dashboard (L2 Panels)

Default time range: 1 hour  
Auto-refresh: 15-30 seconds  
Max panels: 6-8

### 1. Latency Panel
- Type: Line chart with SLO threshold
- Metrics:
  - P50 (green)
  - P95 (yellow/orange) - SLO: 800ms target 99%
  - P99 (red)
- Units: milliseconds
- Threshold Line: 800ms (SLO objective)
- Incident Flag: `rag_slow` (baseline ~150ms, slow scenario ~2500ms)

### 2. Traffic / Request Count (QPS)
- Type: Bar chart or area chart
- Metrics:
  - Total requests (traffic)
  - Requests per second (QPS)
- Units: requests/sec
- Drill-down: By feature (qa, compare, recommend)

### 3. Error Rate with Breakdown
- Type: Stacked bar chart + pie chart
- Main Metric: error_rate_pct - SLO: 5% target 99%
- Breakdown by error type:
  - Tool failures (rag_tool_fail)
  - LLM failures
  - Integration errors
- Units: percentage
- Incident Flag: `tool_fail` incident

### 4. Cost Over Time
- Type: Line chart with cumulative cost
- Metrics:
  - cost_per_request_usd - SLO: $0.003 target 99%
  - total_cost_usd (cumulative)
  - avg_cost_usd
- Units: USD
- Threshold Line: $0.003 per request (SLO objective)
- Incident Flag: `cost_spike` scenario
- Drill-down: By model (claude-sonnet-4-5)

### 5. Tokens In/Out Analysis
- Type: Dual-axis line chart
- Metrics:
  - tokens_in_total (blue)
  - tokens_out_total (orange)
  - ratio (tokens_out / tokens_in)
- Units: tokens
- Purpose: Monitor prompt compression and response generation

### 6. Quality Score / SLO Proxy
- Type: Gauge + line chart
- Metrics:
  - quality_score_avg - SLO: 0.8 target 95%
  - quality_score distribution
- Units: 0.0 - 1.0 score
- Threshold: 0.8 (SLO objective)
- Note: Heuristic quality based on response characteristics (baseline ~0.8)

---

## Layer 2: Detailed Metrics

### Latency Distribution
- Heatmap or histogram of response times
- Percentile breakdown: P10, P25, P50, P75, P90, P95, P99
- Correlation with incidents and feature types

### Request Breakdown by Feature
- qa (question answering)
- compare (vehicle comparison)
- recommend (recommendation engine)

### User/Session Analytics
- Unique users (hashed)
- Session duration
- Requests per session

### Correlation ID Tracking
- Trace linking across logs
- Langfuse trace integration (when enabled)
- End-to-end request flow visualization

---

## Layer 3: SLO & Incident Management

### SLO Status Board
| SLI | Objective | Target | Current | Status |
|-----|-----------|--------|---------|--------|
| Latency P95 | 800ms | 99.0% | - | - |
| Error Rate | 5% | 99.0% | - | - |
| Cost/Request | $0.003 | 99.0% | - | - |
| Quality Score | 0.8 | 95.0% | - | - |

### Incident Toggles
- rag_slow: Simulates RAG lookup delays (~2500ms latency spike)
- tool_fail: Simulates tool execution failures (increases error rate)
- cost_spike: Simulates cost overruns (exceeds cost_per_request threshold)

Current Status: Display real-time toggle state

### Alert Rules
- Latency P95 > 800ms for 5 min → WARN
- Error Rate > 5% for 5 min → WARN
- Cost/Request > $0.003 for 10 min → WARN
- Quality Score < 0.8 for sustained period → WARN

---

## Data Sources

### Metrics Collection Points
- `/metrics` endpoint - real-time snapshot
- `data/logs.jsonl` - structured event logs
- Correlation ID context propagation
- Langfuse tracing (optional)

### Log Events Tracked
- `app_started` - startup event with tracing status
- `request_received` - inbound chat request
- `response_sent` - response with latency/cost/quality metrics
- `span_latency` - individual span timings (rag, llm, agent-run)
- `incident_*` - incident state changes

### Context Fields
- correlation_id
- user_id_hash
- session_id
- feature (qa/compare/recommend)
- model (claude-sonnet-4-5)
- env (dev/prod)

---

## UI/UX Considerations

### Color Coding
- Green: Within SLO thresholds
- Yellow/Orange: Approaching thresholds
- Red: Breached SLO
- Gray: No data / disabled

### Refresh Behavior
- Main dashboard: auto-refresh every 15-30 seconds
- Detailed metrics: on-demand or 1 min refresh
- Incident toggles: immediate effect

### Time Range Controls
- Quick presets: 1h, 6h, 24h, 7d, 28d
- Custom range selector
- Relative time (last N minutes)

### Drill-Down Capabilities
- Click latency panel → see percentile breakdown
- Click error rate → see error type details
- Click cost chart → see cost by model/feature
- Click trace ID → open Langfuse dashboard

---

## Implementation Notes

- All metrics aggregated in-memory (metrics.py)
- Logs persisted to JSONL for replay/analysis
- SLO thresholds configurable via slo.yaml
- Incident simulation via toggle endpoints
- Optional Langfuse integration for distributed tracing

