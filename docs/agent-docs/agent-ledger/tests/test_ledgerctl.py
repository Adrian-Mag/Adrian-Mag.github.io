"""Focused black-box tests for the private Agent Ledger runtime."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ledgerctl.py"
sys.path.insert(0, str(SCRIPT.parent))
import ledgerctl  # noqa: E402


class LedgerCtlTests(unittest.TestCase):
    """Exercise schema checks and state transitions without touching real runtime state."""

    def run_ledger(self, runtime: Path, *arguments: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        """Run one command against an isolated runtime and assert its status."""
        completed = subprocess.run([sys.executable, str(SCRIPT), "--runtime", str(runtime), *arguments], text=True, capture_output=True)
        self.assertEqual(completed.returncode, expect, completed.stderr)
        return completed

    def test_full_declared_phase_writes_safe_state_and_no_findings(self) -> None:
        """A closed phase records only controlled categories and produces no gap finding."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            phase = self.run_ledger(runtime, "begin", "--route", "change-planned").stdout.strip()
            self.assertRegex(phase, r"^wp-[0-9a-f]{24}$")
            self.run_ledger(runtime, "record", "--record-type", "plan")
            self.run_ledger(runtime, "record", "--record-type", "reference")
            self.run_ledger(runtime, "step", "--step", "work")
            self.run_ledger(runtime, "check", "--outcome", "passed")
            self.run_ledger(runtime, "close")
            report = json.loads(self.run_ledger(runtime, "report").stdout)
            state = json.loads((runtime / "state.json").read_text())
            events = [json.loads(line) for line in (runtime / "events.jsonl").read_text().splitlines()]
            self.assertEqual(state["status"], "closed")
            self.assertEqual(report["findings"], [])
            self.assertTrue(all(set(item) <= {"schema_version", "at", "kind", "work_phase", "route", "source", "outcome", "record_type", "step", "tool_class"} for item in events))

    def test_unclosed_phase_is_reported_as_a_gap(self) -> None:
        """The reporter flags an open phase without claiming misconduct."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            self.run_ledger(runtime, "begin", "--route", "inspect")
            report = json.loads(self.run_ledger(runtime, "report").stdout)
            self.assertEqual(report["findings"][0]["kind"], "ledger.work_phase_unclosed")
            self.assertEqual(report["findings"][0]["outcome"], "missing")

    def test_unsafe_work_phase_is_rejected(self) -> None:
        """Raw-path-like values cannot be used as an event correlation token."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            completed = self.run_ledger(runtime, "observe", "--kind", "host.tool_requested", "--work-phase", "../private", expect=1)
            self.assertIn("opaque token", completed.stderr)

    def test_pending_host_phase_is_claimed_by_a_later_route_declaration(self) -> None:
        """A host tool event and later declared route share one opaque phase token."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            phase = ledgerctl.begin_turn(runtime)
            self.assertTrue(ledgerctl.observe_host(runtime, "host.tool_requested", "patch"))
            self.assertEqual(self.run_ledger(runtime, "begin", "--route", "change-planned").stdout.strip(), phase)
            events = [json.loads(line) for line in (runtime / "events.jsonl").read_text().splitlines()]
            self.assertEqual([item["kind"] for item in events], ["host.turn_submitted", "host.tool_requested", "agent.route_declared"])
            self.assertTrue(all(item["work_phase"] == phase for item in events))

    def test_parallel_observations_do_not_lose_events(self) -> None:
        """The advisory lock keeps concurrent hook-style writers from dropping lines."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            self.run_ledger(runtime, "begin", "--route", "inspect")
            commands = [[sys.executable, str(SCRIPT), "--runtime", str(runtime), "observe", "--kind", "host.tool_completed"] for _ in range(12)]
            workers = [subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for command in commands]
            for worker in workers:
                _, stderr = worker.communicate()
                self.assertEqual(worker.returncode, 0, stderr)
            events = [json.loads(line) for line in (runtime / "events.jsonl").read_text().splitlines()]
            self.assertEqual(sum(item["kind"] == "host.tool_completed" for item in events), 12)


if __name__ == "__main__":
    unittest.main()
