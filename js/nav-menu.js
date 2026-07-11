/*
 * nav-menu.js — mobile hamburger menu.
 *
 * On narrow screens the primary links (About / Research / CV and the
 * Research sub-menu) are hidden by .hide-sm. This script adds a burger
 * button that opens a dropdown panel built by CLONING those links, so
 * every page's relative paths are reused as-is. Contact, the theme
 * toggle, and search stay visible in the bar.
 */
(function () {
    "use strict";

    var BURGER = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
    var CLOSE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';

    function init() {
        var nav = document.querySelector(".nav");
        var links = nav && nav.querySelector(".nav-links");
        if (!links) return;

        // ---- panel: clone the hidden-on-mobile links ----
        var panel = document.createElement("div");
        panel.className = "nav-mobile-panel";

        links.querySelectorAll(":scope > a.hide-sm").forEach(function (a) {
            // insert Research group right after About (source order preserved below)
            panel.appendChild(a.cloneNode(true));
            if (a.nextElementSibling && a.nextElementSibling.classList.contains("nav-drop")) {
                var drop = a.nextElementSibling;
                var main = drop.querySelector(":scope > a");
                if (main) panel.appendChild(main.cloneNode(true));
                drop.querySelectorAll(".nav-drop-menu > *").forEach(function (item) {
                    var c = item.cloneNode(true);
                    if (c.tagName === "A") c.classList.add("nav-mobile-sub");
                    panel.appendChild(c);
                });
            }
        });
        panel.querySelectorAll("a").forEach(function (a) { a.classList.remove("hide-sm"); });

        // ---- burger button ----
        var btn = document.createElement("button");
        btn.className = "nav-burger";
        btn.type = "button";
        btn.setAttribute("aria-label", "Menu");
        btn.setAttribute("aria-expanded", "false");
        btn.innerHTML = BURGER;

        function setOpen(open) {
            panel.classList.toggle("open", open);
            btn.setAttribute("aria-expanded", open ? "true" : "false");
            btn.innerHTML = open ? CLOSE : BURGER;
        }
        btn.addEventListener("click", function (e) {
            e.stopPropagation();
            setOpen(!panel.classList.contains("open"));
        });
        document.addEventListener("click", function (e) {
            if (panel.classList.contains("open") && !panel.contains(e.target)) setOpen(false);
        });
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") setOpen(false);
        });

        links.insertBefore(btn, links.firstChild);
        nav.appendChild(panel);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
