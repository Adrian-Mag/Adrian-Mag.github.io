/*
 * harness-toolloop.js
 * Act 4 panel — "The CPU and the Computer"
 *
 * Steps through a REAL recorded tool loop, one move at a time, so the
 * alternation is impossible to miss: the model only ever asks; the harness
 * is the only thing that acts.
 *
 * Data: media/research/harness/toolloop.json, extracted from actual Claude
 * Code session logs by figure_generation/harness/extract_toolloop.py.
 * Long tool results are truncated, and every truncation is flagged in the
 * data and rendered as such here — no step is silently dropped.
 */
(function () {
    "use strict";

    var root = document.getElementById("toolloop-panel");
    if (!root) return;

    var DATA_URL = root.getAttribute("data-src");
    var state = { data: null, t: 0, step: 1 };

    function el(tag, cls, text) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (text != null) n.textContent = text;
        return n;
    }

    function shortTool(name) {
        if (!name) return "";
        // MCP tools arrive namespaced: mcp__<plugin>__<tool>. Show the tail,
        // but keep the prefix visible as a badge — it is the point of Act 9.
        var m = /^mcp__(.+?)__(.+)$/.exec(name);
        return m ? { mcp: true, server: m[1], tool: m[2] } : { mcp: false, tool: name };
    }

    function renderStep(s, idx, isCurrent) {
        var row = el("div", "hz-loop-step hz-loop-" + s.actor +
                     (isCurrent ? " is-current" : "") +
                     (idx + 1 > state.step ? " is-future" : ""));

        var gutter = el("div", "hz-loop-gutter");
        gutter.appendChild(el("span", "hz-loop-actor",
            s.actor === "model" ? "MODEL" : "HARNESS"));
        gutter.appendChild(el("span", "hz-loop-verb",
            s.kind === "request" ? "asks" : s.kind === "result" ? "returns" : "says"));
        row.appendChild(gutter);

        var body = el("div", "hz-loop-body");
        if (s.tool) {
            var t = shortTool(s.tool);
            var head = el("div", "hz-loop-tool");
            if (t.mcp) {
                head.appendChild(el("span", "hz-loop-mcp", "MCP"));
                head.appendChild(el("span", "hz-loop-server", t.server));
            }
            head.appendChild(el("span", "hz-loop-toolname", t.tool));
            body.appendChild(head);
        }
        body.appendChild(el("div", "hz-loop-text", s.text));
        if (s.elided) {
            body.appendChild(el("div", "hz-loop-elided",
                "⋮ truncated for display — " + s.full_len.toLocaleString() +
                " characters were returned to the model"));
        }
        row.appendChild(body);
        return row;
    }

    function render() {
        var data = state.data;
        var tr = data.traces[state.t];
        root.innerHTML = "";

        var head = el("div", "hz-panel-head");
        head.appendChild(el("div", "hz-panel-title", "One turn of the loop, as it happened"));
        var sel = el("div", "hz-toggle");
        data.traces.forEach(function (x, i) {
            var b = el("button", "hz-btn" + (i === state.t ? " is-on" : ""), x.label);
            b.type = "button";
            b.addEventListener("click", function () {
                state.t = i; state.step = 1; render();
            });
            sel.appendChild(b);
        });
        head.appendChild(sel);
        root.appendChild(head);

        var body = el("div", "hz-panel-body");

        var list = el("div", "hz-loop");
        tr.steps.forEach(function (s, i) {
            if (i + 1 <= state.step) list.appendChild(renderStep(s, i, i + 1 === state.step));
        });
        body.appendChild(list);

        var ctl = el("div", "hz-panel-controls");
        ctl.style.marginTop = "16px";

        var back = el("button", "hz-btn", "← Back");
        back.type = "button";
        back.disabled = state.step === 1;
        back.addEventListener("click", function () { state.step--; render(); });

        var fwd = el("button", "hz-btn", "Next move →");
        fwd.type = "button";
        fwd.disabled = state.step >= tr.steps.length;
        fwd.addEventListener("click", function () { state.step++; render(); });

        var all = el("button", "hz-btn", "Play it out");
        all.type = "button";
        all.disabled = state.step >= tr.steps.length;
        all.addEventListener("click", function () {
            var timer = setInterval(function () {
                if (state.step >= tr.steps.length) { clearInterval(timer); return; }
                state.step++; render();
            }, 480);
        });

        var reset = el("button", "hz-btn", "Reset");
        reset.type = "button";
        reset.addEventListener("click", function () { state.step = 1; render(); });

        ctl.appendChild(back);
        ctl.appendChild(fwd);
        ctl.appendChild(all);
        ctl.appendChild(reset);
        ctl.appendChild(el("span", "hz-panel-fallback",
            "move " + state.step + " of " + tr.steps.length));
        body.appendChild(ctl);

        /* running tally — who has actually done anything */
        var shown = tr.steps.slice(0, state.step);
        var asks = shown.filter(function (s) { return s.kind === "request"; }).length;
        var acts = shown.filter(function (s) { return s.kind === "result"; }).length;
        var tally = el("div", "hz-trend");
        tally.style.marginTop = "12px";
        tally.appendChild(el("span", "hz-trend-v", String(asks)));
        tally.appendChild(el("span", "hz-trend-sep", "requests by the model"));
        tally.appendChild(el("span", "hz-trend-v", String(acts)));
        tally.appendChild(el("span", "hz-trend-sep", "executions by the harness"));
        tally.appendChild(el("span", "hz-trend-note",
            "  the model has executed nothing — it has no way to"));
        body.appendChild(tally);

        var note = el("p", "hz-panel-fallback");
        note.style.marginTop = "12px";
        note.textContent = tr.note;
        body.appendChild(note);

        var prov = el("p", "hz-panel-fallback");
        prov.style.marginTop = "6px";
        prov.style.opacity = "0.75";
        prov.textContent = "Real session log · " + tr.source + " · extracted verbatim, " +
                           "truncations marked.";
        body.appendChild(prov);

        root.appendChild(body);
    }

    fetch(DATA_URL, { cache: "no-cache" })
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(function (d) {
            if (!d || !d.traces || !d.traces.length) throw new Error("no traces");
            state.data = d; render();
        })
        .catch(function (e) {
            root.innerHTML = "";
            var b = el("div", "hz-panel-body");
            var p = el("p", "hz-panel-fallback");
            p.innerHTML = "<b>Trace unavailable.</b> This panel replays a real recorded " +
                          "session; the extract is missing. Regenerate with " +
                          "<code>figure_generation/harness/extract_toolloop.py</code>. " +
                          "<span style='opacity:.7'>(" + (e.message || e) + ")</span>";
            b.appendChild(p);
            root.appendChild(b);
        });
})();
