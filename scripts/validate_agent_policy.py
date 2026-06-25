#!/usr/bin/env python3
"""Validate a Solana AI agent safety policy JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


VALID_CLUSTERS = {"localnet", "devnet", "testnet", "mainnet-beta"}
VALID_CONFIRMATION_TARGETS = {"processed", "confirmed", "finalized"}
VALID_ROLES = {
    "observer",
    "proposer",
    "simulator",
    "signer",
    "broadcaster",
    "reconciler",
    "emergency_admin",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"Policy file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("Policy root must be a JSON object")
    return data


def require_obj(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"Missing object: {key}")
        return {}
    return value


def require_list(parent: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"Missing list: {key}")
        return []
    return value


def require_bool(parent: dict[str, Any], key: str, errors: list[str]) -> bool | None:
    value = parent.get(key)
    if not isinstance(value, bool):
        errors.append(f"Missing boolean: {key}")
        return None
    return value


def number(parent: dict[str, Any], key: str, errors: list[str], *, minimum: float = 0) -> float | None:
    value = parent.get(key)
    if not isinstance(value, (int, float)):
        errors.append(f"Missing numeric limit: {key}")
        return None
    if value < minimum:
        errors.append(f"{key} must be >= {minimum}")
    return float(value)


def validate(policy: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in ("name", "version", "cluster"):
        if not isinstance(policy.get(key), str) or not policy[key].strip():
            errors.append(f"Missing string: {key}")

    cluster = policy.get("cluster")
    if cluster not in VALID_CLUSTERS:
        errors.append(f"cluster must be one of {sorted(VALID_CLUSTERS)}")

    wallets = require_list(policy, "wallets", errors)
    roles_seen: set[str] = set()
    for index, wallet in enumerate(wallets):
        if not isinstance(wallet, dict):
            errors.append(f"wallets[{index}] must be an object")
            continue
        role = wallet.get("role")
        if role not in VALID_ROLES:
            errors.append(f"wallets[{index}].role must be one of {sorted(VALID_ROLES)}")
        else:
            roles_seen.add(role)
        if not isinstance(wallet.get("publicKey"), str) or not wallet["publicKey"].strip():
            errors.append(f"wallets[{index}].publicKey is required")
        can_sign = wallet.get("canSign")
        can_broadcast = wallet.get("canBroadcast")
        if not isinstance(can_sign, bool):
            errors.append(f"wallets[{index}].canSign must be boolean")
        if not isinstance(can_broadcast, bool):
            errors.append(f"wallets[{index}].canBroadcast must be boolean")
        if role == "proposer" and can_sign:
            errors.append("proposer wallet must not be able to sign")
        if role == "signer" and can_broadcast:
            errors.append("signer wallet must not also broadcast")

    for required_role in ("proposer", "signer", "broadcaster"):
        if required_role not in roles_seen:
            errors.append(f"wallets must include role: {required_role}")

    allowlists = require_obj(policy, "allowlists", errors)
    program_ids = require_list(allowlists, "programIds", errors)
    if not program_ids:
        errors.append("allowlists.programIds must not be empty")
    for index, item in enumerate(program_ids):
        if isinstance(item, str):
            warnings.append(f"allowlists.programIds[{index}] should include name and allowedInstructionFamilies")
        elif isinstance(item, dict):
            if not item.get("id"):
                errors.append(f"allowlists.programIds[{index}].id is required")
            families = item.get("allowedInstructionFamilies")
            if not isinstance(families, list) or not families:
                warnings.append(f"allowlists.programIds[{index}] should list allowedInstructionFamilies")
        else:
            errors.append(f"allowlists.programIds[{index}] must be string or object")

    token_mints = require_list(allowlists, "tokenMints", errors)
    destinations = require_list(allowlists, "destinations", errors)
    if not token_mints:
        warnings.append("allowlists.tokenMints is empty; this is only safe for non-token agents")
    if not destinations:
        warnings.append("allowlists.destinations is empty; destination checks may be too broad")

    denylists = require_obj(policy, "denylists", errors)
    require_list(denylists, "programIds", errors)
    require_list(denylists, "destinations", errors)

    limits = require_obj(policy, "limits", errors)
    per_tx = number(limits, "perTransactionUsd", errors)
    per_hour = number(limits, "perHourUsd", errors)
    per_day = number(limits, "perDayUsd", errors)
    slippage = number(limits, "maxSlippageBps", errors)
    priority_fee = number(limits, "maxPriorityFeeLamports", errors)
    max_writable = number(limits, "maxWritableAccounts", errors)
    max_signers = number(limits, "maxSigners", errors, minimum=1)
    retries = number(limits, "maxRetriesPerIntent", errors)

    if per_tx is not None and per_hour is not None and per_tx > per_hour:
        errors.append("perTransactionUsd must be <= perHourUsd")
    if per_hour is not None and per_day is not None and per_hour > per_day:
        errors.append("perHourUsd must be <= perDayUsd")
    if slippage is not None and slippage > 100:
        warnings.append("maxSlippageBps above 100 bps is risky for unattended agents")
    if priority_fee is not None and priority_fee > 1_000_000:
        warnings.append("maxPriorityFeeLamports is high; confirm fee escalation policy")
    if max_writable is not None and max_writable > 32:
        warnings.append("maxWritableAccounts above 32 makes account-effect review harder")
    if max_signers is not None and max_signers > 3:
        warnings.append("maxSigners above 3 deserves a multisig or explicit reviewer note")
    if retries is not None and retries > 3:
        warnings.append("maxRetriesPerIntent above 3 can hide runaway retry loops")

    gates = require_obj(policy, "gates", errors)
    for key in (
        "requireSimulation",
        "requireSigVerifyWhenAvailable",
        "requireIdempotencyKey",
        "requireMessageHashMatchAfterSigning",
        "requireHumanApprovalOnMainnet",
        "requireHumanApprovalForNewProgram",
        "requireHumanApprovalForAuthorityChanges",
    ):
        require_bool(gates, key, errors)

    if gates.get("requireSimulation") is not True:
        errors.append("requireSimulation must be true")
    if gates.get("requireIdempotencyKey") is not True:
        errors.append("requireIdempotencyKey must be true")
    if gates.get("requireMessageHashMatchAfterSigning") is not True:
        errors.append("requireMessageHashMatchAfterSigning must be true")
    if cluster == "mainnet-beta" and gates.get("requireHumanApprovalOnMainnet") is not True:
        errors.append("mainnet-beta requires requireHumanApprovalOnMainnet=true")

    confirmation = gates.get("confirmationTarget")
    if confirmation not in VALID_CONFIRMATION_TARGETS:
        errors.append(f"confirmationTarget must be one of {sorted(VALID_CONFIRMATION_TARGETS)}")

    stale_slots = number(gates, "staleBlockhashSlots", errors, minimum=1)
    if stale_slots is not None and stale_slots > 150:
        errors.append("staleBlockhashSlots should not exceed Solana recent blockhash validity")

    monitoring = require_obj(policy, "monitoring", errors)
    if not isinstance(monitoring.get("auditLogPath"), str) or not monitoring["auditLogPath"].strip():
        errors.append("monitoring.auditLogPath is required")
    alert_channels = require_list(monitoring, "alertChannels", errors)
    if not alert_channels:
        warnings.append("monitoring.alertChannels is empty")
    number(monitoring, "stuckTransactionTimeoutSeconds", errors, minimum=1)
    number(monitoring, "pollIntervalSeconds", errors, minimum=1)
    emergency_stop = require_obj(monitoring, "emergencyStop", errors)
    if emergency_stop.get("enabled") is not True:
        errors.append("monitoring.emergencyStop.enabled must be true")
    if not emergency_stop.get("owner"):
        errors.append("monitoring.emergencyStop.owner is required")
    if not emergency_stop.get("procedure"):
        errors.append("monitoring.emergencyStop.procedure is required")

    return errors, warnings


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_agent_policy.py <policy.json>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    policy = load_json(path)
    errors, warnings = validate(policy)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Policy validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"Policy validation passed: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
