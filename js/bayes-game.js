/*
 * bayes-game.js — interactive posterior-update simulator for
 * "Bayes, Measure-Theoretically", Part 1.
 *
 * The reader (or the prior) picks a hidden switch configuration
 * m ∈ {00, 01, 10, 11}; the bulb is on iff the switches agree
 * (G(m) = 1 for 00 and 11); an unreliable reporter announces the bulb
 * state, telling the truth with probability 0.8.  Each report updates
 * a live posterior bar chart, computed with exactly the update rule
 * Part 2 constructs.  Numbers match the notes: prior (0.4, 0.1, 0.1, 0.4),
 * posterior after d=0 uniform, after d=1 equal to (8/17, 1/34, 1/34, 8/17).
 *
 * Repeated reports reuse the same one-report rule with the previous
 * posterior as the new prior — a small step beyond the notes, flagged
 * in the panel footer.
 *
 * Self-contained vanilla JS; attaches to #bayes-game.
 */
(function () {
    "use strict";

    var STATES = ["00", "01", "10", "11"];
    var PRIOR = [0.4, 0.1, 0.1, 0.4];
    var G = [1, 0, 0, 1];          // bulb state per m: on iff switches agree
    var P_TRUST = 0.8;

    // --- state ---------------------------------------------------------------

    var trueIdx = null;            // index into STATES, or null before start
    var secret = true;             // true if drawn from prior (hidden from reader)
    var reports = [];              // { d: 0|1, lie: bool }
    var revealed = false;

    // --- pure math ------------------------------------------------------------

    function posterior() {
        // post(m) ∝ prior(m) · Π_reports k(d | m),  k(d|m) = 0.8 if d = G(m) else 0.2
        var w = PRIOR.slice();
        reports.forEach(function (rep) {
            for (var i = 0; i < 4; i++) {
                w[i] *= (rep.d === G[i]) ? P_TRUST : (1 - P_TRUST);
            }
        });
        var Z = w.reduce(function (a, b) { return a + b; }, 0);
        return w.map(function (v) { return v / Z; });
    }

    // --- UI -------------------------------------------------------------------

    var els = {};

    function init() {
        var panel = document.getElementById("bayes-game");
        if (!panel) return;

        // choose-state row
        var chooser = div("bg-row");
        chooser.appendChild(label("Set the hidden switches:"));

        var drawBtn = button("Draw m from the prior", "bg-btn bg-btn-primary", function () {
            var u = Math.random(), acc = 0;
            for (var i = 0; i < 4; i++) { acc += PRIOR[i]; if (u < acc) { start(i, true); return; } }
            start(3, true);
        });
        chooser.appendChild(drawBtn);

        chooser.appendChild(label("or pick it yourself:"));
        STATES.forEach(function (s, i) {
            chooser.appendChild(button(s, "bg-btn bg-btn-state", function () { start(i, false); }));
        });
        panel.appendChild(chooser);

        // reporter row
        var repRow = div("bg-row");
        els.askBtn = button("Ask the reporter", "bg-btn bg-btn-primary", function () {
            if (trueIdx === null) return;
            var bulb = G[trueIdx];
            var lie = Math.random() > P_TRUST;
            var d = lie ? 1 - bulb : bulb;
            reports.push({ d: d, lie: lie });
            render();
        });
        els.askBtn.disabled = true;
        els.revealBtn = button("Reveal the truth", "bg-btn", function () {
            if (trueIdx === null) return;
            revealed = true;
            render();
        });
        els.revealBtn.disabled = true;
        els.resetBtn = button("Reset", "bg-btn", function () {
            trueIdx = null; reports = []; revealed = false; secret = true;
            render();
        });
        repRow.appendChild(els.askBtn);
        repRow.appendChild(els.revealBtn);
        repRow.appendChild(els.resetBtn);
        panel.appendChild(repRow);

        // hidden-state display
        els.stateLine = div("bg-state-line");
        panel.appendChild(els.stateLine);

        // report history
        var histWrap = div("bg-row");
        histWrap.appendChild(label("Reports heard:"));
        els.history = div("bg-history");
        histWrap.appendChild(els.history);
        panel.appendChild(histWrap);

        // posterior bars
        els.bars = [];
        var chart = div("bg-chart");
        STATES.forEach(function (s, i) {
            var row = div("bg-bar-row");
            var lab = document.createElement("span");
            lab.className = "bg-bar-label";
            lab.textContent = s;
            var track = div("bg-bar-track");
            var fill = div("bg-bar-fill");
            var tick = div("bg-prior-tick");
            tick.style.left = (PRIOR[i] * 100) + "%";
            tick.title = "prior = " + PRIOR[i].toFixed(2);
            track.appendChild(fill);
            track.appendChild(tick);
            var val = document.createElement("span");
            val.className = "bg-bar-value";
            row.appendChild(lab);
            row.appendChild(track);
            row.appendChild(val);
            chart.appendChild(row);
            els.bars.push({ fill: fill, val: val });
        });
        panel.appendChild(chart);

        var legend = div("bg-legend");
        legend.innerHTML =
            '<span class="bg-legend-item"><span class="bg-legend-fill"></span>posterior</span>' +
            '<span class="bg-legend-item"><span class="bg-legend-tick"></span>prior</span>';
        panel.appendChild(legend);

        // status
        els.status = div("bg-status");
        panel.appendChild(els.status);

        render();
    }

    function start(idx, fromPrior) {
        trueIdx = idx;
        secret = fromPrior;
        reports = [];
        revealed = false;
        render();
    }

    // --- rendering -------------------------------------------------------------

    function render() {
        var post = posterior();

        els.askBtn.disabled = (trueIdx === null);
        els.revealBtn.disabled = (trueIdx === null || revealed);

        // hidden-state line
        if (trueIdx === null) {
            els.stateLine.textContent = "No hidden state set yet.";
        } else if (revealed) {
            var lies = reports.filter(function (r) { return r.lie; }).length;
            els.stateLine.innerHTML =
                "Truth: m = <b>" + STATES[trueIdx] + "</b>, bulb " +
                (G[trueIdx] ? "on (1)" : "off (0)") + ". The reporter lied " +
                lies + " of " + reports.length + " times.";
        } else if (secret) {
            els.stateLine.textContent = "The switches are set (drawn from the prior) — hidden inside the box.";
        } else {
            els.stateLine.innerHTML = "You set m = <b>" + STATES[trueIdx] + "</b> — now watch what the reports alone can recover.";
        }

        // history chips
        els.history.innerHTML = "";
        reports.forEach(function (rep) {
            var chip = document.createElement("span");
            chip.className = "bg-chip" + (revealed && rep.lie ? " bg-chip-lie" : "");
            chip.textContent = String(rep.d);
            if (revealed && rep.lie) chip.title = "a lie";
            els.history.appendChild(chip);
        });
        if (!reports.length) {
            var none = document.createElement("span");
            none.className = "bg-chip-none";
            none.textContent = "(none yet)";
            els.history.appendChild(none);
        }

        // bars
        post.forEach(function (v, i) {
            els.bars[i].fill.style.width = (v * 100) + "%";
            els.bars[i].val.textContent = v.toFixed(3);
        });

        setStatus(post);
    }

    function setStatus(post) {
        var msg;
        var pairSame = post[0] + post[3];   // {00, 11}
        var pairDiff = post[1] + post[2];   // {01, 10}

        if (trueIdx === null) {
            msg = "Before any report, the posterior IS the prior: (0.40, 0.10, 0.10, 0.40). " +
                  "Set the switches to begin.";
        } else if (reports.length === 0) {
            msg = "No reports yet, so the bars still show the prior. Ask the reporter.";
        } else if (reports.length === 1) {
            if (reports[0].d === 0) {
                msg = "One report of 0 gives the uniform posterior (0.25 each) — exactly Part 2’s " +
                      "computation: the report’s pull toward {01, 10} perfectly cancels the " +
                      "prior’s preference for {00, 11}.";
            } else {
                msg = "One report of 1 gives (8/17, 1/34, 1/34, 8/17) ≈ (0.471, 0.029, 0.029, 0.471) " +
                      "— exactly Part 2’s computation. The prior and the report now agree.";
            }
        } else if (Math.max(pairSame, pairDiff) > 0.95) {
            var pair = pairSame > pairDiff ? "{00, 11}" : "{01, 10}";
            msg = "The posterior is nearly certain the truth lies in " + pair + " — but the two members " +
                  "stay in the same ratio forever. The reports only ever describe the bulb, and the bulb " +
                  "cannot tell them apart. No amount of data can recover what G never carried.";
        } else {
            msg = "Each new report multiplies in the same one-report rule (0.8 for agreement, 0.2 for " +
                  "disagreement) and renormalizes. Keep asking and watch where the mass flows.";
        }
        els.status.textContent = msg;
    }

    // --- tiny DOM helpers -------------------------------------------------------

    function div(cls) {
        var d = document.createElement("div");
        d.className = cls;
        return d;
    }

    function label(text) {
        var s = document.createElement("span");
        s.className = "bg-label";
        s.textContent = text;
        return s;
    }

    function button(text, cls, onClick) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = cls;
        b.textContent = text;
        b.addEventListener("click", onClick);
        return b;
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
