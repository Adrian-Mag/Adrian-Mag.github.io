/*
 * harness-kernel.js
 * Act 2 panels — "Inside the Kernel"
 *
 *   1. #tokenizer-panel   — text splits into sub-word tokens, not words.
 *   2. #nexttoken-panel   — the model emits a distribution, not an answer.
 *
 * BOTH PANELS ARE ILLUSTRATIVE and say so on screen.
 *
 * The tokenizer uses a small hand-built vocabulary that reproduces the
 * *behaviours* of a real BPE tokenizer (leading spaces belong to tokens,
 * common words are single tokens, rare and technical words fragment, case
 * and digits split awkwardly). It is not a real vocabulary and the token
 * counts are not real token counts.
 *
 * The distributions in panel 2 are hand-authored. Real next-token
 * probabilities are not something this page can obtain: it is a static site,
 * and exposing them would require a model that returns per-token
 * probabilities. The shape of the lesson — a distribution, not an answer —
 * is faithful; the specific numbers are invented.
 */
(function () {
    "use strict";

    function el(tag, cls, text) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (text != null) n.textContent = text;
        return n;
    }

    /* =========================================================
       1. TOKENIZER
       ========================================================= */
    (function tokenizer() {
        var root = document.getElementById("tokenizer-panel");
        if (!root) return;

        // Illustrative vocabulary. Ordered longest-first at match time.
        // Leading spaces are part of the token, as in real BPE vocabularies.
        // Deliberately contains only ordinary words. Technical and unfamiliar
        // vocabulary is absent so that it fragments, which is the behaviour the
        // act is describing — a real vocabulary is built the same way, from
        // frequency, and long specialist terms rarely earn a slot.
        var VOCAB = [
            " different", " because", " question", " sentence", " remember",
            " language", " context", " machine", " between", " nothing",
            " numbers", " problems", " answer", " around", " really", " should",
            " simple", " little", " It", " If", " As",
            " model", " token", " words", " there", " which", " these", " where",
            " about", " would", " could", " every", " first", " never", " being",
            " what", " with", " that", " this", " from", " they", " have", " does",
            " will", " your", " when", " here", " than", " some", " like", " just",
            " into", " over", " only", " each", " both", " most", " many",
            " the", " and", " for", " are", " but", " not", " you", " all", " can",
            " has", " was", " one", " out", " its", " who", " why", " how",
            " a", " I", " is", " it", " to", " of", " in", " on", " at", " an",
            " as", " be", " by", " do", " if", " no", " or", " so", " up", " we",
            "understand", "seism", "ology", "ology", "ization", "isation",
            "ational", "ation", "ings", "ing", "ted", "ers", "er", "ly", "ed",
            "es", "s", "'s", "n't", "'re", "'ve", "'ll",
            "the", "and", "you", "The", "This", "That", "What", "It", "A", "I"
        ];

        var els = {};

        function tokenize(text) {
            var out = [];
            var i = 0;
            while (i < text.length) {
                var best = null;
                for (var v = 0; v < VOCAB.length; v++) {
                    var cand = VOCAB[v];
                    if (!cand) continue;
                    if (text.substr(i, cand.length) === cand) {
                        if (!best || cand.length > best.length) best = cand;
                    }
                }
                if (best) {
                    out.push(best);
                    i += best.length;
                } else {
                    // fall back: digits split individually, other runs of letters
                    // break into chunks of <=4 — imitating how unfamiliar strings
                    // fragment in a real tokenizer
                    var ch = text[i];
                    var run;
                    if (/[0-9]/.test(ch)) {
                        // digits split individually, as they often do in practice
                        out.push(ch);
                        i += 1;
                    } else if (ch === " " && /[A-Za-z0-9]/.test(text[i + 1] || "")) {
                        // a space belongs to the token that follows it, never alone
                        if (/[0-9]/.test(text[i + 1])) {
                            out.push(" " + text[i + 1]);
                            i += 2;
                        } else {
                            run = /^[A-Za-z]+/.exec(text.slice(i + 1))[0].slice(0, 4);
                            out.push(" " + run);
                            i += run.length + 1;
                        }
                    } else if (/[A-Za-z]/.test(ch)) {
                        run = /^[A-Za-z]+/.exec(text.slice(i))[0].slice(0, 4);
                        out.push(run);
                        i += run.length;
                    } else {
                        out.push(ch);
                        i += 1;
                    }
                }
            }
            return out;
        }

        function render() {
            var text = els.input.value;
            var toks = tokenize(text);
            els.out.innerHTML = "";
            toks.forEach(function (t, i) {
                var chip = el("span", "hz-tok hz-tok-" + (i % 2));
                // show a visible marker for the leading space
                chip.textContent = t.replace(/^ /, "·");
                chip.title = JSON.stringify(t);
                els.out.appendChild(chip);
            });
            els.count.textContent = text.length + " characters  →  " +
                                    toks.length + " tokens";
        }

        root.innerHTML = "";
        var head = el("div", "hz-panel-head");
        var t = el("div", "hz-panel-title", "How text is actually split ");
        t.appendChild(el("span", "hz-illustrative", "illustrative"));
        head.appendChild(t);
        root.appendChild(head);

        var body = el("div", "hz-panel-body");
        els.input = el("input", "hz-input");
        els.input.type = "text";
        els.input.value = "The model does not read words. It reads tokens like seismology.";
        els.input.setAttribute("aria-label", "Text to tokenize");
        els.input.addEventListener("input", render);
        body.appendChild(els.input);

        els.out = el("div", "hz-toks");
        body.appendChild(els.out);

        els.count = el("div", "hz-meter-k");
        els.count.style.marginTop = "10px";
        body.appendChild(els.count);

        var note = el("p", "hz-panel-fallback");
        note.style.marginTop = "12px";
        note.innerHTML = "A small hand-built vocabulary, not a real one. It reproduces the " +
            "<em>behaviours</em> that matter &mdash; a leading space belongs to the token " +
            "(shown as &middot;), common words survive whole, unfamiliar and technical words " +
            "shatter &mdash; but the pieces and the counts are illustrative, not measured.";
        body.appendChild(note);

        root.appendChild(body);
        render();
    })();

    /* =========================================================
       2. NEXT-TOKEN DISTRIBUTION
       ========================================================= */
    (function nextToken() {
        var root = document.getElementById("nexttoken-panel");
        if (!root) return;

        // Hand-authored distributions. See file header.
        var PROMPTS = [
            {
                text: "The capital of France is",
                dist: [[" Paris", 0.91], [" the", 0.03], [" a", 0.02],
                       [" located", 0.02], [" now", 0.01], [" one", 0.01]]
            },
            {
                text: "The best way to learn mathematics is",
                dist: [[" to", 0.42], [" by", 0.24], [" through", 0.12],
                       [" not", 0.07], [" probably", 0.06], [" arguably", 0.05],
                       [" simple", 0.04]]
            },
            {
                text: "My favourite colour is",
                dist: [[" blue", 0.28], [" green", 0.17], [" red", 0.14],
                       [" probably", 0.13], [" a", 0.11], [" purple", 0.09],
                       [" orange", 0.08]]
            }
        ];

        var state = { p: 0, temp: 1.0, sampled: [] };
        var els = {};

        function reweight(dist, T) {
            // Temperature applied to probabilities: p^(1/T), renormalised.
            var pow = dist.map(function (d) { return Math.pow(d[1], 1 / Math.max(T, 0.01)); });
            var sum = pow.reduce(function (a, b) { return a + b; }, 0);
            return dist.map(function (d, i) { return [d[0], pow[i] / sum]; });
        }

        function render() {
            var prompt = PROMPTS[state.p];
            var dist = reweight(prompt.dist, state.temp);

            els.prompt.textContent = prompt.text + state.sampled.join("");
            els.bars.innerHTML = "";
            dist.slice().sort(function (a, b) { return b[1] - a[1]; }).forEach(function (d) {
                var row = el("div", "hz-bar-row");
                row.appendChild(el("span", "hz-bar-tok", d[0].replace(/^ /, "·")));
                var track = el("span", "hz-bar-track");
                var fill = el("span", "hz-bar-fill");
                fill.style.width = (d[1] * 100).toFixed(1) + "%";
                track.appendChild(fill);
                row.appendChild(track);
                row.appendChild(el("span", "hz-bar-pct", (d[1] * 100).toFixed(1) + "%"));
                els.bars.appendChild(row);
            });
            els.tempOut.textContent = state.temp.toFixed(2);
        }

        function sample() {
            var dist = reweight(PROMPTS[state.p].dist, state.temp);
            var r = Math.random(), acc = 0;
            for (var i = 0; i < dist.length; i++) {
                acc += dist[i][1];
                if (r <= acc) { state.sampled.push(dist[i][0]); break; }
            }
            render();
        }

        root.innerHTML = "";
        var head = el("div", "hz-panel-head");
        var t = el("div", "hz-panel-title", "What the model actually returns ");
        t.appendChild(el("span", "hz-illustrative", "illustrative"));
        head.appendChild(t);
        root.appendChild(head);

        var body = el("div", "hz-panel-body");

        var sel = el("div", "hz-panel-controls");
        PROMPTS.forEach(function (p, i) {
            var b = el("button", "hz-btn" + (i === 0 ? " is-on" : ""), "“" + p.text + "…”");
            b.type = "button";
            b.addEventListener("click", function () {
                state.p = i; state.sampled = [];
                [].forEach.call(sel.children, function (c, j) {
                    c.className = "hz-btn" + (j === i ? " is-on" : "");
                });
                render();
            });
            sel.appendChild(b);
        });
        body.appendChild(sel);

        els.prompt = el("div", "hz-prompt");
        body.appendChild(els.prompt);

        els.bars = el("div", "hz-bars");
        body.appendChild(els.bars);

        var ctl = el("div", "hz-panel-controls");
        ctl.style.marginTop = "14px";

        var lab = el("label", "hz-meter-k", "temperature ");
        var slider = el("input");
        slider.type = "range";
        slider.min = "0.1"; slider.max = "2"; slider.step = "0.05"; slider.value = "1";
        slider.className = "hz-range";
        slider.setAttribute("aria-label", "Sampling temperature");
        slider.addEventListener("input", function () {
            state.temp = parseFloat(slider.value); render();
        });
        els.tempOut = el("span", "hz-meter-k", "1.00");
        lab.appendChild(slider);
        lab.appendChild(els.tempOut);
        ctl.appendChild(lab);

        var samp = el("button", "hz-btn", "Sample a token →");
        samp.type = "button";
        samp.addEventListener("click", sample);
        ctl.appendChild(samp);

        var reset = el("button", "hz-btn", "Reset");
        reset.type = "button";
        reset.addEventListener("click", function () { state.sampled = []; render(); });
        ctl.appendChild(reset);

        body.appendChild(ctl);

        var note = el("p", "hz-panel-fallback");
        note.style.marginTop = "12px";
        note.innerHTML = "The probabilities here are hand-authored to show the shape of the " +
            "thing, not measured from a model &mdash; a static page cannot obtain real ones. " +
            "What is faithful: the model returns a <em>distribution over next tokens</em>, " +
            "something downstream picks one, and temperature controls how much of the tail " +
            "is in play. Press sample repeatedly on the second and third prompts.";
        body.appendChild(note);

        root.appendChild(body);
        render();
    })();
})();
