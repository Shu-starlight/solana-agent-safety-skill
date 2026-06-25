# Solana Agent Safety Skill

Claude Code / Codex skill for building Solana AI agents that can propose, simulate, gate, monitor, and recover from transactions without turning a wallet into an unbounded hot-key.

## Problem

Solana agents are moving from chat demos to systems that can route payments, manage vaults, create orders, rebalance positions, and call APIs around the clock. The failure mode is not just a bad answer. It can be an unsigned transaction leak, a stale blockhash loop, an unsafe retry, an over-broad signer, a hidden CPI path, or a policy bypass that spends real funds.

This skill gives an AI coding agent a repeatable operating model for:

- Designing least-privilege wallet and signer policies.
- Adding pre-sign and pre-broadcast transaction gates.
- Using simulation and status polling as safety boundaries.
- Keeping audit evidence that can be reviewed by humans.
- Handling incidents without exposing secrets or improvising under pressure.

## What is included

```text
solana-agent-safety-skill/
├── README.md
├── LICENSE
├── install.sh
├── validate.sh
├── skill/
│   ├── SKILL.md
│   ├── policy-design.md
│   ├── transaction-gates.md
│   ├── runtime-monitoring.md
│   ├── incident-response.md
│   └── resources.md
├── scripts/
│   └── validate_agent_policy.py
├── templates/
│   └── agent-policy.example.json
├── commands/
│   └── agent-safety-review.md
├── rules/
│   └── solana-agent-safety.md
└── agents/
    └── agent-security-reviewer.md
```

## Install

Default install:

```bash
./install.sh -y
```

This copies the skill to:

```text
~/.claude/skills/solana-agent-safety
```

Custom install:

```bash
./install.sh --path ./.claude/skills
```

## Validate the bundled policy example

```bash
./validate.sh
```

Or run the validator directly:

```bash
python3 scripts/validate_agent_policy.py templates/agent-policy.example.json
```

The validator is dependency-free and checks for missing policy fields, unsafe mainnet defaults, invalid signer roles, missing idempotency, absent simulation gates, excessive slippage, and weak monitoring configuration.

## Usage examples

Ask Claude Code or Codex:

```text
Use solana-agent-safety to design a transaction approval policy for an AI agent that can trade up to 50 USDC per day on devnet.
```

```text
Use solana-agent-safety to review this Solana agent repository before we connect a signer.
```

```text
Use solana-agent-safety to add simulation, idempotency, and confirmation polling to this transaction broadcaster.
```

```text
Use solana-agent-safety to write an incident runbook for a stuck transaction loop.
```

## Scope

This skill does not ask an agent to hold seed phrases, private keys, exchange credentials, or recovery codes. It assumes keys live in an external wallet, KMS, multisig, hardware signer, or policy service. The AI agent may prepare transactions and evidence, but signing and broadcast should pass through explicit policy gates.

## Sources and fit

This skill follows the structure requested by the Superteam Earn bounty:

- `skill/SKILL.md` as the entry point.
- Focused progressive-loading skill files.
- Optional `agents/`, `commands/`, and `rules/`.
- Installer script and clear README.
- MIT license.

It aligns with Solana's current transaction model: transactions are atomic, include one or more instructions plus signatures and a recent blockhash, and should be simulated before broadcast when an automated system is involved.

## License

MIT. See `LICENSE`.
