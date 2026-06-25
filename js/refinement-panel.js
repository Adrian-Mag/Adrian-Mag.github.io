(function () {
    "use strict";

    var PANEL_ID = "refinement-panel";
    var DATA_SRC = null;
    var data = null;
    var currentN = 10;
    var showNaive = true;
    var showBessel = true;
    var ns = [];
    var plotDiv = null;
    var summaryDiv = null;
    var slider = null;
    var sliderLabel = null;
    var toggleNaive = null;
    var toggleBessel = null;

    // Dark-theme color palette (matches figure style.py)
    var COLORS = {
        trueModel: "#e0e0e0",
        naive: "#ff6b6b",
        bessel: "#4ecdc4",
        grid: "rgba(255,255,255,0.08)",
        paper: "rgba(0,0,0,0)",
        font: "rgba(255,255,255,0.75)"
    };

    function init() {
        var panel = document.getElementById(PANEL_ID);
        if (!panel) return;
        DATA_SRC = panel.getAttribute("data-src");
        if (!DATA_SRC) return;

        if (typeof window.Plotly === "undefined") {
            // Plotly not loaded — static fallback image stays in place
            return;
        }

        buildControls(panel);
        plotDiv = document.createElement("div");
        plotDiv.className = "tfdl-plotly-main";
        summaryDiv = document.createElement("div");
        summaryDiv.className = "tfdl-plotly-summary";

        var plotContainer = document.createElement("div");
        plotContainer.className = "tfdl-plotly-container";
        plotContainer.appendChild(plotDiv);
        plotContainer.appendChild(summaryDiv);

        // Replace the static <img> with the interactive container
        var staticImg = panel.querySelector("img");
        var staticCap = panel.querySelector("figcaption");
        if (staticImg) staticImg.style.display = "none";

        panel.insertBefore(plotContainer, staticCap);

        fetch(DATA_SRC)
            .then(function (r) { return r.json(); })
            .then(function (d) {
                data = d;
                ns = data.ns;
                currentN = ns[0];
                renderAll();
            })
            .catch(function () {
                // Fetch failed — restore static image
                if (staticImg) staticImg.style.display = "";
                if (plotContainer) plotContainer.style.display = "none";
            });
    }

    function buildControls(panel) {
        var controls = document.createElement("div");
        controls.className = "tfdl-panel-controls";

        // Slider
        var sliderWrap = document.createElement("div");
        sliderWrap.className = "tfdl-slider-wrap";

        sliderLabel = document.createElement("span");
        sliderLabel.className = "tfdl-slider-label";
        sliderLabel.textContent = "N = 10";

        slider = document.createElement("input");
        slider.type = "range";
        slider.className = "tfdl-slider";
        slider.min = "0";
        slider.max = "4";
        slider.step = "1";
        slider.value = "0";
        slider.setAttribute("aria-label", "Resolution N slider");

        slider.addEventListener("input", function () {
            var idx = parseInt(slider.value, 10);
            currentN = ns[idx];
            sliderLabel.textContent = "N = " + currentN;
            renderAll();
        });

        sliderWrap.appendChild(sliderLabel);
        sliderWrap.appendChild(slider);
        controls.appendChild(sliderWrap);

        // Toggles
        var toggleWrap = document.createElement("div");
        toggleWrap.className = "tfdl-toggle-wrap";

        toggleNaive = makeToggle("naive", "Naive σ²I", true, COLORS.naive, function (on) {
            showNaive = on;
            renderAll();
        });
        toggleBessel = makeToggle("bessel", "Bessel (proper)", true, COLORS.bessel, function (on) {
            showBessel = on;
            renderAll();
        });

        toggleWrap.appendChild(toggleNaive.el);
        toggleWrap.appendChild(toggleBessel.el);
        controls.appendChild(toggleWrap);

        // Insert controls before the figure content
        var figcap = panel.querySelector("figcaption");
        panel.insertBefore(controls, figcap);
    }

    function makeToggle(id, label, defaultOn, color, onChange) {
        var btn = document.createElement("button");
        btn.className = "tfdl-toggle" + (defaultOn ? " is-on" : "");
        btn.setAttribute("type", "button");
        btn.setAttribute("aria-pressed", defaultOn ? "true" : "false");
        btn.setAttribute("data-color", color);
        btn.innerHTML =
            '<span class="tfdl-toggle-dot" style="background:' + color + '"></span>' +
            '<span class="tfdl-toggle-text">' + label + "</span>";

        btn.addEventListener("click", function () {
            var on = btn.classList.toggle("is-on");
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            onChange(on);
        });

        return { el: btn, btn: btn };
    }

    function renderAll() {
        renderMain();
        renderSummary();
    }

    function renderMain() {
        if (!data || !plotDiv) return;
        var x = data.x;
        var trueY = data.true;
        var key = String(currentN);
        var traces = [];

        traces.push({
            x: x, y: trueY,
            mode: "lines",
            name: "True model",
            line: { color: COLORS.trueModel, width: 2, dash: "dash" },
            hoverinfo: "x+y"
        });

        if (showNaive && data.naive[key]) {
            var nm = data.naive[key];
            traces.push({
                x: x, y: nm.mean,
                mode: "lines",
                name: "Naive mean",
                line: { color: COLORS.naive, width: 2 },
                hoverinfo: "x+y"
            });
            traces.push({
                x: x.concat(x.slice().reverse()),
                y: nm.mean.map(function (m, i) { return m + nm.std[i]; })
                    .concat(nm.mean.map(function (m, i) { return m - nm.std[i]; }).reverse()),
                fill: "toself",
                fillcolor: "rgba(255,107,107,0.15)",
                line: { color: "transparent", width: 0 },
                name: "Naive ±1σ",
                showlegend: false,
                hoverinfo: "skip"
            });
        }

        if (showBessel && data.bessel[key]) {
            var bm = data.bessel[key];
            traces.push({
                x: x, y: bm.mean,
                mode: "lines",
                name: "Bessel mean",
                line: { color: COLORS.bessel, width: 2 },
                hoverinfo: "x+y"
            });
            traces.push({
                x: x.concat(x.slice().reverse()),
                y: bm.mean.map(function (m, i) { return m + bm.std[i]; })
                    .concat(bm.mean.map(function (m, i) { return m - bm.std[i]; }).reverse()),
                fill: "toself",
                fillcolor: "rgba(78,205,196,0.15)",
                line: { color: "transparent", width: 0 },
                name: "Bessel ±1σ",
                showlegend: false,
                hoverinfo: "skip"
            });
        }

        var layout = {
            paper_bgcolor: COLORS.paper,
            plot_bgcolor: COLORS.paper,
            font: { color: COLORS.font, size: 12, family: "Segoe UI, sans-serif" },
            margin: { l: 50, r: 20, t: 10, b: 40 },
            xaxis: {
                title: "z",
                gridcolor: COLORS.grid,
                zerolinecolor: COLORS.grid,
                range: [0, 1]
            },
            yaxis: {
                title: "m(z)",
                gridcolor: COLORS.grid,
                zerolinecolor: COLORS.grid
            },
            showlegend: true,
            legend: {
                x: 0.02, y: 0.98,
                bgcolor: "rgba(58,62,67,0.6)",
                bordercolor: "rgba(103,145,190,0.2)",
                borderwidth: 1,
                font: { size: 11 }
            },
            transition: { duration: 200, easing: "cubic-in-out" }
        };

        Plotly.react(plotDiv, traces, layout, {
            responsive: true,
            displayModeBar: false
        });
    }

    function renderSummary() {
        if (!data || !summaryDiv) return;
        var s = data.summary;
        var currentIdx = ns.indexOf(currentN);

        var traces = [];

        if (showNaive) {
            traces.push({
                x: s.ns, y: s.naive_rms_std,
                mode: "lines+markers",
                name: "Naive RMS std",
                line: { color: COLORS.naive, width: 2 },
                marker: { size: 7, color: COLORS.naive },
                hoverinfo: "x+y"
            });
        }

        if (showBessel) {
            traces.push({
                x: s.ns, y: s.bessel_rms_std,
                mode: "lines+markers",
                name: "Bessel RMS std",
                line: { color: COLORS.bessel, width: 2 },
                marker: { size: 7, color: COLORS.bessel },
                hoverinfo: "x+y"
            });
        }

        // Vertical line at current N
        traces.push({
            x: [currentN, currentN],
            y: [0, Math.max(
                showNaive ? Math.max.apply(null, s.naive_rms_std) : 0,
                showBessel ? Math.max.apply(null, s.bessel_rms_std) : 0
            ) * 1.1],
            mode: "lines",
            line: { color: "rgba(255,255,255,0.25)", width: 1.5, dash: "dot" },
            showlegend: false,
            hoverinfo: "skip"
        });

        var layout = {
            paper_bgcolor: COLORS.paper,
            plot_bgcolor: COLORS.paper,
            font: { color: COLORS.font, size: 11, family: "Segoe UI, sans-serif" },
            margin: { l: 50, r: 20, t: 10, b: 35 },
            xaxis: {
                title: "N (resolution)",
                gridcolor: COLORS.grid,
                dtick: 10
            },
            yaxis: {
                title: "RMS posterior std",
                gridcolor: COLORS.grid
            },
            showlegend: false,
            transition: { duration: 200, easing: "cubic-in-out" }
        };

        Plotly.react(summaryDiv, traces, layout, {
            responsive: true,
            displayModeBar: false
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
