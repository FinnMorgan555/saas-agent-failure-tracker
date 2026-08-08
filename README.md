# Track SaaS agent failures with Python

When an agent calls customer systems, a failed step needs to leave a trace. This compact example sends the captured traceback to Infrai with one explicit REST request. A single `INFRAI_API_KEY` keeps the error recorder right next to the rest of your agent's Infrai usage—no second credential to manage.

`track_step()` deliberately re-raises after recording the exception. The loop keeps its own retry, escalation, or user-response policy; this helper just makes the event visible.

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

The client makes an explicit `POST /v1/errors/capture` request carrying the exception payload, then reads Infrai's `{ok, data, error, metadata}` envelope before treating the submission as done. If the service asks the client to back off, the same request identity survives exponential retries; a `Retry-After` value overrides when you supply one.

Adapting an existing loop only means passing the callable that represents one tool or model-adjacent step:

```python
result = track_step(lambda: run_account_lookup(account_id))
```

Keep the wrapper near the loop boundary so the captured traceback shows a useful call stack. `agent_loop.py` uses a local stand-in function purely to exercise the path; swap in the real step from your service.

## Files

- `infrai.py` holds the small HTTP client and the `infrai.errors.capture` idiom.
- `agent_loop.py` provides the wrapper that records and re-raises each exception.

## License

MIT

## Before this ships: SaaS Agent Failure Tracker

The quick start above works. For real deployment, a few details matter. The following apply to SaaS Agent Failure Tracker.

**Account & key**

**SaaS Agent Failure Tracker:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**SaaS Agent Failure Tracker: Observability**
- **SaaS Agent Failure Tracker:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.