# Transaction Gates

Use transaction gates to turn an agent's intent into a bounded transaction workflow.

## Required pipeline

```text
intent
  -> build unsigned transaction
  -> normalize and decode message
  -> classify programs, accounts, mints, authorities, writable set
  -> policy check
  -> simulation
  -> simulation log review
  -> approval decision
  -> external signing
  -> broadcast with idempotency key
  -> status polling
  -> reconciliation
```

Never let an agent sign and broadcast directly from the same unreviewed tool call.

## Pre-sign checks

Reject or require human approval if any check fails:

- Cluster in transaction context does not match policy.
- Any program ID is missing from the allowlist.
- A denylisted program appears.
- Destination, mint, authority, or token account is outside policy.
- Transaction value exceeds per-transaction, hourly, or daily budget.
- Slippage exceeds policy.
- Priority fee exceeds policy.
- Writable account count or signer count exceeds policy.
- Transaction includes authority changes, account close, delegation, upgrade, freeze, or revoke operations without a specific approval rule.
- The transaction has a stale blockhash or a missing durable nonce plan.
- An aggregator-produced transaction cannot be decoded into expected program and account effects.

## Simulation gate

Simulate before signing or before final approval whenever the environment allows it.

Require:

- `err` is null.
- Logs do not show unexpected programs, panic paths, or missing account warnings.
- Token balance deltas match the expected direction and upper bounds.
- SOL lamport deltas stay within fee and transfer limits.
- Compute units stay under the configured ceiling.
- The simulation slot and blockhash freshness are acceptable.

Treat simulation as necessary but not sufficient. A successful simulation does not prove intent safety.

## Broadcast gate

Broadcast only after:

- A policy decision was recorded.
- The exact signed message hash matches the simulated or approved message.
- An idempotency key exists for the intent.
- The retry budget is bounded.
- The agent has a status polling plan.

If retrying, do not rebuild a different economic transaction under the same idempotency key. Either reuse the same intent with explicit replacement metadata or open a new intent.

## Confirmation and reconciliation

Poll status until the target confirmation or until the timeout is reached. Record:

- Signature.
- Confirmation status.
- Error, if any.
- Pre and post balances where available.
- Final action: settled, failed, expired, replaced, or needs human.

If a status lookup returns null, do not assume failure. Check blockhash expiry, recent status cache behavior, and transaction history settings before retrying.

## TypeScript gate skeleton

```ts
type GateDecision =
  | { ok: true; approvalId: string; warnings: string[] }
  | { ok: false; code: string; reason: string; needsHuman?: boolean };

export async function evaluateCandidate(input: {
  intentId: string;
  cluster: string;
  decodedMessage: DecodedMessage;
  policy: AgentPolicy;
  simulate: () => Promise<SimulationResult>;
}): Promise<GateDecision> {
  const policyDecision = checkPolicy(input.decodedMessage, input.policy);
  if (!policyDecision.ok) return policyDecision;

  const simulation = await input.simulate();
  const simulationDecision = checkSimulation(simulation, input.policy);
  if (!simulationDecision.ok) return simulationDecision;

  return {
    ok: true,
    approvalId: `${input.intentId}:${hashMessage(input.decodedMessage)}`,
    warnings: [...policyDecision.warnings, ...simulationDecision.warnings],
  };
}
```

Keep the gate pure where possible: classification and policy decisions should be deterministic and testable without a wallet.
