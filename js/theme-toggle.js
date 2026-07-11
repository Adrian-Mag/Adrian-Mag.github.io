/*
 * theme-toggle.js — Space / Earth mode switch.
 *
 * The palettes are named token sets in css/theme.css:
 *   space — dark, from the astrophotography (default)
 *   earth — light/earthy, from the mountain photography
 *
 * A tiny inline snippet in each page's <head> stamps the stored theme
 * before first paint; this script only renders the button and handles
 * clicks. Hero images swap via [data-hero] CSS overrides in theme.css.
 */
(function () {
    "use strict";

    var KEY = "site-theme";

    // shown icon = the mode you will switch TO
    var ICON_MOUNTAIN = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 19h18L14 6l-3.5 6L8 9z"/></svg>';
    var ICON_STARS = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.6 3.8L17 8.4l-3.4 1.6L12 14l-1.6-4L7 8.4l3.4-1.6z"/><path d="M18 14l.9 2.1L21 17l-2.1.9L18 20l-.9-2.1L15 17l2.1-.9z"/></svg>';

    function current() {
        return document.documentElement.getAttribute("data-theme") === "earth" ? "earth" : "space";
    }

    function render(btn) {
        if (current() === "earth") {
            btn.innerHTML = ICON_STARS;
            btn.setAttribute("aria-label", "Switch to space mode");
            btn.title = "Space mode";
        } else {
            btn.innerHTML = ICON_MOUNTAIN;
            btn.setAttribute("aria-label", "Switch to earth mode");
            btn.title = "Earth mode";
        }
    }

    function init() {
        var navLinks = document.querySelector(".nav .nav-links");
        if (!navLinks) return; // pages without the main nav follow the stored theme silently
        var btn = document.createElement("button");
        btn.className = "theme-toggle";
        btn.type = "button";
        render(btn);
        btn.addEventListener("click", function () {
            var next = current() === "earth" ? "space" : "earth";
            document.documentElement.setAttribute("data-theme", next);
            try { localStorage.setItem(KEY, next); } catch (e) { /* private mode */ }
            render(btn);
        });
        var search = navLinks.querySelector(".nav-search");
        navLinks.insertBefore(btn, search || null);
    }

    /* Keep the choice global, not per page-view:
       - pageshow: re-apply on back/forward-cache restores, which resurrect
         the old DOM without re-running the <head> stamp;
       - storage: follow toggles made in any other open tab live. */
    function applyStored() {
        var t = null;
        try { t = localStorage.getItem(KEY); } catch (e) { /* ignore */ }
        if (t === "earth" || t === "space") {
            document.documentElement.setAttribute("data-theme", t);
        }
        var btn = document.querySelector(".theme-toggle");
        if (btn) render(btn);
    }
    window.addEventListener("pageshow", function (e) { if (e.persisted) applyStored(); });
    window.addEventListener("storage", function (e) { if (e.key === KEY) applyStored(); });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
