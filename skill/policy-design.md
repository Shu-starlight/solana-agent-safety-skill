# Policy Design

Design the policy before writing transaction code. A Solana agent policy should answer what the agent may propose, what may be signed, what may be broadcast, and what evidence must be kept.

## Capability model

Use separate roles:

| Role | Can do | Must not do |
| --- | --- | --- |
| observer | Read balances, positions, account data, market data | Build, sign, or broadcast transactions |
| proposer | Create unsigned transaction candidates and rationale | Access signing keys or broadcast directly |
| simulator | Simulate candidates and classify logs | Treat simulation success as approval |
| signer | Sign approved transactions through wallet, KMS, multisig, or hardware signer | Change policy at runtime |
| broadcaster | Send approved signed transactions | Retry without idempotency |
| reconciler | Poll status, reconcile balances, write audit logs | Hide or mutate evidence |
| emergency_admin | Pause, revoke, rotate, and lower limits | Trade, transfer, or widen limits during incident response |

Do not combine proposer, signer, and policy owner in one unattended process for mainnet.

## Policy fields

Create or require a policy with:

- `cluster`: localnet, devnet, testnet, or mainnet-beta.
- `wallets`: role, public key placeholder, allowed actions, and budget.
- `allowlists.programIds`: explicit program IDs the agent may touch.
- `allowlists.tokenMints`: explicit mint allowlist or a documented discovery rule.
- `denylists.programIds`: known-dangerous or out-of-scope programs.
- `limits`: per-transaction, hourly, daily, slippage, priority fee, compute unit, and account-write limits.
- `gates`: simulation, signer review, idempotency, blockhash freshness, and confirmation target.
- `monitoring`: audit path, alert channels, stuck transaction timeout, and emergency stop.

Use `templates/agent-policy.example.json` as a starting point.

## Budget design

Start from the smallest useful limit:

1. `perTransactionUsd`: max value exposed by one transaction.
2. `perHourUsd`: max loss from a loop before alerts fire.
3. `perDayUsd`: max intended daily work.
4. `maxPriorityFeeLamports`: bound fee escalation.
5. `maxSlippageBps`: route-specific slippage cap.

For mainnet, require `perTransactionUsd <= perHourUsd <= perDayUsd`.

## Allowlist design

Program allowlists should be explicit. For each program, record:

- Program ID.
- Human-readable name.
- Allowed instruction families.
- Expected writable accounts.
- Whether CPI to unknown programs is acceptable.
- Whether Token-2022 extensions, transfer hooks, or delegate authority are involved.

If the agent integrates an aggregator or router, gate by route output too. An allowlisted router can still produce a transaction that touches unexpected mints, accounts, or authorities.

## Human approval boundaries

Require explicit human approval when:

- First mainnet transaction for a new policy.
- New program ID, token mint, or destination address.
- Any policy limit increase.
- Any transaction that creates, delegates, closes, upgrades, freezes, or changes authority.
- Any failed simulation override.
- Any post-incident resume.

## Review output

When reviewing a policy, return:

- `approve`: policy is safe enough for the stated cluster and budget.
- `approve_with_limits`: policy is acceptable only with lower limits or extra gates.
- `deny`: policy allows unsafe signing or broadcast.
- `needs_human`: policy change or live wallet action needs explicit human approval.
