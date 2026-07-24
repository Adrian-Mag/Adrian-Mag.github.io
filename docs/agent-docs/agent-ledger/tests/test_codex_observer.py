"""Focused privacy and correlation tests for the Codex Agent Ledger adapter."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ADAPTER_PATH = Path(__file__).resolve().parents[1] / "adapters" / "codex" / "codex_observer.py"
SPEC = importlib.util.spec_from_file_location("agent_ledger_codex_observer", ADAPTER_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class CodexObserverTests(unittest.TestCase):
    """Ensure provider payload details are reduced before reaching the Ledger."""

    def test_prompt_and_tool_payloads_reduce_to_safe_correlated_events(self) -> None:
        """A hook never copies prompt-like fields, arguments, transcript, or cwd into events."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            with patch.object(adapter, "repository", return_value=Path("/private/repository")), patch.object(adapter.ledgerctl, "default_runtime", return_value=runtime):
                adapter.observe({"hook_event_name": "UserPromptSubmit", "cwd": "/private/repository", "transcript_path": "/private/chat.json", "prompt": "never retain this"})
                adapter.observe({"hook_event_name": "PreToolUse", "cwd": "/private/repository", "tool_name": "apply_patch", "tool_input": {"path": "/private/file", "content": "never retain this"}})
            events = [json.loads(line) for line in (runtime / "events.jsonl").read_text().splitlines()]
            self.assertEqual([item["kind"] for item in events], ["host.turn_submitted", "host.tool_requested"])
            self.assertEqual(events[1]["tool_class"], "patch")
            self.assertEqual(len({item["work_phase"] for item in events}), 1)
            forbidden = {"prompt", "command", "path", "content", "output", "transcript", "cwd", "tool_name", "tool_input"}
            self.assertTrue(all(not (forbidden & set(item)) for item in events))

    def test_stop_is_turn_stop_and_session_end_is_session_end(self) -> None:
        """The adapter keeps Codex turn and true-session lifecycle signals distinct."""
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            with patch.object(adapter, "repository", return_value=Path("/private/repository")), patch.object(adapter.ledgerctl, "default_runtime", return_value=runtime):
                adapter.observe({"hook_event_name": "UserPromptSubmit"})
                adapter.observe({"hook_event_name": "Stop"})
                adapter.observe({"hook_event_name": "SessionEnd"})
            events = [json.loads(line) for line in (runtime / "events.jsonl").read_text().splitlines()]
            self.assertEqual([item["kind"] for item in events], ["host.turn_submitted", "host.turn_stopped", "host.session_ended"])


if __name__ == "__main__":
    unittest.main()
