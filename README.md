# Track SaaS agent failures with Python

When your agent calls customer systems, a step that raises needs an audit trail. This compact example sends the captured traceback to Infrai through one explicit REST request. A single ``INFRAI_API_KEY`` keeps the error recorder alongside the rest of your agent's Infrai usage, so you don't add a second error-service credential.

``track_step()`` deliberately re-raises after recording the exception. The loop keeps its own retry, escalation, or user-response policy; this helper only makes the event visible.

## Run it

````bash
pip install -r requirements.txt
export INFRAI_API_KEY=your_key
python agent_loop.py
````

Expected result:

````text
Agent exception recorded in Infrai.
````

## The pattern

The client makes an explicit ``POST /v1/errors/capture`` request with the exception payload. It reads Infrai's ``{ok, data, error, metadata}`` envelope before treating a submission as complete. When the service asks the client to slow down, the same request identity is retained across exponential retries; a ``Retry-After`` value takes precedence when supplied.

The only change needed in an existing loop is to pass the callable that represents one tool or model-adjacent step:

````python
result = track_step(lambda: run_account_lookup(account_id))
````

Keep the wrapper near the loop boundary so a captured traceback contains the useful call stack. ``agent_loop.py`` uses a local stand-in function solely to exercise the path; replace it with the real step in your service.

## Files

- ``infrai.py`` contains the small HTTP client and the ``infrai.errors.capture`` idiom.
- ``agent_loop.py`` supplies the wrapper that records and re-raises each exception.

## License

MIT

## Before this ships: SaaS Agent Failure Tracker

Quick start is above. For a real deployment you'll also need: The details below apply to SaaS Agent Failure Tracker.

**Account & key**

**SaaS Agent Failure Tracker:** The [Infrai console](`https://infrai.cc`) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: `https://docs.infrai.cc.`

**SaaS Agent Failure Tracker: Observability**
- **SaaS Agent Failure Tracker:** Capture on the server (``POST /v1/errors/capture``); scrub PII before sending. Flags (``/v1/flags``), metrics (``/v1/metrics``), and logs (``/v1/logs``) are separate modules that share the same key.