---
description: Review a Solana AI agent or transaction pipeline for wallet, signer, simulation, retry, and monitoring safety.
argument-hint: "[repository path or policy file]"
---

Use `solana-agent-safety`.

Review the target for:

1. Wallet and signer boundary.
2. Policy allowlists and budget limits.
3. Transaction simulation before approval.
4. Message hash match after signing.
5. Idempotency and retry limits.
6. Confirmation polling and reconciliation.
7. Audit logs without secrets.
8. Emergency stop path.

Return:

- Critical blockers.
- Recommended fixes.
- Tests or validation commands.
- Remaining human-approval requirements.
