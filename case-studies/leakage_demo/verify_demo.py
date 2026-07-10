#!/usr/bin/env python3
"""Independently verify the synthetic temporal-leakage demonstration.

The verifier treats ``run_demo.py`` as an external producer. It invokes the
runner in a subprocess, consumes only the emitted raw panel and summary, then
rebuilds the features and AUC with separate code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
RUNNER = HERE / "run_demo.py"
EXPECTED = HERE / "expected_output.json"
SEEDS = (20260710, 104729, 982451653)
ENTITY_RE = re.compile(r"^entity-(\d+)-(\d{2})-(\d{2})$")
GROUP_RE = re.compile(r"^group-(\d{2})$")


class VerificationError(ValueError):
    """The public evidence failed a structural or behavioral check."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _invoke_runner(seed: int, directory: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    panel_path = directory / f"panel-{seed}.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--seed",
            str(seed),
            "--emit-panel",
            str(panel_path),
            "--json",
        ],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if completed.returncode != 0:
        raise VerificationError(f"runner failed for seed {seed}: {completed.stderr.strip()}")
    try:
        claimed = json.loads(completed.stdout)
        panel = _load_json(panel_path)
    except (json.JSONDecodeError, OSError) as exc:
        raise VerificationError(f"runner emitted invalid evidence for seed {seed}: {exc}") from exc
    return panel, claimed, _sha256(panel_path)


def validate_panel(panel: Any, seed: int) -> list[dict[str, Any]]:
    if not isinstance(panel, dict) or set(panel) != {
        "schema",
        "seed",
        "cutoff_period",
        "rows",
    }:
        raise VerificationError("panel must contain exactly schema, seed, cutoff_period, and rows")
    if panel["schema"] != "temporal-leakage-panel.v1":
        raise VerificationError("unexpected panel schema")
    if panel["seed"] != seed or isinstance(panel["seed"], bool):
        raise VerificationError("panel seed does not match the invocation")
    cutoff = panel["cutoff_period"]
    if cutoff != 2 or isinstance(cutoff, bool):
        raise VerificationError("the frozen public experiment uses cutoff period 2")
    rows = panel["rows"]
    if not isinstance(rows, list) or len(rows) != 2000:
        raise VerificationError("panel must contain exactly 2,000 rows")

    entity_periods: dict[str, set[int]] = defaultdict(set)
    group_entities: dict[str, set[str]] = defaultdict(set)
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {
            "entity_id",
            "peer_group",
            "period",
            "label",
        }:
            raise VerificationError(f"row {index} has an unexpected shape")
        entity = row["entity_id"]
        group = row["peer_group"]
        period = row["period"]
        label = row["label"]
        entity_match = ENTITY_RE.fullmatch(entity) if isinstance(entity, str) else None
        group_match = GROUP_RE.fullmatch(group) if isinstance(group, str) else None
        if entity_match is None or int(entity_match.group(1)) != seed:
            raise VerificationError(f"row {index} has a non-synthetic or mismatched entity ID")
        if group_match is None or entity_match.group(2) != group_match.group(1):
            raise VerificationError(f"row {index} has inconsistent group membership")
        if not isinstance(period, int) or isinstance(period, bool) or period not in range(5):
            raise VerificationError(f"row {index} has an invalid period")
        if not isinstance(label, int) or isinstance(label, bool) or label not in (0, 1):
            raise VerificationError(f"row {index} has a non-binary label")
        if period in entity_periods[entity]:
            raise VerificationError(f"entity {entity} repeats period {period}")
        entity_periods[entity].add(period)
        group_entities[group].add(entity)

    if len(entity_periods) != 400 or any(periods != set(range(5)) for periods in entity_periods.values()):
        raise VerificationError("panel must contain 400 complete five-period entities")
    if len(group_entities) != 40 or any(len(entities) != 10 for entities in group_entities.values()):
        raise VerificationError("panel must contain 40 groups of ten entities")
    return rows


def _peer_scores(
    rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    include: Callable[[dict[str, Any]], bool],
) -> list[float]:
    group_sum: dict[str, int] = defaultdict(int)
    group_count: dict[str, int] = defaultdict(int)
    entity_sum: dict[str, int] = defaultdict(int)
    entity_count: dict[str, int] = defaultdict(int)
    for row in rows:
        if include(row):
            group_sum[row["peer_group"]] += row["label"]
            group_count[row["peer_group"]] += 1
            entity_sum[row["entity_id"]] += row["label"]
            entity_count[row["entity_id"]] += 1
    scores: list[float] = []
    for row in evaluation_rows:
        numerator = group_sum[row["peer_group"]] - entity_sum[row["entity_id"]]
        denominator = group_count[row["peer_group"]] - entity_count[row["entity_id"]]
        if denominator <= 0:
            raise VerificationError("a peer score has no independent peers")
        scores.append(numerator / denominator)
    return scores


def _rank_auc(labels: list[int], scores: list[float]) -> float:
    ordered = sorted(zip(scores, labels), key=lambda item: item[0])
    positive_rank_sum = 0.0
    positive_count = sum(labels)
    negative_count = len(labels) - positive_count
    if not positive_count or not negative_count:
        raise VerificationError("AUC requires both positive and negative rows")
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = ((index + 1) + end) / 2
        positive_rank_sum += average_rank * sum(label for _score, label in ordered[index:end])
        index = end
    return (
        positive_rank_sum - positive_count * (positive_count + 1) / 2
    ) / (positive_count * negative_count)


def independent_summary(panel: dict[str, Any], seed: int) -> dict[str, Any]:
    rows = validate_panel(panel, seed)
    cutoff = panel["cutoff_period"]
    evaluation_rows = sorted(
        (row for row in rows if row["period"] == cutoff),
        key=lambda row: row["entity_id"],
    )
    labels = [row["label"] for row in evaluation_rows]
    leaky_scores = _peer_scores(rows, evaluation_rows, lambda _row: True)
    honest_scores = _peer_scores(rows, evaluation_rows, lambda row: row["period"] < cutoff)

    perturbed = [dict(row) for row in rows]
    for row in perturbed:
        if row["period"] > cutoff:
            row["label"] = 1 - row["label"]
    perturbed_leaky = _peer_scores(perturbed, evaluation_rows, lambda _row: True)
    perturbed_honest = _peer_scores(
        perturbed,
        evaluation_rows,
        lambda row: row["period"] < cutoff,
    )
    return {
        "seed": seed,
        "rows": len(rows),
        "cutoff_period": cutoff,
        "leaky_auc": round(_rank_auc(labels, leaky_scores), 6),
        "honest_cutoff_auc": round(_rank_auc(labels, honest_scores), 6),
        "future_censor_leaky_auc": round(_rank_auc(labels, perturbed_leaky), 6),
        "future_censor_leaky_rows_changed": sum(
            before != after for before, after in zip(leaky_scores, perturbed_leaky)
        ),
        "future_censor_honest_rows_changed": sum(
            before != after for before, after in zip(honest_scores, perturbed_honest)
        ),
    }


def verify_all() -> dict[str, Any]:
    expected = _load_json(EXPECTED)
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="leakage-verifier-") as raw_directory:
        directory = Path(raw_directory)
        for seed in SEEDS:
            panel, claimed, panel_sha256 = _invoke_runner(seed, directory)
            computed = independent_summary(panel, seed)
            if claimed != computed:
                raise VerificationError(
                    f"runner and independent verifier disagree for seed {seed}"
                )
            if seed == SEEDS[0] and claimed != expected:
                raise VerificationError("the documented seed differs from expected_output.json")
            if not (
                computed["leaky_auc"] >= 0.99
                and computed["honest_cutoff_auc"] == 0.5
                and computed["future_censor_leaky_auc"] <= 0.01
                and computed["future_censor_leaky_rows_changed"] == 400
                and computed["future_censor_honest_rows_changed"] == 0
            ):
                raise VerificationError(f"causal leakage invariants failed for seed {seed}")
            results.append({**computed, "panel_sha256": panel_sha256})
    return {
        "schema": "temporal-leakage-verification.v1",
        "verified": True,
        "runner_sha256": _sha256(RUNNER),
        "expected_output_sha256": _sha256(EXPECTED),
        "seeds": list(SEEDS),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit compact JSON")
    args = parser.parse_args()
    try:
        receipt = verify_all()
    except VerificationError as exc:
        print(json.dumps({"verified": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(receipt, indent=None if args.json else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
