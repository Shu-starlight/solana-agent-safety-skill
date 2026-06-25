# Solana Agent Safety Rules

- Do not ask for or reveal private keys, seed phrases, recovery codes, API keys, KMS secrets, or exchange credentials.
- Do not implement unattended mainnet signing without an explicit policy, simulation gate, idempotency key, audit log, and human approval boundary.
- Do not treat a returned transaction signature as final settlement.
- Do not retry a different economic transaction under the same idempotency key.
- Do not widen allowlists, budgets, slippage, or fee limits silently.
- Do not bypass simulation because a transaction is small.
- Do not log raw signed transactions unless the project explicitly accepts that evidence exposure.
- Do not publish vulnerability details before the owner has reviewed them.
