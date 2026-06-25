# Runtime Monitoring

Production agent safety depends on evidence. Monitor intent, transaction, status, and balance reconciliation as one trace.

## Event model

Log one JSON event per stage:

```json
{
  "ts": "2026-06-25T00:00:00Z",
  "agentId": "treasury-agent",
  "intentId": "intent-001",
  "stage": "simulation",
  "cluster": "devnet",
  "policyVersion": "2026-06-25",
  "decision": "approved",
  "signature": null,
  "messageHash": "sha256:...",
  "programIds": ["11111111111111111111111111111111"],
  "risk": "low"
}
```

Never log seed phrases, private keys, raw signer payloads, auth tokens, or unredacted API keys.

## Metrics

Track:

- Intents proposed, approved, denied, expired, and manually reviewed.
- Simulation failures by program and reason.
- Broadcast success rate.
- Time from intent to finalized status.
- Null status lookups and expired blockhashes.
- Retry count per intent.
- Budget consumed per wallet and policy period.
- Emergency stop state.

## Alerts

Alert on:

- Any mainnet transaction without a recorded approval ID.
- Policy version changes.
- New program ID, mint, destination, or authority.
- Repeated simulation failure.
- Retry loop over threshold.
- Confirmation timeout.
- Status disagreement across RPC providers.
- Balance delta exceeding expected value.
- Attempted access to secret-like material in logs.

## Reconciliation

For each settled transaction:

1. Fetch status.
2. Fetch transaction details when available.
3. Compare observed balance/token deltas to expected deltas.
4. Attach transaction signature, message hash, and policy approval ID.
5. Mark the intent settled only after deltas are consistent or a human records an exception.

Do not count a transaction as complete only because `sendTransaction` returned a signature.

## RPC failover

Use multiple RPC endpoints for monitoring only if the project can tolerate inconsistent freshness. Keep one canonical broadcast endpoint per signed transaction unless the broadcaster is designed for duplicate-safe rebroadcast.

When endpoints disagree:

- Do not rebroadcast immediately.
- Check status cache limitations and transaction history.
- Compare slots and commitment levels.
- Escalate if funds, authority, or policy limits are at risk.
