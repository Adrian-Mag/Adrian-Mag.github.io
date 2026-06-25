(function () {
    "use strict";

    var PANEL_ID = "discretization-panel";
    var DATA_SRC = null;
    var data = null;
    var currentN = 30;
    var ns = [];
    var plotDiv = null;
    var summaryDiv = null;
    var slider = null;
    var sliderLabel = null;

    var COLORS = {
        trueModel: "#f4a259",
        naive: "#ef6f6c",
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

        var staticImg = panel.querySelector("img");
        var staticCap = panel.querySelector("figcaption");
        if (staticImg) staticImg.style.display = "none";

        panel.insertBefore(plotContainer, staticCap);

        fetch(DATA_SRC)
            .then(function (r) { return r.json(); })
            .then(function (d) {
                data = d;
                ns = data.ns;
                slider.max = String(ns.length - 1);
                currentN = ns[Math.floor(ns.length / 2)];
                slider.value = String(Math.floor(ns.length / 2));
                sliderLabel.textContent = "N = " + currentN;
                renderAll();
            })
            .catch(function () {
                if (staticImg) staticImg.style.display = "";
                if (plotContainer) plotContainer.style.display = "none";
            });
    }

    function buildControls(panel) {
        var controls = document.createElement("div");
        controls.className = "tfdl-panel-controls";

        var sliderWrap = document.createElement("div");
        sliderWrap.className = "tfdl-slider-wrap";

        sliderLabel = document.createElement("span");
        sliderLabel.className = "tfdl-slider-label";
        sliderLabel.textContent = "N = 30";

        slider = document.createElement("input");
        slider.type = "range";
        slider.className = "tfdl-slider";
        slider.min = "0";
        slider.max = "8";  // placeholder; updated after data loads
        slider.step = "1";
        slider.value = "4";
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

        var figcap = panel.querySelector("figcaption");
        panel.insertBefore(controls, figcap);
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
            line: { color: COLORS.trueModel, width: 2.5, dash: "dash" },
            hoverinfo: "x+y"
        });

        if (data.naive[key]) {
            var nm = data.naive[key];

            for (var i = 0; i < nm.samples.length; i++) {
                traces.push({
                    x: x, y: nm.samples[i],
                    mode: "lines",
                    name: "sample " + (i + 1),
                    line: { color: COLORS.naive, width: 1 },
                    opacity: 0.25,
                    showlegend: false,
                    hoverinfo: "skip"
                });
            }

            traces.push({
                x: x, y: nm.mean,
                mode: "lines",
                name: "Posterior mean",
                line: { color: COLORS.naive, width: 2.5 },
                hoverinfo: "x+y"
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

        var traces = [{
            x: s.ns, y: s.naive_rms_std,
            mode: "lines+markers",
            name: "RMS posterior std",
            line: { color: COLORS.naive, width: 2 },
            marker: { size: 7, color: COLORS.naive },
            hoverinfo: "x+y"
        }];

        var maxY = Math.max.apply(null, s.naive_rms_std);

        traces.push({
            x: [currentN, currentN],
            y: [0, maxY * 1.1],
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
                dtick: 5
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
