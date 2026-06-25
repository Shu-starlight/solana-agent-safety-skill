---
name: solana-agent-safety
description: Solana AI agent wallet safety, transaction policy, simulation gates, broadcast controls, monitoring, and incident response. Use when building or reviewing autonomous Solana agents, wallet automation, trading bots, payment agents, scheduled transaction systems, or agentic workflows that prepare, sign, broadcast, retry, or monitor Solana transactions.
user-invocable: true
---

# Solana Agent Safety

Use this skill to keep Solana AI agents from becoming unsafe hot-key automations.

## Operating rules

- Never request, store, print, or transform private keys, seed phrases, wallet recovery codes, exchange credentials, or KMS secrets.
- Treat mainnet signing and transaction broadcast as high-impact external actions. Require an explicit human approval step unless the user has already provided a narrow policy that allows it.
- Prefer devnet or localnet until policy, simulation, idempotency, monitoring, and rollback evidence are in place.
- Separate proposal, policy check, signing, broadcasting, and reconciliation into distinct steps.
- Make every denial explainable: return a policy reason, evidence, and a safe next action.

## Task routing

Read only the focused file needed for the current task.

| User asks about | Read |
| --- | --- |
| Designing wallet roles, budgets, permissions, allowlists, or signer scope | `policy-design.md` |
| Adding pre-sign, simulation, slippage, program allowlist, blockhash, retry, or broadcast gates | `transaction-gates.md` |
| Logs, metrics, reconciliation, stuck transaction detection, status polling, or production observability | `runtime-monitoring.md` |
| Compromised signer, runaway agent, bad transaction, leaked key, failed retry loop, or emergency pause | `incident-response.md` |
| Official docs, SDK links, RPC references, and source material | `resources.md` |

## Default safety architecture

Use this boundary unless the codebase already has a stronger one:

```text
intent -> transaction proposal -> policy classifier -> simulation -> human/policy approval
       -> external signer -> broadcaster -> status monitor -> reconciler -> audit log
```

The AI agent may create intents, draft transactions, inspect logs, and propose fixes. The AI agent must not silently bypass the policy classifier, external signer, or audit log.

## Baseline checks

Before any implementation, identify:

1. Cluster: localnet, devnet, testnet, or mainnet-beta.
2. Signer boundary: wallet adapter, server KMS, multisig, hardware wallet, or custodial API.
3. Allowed programs and token mints.
4. Per-transaction, per-hour, and per-day budget.
5. Simulation requirement and accepted failure modes.
6. Retry and idempotency strategy.
7. Confirmation target and reconciliation path.
8. Emergency stop owner and trigger.

## Bundled validator

Use the bundled policy validator when a repository has a JSON policy or when designing one:

```bash
python3 scripts/validate_agent_policy.py templates/agent-policy.example.json
```

If adapting this skill inside a target project, copy `templates/agent-policy.example.json` into the project, edit it, and validate the edited copy.

## Deliverables

For implementation work, return:

- Files changed.
- Safety boundary added or improved.
- Policy decisions and assumptions.
- Test or validation commands.
- Remaining risks that still require human approval.
