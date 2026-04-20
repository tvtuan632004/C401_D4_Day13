# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 800 for 5m`
- Impact: tail latency breaches SLO, users experience slow responses
- First checks:
  1. Check metrics dashboard for latency spike
  2. Open recent traces in Langfuse
  3. Compare RAG span vs LLM span
  4. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - optimize retrieval latency
  - reduce prompt size
  - cache frequent queries

---

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Check error_rate_pct in metrics
  2. Group logs by `error_type`
  3. Inspect failed traces
  4. Check if `tool_fail` incident is enabled
- Mitigation:
  - disable failing component
  - retry with fallback logic
  - rollback recent changes

---

## 3. Cost spike
- Severity: P2
- Trigger: `cost_per_request_usd > 0.003 for 5m`
- Impact: increased cost per request, potential budget overrun
- First checks:
  1. Check cost_per_request_usd in metrics
  2. Inspect traces for token usage
  3. Compare tokens_in vs tokens_out
  4. Check if `cost_spike` incident is enabled
- Mitigation:
  - reduce prompt size
  - limit output tokens
  - optimize model usage

---

## 4. Low quality score
- Severity: P3
- Trigger: `quality_score_avg < 0.8 for 10m`
- Impact: degraded answer quality, user dissatisfaction
- First checks:
  1. Check quality_score_avg in metrics
  2. Review recent responses
  3. Inspect retrieved documents
  4. Verify RAG relevance
- Mitigation:
  - improve retrieval quality
  - refine prompt template
  - add fallback responses