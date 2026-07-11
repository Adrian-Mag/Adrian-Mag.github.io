/*
 * notes-extras.js — small quality-of-life additions for the notes pages.
 *
 *   1. Reading-time badge on act/part pages (word count of the article).
 *   2. "Continue where you left off" — content pages record themselves in
 *      localStorage; each series landing page offers a Resume link.
 *   3. "Spotted an error?" link opening a pre-filled GitHub issue.
 *
 * Everything is injected at runtime (same pattern as ai-assist.js):
 * no per-page markup, series detected from the URL.
 */
(function () {
    "use strict";

    var REPO_ISSUES = "https://github.com/Adrian-Mag/Adrian-Mag.github.io/issues/new";

    var SERIES = {
        "sola": { landing: "my-take-on-sola.html", title: "My Take on SOLA" },
        "think-first": { landing: "think-first-discretize-later.html", title: "Think First, Discretize Later" },
        "bayes": { landing: "bayes-measure-theoretically.html", title: "Bayes, Measure-Theoretically" },
        "frequentist": { landing: "bayesian-frequentist.html", title: "Bayesian vs Frequentist" }
    };

    function detect() {
        var m = window.location.pathname.match(/\/overview\/([^/]+)\/([^/]+\.html)$/);
        if (!m || !SERIES[m[1]]) return null;
        return { key: m[1], page: m[2], series: SERIES[m[1]], isLanding: m[2] === SERIES[m[1]].landing };
    }

    function injectStyles() {
        var css =
            ".notes-meta{max-width:760px;margin:0.8rem auto -0.6rem;padding:0 1rem;" +
            "display:flex;align-items:center;gap:1rem;flex-wrap:wrap;" +
            "font-size:0.85rem;color:var(--muted);}" +
            ".notes-resume{max-width:760px;margin:1.2rem auto -0.4rem;padding:0.7rem 1.1rem;" +
            "border-radius:8px;background:rgba(103,145,190,0.10);" +
            "border:1px solid rgba(103,145,190,0.30);font-size:0.92rem;" +
            "color:var(--text);}" +
            ".notes-resume a{color:var(--accent-bright);font-weight:600;text-decoration:none;}" +
            ".notes-resume a:hover{text-decoration:underline;}" +
            ".notes-errlink{max-width:760px;margin:2rem auto 0;padding:0 1rem;" +
            "font-size:0.85rem;color:var(--muted);text-align:center;}" +
            ".notes-errlink a{color:var(--accent-bright);text-decoration:none;}" +
            ".notes-errlink a:hover{text-decoration:underline;color:var(--accent-bright);}";
        var el = document.createElement("style");
        el.textContent = css;
        document.head.appendChild(el);
    }

    function anchorPoint() {
        return document.querySelector(".part-nav") || document.querySelector(".page-header");
    }

    function insertAfterAnchor(el) {
        var a = anchorPoint();
        if (a && a.parentNode) a.parentNode.insertBefore(el, a.nextSibling);
    }

    // --- 1. reading time -------------------------------------------------------

    function readingTime() {
        var article = document.querySelector(".math-article") || document.querySelector("main");
        if (!article) return null;
        var text = article.textContent || "";
        var words = (text.match(/\S+/g) || []).length;
        // long-form math reads slower than prose; ~180 wpm
        return Math.max(1, Math.round(words / 180));
    }

    // --- 2. resume bookkeeping ---------------------------------------------------

    function storageKey(key) { return "notes-resume:" + key; }

    function recordVisit(ctx) {
        try {
            var h1 = document.querySelector("main h1");
            localStorage.setItem(storageKey(ctx.key), JSON.stringify({
                page: ctx.page,
                title: (h1 && h1.textContent.trim()) || document.title,
                t: Date.now()
            }));
        } catch (e) { /* private mode etc. — fine */ }
    }

    function resumeBanner(ctx) {
        var raw;
        try { raw = localStorage.getItem(storageKey(ctx.key)); } catch (e) { return; }
        if (!raw) return;
        var last;
        try { last = JSON.parse(raw); } catch (e) { return; }
        if (!last || !last.page || last.page === ctx.series.landing) return;

        var box = document.createElement("div");
        box.className = "notes-resume";
        var link = document.createElement("a");
        link.href = last.page;
        link.textContent = last.title;
        box.appendChild(document.createTextNode("Continue where you left off: "));
        box.appendChild(link);
        box.appendChild(document.createTextNode(" →"));
        insertAfterAnchor(box);
    }

    // --- 3. error-report link -----------------------------------------------------

    function errorLink() {
        var target = document.querySelector(".part-prevnext");
        var url = window.location.href.split("#")[0];
        var title = document.title;
        var issueUrl = REPO_ISSUES +
            "?title=" + encodeURIComponent("Error in: " + title) +
            "&body=" + encodeURIComponent(
                "Page: " + url + "\n\n" +
                "What is wrong (quote the passage or equation):\n\n\n" +
                "What it should say (if known):\n"
            );

        var p = document.createElement("p");
        p.className = "notes-errlink";
        var a = document.createElement("a");
        a.href = issueUrl;
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = "Spotted a mistake? Open an issue";
        p.appendChild(a);
        p.appendChild(document.createTextNode(" — these notes take correctness personally."));

        if (target && target.parentNode) {
            target.parentNode.insertBefore(p, target);
        } else {
            var article = document.querySelector(".math-article") || document.querySelector("main");
            if (article) article.appendChild(p);
        }
    }

    // --- run -----------------------------------------------------------------------

    function init() {
        var ctx = detect();
        if (!ctx) return;
        injectStyles();

        if (ctx.isLanding) {
            resumeBanner(ctx);
        } else {
            var mins = readingTime();
            if (mins) {
                var meta = document.createElement("div");
                meta.className = "notes-meta";
                meta.textContent = "≈ " + mins + " min read";
                insertAfterAnchor(meta);
            }
            recordVisit(ctx);
        }
        errorLink();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
