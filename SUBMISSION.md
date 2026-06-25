# Superteam Earn submission draft

Listing: Ship useful agent skills we can add to Solana AI Kit

## Submission link

TODO: Add public GitHub repository or PR URL after publishing.

## Title

Solana Agent Safety Skill

## Short description

A Claude Code / Codex skill for building and reviewing Solana AI agents with safer wallet roles, transaction policy, simulation gates, broadcast controls, monitoring, and incident response.

## Why this matters

Solana AI agents are increasingly able to prepare transactions, call routers, manage payments, and automate operational workflows. The hard recurring problem is not only coding the transaction. It is preventing unattended agents from bypassing wallet policy, over-spending, retrying unsafe transactions, logging secrets, or treating a returned signature as settlement.

This skill gives builders a production-oriented operating model for agentic Solana transaction safety.

## What is included

- Progressive `skill/SKILL.md` entry point.
- Focused files for policy design, transaction gates, runtime monitoring, incident response, and resources.
- Dependency-free policy validator script.
- Example JSON policy template.
- Claude/Codex command, rules, and reviewer agent.
- Installer and validation scripts.
- MIT license.

## Validation

Validated locally:

```bash
bash validate.sh
python3 -c "import py_compile; py_compile.compile('solana-agent-safety-skill/scripts/validate_agent_policy.py', cfile='/private/tmp/validate_agent_policy.pyc', doraise=True); print('py_compile ok')"
bash install.sh -y --path /private/tmp/solana-agent-safety-install-test
```

## Fit with the bounty

- Solves a real recurring builder problem: agent wallet and transaction safety.
- Cross-domain: AI agents, Solana transactions, wallet policy, ops, security, incident response.
- Progressive and token-efficient: entry point routes to focused docs.
- Ready to merge or submodule: includes installer, README, MIT license, and validation script.
