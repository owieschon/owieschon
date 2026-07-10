"""Regression tests for the public, implementation-independent verifier."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from verify_demo import HERE, RUNNER, SEEDS, VerificationError, validate_panel, verify_all


class LeakageVerifierTests(unittest.TestCase):
    def test_multi_seed_black_box_verification(self) -> None:
        receipt = verify_all()
        self.assertTrue(receipt["verified"])
        self.assertEqual(receipt["seeds"], list(SEEDS))
        self.assertEqual(len(receipt["results"]), 3)

    def test_structural_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            panel_path = Path(raw_directory) / "panel.json"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--seed",
                    str(SEEDS[0]),
                    "--emit-panel",
                    str(panel_path),
                    "--json",
                ],
                cwd=HERE,
                capture_output=True,
                text=True,
                check=True,
            )
            panel = json.loads(panel_path.read_text(encoding="utf-8"))
        tampered = copy.deepcopy(panel)
        tampered["rows"][0]["entity_id"] = "customer-123"
        with self.assertRaisesRegex(VerificationError, "non-synthetic"):
            validate_panel(tampered, SEEDS[0])


if __name__ == "__main__":
    unittest.main()
