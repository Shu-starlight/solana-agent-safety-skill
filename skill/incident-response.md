# Incident Response

Use this when an agent may have signed, broadcast, retried, or exposed something unsafe.

## First five minutes

1. Pause the agent and schedulers.
2. Disable broadcaster credentials or signer access where possible.
3. Preserve logs, policy version, transaction messages, signatures, and deployment SHAs.
4. Check whether any private key, seed phrase, token, or API credential was logged.
5. Identify affected wallets, programs, token mints, and authorities.

Do not delete logs during an incident. Redact copies for sharing, but preserve originals in the incident store.

## Triage

Classify the incident:

- `policy_bypass`: transaction skipped a required gate.
- `bad_policy`: policy allowed an unsafe action.
- `signer_exposure`: secret or signing path leaked.
- `retry_loop`: repeated broadcast or replacement caused unintended exposure.
- `stuck_or_unknown`: transaction status cannot be reconciled.
- `wrong_destination`: funds, authority, or assets moved to an unexpected address.
- `program_risk`: called program behaved unexpectedly or dependency was compromised.

## Containment

Recommended actions by class:

| Class | Containment |
| --- | --- |
| policy_bypass | pause agent, block signer, invalidate policy version, add regression test |
| bad_policy | lower limits to zero, require human review, patch policy, revalidate |
| signer_exposure | rotate key or move funds to clean wallet, revoke sessions, inspect logs |
| retry_loop | disable scheduler, mark idempotency keys closed, reconcile all signatures |
| stuck_or_unknown | stop retries, poll status with history, inspect blockhash expiry |
| wrong_destination | preserve evidence, notify owner, do not attempt recovery without approval |
| program_risk | disable allowlist entry, alert integrators, review recent interactions |

## Resume checklist

Resume only after:

- Root cause is documented.
- Policy validator passes.
- Regression test covers the failure mode.
- Emergency admin approves the restart.
- First resumed transaction is devnet or a low-value mainnet canary.
- Monitoring alert thresholds are active.

## Incident report template

```text
Summary:
Timeline:
Cluster:
Wallets affected:
Programs affected:
Policy version:
Signatures:
Expected behavior:
Actual behavior:
Root cause:
Containment:
Fix:
Regression test:
Remaining risk:
Human approval:
```
