/*
 * ai-assist.js — "Read with AI" toolbar for the research notes pages.
 *
 * Injects a small toolbar below the page header (or part-nav) with:
 *   1. "Copy for AI" — copies the article text (LaTeX intact) plus a
 *      context preamble to the clipboard, ready to paste into any LLM.
 *   2. "Open in ChatGPT" — pre-filled prompt pointing at this page and
 *      the series reading companion.
 *   3. "AI companion" — link to the plain-text reading companion for
 *      the series (narrative arc, notation, guardrails).
 *
 * The copy payload is extracted from the page's own raw HTML (fetched
 * fresh), so the original LaTeX source survives MathJax rendering.
 *
 * Series are auto-detected from the URL path. No per-page configuration.
 */
(function () {
    "use strict";

    var SITE_ROOT = "https://adrian-mag.github.io";

    var SERIES = {
        "sola": {
            title: "My Take on SOLA",
            landing: "my-take-on-sola.html",
            companion: "ai-companion.txt",
            intent: "These notes build the SOLA (Subtractive Optimally Localized Averages) method from scratch and then examine critically what its outputs mean. The central claim: SOLA estimates properties seen through RESOLVING kernels, not the desired TARGET kernels, and without model-side prior information the gap between the two is unbounded. Do not present SOLA's outputs as estimates of the true target properties, and do not present propagated data noise as posterior uncertainty.",
            pages: [
                "my-take-on-sola.html",
                "act-1.html", "act-2.html", "act-3.html", "act-4.html",
                "act-5.html", "act-6.html", "act-7.html", "act-8.html",
                "act-9.html", "act-10.html",
                "summary.html"
            ]
        },
        "think-first": {
            title: "Think First, Discretize Later",
            landing: "think-first-discretize-later.html",
            companion: "ai-companion.txt",
            intent: "These notes argue that a linear inverse problem must be formulated in function space (model space, geometry, adjoint, prior measure) BEFORE discretizing. The naive discretize-first workflow produces mesh-dependent posteriors that do not converge under refinement. Do not present the naive discretized posterior as a harmless default.",
            pages: [
                "think-first-discretize-later.html",
                "act-1.html", "act-2.html", "act-3.html", "act-4.html",
                "act-5.html", "act-6.html", "act-7.html", "act-8.html",
                "summary.html"
            ]
        },
        "bayes": {
            title: "Bayes, Measure-Theoretically",
            landing: "bayes-measure-theoretically.html",
            companion: "ai-companion.txt",
            intent: "These notes develop Bayesian inference twice on the same finite toy problem: first with elementary joint-table probability, then measure-theoretically (measurable spaces, kernels, joint measure, disintegration). The point is that the measure-theoretic machinery computes the SAME answer and is the correct language for infinite-dimensional generalization. Keep the two formulations in strict parallel; do not substitute density-based shortcuts that fail in infinite dimensions.",
            pages: [
                "bayes-measure-theoretically.html",
                "part-1.html", "part-2.html",
                "part-3a.html", "part-3b.html", "part-3c.html",
                "part-3d.html", "part-3e.html", "part-3f.html",
                "part-4.html"
            ]
        },
        "frequentist": {
            title: "Bayesian and Frequentist Inference",
            landing: "bayesian-frequentist.html",
            companion: "ai-companion.txt",
            intent: "These notes contrast the Bayesian and frequentist paths for the same observation equation, being precise about what each does and does not claim. Frequentist confidence sets make PRE-observation coverage statements about a procedure; they are not post-observation probability statements about the truth. Do not blur that distinction.",
            pages: [
                "bayesian-frequentist.html",
                "part-1.html", "part-2.html", "part-3.html",
                "part-4.html", "part-5.html"
            ]
        }
    };

    function detectSeries() {
        var parts = window.location.pathname.split("/");
        for (var i = parts.length - 2; i >= 0; i--) {
            if (SERIES.hasOwnProperty(parts[i])) {
                return SERIES[parts[i]];
            }
        }
        return null;
    }

    var series = detectSeries();
    if (!series) { return; }

    var pageUrl = SITE_ROOT + window.location.pathname;
    var dirUrl = pageUrl.substring(0, pageUrl.lastIndexOf("/") + 1);
    var companionUrl = dirUrl + series.companion;
    var landingUrl = dirUrl + series.landing;
    var pageTitle = document.title;

    /* ------------------------------------------------------------------ */
    /* Styles                                                              */
    /* ------------------------------------------------------------------ */

    var css = [
        ".ai-assist-bar {",
        "  display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem;",
        "  max-width: 900px; margin: 0.8rem auto 0 auto; padding: 0 1.2rem;",
        "  justify-content: flex-end; font-size: 0.82rem;",
        "}",
        ".ai-assist-label {",
        "  color: var(--muted); margin-right: 0.2rem;",
        "}",
        ".ai-assist-btn {",
        "  display: inline-flex; align-items: center; gap: 0.35em;",
        "  padding: 0.28em 0.85em; border-radius: 999px;",
        "  background: rgba(103,145,190,0.13); color: var(--accent-bright);",
        "  border: 1px solid rgba(103,145,190,0.35);",
        "  cursor: pointer; text-decoration: none; font-size: inherit;",
        "  font-family: inherit; line-height: 1.4; white-space: nowrap;",
        "  transition: background 0.15s, color 0.15s;",
        "}",
        ".ai-assist-btn:hover {",
        "  background: rgba(103,145,190,0.28); color: var(--text);",
        "}",
        ".ai-assist-btn.copied {",
        "  background: rgba(110,190,130,0.2); color: var(--sem-green-text);",
        "  border-color: rgba(110,190,130,0.4);",
        "}",
        "@media (max-width: 700px) {",
        "  .ai-assist-bar { justify-content: flex-start; }",
        "}"
    ].join("\n");

    var styleEl = document.createElement("style");
    styleEl.textContent = css;
    document.head.appendChild(styleEl);

    /* ------------------------------------------------------------------ */
    /* Payload construction                                                */
    /* ------------------------------------------------------------------ */

    function extractMacros(rawHtml) {
        var m = rawHtml.match(/macros:\s*\{[\s\S]*?\n\s*\}/);
        return m ? m[0] : null;
    }

    function extractArticleText(rawHtml) {
        var doc = new DOMParser().parseFromString(rawHtml, "text/html");
        var article = doc.querySelector(".math-article") || doc.querySelector("main");
        if (!article) { return null; }

        var junk = article.querySelectorAll(
            "script, style, nav, button, .part-prevnext, .part-prevnext-spacer, .ai-assist-bar"
        );
        junk.forEach(function (el) { el.remove(); });

        article.querySelectorAll("figure").forEach(function (fig) {
            var cap = fig.querySelector("figcaption");
            var capText = cap ? cap.textContent.replace(/\s+/g, " ").trim() : "";
            var repl = doc.createElement("p");
            repl.textContent = capText ? "[Figure. Caption: " + capText + "]" : "[Figure]";
            fig.replaceWith(repl);
        });

        // Insert markdown-ish heading markers so structure survives textContent.
        article.querySelectorAll("h1, h2, h3, h4").forEach(function (h) {
            var level = parseInt(h.tagName.charAt(1), 10);
            h.textContent = "\n" + new Array(level + 1).join("#") + " " + h.textContent.trim() + "\n";
        });

        var text = article.textContent;
        // Collapse >2 consecutive blank lines and trim trailing spaces.
        text = text.replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
        return text;
    }

    function buildPayload(rawHtml) {
        var articleText = extractArticleText(rawHtml);
        if (!articleText) { return null; }
        var macros = extractMacros(rawHtml);

        var lines = [
            "=== CONTEXT FOR AI ASSISTANT ===",
            "The reader is studying a page from \u201C" + series.title + "\u201D, a series of research notes by Adrian Mag.",
            "",
            "Page: " + pageTitle,
            "URL: " + pageUrl,
            "Series landing page: " + landingUrl,
            "Reading companion (narrative arc, notation, guardrails): " + companionUrl,
            "",
            "Intent of the series: " + series.intent,
            "",
            "Instructions: Help the reader understand this page IN ITS OWN FRAMING and notation. If a standard textbook treatment differs from the treatment here, explain the difference explicitly rather than silently replacing the notes' framing. Mathematics below is written in LaTeX (inline \\( ... \\), display \\[ ... \\]).",
            ""
        ];

        if (macros) {
            lines.push("MathJax macro definitions used on this page:");
            lines.push(macros);
            lines.push("");
        }

        lines.push("=== PAGE CONTENT ===");
        lines.push("");
        lines.push(articleText);

        return lines.join("\n");
    }

    function buildSeriesPayload(pageTexts, macros) {
        var lines = [
            "=== CONTEXT FOR AI ASSISTANT ===",
            "The reader is studying the ENTIRE series \u201C" + series.title + "\u201D by Adrian Mag.",
            "",
            "Series landing page: " + landingUrl,
            "Reading companion (narrative arc, notation, guardrails): " + companionUrl,
            "",
            "Intent of the series: " + series.intent,
            "",
            "Instructions: Help the reader understand these notes IN THEIR OWN FRAMING and notation. If a standard textbook treatment differs from the treatment here, explain the difference explicitly rather than silently replacing the notes' framing. Mathematics below is written in LaTeX (inline \\( ... \\), display \\[ ... \\]). The notes are split into multiple pages (acts/parts); they are presented below in reading order, separated by dividers.",
            ""
        ];

        if (macros) {
            lines.push("MathJax macro definitions used across the series:");
            lines.push(macros);
            lines.push("");
        }

        lines.push("=== FULL SERIES CONTENT ===");
        lines.push("");

        for (var i = 0; i < pageTexts.length; i++) {
            if (pageTexts[i]) {
                lines.push(pageTexts[i]);
                lines.push("");
                lines.push("---");
                lines.push("");
            }
        }

        return lines.join("\n");
    }

    /* ------------------------------------------------------------------ */
    /* Toolbar                                                             */
    /* ------------------------------------------------------------------ */

    function makeToolbar() {
        var bar = document.createElement("div");
        bar.className = "ai-assist-bar";

        var label = document.createElement("span");
        label.className = "ai-assist-label";
        label.textContent = "Read with AI:";
        bar.appendChild(label);

        // 1a. Copy page for AI
        var copyBtn = document.createElement("button");
        copyBtn.type = "button";
        copyBtn.className = "ai-assist-btn";
        copyBtn.textContent = "\uD83D\uDCCB Copy page for AI";
        copyBtn.addEventListener("click", function () {
            copyBtn.disabled = true;
            fetch(window.location.href, { cache: "no-cache" })
                .then(function (r) { return r.text(); })
                .then(function (rawHtml) {
                    var payload = buildPayload(rawHtml);
                    if (!payload) { throw new Error("extract failed"); }
                    return navigator.clipboard.writeText(payload);
                })
                .then(function () {
                    copyBtn.textContent = "\u2713 Copied \u2014 paste into any AI chat";
                    copyBtn.classList.add("copied");
                    setTimeout(function () {
                        copyBtn.textContent = "\uD83D\uDCCB Copy page for AI";
                        copyBtn.classList.remove("copied");
                        copyBtn.disabled = false;
                    }, 3000);
                })
                .catch(function () {
                    copyBtn.textContent = "Copy failed \u2014 try selecting text manually";
                    setTimeout(function () {
                        copyBtn.textContent = "\uD83D\uDCCB Copy page for AI";
                        copyBtn.disabled = false;
                    }, 3000);
                });
        });
        bar.appendChild(copyBtn);

        // 1b. Copy entire series for AI
        var copySeriesBtn = document.createElement("button");
        copySeriesBtn.type = "button";
        copySeriesBtn.className = "ai-assist-btn";
        copySeriesBtn.textContent = "\uD83D\uDCDA Copy entire series for AI";
        copySeriesBtn.addEventListener("click", function () {
            copySeriesBtn.disabled = true;
            copySeriesBtn.textContent = "Fetching all pages...";
            var pageUrls = series.pages.map(function (p) { return dirUrl + p; });
            var macrosFound = null;
            var pageTexts = new Array(pageUrls.length);
            var fetches = pageUrls.map(function (url, idx) {
                return fetch(url, { cache: "no-cache" })
                    .then(function (r) { return r.text(); })
                    .then(function (rawHtml) {
                        if (!macrosFound) {
                            macrosFound = extractMacros(rawHtml);
                        }
                        var text = extractArticleText(rawHtml);
                        if (text) {
                            var titleMatch = rawHtml.match(/<title>(.*?)<\/title>/);
                            var title = titleMatch ? titleMatch[1].replace(/\s+/g, " ").trim() : series.pages[idx];
                            pageTexts[idx] = "## " + title + "\n\n" + text;
                        }
                    })
                    .catch(function () { /* skip failed pages */ });
            });
            Promise.all(fetches).then(function () {
                var payload = buildSeriesPayload(pageTexts, macrosFound);
                return navigator.clipboard.writeText(payload);
            }).then(function () {
                copySeriesBtn.textContent = "\u2713 Entire series copied \u2014 paste into any AI chat";
                copySeriesBtn.classList.add("copied");
                setTimeout(function () {
                    copySeriesBtn.textContent = "\uD83D\uDCDA Copy entire series for AI";
                    copySeriesBtn.classList.remove("copied");
                    copySeriesBtn.disabled = false;
                }, 4000);
            }).catch(function () {
                copySeriesBtn.textContent = "Copy failed \u2014 try again";
                setTimeout(function () {
                    copySeriesBtn.textContent = "\uD83D\uDCDA Copy entire series for AI";
                    copySeriesBtn.disabled = false;
                }, 3000);
            });
        });
        bar.appendChild(copySeriesBtn);

        // 2. Open in ChatGPT (prefilled prompt)
        var prompt =
            "Please read this page: " + pageUrl +
            " and its reading companion: " + companionUrl +
            " . The page is part of the notes series \u201C" + series.title +
            "\u201D by Adrian Mag. Help me understand the page in its own framing and notation" +
            " (the companion explains both). If standard treatments differ from these notes," +
            " point out the difference explicitly instead of replacing the notes' framing.";
        var gptLink = document.createElement("a");
        gptLink.className = "ai-assist-btn";
        gptLink.href = "https://chatgpt.com/?q=" + encodeURIComponent(prompt);
        gptLink.target = "_blank";
        gptLink.rel = "noopener";
        gptLink.textContent = "Open in ChatGPT \u2197";
        bar.appendChild(gptLink);

        // 3. Companion link
        var compLink = document.createElement("a");
        compLink.className = "ai-assist-btn";
        compLink.href = companionUrl;
        compLink.target = "_blank";
        compLink.rel = "noopener";
        compLink.textContent = "AI reading companion";
        bar.appendChild(compLink);

        return bar;
    }

    function insertToolbar() {
        var bar = makeToolbar();
        var partNav = document.querySelector(".part-nav");
        if (partNav && partNav.parentNode) {
            partNav.parentNode.insertBefore(bar, partNav.nextSibling);
            return;
        }
        var header = document.querySelector(".page-header");
        if (header && header.parentNode) {
            header.parentNode.insertBefore(bar, header.nextSibling);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertToolbar);
    } else {
        insertToolbar();
    }
})();
