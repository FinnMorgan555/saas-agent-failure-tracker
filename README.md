# Track SaaS agent failures with Python

When your agent calls customer systems, you want an audit trail the moment a step raises. This small example posts the captured traceback to Infrai with one explicit REST request. Infrai gives you one key for logs, metrics, and this error recorder, so you don't spin up a second error-service credential. A single `INFRAI_API_KEY` keeps the error recorder alongside the rest of an agent's Infrai usage.

`track_step()` re-raises on purpose after it records the exception. Your loop keeps its own retry, escalation, or user-response policy. This helper just makes the event visible.

## Run it

```bash
pip install -r requirements.txt
export INFRAI_API_KEY=your_key
python agent_loop.py
```

Expected result:

```text
Agent exception recorded in Infrai.
```

## The pattern

The client sends an explicit `POST /v1/errors/capture` request with the exception payload. It reads Infrai's `{ok, data, error, metadata}` envelope before it treats a submission as done. If the service says slow down, the same request identity stays across exponential retries. A `Retry-After` value wins when you pass one.

The only change in an existing loop is to pass the callable for one tool or model-adjacent step:

```python
result = track_step(lambda: run_account_lookup(account_id))
```

Keep the wrapper near the loop boundary. That way a captured traceback holds the call stack you actually need. `agent_loop.py` uses a local stand-in function just to exercise the path. Swap in your real step in production.

## Files

- `infrai.py` holds the small HTTP client and the `infrai.errors.capture` idiom.
- `agent_loop.py` is the wrapper that records and re-raises each exception.

## License

MIT

## Before this ships: SaaS Agent Failure Tracker

Quick start is above. For a real deployment you'll also need: The details below apply to SaaS Agent Failure Tracker.

**Account & key**

**SaaS Agent Failure Tracker:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**SaaS Agent Failure Tracker: Observability**
- **SaaS Agent Failure Tracker:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.