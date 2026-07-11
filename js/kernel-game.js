/*
 * kernel-game.js — interactive "Kernel Game" panel for SOLA Act 1.
 *
 * The reader mixes six sensitivity kernels K_i(r) with weights x_i and
 * tries to make the combined kernel  A(r) = sum_i x_i K_i(r)  match a
 * target kernel T(r).  Live readouts show the kernel mismatch and the
 * noise amplification sqrt(sum x_i^2), and a "Let SOLA solve it" button
 * computes the optimal weights for an adjustable noise penalty — the
 * same tradeoff SOLA itself negotiates.
 *
 * Self-contained vanilla JS + canvas; attaches to #kernel-game.
 */
(function () {
    "use strict";

    var N_GRID = 241;
    var N_K = 6;

    // Two canvas palettes: space (dark panel) and earth (light panel).
    var PALETTES = {
        space: {
            target: "#e0e0e0",
            resolving: "#4ecdc4",
            mismatch: "rgba(255,107,107,0.28)",
            kernels: ["#6791BE", "#9ed49e", "#e8a878", "#c8a8e0", "#B8B7C5", "#d4c46a"],
            grid: "rgba(255,255,255,0.08)",
            axis: "rgba(255,255,255,0.35)",
            font: "rgba(255,255,255,0.75)"
        },
        earth: {
            target: "#3A3627",
            resolving: "#2E7D6B",
            mismatch: "rgba(162,60,54,0.30)",
            kernels: ["#5C6D33", "#3E7D5E", "#B0741B", "#6E4390", "#6A644F", "#8F7A1E"],
            grid: "rgba(41,38,27,0.10)",
            axis: "rgba(41,38,27,0.40)",
            font: "rgba(41,38,27,0.80)"
        }
    };
    function themeName() {
        return document.documentElement.getAttribute("data-theme") === "earth" ? "earth" : "space";
    }
    var COLORS = PALETTES[themeName()];

    // --- problem definition -------------------------------------------------

    var grid = [];
    (function () {
        for (var i = 0; i < N_GRID; i++) grid.push(i / (N_GRID - 1));
    })();

    function win(r, c, w) { var t = (r - c) / w; return Math.exp(-t * t); }

    // Six sensitivity kernels: smooth bumps, a broad averager, and two
    // oscillatory (sign-flipping) kernels.  Coverage fades beyond r ~ 0.75,
    // deliberately: the data are nearly deaf there.
    var KERNEL_DEFS = [
        { label: "K₁", f: function (r) { return win(r, 0.12, 0.09); } },
        { label: "K₂", f: function (r) { return win(r, 0.28, 0.11); } },
        { label: "K₃", f: function (r) { return win(r, 0.40, 0.18) * Math.sin(6 * Math.PI * r); } },
        { label: "K₄", f: function (r) { return win(r, 0.52, 0.10); } },
        { label: "K₅", f: function (r) { return win(r, 0.35, 0.25); } },
        { label: "K₆", f: function (r) { return win(r, 0.62, 0.15) * Math.sin(9 * Math.PI * r + 0.8); } }
    ];

    var TARGETS = [
        { id: "shallow", label: "T at r = 0.30", c: 0.30, w: 0.09 },
        { id: "mid", label: "T at r = 0.50", c: 0.50, w: 0.09 },
        { id: "deep", label: "T at r = 0.85", c: 0.85, w: 0.09 }
    ];

    // Precompute kernels on the grid, peak-normalized.
    var K = KERNEL_DEFS.map(function (def) {
        var v = grid.map(def.f);
        var peak = Math.max.apply(null, v.map(Math.abs));
        return v.map(function (y) { return y / peak; });
    });

    function targetValues(t) {
        return grid.map(function (r) { return win(r, t.c, t.w); });
    }

    function inner(a, b) {
        // trapezoid rule on the uniform grid
        var h = 1 / (N_GRID - 1), s = 0;
        for (var i = 0; i < N_GRID; i++) {
            var w = (i === 0 || i === N_GRID - 1) ? 0.5 : 1;
            s += w * a[i] * b[i];
        }
        return s * h;
    }

    // Gram matrix of the kernels (for the SOLA solve)
    var GRAM = [];
    (function () {
        for (var i = 0; i < N_K; i++) {
            GRAM.push([]);
            for (var j = 0; j < N_K; j++) GRAM[i].push(inner(K[i], K[j]));
        }
    })();

    function solveLinear(A, b) {
        // Gaussian elimination with partial pivoting; A is n x n (copied).
        var n = b.length, i, j, k;
        var M = A.map(function (row, r) { return row.concat([b[r]]); });
        for (k = 0; k < n; k++) {
            var p = k;
            for (i = k + 1; i < n; i++) if (Math.abs(M[i][k]) > Math.abs(M[p][k])) p = i;
            var tmp = M[k]; M[k] = M[p]; M[p] = tmp;
            if (Math.abs(M[k][k]) < 1e-14) continue;
            for (i = k + 1; i < n; i++) {
                var f = M[i][k] / M[k][k];
                for (j = k; j <= n; j++) M[i][j] -= f * M[k][j];
            }
        }
        var x = new Array(n).fill(0);
        for (i = n - 1; i >= 0; i--) {
            var s = M[i][n];
            for (j = i + 1; j < n; j++) s -= M[i][j] * x[j];
            x[i] = Math.abs(M[i][i]) < 1e-14 ? 0 : s / M[i][i];
        }
        return x;
    }

    // --- state ---------------------------------------------------------------

    var weights = new Array(N_K).fill(0);
    var targetIdx = 0;
    var T = targetValues(TARGETS[0]);
    var normT2 = inner(T, T);
    var touched = false;

    // --- UI ------------------------------------------------------------------

    var canvas, ctx, sliders = [], readNum = [], statusEl, misfitBar, noiseBar,
        misfitVal, noiseVal, penaltySlider, penaltyLabel;

    function init() {
        var panel = document.getElementById("kernel-game");
        if (!panel) return;

        var controls = document.createElement("div");
        controls.className = "kg-controls";

        // target chooser
        var targWrap = document.createElement("div");
        targWrap.className = "kg-targets";
        var targLabel = document.createElement("span");
        targLabel.className = "kg-label";
        targLabel.textContent = "Target kernel:";
        targWrap.appendChild(targLabel);
        TARGETS.forEach(function (t, idx) {
            var b = document.createElement("button");
            b.type = "button";
            b.className = "kg-target-btn" + (idx === 0 ? " is-on" : "");
            b.textContent = t.label;
            b.addEventListener("click", function () {
                targetIdx = idx;
                T = targetValues(t);
                normT2 = inner(T, T);
                panel.querySelectorAll(".kg-target-btn").forEach(function (el, i2) {
                    el.classList.toggle("is-on", i2 === idx);
                });
                update();
            });
            targWrap.appendChild(b);
        });
        controls.appendChild(targWrap);

        // weight sliders
        var slWrap = document.createElement("div");
        slWrap.className = "kg-sliders";
        KERNEL_DEFS.forEach(function (def, i) {
            var row = document.createElement("div");
            row.className = "kg-slider-row";

            var lab = document.createElement("span");
            lab.className = "kg-slider-label";
            lab.innerHTML = '<span class="kg-dot" style="background:' + COLORS.kernels[i] + '"></span>x for ' + def.label;

            var s = document.createElement("input");
            s.type = "range";
            s.min = "-3"; s.max = "3"; s.step = "0.05"; s.value = "0";
            s.className = "kg-slider";
            s.setAttribute("aria-label", "Weight for kernel " + (i + 1));
            s.addEventListener("input", function () {
                weights[i] = parseFloat(s.value);
                touched = true;
                readNum[i].textContent = fmt(weights[i]);
                update();
            });

            var num = document.createElement("span");
            num.className = "kg-slider-value";
            num.textContent = "0.00";

            row.appendChild(lab);
            row.appendChild(s);
            row.appendChild(num);
            slWrap.appendChild(row);
            sliders.push(s);
            readNum.push(num);
        });
        controls.appendChild(slWrap);

        // buttons + penalty
        var btnWrap = document.createElement("div");
        btnWrap.className = "kg-buttons";

        var resetBtn = document.createElement("button");
        resetBtn.type = "button";
        resetBtn.className = "kg-btn";
        resetBtn.textContent = "Reset";
        resetBtn.addEventListener("click", function () {
            weights = new Array(N_K).fill(0);
            touched = false;
            syncSliders();
            update();
        });

        var solveBtn = document.createElement("button");
        solveBtn.type = "button";
        solveBtn.className = "kg-btn kg-btn-primary";
        solveBtn.textContent = "Let SOLA solve it";
        solveBtn.addEventListener("click", function () {
            var eta = penaltyValue();
            var A = GRAM.map(function (row, i) {
                return row.map(function (v, j) { return v + (i === j ? eta : 0); });
            });
            var b = K.map(function (k) { return inner(k, T); });
            var x = solveLinear(A, b);
            weights = x.map(function (v) { return Math.max(-3, Math.min(3, v)); });
            touched = true;
            syncSliders();
            update(true);
        });

        var penWrap = document.createElement("div");
        penWrap.className = "kg-penalty";
        penaltyLabel = document.createElement("span");
        penaltyLabel.className = "kg-label";
        penWrap.appendChild(penaltyLabel);
        penaltySlider = document.createElement("input");
        penaltySlider.type = "range";
        penaltySlider.min = "0"; penaltySlider.max = "100"; penaltySlider.step = "1";
        penaltySlider.value = "35";
        penaltySlider.className = "kg-slider";
        penaltySlider.setAttribute("aria-label", "Noise penalty for the SOLA solve");
        penaltySlider.addEventListener("input", function () { setPenaltyLabel(); });
        penWrap.appendChild(penaltySlider);
        setPenaltyLabel();

        btnWrap.appendChild(resetBtn);
        btnWrap.appendChild(solveBtn);
        btnWrap.appendChild(penWrap);
        controls.appendChild(btnWrap);

        // canvas
        canvas = document.createElement("canvas");
        canvas.className = "kg-canvas";
        ctx = canvas.getContext("2d");

        // scoreboard
        var score = document.createElement("div");
        score.className = "kg-score";
        var m = makeBar("Kernel mismatch", "kg-bar-misfit");
        misfitBar = m.fill; misfitVal = m.val;
        var nz = makeBar("Noise amplification", "kg-bar-noise");
        noiseBar = nz.fill; noiseVal = nz.val;
        score.appendChild(m.row);
        score.appendChild(nz.row);

        statusEl = document.createElement("div");
        statusEl.className = "kg-status";

        panel.appendChild(controls);
        panel.appendChild(canvas);
        panel.appendChild(score);
        panel.appendChild(statusEl);

        window.addEventListener("resize", function () { resize(); draw(); });
        resize();
        update();
    }

    function makeBar(label, cls) {
        var row = document.createElement("div");
        row.className = "kg-bar-row";
        var lab = document.createElement("span");
        lab.className = "kg-label";
        lab.textContent = label;
        var track = document.createElement("div");
        track.className = "kg-bar-track";
        var fill = document.createElement("div");
        fill.className = "kg-bar-fill " + cls;
        track.appendChild(fill);
        var val = document.createElement("span");
        val.className = "kg-bar-value";
        row.appendChild(lab);
        row.appendChild(track);
        row.appendChild(val);
        return { row: row, fill: fill, val: val };
    }

    function fmt(x) { return (x >= 0 ? "" : "−") + Math.abs(x).toFixed(2); }

    function penaltyValue() {
        // slider 0..100 -> eta in 10^-5 .. 10^0 (log scale)
        var t = parseFloat(penaltySlider.value) / 100;
        return Math.pow(10, -5 + 5 * t);
    }

    function setPenaltyLabel() {
        var e = penaltyValue();
        penaltyLabel.innerHTML = "Noise penalty η = 10<sup>" +
            (Math.log10(e)).toFixed(1) + "</sup>";
    }

    function syncSliders() {
        for (var i = 0; i < N_K; i++) {
            sliders[i].value = String(weights[i]);
            readNum[i].textContent = fmt(weights[i]);
        }
    }

    // --- scoring -------------------------------------------------------------

    function combined() {
        var A = new Array(N_GRID).fill(0);
        for (var i = 0; i < N_K; i++) {
            if (weights[i] === 0) continue;
            for (var j = 0; j < N_GRID; j++) A[j] += weights[i] * K[i][j];
        }
        return A;
    }

    new MutationObserver(function () {
        COLORS = PALETTES[themeName()];
        document.querySelectorAll("#kernel-game .kg-dot").forEach(function (dot, i) {
            dot.style.background = COLORS.kernels[i % COLORS.kernels.length];
        });
        update(false);
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

    function update(solved) {
        var A = combined();

        var diff = A.map(function (v, i) { return v - T[i]; });
        var misfit = Math.sqrt(inner(diff, diff) / normT2);       // relative L2 mismatch
        var noise = Math.sqrt(weights.reduce(function (s, x) { return s + x * x; }, 0));

        misfitBar.style.width = Math.min(100, misfit * 100) + "%";
        misfitVal.textContent = (misfit * 100).toFixed(0) + "%";
        noiseBar.style.width = Math.min(100, (noise / 5) * 100) + "%";
        noiseVal.textContent = "×" + noise.toFixed(2);

        setStatus(misfit, noise, solved);
        draw(A);
    }

    function setStatus(misfit, noise, solved) {
        var t = TARGETS[targetIdx];
        var msg;
        if (!touched) {
            msg = "Move the sliders to combine the kernels. Try to make the teal curve match the dashed target.";
        } else if (t.id === "deep" && misfit > 0.7) {
            msg = "No combination of these kernels can reach r ≈ 0.85 — every kernel is nearly zero there. " +
                  "The data are deaf to that region, and no weighting can fix it.";
        } else if (solved) {
            msg = "This is SOLA’s answer for this noise penalty. Lower the penalty for a better kernel match " +
                  "(at the price of noise); raise it for a calmer estimate that matches the target less well.";
        } else if (misfit < 0.10) {
            msg = "Excellent match — but look at the noise amplification. A perfect-looking kernel bought with " +
                  "huge weights is a noisy estimate. This tension is the whole game.";
        } else if (misfit < 0.30) {
            msg = "Getting close. Watch both bars: every improvement in the kernel match has a noise price.";
        } else {
            msg = "The teal curve is your resolving kernel — what your data combination actually averages. " +
                  "Red shading marks where it disagrees with the target.";
        }
        statusEl.textContent = msg;
    }

    // --- drawing -------------------------------------------------------------

    var W = 900, H = 380, PAD = { l: 46, r: 14, t: 12, b: 30 };

    function resize() {
        var cssW = canvas.clientWidth || 900;
        var dpr = window.devicePixelRatio || 1;
        W = cssW;
        H = Math.max(280, Math.round(cssW * 0.42));
        canvas.style.height = H + "px";
        canvas.width = Math.round(W * dpr);
        canvas.height = Math.round(H * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function draw(A) {
        if (!ctx) return;
        A = A || combined();

        var lo = -1.4, hi = 1.6;
        var mn = Math.min.apply(null, A.concat(T));
        var mx = Math.max.apply(null, A.concat(T));
        lo = Math.min(lo, mn - 0.2);
        hi = Math.max(hi, mx + 0.2);

        function X(r) { return PAD.l + r * (W - PAD.l - PAD.r); }
        function Y(v) { return PAD.t + (hi - v) / (hi - lo) * (H - PAD.t - PAD.b); }

        ctx.clearRect(0, 0, W, H);

        // grid + axes
        ctx.strokeStyle = COLORS.grid;
        ctx.lineWidth = 1;
        [0, 0.25, 0.5, 0.75, 1].forEach(function (r) {
            ctx.beginPath(); ctx.moveTo(X(r), PAD.t); ctx.lineTo(X(r), H - PAD.b); ctx.stroke();
        });
        [-1, 0, 1].forEach(function (v) {
            if (v < lo || v > hi) return;
            ctx.beginPath(); ctx.moveTo(PAD.l, Y(v)); ctx.lineTo(W - PAD.r, Y(v)); ctx.stroke();
        });
        ctx.strokeStyle = COLORS.axis;
        ctx.beginPath(); ctx.moveTo(PAD.l, Y(0)); ctx.lineTo(W - PAD.r, Y(0)); ctx.stroke();

        ctx.fillStyle = COLORS.font;
        ctx.font = "11px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        [0, 0.5, 1].forEach(function (r) { ctx.fillText(String(r), X(r), H - PAD.b + 16); });
        ctx.fillText("r", X(0.98), H - PAD.b + 16);
        ctx.textAlign = "right";
        [-1, 0, 1].forEach(function (v) {
            if (v < lo || v > hi) return;
            ctx.fillText(String(v), PAD.l - 6, Y(v) + 4);
        });

        // mismatch shading between A and T
        ctx.beginPath();
        ctx.moveTo(X(grid[0]), Y(A[0]));
        for (var i = 1; i < N_GRID; i++) ctx.lineTo(X(grid[i]), Y(A[i]));
        for (i = N_GRID - 1; i >= 0; i--) ctx.lineTo(X(grid[i]), Y(T[i]));
        ctx.closePath();
        ctx.fillStyle = COLORS.mismatch;
        ctx.fill();

        // faint individual weighted kernels
        for (var k = 0; k < N_K; k++) {
            if (weights[k] === 0) continue;
            ctx.beginPath();
            for (i = 0; i < N_GRID; i++) {
                var y = Y(weights[k] * K[k][i]);
                if (i === 0) ctx.moveTo(X(grid[i]), y); else ctx.lineTo(X(grid[i]), y);
            }
            ctx.strokeStyle = COLORS.kernels[k];
            ctx.globalAlpha = 0.35;
            ctx.lineWidth = 1.2;
            ctx.stroke();
            ctx.globalAlpha = 1;
        }

        // target (dashed)
        ctx.beginPath();
        ctx.setLineDash([7, 5]);
        for (i = 0; i < N_GRID; i++) {
            if (i === 0) ctx.moveTo(X(grid[i]), Y(T[i])); else ctx.lineTo(X(grid[i]), Y(T[i]));
        }
        ctx.strokeStyle = COLORS.target;
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.setLineDash([]);

        // combined kernel
        ctx.beginPath();
        for (i = 0; i < N_GRID; i++) {
            if (i === 0) ctx.moveTo(X(grid[i]), Y(A[i])); else ctx.lineTo(X(grid[i]), Y(A[i]));
        }
        ctx.strokeStyle = COLORS.resolving;
        ctx.lineWidth = 2.4;
        ctx.stroke();

        // legend
        ctx.font = "12px 'Segoe UI', sans-serif";
        ctx.textAlign = "left";
        var lx = PAD.l + 10, ly = PAD.t + 14;
        ctx.strokeStyle = COLORS.target; ctx.setLineDash([7, 5]); ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(lx, ly - 4); ctx.lineTo(lx + 26, ly - 4); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = COLORS.font;
        ctx.fillText("target T(r)", lx + 32, ly);
        ctx.strokeStyle = COLORS.resolving; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(lx, ly + 14); ctx.lineTo(lx + 26, ly + 14); ctx.stroke();
        ctx.fillText("your kernel Σ xᵢKᵢ(r)", lx + 32, ly + 18);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
