#!/usr/bin/env python3
"""
Record the statelessness demonstration for Act 3 of
"The Machine Around the Model".

WHAT THIS DOES
--------------
Runs the *same* three user turns twice against the Claude API:

  Run A "stateful"   — every request carries the full conversation so far.
                       This is what a chat product does on your behalf.
  Run B "stateless"  — every request carries ONLY the latest user turn.
                       Nothing is remembered, because nothing is re-sent.

The API itself is stateless in both runs. The difference is entirely in what
the *client* chooses to put in the request. That is the point of the act.

It records, verbatim: the exact messages array sent on every turn, the reply,
and the token usage. The token counts are the receipt — input tokens climb
turn over turn in run A and stay flat in run B, because in run A you are
re-sending (and paying for) the whole conversation every single time.

Output: media/research/harness/statelessness.json  (consumed by the Act 3 panel)

SETUP
-----
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...        # or: ant auth login

If you use an `ant auth login` profile, no env var is needed — the SDK picks
the profile up automatically and a bare Anthropic() client just works.

RUN
---
    python3 figure_generation/harness/record_statelessness.py

Cost is negligible (6 short requests). Nothing here is edited by hand
afterwards: what the script writes is what the page shows.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit(
        "The 'anthropic' package is not installed.\n"
        "  pip install anthropic\n"
        "then re-run this script."
    )

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "media" / "research" / "harness" / "statelessness.json"

# Opus 4.8 runs without extended thinking when `thinking` is omitted, which keeps
# the recorded replies short and legible in the exhibit. Change if you prefer.
MODEL = "claude-opus-4-8"
MAX_TOKENS = 1024

# Part of the real request, so it appears in the exhibit payload. Brevity keeps
# the replies readable on a web page; it does not affect the demonstration.
SYSTEM = "Answer in at most two sentences. Be direct."

# The same three user turns are sent in both runs. Turn 2 shows that context
# changes what a question even means; turn 3 shows plain recall.
USER_TURNS = [
    "I work on linear inverse problems in seismology.",
    "What does resolution mean here?",
    "What was the first thing I told you?",
]


def record(client: "anthropic.Anthropic", carry_history: bool) -> list[dict]:
    """Run the three turns, either carrying history forward or not."""
    history: list[dict] = []
    turns = []

    for i, user_text in enumerate(USER_TURNS, start=1):
        # THE ONE LINE THAT MATTERS.
        # carry_history=True  -> everything said so far, re-sent
        # carry_history=False -> just this turn, nothing else
        messages = (history + [{"role": "user", "content": user_text}]
                    if carry_history else
                    [{"role": "user", "content": user_text}])

        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM,
            messages=messages,
        )
        reply = "".join(b.text for b in resp.content if b.type == "text").strip()

        turns.append({
            "n": i,
            "user": user_text,
            # verbatim request payload for this turn — what the panel displays
            "request_messages": messages,
            "reply": reply,
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
            "stop_reason": resp.stop_reason,
        })

        # Only the stateful run accumulates. The stateless run deliberately forgets.
        if carry_history:
            history = messages + [{"role": "assistant", "content": reply}]

        print(f"  turn {i}: {resp.usage.input_tokens:>4} in / "
              f"{resp.usage.output_tokens:>3} out  |  {reply[:64]}")

    return turns


def main() -> None:
    client = anthropic.Anthropic()  # resolves API key or `ant auth login` profile

    print(f"model: {MODEL}\n")
    print("RUN A — stateful (full history re-sent every turn)")
    stateful = record(client, carry_history=True)
    print("\nRUN B — stateless (only the latest turn sent)")
    stateless = record(client, carry_history=False)

    payload = {
        "_comment": (
            "Recorded verbatim by figure_generation/harness/record_statelessness.py. "
            "Not hand-edited. Both runs send identical user turns; they differ only "
            "in whether prior turns are included in the request."
        ),
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": MODEL,
        "system": SYSTEM,
        "user_turns": USER_TURNS,
        "runs": {
            "stateful": {
                "label": "History re-sent every turn",
                "note": "What a chat product does for you, invisibly.",
                "turns": stateful,
            },
            "stateless": {
                "label": "Only the latest turn sent",
                "note": "The same API, asked the same questions, with nothing carried forward.",
                "turns": stateless,
            },
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")

    a = [t["input_tokens"] for t in stateful]
    b = [t["input_tokens"] for t in stateless]
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print(f"  input tokens, stateful : {a}   <- grows; you re-send and re-pay for the history")
    print(f"  input tokens, stateless: {b}   <- flat; nothing is carried")
    if not (a[-1] > a[0]):
        print("  WARNING: stateful input tokens did not grow — check the run before using this.")


if __name__ == "__main__":
    main()
