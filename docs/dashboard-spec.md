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
  - P50 (baseline latency)
  - P95 (primary SLO metric) - SLO: 800ms target 99%
  - P99 (tail latency / worst-case behavior)
- Units: milliseconds
- Threshold Line: 800ms (SLO objective)
- Incident Flag: `rag_slow` (simulates degraded retrieval latency ~2500ms)

### 2. Traffic / Request Count (QPS)
- Type: Line/area chart
- Metrics:
  - Total requests per time bucket
  - Request throughput (QPS approximation)
- Units: requests/sec
- Drill-down: By feature (qa, compare, recommend)
- Purpose: Detect traffic spikes and correlate with latency or errors

### 3. Error Rate with Breakdown
- Type: Line chart (error %) + bar chart (error breakdown)
- Main Metric: error_rate_pct - SLO: 5% target 99%
- Breakdown by error type:
  - user_error (invalid input / empty message)
  - system_error (agent / processing failure)
  - integration_error (external tool/API issues)
- Units: percentage
- Incident Flag: `tool_fail` (simulates tool execution failures)
- Purpose: Identify reliability issues and root cause distribution

### 4. Cost Over Time
- Type: Bar + line chart (cost per bucket + cumulative cost)
- Metrics:
  - cost_per_request_usd (derived from token usage)
  - total_cost_usd (cumulative)
  - avg_cost_usd
- Units: USD
- Threshold Line: $0.003 per request (SLO objective)
- Incident Flag: `cost_spike` (simulates abnormal token usage)
- Purpose: Monitor cost efficiency and detect abnormal spikes

### 5. Tokens In/Out Analysis
- Type: Stacked bar chart
- Metrics:
  - tokens_in_total
  - tokens_out_total
  - implicit ratio (tokens_out / tokens_in)
- Units: tokens
- Purpose: Analyze prompt size vs response generation and cost drivers

### 6. Quality Score / SLO Proxy
- Type: Line chart (time series)
- Metrics:
  - quality_score_avg - SLO: 0.8 target 95%
  - low_quality_percentage (responses below threshold)
- Units: 0.0 - 1.0 score
- Threshold: 0.8 (SLO objective)
- Note: Quality is heuristic-based (derived from response characteristics)

---

## Layer 2: Detailed Metrics

### Latency Distribution
- Percentile breakdown: P50, P95, P99 (time series)
- Span-level latency:
  - rag
  - llm
  - agent-run
- Purpose: Identify bottlenecks within the pipeline

### Request Breakdown by Feature
- qa (question answering)
- compare (vehicle comparison)
- recommend (recommendation engine)
- Purpose: Understand feature usage distribution

### User/Session Analytics
- Unique users (hashed)
- Requests per session
- Session activity patterns
- Purpose: Analyze engagement and usage behavior

### Correlation ID Tracking
- Trace requests across logs using correlation_id
- Link request → response → error events
- Used in L3 dashboard for debugging and traceability

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
- rag_slow: Simulates latency degradation in retrieval pipeline
- tool_fail: Simulates downstream tool/API failures
- cost_spike: Simulates abnormal cost increase due to token inflation

Current Status: Display real-time toggle state

### Alert Rules
- Latency P95 > 800ms for 5 min → WARN
- Error Rate > 5% for 5 min → WARN
- Cost/Request > $0.003 for 10 min → WARN
- Quality Score < 0.8 for sustained period → WARN

---

## Data Sources

### Metrics Collection Points
- `/metrics` endpoint (real-time snapshot from in-memory metrics)
- `data/logs.jsonl` (structured event logs)
- Correlation ID propagation across request lifecycle

### Log Events Tracked
- `app_started` - system startup
- `request_received` - incoming request
- `response_sent` - successful response with metrics
- `request_failed` - failed request with error metadata
- `span_latency` - component-level latency (rag, llm, agent)

### Context Fields
- correlation_id
- user_id_hash
- session_id
- feature (qa/compare/recommend)
- model
- environment

---

## UI/UX Considerations

### Color Coding
- Green: Within SLO thresholds
- Yellow/Orange: Approaching threshold
- Red: SLO violation
- Gray: No data

### Refresh Behavior
- Main dashboard: auto-refresh every 15-30 seconds
- Detailed metrics: on-demand
- Incident toggles: immediate effect

### Time Range Controls
- Default: 1 hour
- Extendable: 6h, 24h (future improvement)

### Drill-Down Capabilities
- L1 → L2: aggregated → detailed metrics
- L2 → L3: metric → raw log trace
- L3: inspect full request lifecycle

---

## Implementation Notes

- Metrics are aggregated in-memory (metrics.py)
- Logs are stored in JSONL format for replay and analysis
- Data aggregation is performed in `dashboard_shared.py`
- Incident simulation is controlled via toggle flags
- Dashboard rendering is server-side (FastAPI + HTML + Chart.js)