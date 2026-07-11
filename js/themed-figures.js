/*
 * themed-figures.js — swap note figures between space and earth variants.
 *
 * Figures are generated twice by figure_generation/ (FIG_MODE=earth writes
 * *_earth.png next to the space original). Any <img data-themed> is swapped
 * to its _earth variant while <html data-theme="earth"> is active, live on
 * toggle via a MutationObserver. Sweep-panel images (f6e/f6f) are NOT
 * swapped — they keep a dark instrument backdrop in both themes.
 */
(function () {
    "use strict";

    function variant(src, earth) {
        var m = src.match(/^(.*?)(_earth)?(\.png)([?#].*)?$/);
        if (!m) return src;
        return m[1] + (earth ? "_earth" : "") + m[3] + (m[4] || "");
    }

    function apply() {
        var earth = document.documentElement.getAttribute("data-theme") === "earth";
        document.querySelectorAll("img[data-themed]").forEach(function (img) {
            var next = variant(img.getAttribute("src"), earth);
            if (next !== img.getAttribute("src")) img.setAttribute("src", next);
        });
    }

    new MutationObserver(apply).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["data-theme"]
    });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", apply);
    } else {
        apply();
    }
})();
