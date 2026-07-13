/*
 * cg-explorer.js — interactive descent panels for the series
 * "The Road to Conjugate Gradients".
 *
 * Panels attach to elements with class .cg-panel and a data-cg type:
 *
 *   data-cg="descent"    steepest descent on a 2-D quadratic; kappa slider,
 *                        click to place the start, Step / Run / Reset.
 *   data-cg="geometry"   the same engine plus an "A-geometry" view toggle
 *                        that redraws the landscape in stretched coordinates
 *                        (w = A^{1/2} v), where the contours become circles.
 *   data-cg="conjugate"  conjugate directions: the reader picks the FIRST
 *                        direction with a slider; the second is forced, and
 *                        the method finishes in two steps. Ghost GD path
 *                        for contrast.
 *   data-cg="race"       gradient descent vs conjugate gradients from the
 *                        same start, animated together, with a log error
 *                        chart underneath.
 *
 * Self-contained vanilla JS + canvas. Theme-aware: redraws when the
 * data-theme attribute flips (same pattern as kernel-game.js).
 */
(function () {
    "use strict";

    /* ------------------------------------------------------------------ */
    /* palettes                                                            */
    /* ------------------------------------------------------------------ */

    var PALETTES = {
        space: {
            contour: "rgba(255,255,255,0.15)",
            contourEm: "rgba(255,255,255,0.28)",
            axis: "rgba(255,255,255,0.22)",
            gd: "#e8a878",
            cg: "#4ecdc4",
            ghost: "rgba(232,168,120,0.55)",
            start: "#ef6f6c",
            sol: "#f4a259",
            downhill: "#9ed49e",
            text: "rgba(255,255,255,0.78)"
        },
        earth: {
            contour: "rgba(41,38,27,0.16)",
            contourEm: "rgba(41,38,27,0.30)",
            axis: "rgba(41,38,27,0.28)",
            gd: "#B0741B",
            cg: "#3E7D5E",
            ghost: "rgba(176,116,27,0.55)",
            start: "#C24E44",
            sol: "#8A611C",
            downhill: "#5C6D33",
            text: "rgba(41,38,27,0.82)"
        }
    };

    function themeName() {
        return document.documentElement.getAttribute("data-theme") === "earth" ? "earth" : "space";
    }

    /* ------------------------------------------------------------------ */
    /* the 2-D quadratic:  J(v) = (1/2)(Av, v),  solution at the origin    */
    /* A = R diag(kappa, 1) R^T with axes rotated by THETA                 */
    /* ------------------------------------------------------------------ */

    var THETA = -30 * Math.PI / 180;
    var COS = Math.cos(THETA), SIN = Math.sin(THETA);
    var V1 = [COS, SIN];       // eigenvector, eigenvalue kappa
    var V2 = [-SIN, COS];      // eigenvector, eigenvalue 1

    function applyA(kappa, x) {
        var y1 = V1[0] * x[0] + V1[1] * x[1];
        var y2 = V2[0] * x[0] + V2[1] * x[1];
        y1 *= kappa;
        return [V1[0] * y1 + V2[0] * y2, V1[1] * y1 + V2[1] * y2];
    }

    function applySqrtA(kappa, x) {
        var y1 = V1[0] * x[0] + V1[1] * x[1];
        var y2 = V2[0] * x[0] + V2[1] * x[1];
        y1 *= Math.sqrt(kappa);
        return [V1[0] * y1 + V2[0] * y2, V1[1] * y1 + V2[1] * y2];
    }

    function dot(a, b) { return a[0] * b[0] + a[1] * b[1]; }
    function sub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
    function add(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
    function scl(s, a) { return [s * a[0], s * a[1]]; }

    function energyErr(kappa, x) {   // ||x - 0||_A
        return Math.sqrt(Math.max(dot(x, applyA(kappa, x)), 0));
    }

    // worst-case start for steepest descent: equal energy-norm error
    // components along the two eigenvectors
    function worstStart(kappa, scale) {
        var x = add(scl(-1 / Math.sqrt(kappa), V1), V2);
        var n = Math.sqrt(dot(x, x));
        x = scl(scale / n, x);
        if (x[0] > 0) x = scl(-1, x);
        return x;
    }

    function gdStep(kappa, x) {
        var r = scl(-1, applyA(kappa, x));
        var rr = dot(r, r);
        if (rr < 1e-24) return null;
        var Ar = applyA(kappa, r);
        var alpha = rr / dot(r, Ar);
        return add(x, scl(alpha, r));
    }

    function gdPath(kappa, x0, relTol, maxit) {
        var xs = [x0.slice()];
        var e0 = energyErr(kappa, x0) || 1;
        var x = x0.slice();
        for (var k = 0; k < maxit; k++) {
            var nx = gdStep(kappa, x);
            if (!nx) break;
            x = nx;
            xs.push(x.slice());
            if (energyErr(kappa, x) / e0 < relTol) break;
        }
        return xs;
    }

    function cgPath(kappa, x0) {
        var xs = [x0.slice()];
        var x = x0.slice();
        var r = scl(-1, applyA(kappa, x));
        var p = r.slice();
        for (var k = 0; k < 2; k++) {
            var rr = dot(r, r);
            if (rr < 1e-24) break;
            var Ap = applyA(kappa, p);
            var alpha = rr / dot(p, Ap);
            x = add(x, scl(alpha, p));
            xs.push(x.slice());
            r = sub(r, scl(alpha, Ap));
            var beta = dot(r, r) / rr;
            p = add(r, scl(beta, p));
        }
        return xs;
    }

    // two exact line searches along A-conjugate directions, with an
    // ARBITRARY first direction p0; also returns (Ap0, p1) for the readout
    function conjugatePath(kappa, x0, p0) {
        var xs = [x0.slice()];
        var x = x0.slice(), p = p0.slice();
        var Ap0 = null, p1 = null;
        for (var k = 0; k < 2; k++) {
            var r = scl(-1, applyA(kappa, x));
            var Ap = applyA(kappa, p);
            var pAp = dot(p, Ap);
            if (Math.abs(pAp) < 1e-24) break;
            var alpha = dot(r, p) / pAp;
            x = add(x, scl(alpha, p));
            xs.push(x.slice());
            if (k === 0) {
                Ap0 = Ap;
                var rNew = scl(-1, applyA(kappa, x));
                var beta = -dot(rNew, Ap) / pAp;
                p = add(rNew, scl(beta, p));
                p1 = p.slice();
            }
        }
        return { xs: xs, conj: (Ap0 && p1) ? dot(Ap0, p1) : 0 };
    }

    /* ------------------------------------------------------------------ */
    /* panel construction                                                  */
    /* ------------------------------------------------------------------ */

    function el(tag, cls, html) {
        var e = document.createElement(tag);
        if (cls) e.className = cls;
        if (html !== undefined) e.innerHTML = html;
        return e;
    }

    function sliderRow(labelHtml, min, max, step, value) {
        var row = el("div", "cgx-slider-row");
        var lab = el("span", "cgx-slider-label", labelHtml);
        var input = document.createElement("input");
        input.type = "range";
        input.className = "cgx-slider";
        input.min = min; input.max = max; input.step = step; input.value = value;
        var val = el("span", "cgx-slider-value", String(value));
        row.appendChild(lab); row.appendChild(input); row.appendChild(val);
        return { row: row, input: input, val: val };
    }

    function button(label, primary) {
        var b = el("button", "cgx-btn" + (primary ? " cgx-btn-primary" : ""), label);
        b.type = "button";
        return b;
    }

    function initPanel(root) {
        var type = root.getAttribute("data-cg") || "descent";
        var C = PALETTES[themeName()];

        /* ---- state ---- */
        var kappa = parseFloat(root.getAttribute("data-kappa") || "12");
        var view = "original";              // or "stretched"  (geometry panel)
        var start = worstStart(kappa, 2.3);
        var path = [start.slice()];         // descent/geometry: GD iterates
        var timer = null;
        var angle = 155;                    // conjugate panel: first direction, degrees
        var showGhost = true;
        var racePos = 0;                    // race panel: animation cursor
        var raceGd = null, raceCg = null;

        /* ---- DOM ---- */
        var controls = el("div", "cgx-controls");
        var kap = sliderRow("stiffness &kappa;", 1, 40, 1, kappa);
        controls.appendChild(kap.row);

        var ang = null, ghostToggle = null;
        var btnStep = null, btnRun = null, btnGo = null;
        var btnReset = button("Reset");
        var viewWrap = null, btnOrig = null, btnStretch = null;

        if (type === "descent" || type === "geometry") {
            btnStep = button("Take one step", true);
            btnRun = button("Run");
            controls.appendChild(btnStep);
            controls.appendChild(btnRun);
        }
        if (type === "geometry") {
            viewWrap = el("div", "cgx-viewtoggle");
            btnOrig = el("button", "cgx-view-btn is-on", "our map");
            btnStretch = el("button", "cgx-view-btn", "A&rsquo;s map&ensp;w = A<sup>1/2</sup>v");
            btnOrig.type = btnStretch.type = "button";
            viewWrap.appendChild(btnOrig); viewWrap.appendChild(btnStretch);
            controls.appendChild(viewWrap);
        }
        if (type === "conjugate") {
            ang = sliderRow("first direction &ang;", 0, 179, 1, angle);
            controls.appendChild(ang.row);
            ghostToggle = el("label", "cgx-check",
                "<input type='checkbox' checked> show steepest descent for contrast");
            controls.appendChild(ghostToggle);
        }
        if (type === "race") {
            btnGo = button("Race", true);
            controls.appendChild(btnGo);
        }
        controls.appendChild(btnReset);
        root.appendChild(controls);

        var canvas = document.createElement("canvas");
        canvas.className = "cgx-canvas";
        root.appendChild(canvas);

        var chart = null;
        if (type === "race") {
            chart = document.createElement("canvas");
            chart.className = "cgx-chart";
            root.appendChild(chart);
        }

        var status = el("div", "cgx-status");
        root.appendChild(status);
        var hint = el("div", "cgx-hint", "tip: click anywhere on the map to move the starting point");
        root.appendChild(hint);

        /* ---- coordinate mapping ---- */
        var W = 0, H = 0, scale = 1, cx = 0, cy = 0;

        function layout() {
            var cssW = root.clientWidth - 2;
            if (cssW < 200) cssW = 200;
            var cssH = Math.round(cssW * (type === "race" ? 0.52 : 0.58));
            if (cssH > 460) cssH = 460;
            var dpr = window.devicePixelRatio || 1;
            canvas.style.width = cssW + "px";
            canvas.style.height = cssH + "px";
            canvas.width = Math.round(cssW * dpr);
            canvas.height = Math.round(cssH * dpr);
            canvas.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0);
            W = cssW; H = cssH;
            if (chart) {
                var chH = 170;
                chart.style.width = cssW + "px";
                chart.style.height = chH + "px";
                chart.width = Math.round(cssW * dpr);
                chart.height = Math.round(chH * dpr);
                chart.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0);
            }
            computeScale();
        }

        function mapPoint(x) {
            return (view === "stretched") ? applySqrtA(kappa, x) : x;
        }

        function computeScale() {
            // world half-extents that must stay visible (start point and
            // paths included, so nothing ever walks off the canvas)
            var nx = 3.0, ny = 2.1;
            var pts = currentPoints();
            for (var i = 0; i < pts.length; i++) {
                var p = (view === "stretched") ? applySqrtA(kappa, pts[i]) : pts[i];
                nx = Math.max(nx, Math.abs(p[0]) * 1.12);
                ny = Math.max(ny, Math.abs(p[1]) * 1.12);
            }
            if (view === "stretched") { nx = ny = Math.max(nx, ny); }
            cx = W / 2; cy = H / 2;
            scale = Math.min(W / (2 * nx), H / (2 * ny)) * 0.96;
        }

        function currentPoints() {
            var pts = [start];
            if (type === "conjugate") {
                var cp = conjugatePath(kappa, start, dirVec());
                pts = cp.xs;
            } else if (type === "race" && raceGd) {
                pts = raceGd.concat(raceCg);
            } else {
                pts = path;
            }
            return pts;
        }

        function toScreen(x) {
            var p = mapPoint(x);
            return [cx + p[0] * scale, cy - p[1] * scale];
        }

        function fromScreen(sx, sy) {
            var wx = (sx - cx) / scale, wy = (cy - sy) / scale;
            if (view === "stretched") {
                // invert w = A^{1/2} v
                var y1 = V1[0] * wx + V1[1] * wy;
                var y2 = V2[0] * wx + V2[1] * wy;
                y1 /= Math.sqrt(kappa);
                return [V1[0] * y1 + V2[0] * y2, V1[1] * y1 + V2[1] * y2];
            }
            return [wx, wy];
        }

        function dirVec() {
            var a = angle * Math.PI / 180;
            return [Math.cos(a), Math.sin(a)];
        }

        /* ---- drawing ---- */

        function drawContours(ctx) {
            // J at the visible corner sets the outermost level
            var corner = fromScreen(0, 0);
            var jmax = 0.5 * dot(corner, applyA(kappa, corner));
            var n = 9;
            for (var i = 0; i < n; i++) {
                var c = jmax * Math.pow(0.5, i);
                var a1 = Math.sqrt(2 * c / kappa);   // semi-axis along V1
                var a2 = Math.sqrt(2 * c);           // semi-axis along V2
                ctx.beginPath();
                for (var t = 0; t <= 64; t++) {
                    var ph = t / 64 * 2 * Math.PI;
                    var x = add(scl(a1 * Math.cos(ph), V1), scl(a2 * Math.sin(ph), V2));
                    var s = toScreen(x);
                    if (t === 0) ctx.moveTo(s[0], s[1]); else ctx.lineTo(s[0], s[1]);
                }
                ctx.strokeStyle = (i % 3 === 0) ? C.contourEm : C.contour;
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }

        function drawAxes(ctx) {
            ctx.strokeStyle = C.axis;
            ctx.lineWidth = 1;
            ctx.setLineDash([3, 5]);
            ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, H); ctx.stroke();
            ctx.setLineDash([]);
        }

        function drawPath(ctx, pts, color, lw, dots) {
            if (pts.length < 1) return;
            ctx.strokeStyle = color;
            ctx.lineWidth = lw;
            ctx.lineJoin = "round";
            ctx.beginPath();
            for (var i = 0; i < pts.length; i++) {
                var s = toScreen(pts[i]);
                if (i === 0) ctx.moveTo(s[0], s[1]); else ctx.lineTo(s[0], s[1]);
            }
            ctx.stroke();
            if (dots) {
                ctx.fillStyle = color;
                for (var j = 0; j < pts.length; j++) {
                    var q = toScreen(pts[j]);
                    ctx.beginPath();
                    ctx.arc(q[0], q[1], j === 0 ? 5 : 3, 0, 2 * Math.PI);
                    ctx.fill();
                }
            }
        }

        function drawStar(ctx, sx, sy, R, color) {
            ctx.fillStyle = color;
            ctx.beginPath();
            for (var i = 0; i < 10; i++) {
                var rr = (i % 2 === 0) ? R : R * 0.45;
                var a = -Math.PI / 2 + i * Math.PI / 5;
                var px = sx + rr * Math.cos(a), py = sy + rr * Math.sin(a);
                if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.fill();
        }

        function draw() {
            computeScale();
            var ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, W, H);
            drawAxes(ctx);
            drawContours(ctx);

            if (type === "descent" || type === "geometry") {
                if (view === "stretched") {
                    // in A's geometry, downhill from the start points at the answer
                    var s0 = toScreen(start);
                    ctx.strokeStyle = C.downhill;
                    ctx.setLineDash([6, 6]);
                    ctx.lineWidth = 1.6;
                    ctx.beginPath(); ctx.moveTo(s0[0], s0[1]); ctx.lineTo(cx, cy); ctx.stroke();
                    ctx.setLineDash([]);
                    ctx.fillStyle = C.downhill;
                    ctx.font = "12px system-ui, sans-serif";
                    ctx.fillText("straight downhill (in this geometry)", Math.min(s0[0], cx) + 8, (s0[1] + cy) / 2);
                }
                drawPath(ctx, path, C.gd, 2, true);
            } else if (type === "conjugate") {
                var cp = conjugatePath(kappa, start, dirVec());
                if (showGhost) drawPath(ctx, gdPath(kappa, start, 1e-4, 60), C.ghost, 1.2, false);
                drawPath(ctx, cp.xs, C.cg, 2.6, true);
                // the chosen first direction, drawn through the start
                var d = dirVec();
                var a0 = toScreen(add(start, scl(0.8, d)));
                var b0 = toScreen(add(start, scl(-0.8, d)));
                ctx.strokeStyle = C.text;
                ctx.setLineDash([2, 4]);
                ctx.lineWidth = 1;
                ctx.beginPath(); ctx.moveTo(a0[0], a0[1]); ctx.lineTo(b0[0], b0[1]); ctx.stroke();
                ctx.setLineDash([]);
            } else if (type === "race") {
                if (raceGd) {
                    drawPath(ctx, raceGd.slice(0, racePos + 1), C.gd, 1.8, true);
                    drawPath(ctx, raceCg.slice(0, Math.min(racePos, raceCg.length - 1) + 1), C.cg, 2.4, true);
                }
            }

            var st = toScreen(start);
            ctx.fillStyle = C.start;
            ctx.beginPath(); ctx.arc(st[0], st[1], 6, 0, 2 * Math.PI); ctx.fill();
            drawStar(ctx, cx, cy, 9, C.sol);

            if (type === "race") drawChart();
        }

        function drawChart() {
            var ctx = chart.getContext("2d");
            var cw = parseFloat(chart.style.width), ch = parseFloat(chart.style.height);
            ctx.clearRect(0, 0, cw, ch);
            if (!raceGd) return;

            var padL = 46, padR = 12, padT = 18, padB = 26;
            var e0 = energyErr(kappa, raceGd[0]) || 1;
            var maxK = Math.max(raceGd.length - 1, 8);
            var logMin = -8;

            function px(k) { return padL + (cw - padL - padR) * k / maxK; }
            function py(le) { return padT + (ch - padT - padB) * (0 - le) / (0 - logMin); }

            ctx.strokeStyle = C.axis;
            ctx.lineWidth = 1;
            ctx.strokeRect(padL, padT, cw - padL - padR, ch - padT - padB);
            ctx.fillStyle = C.text;
            ctx.font = "11px system-ui, sans-serif";
            for (var d = 0; d >= logMin; d -= 2) {
                var yy = py(d);
                ctx.fillText("1e" + d, 8, yy + 4);
                ctx.strokeStyle = C.contour;
                ctx.beginPath(); ctx.moveTo(padL, yy); ctx.lineTo(cw - padR, yy); ctx.stroke();
            }
            ctx.fillText("iteration", cw / 2 - 20, ch - 8);

            function curve(pts, upTo, color) {
                ctx.strokeStyle = color;
                ctx.lineWidth = 2;
                ctx.beginPath();
                var started = false;
                for (var k = 0; k <= Math.min(upTo, pts.length - 1); k++) {
                    var e = energyErr(kappa, pts[k]) / e0;
                    var le = Math.max(Math.log(e + 1e-300) / Math.LN10, logMin);
                    var X = px(k), Y = py(le);
                    if (!started) { ctx.moveTo(X, Y); started = true; } else ctx.lineTo(X, Y);
                }
                ctx.stroke();
            }
            curve(raceGd, racePos, C.gd);
            curve(raceCg, racePos, C.cg);

            ctx.fillStyle = C.gd; ctx.fillText("gradient descent", padL + 10, padT + 14);
            ctx.fillStyle = C.cg; ctx.fillText("conjugate gradients", padL + 130, padT + 14);
        }

        /* ---- status ---- */

        function fmt(x) {
            if (x === 0) return "0";
            var e = Math.floor(Math.log(Math.abs(x)) / Math.LN10);
            if (e >= -2 && e <= 2) return x.toFixed(3);
            return x.toExponential(1).replace("e", " · 10^");
        }

        function updateStatus() {
            var e0 = energyErr(kappa, start) || 1;
            if (type === "descent" || type === "geometry") {
                var k = path.length - 1;
                var rel = energyErr(kappa, path[k]) / e0;
                if (k === 0) {
                    status.innerHTML = "Ready. The dot is u<sub>0</sub>; the star is the solution. " +
                        "Take a step — the method walks perpendicular to the contour it stands on.";
                } else if (rel < 1e-6) {
                    status.innerHTML = "Converged: " + k + " steps to bring the energy error below 10<sup>−6</sup> " +
                        "of where it started (&kappa; = " + kappa + ").";
                } else {
                    status.innerHTML = k + (k === 1 ? " step" : " steps") + " taken — relative energy error " +
                        "<strong>" + fmt(rel) + "</strong>. " +
                        (kappa >= 15 ? "Notice the staircase: every new direction is Euclidean-perpendicular to the last." :
                            "Now raise &kappa; and watch the valley narrow.");
                }
            } else if (type === "conjugate") {
                var cp = conjugatePath(kappa, start, dirVec());
                var relc = energyErr(kappa, cp.xs[cp.xs.length - 1]) / e0;
                status.innerHTML = "Two steps, done (final relative error " + fmt(relc) + "). " +
                    "The second direction obeyed (Ap<sub>0</sub>, p<sub>1</sub>) = " + fmt(cp.conj) +
                    " — A-perpendicular to machine precision, whatever first direction you chose.";
            } else if (type === "race") {
                if (!raceGd) {
                    status.innerHTML = "Press <strong>Race</strong>: both methods start from the same point, " +
                        "one exact line search per turn.";
                } else {
                    var kg = raceGd.length - 1;
                    var done = racePos >= kg;
                    status.innerHTML = (done ? "Final score — " : "") +
                        "gradient descent: " + Math.min(racePos, kg) + " steps; " +
                        "conjugate gradients: " + Math.min(racePos, raceCg.length - 1) +
                        " (it cannot need more than 2 here: the space is 2-dimensional)." +
                        (done ? " Raise &kappa; and race again — one score changes, the other does not." : "");
                }
            }
        }

        /* ---- interactions ---- */

        function stopTimer() {
            if (timer) { clearInterval(timer); timer = null; }
            if (btnRun) btnRun.textContent = "Run";
        }

        function resetPath() {
            stopTimer();
            path = [start.slice()];
            racePos = 0;
            raceGd = raceCg = null;
            draw(); updateStatus();
        }

        kap.input.addEventListener("input", function () {
            kappa = parseFloat(this.value);
            kap.val.textContent = this.value;
            resetPath();
        });

        if (btnStep) btnStep.addEventListener("click", function () {
            stopTimer();
            var nx = gdStep(kappa, path[path.length - 1]);
            if (nx) path.push(nx);
            draw(); updateStatus();
        });

        if (btnRun) btnRun.addEventListener("click", function () {
            if (timer) { stopTimer(); return; }
            btnRun.textContent = "Pause";
            timer = setInterval(function () {
                var e0 = energyErr(kappa, start) || 1;
                var x = path[path.length - 1];
                if (path.length > 300 || energyErr(kappa, x) / e0 < 1e-6) { stopTimer(); updateStatus(); return; }
                var nx = gdStep(kappa, x);
                if (!nx) { stopTimer(); return; }
                path.push(nx);
                draw(); updateStatus();
            }, 140);
        });

        if (btnGo) btnGo.addEventListener("click", function () {
            stopTimer();
            raceGd = gdPath(kappa, start, 1e-8, 120);
            raceCg = cgPath(kappa, start);
            racePos = 0;
            timer = setInterval(function () {
                // linger on the first steps, then accelerate through the tail
                racePos += (racePos < 10 ? 1 : 4);
                if (racePos >= raceGd.length - 1) { racePos = raceGd.length - 1; stopTimer(); }
                draw(); updateStatus();
            }, 300);
            draw(); updateStatus();
        });

        btnReset.addEventListener("click", function () {
            start = worstStart(kappa, 2.3);
            resetPath();
        });

        if (btnOrig) {
            btnOrig.addEventListener("click", function () {
                view = "original";
                btnOrig.classList.add("is-on"); btnStretch.classList.remove("is-on");
                draw(); updateStatus();
            });
            btnStretch.addEventListener("click", function () {
                view = "stretched";
                btnStretch.classList.add("is-on"); btnOrig.classList.remove("is-on");
                draw(); updateStatus();
            });
        }

        if (ang) ang.input.addEventListener("input", function () {
            angle = parseFloat(this.value);
            ang.val.textContent = this.value + "°";
            draw(); updateStatus();
        });

        if (ghostToggle) ghostToggle.querySelector("input").addEventListener("change", function () {
            showGhost = this.checked;
            draw();
        });

        canvas.addEventListener("click", function (ev) {
            var rect = canvas.getBoundingClientRect();
            var p = fromScreen(ev.clientX - rect.left, ev.clientY - rect.top);
            if (Math.abs(p[0]) < 0.05 && Math.abs(p[1]) < 0.05) return;
            start = p;
            resetPath();
        });

        window.addEventListener("resize", function () { layout(); draw(); });

        new MutationObserver(function () {
            C = PALETTES[themeName()];
            draw();
        }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

        /* ---- go ---- */
        layout();
        draw();
        updateStatus();
        if (ang) ang.val.textContent = angle + "°";
    }

    function init() {
        var panels = document.querySelectorAll(".cg-panel[data-cg]");
        for (var i = 0; i < panels.length; i++) initPanel(panels[i]);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
