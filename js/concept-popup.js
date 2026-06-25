(function () {
    "use strict";

    var overlay = null;
    var dialog = null;
    var closeBtn = null;
    var contentEl = null;
    var lastFocused = null;
    var isOpen = false;

    function init() {
        overlay = document.createElement("div");
        overlay.className = "concept-overlay";
        overlay.setAttribute("role", "presentation");
        overlay.setAttribute("aria-hidden", "true");

        dialog = document.createElement("div");
        dialog.className = "concept-dialog";
        dialog.setAttribute("role", "dialog");
        dialog.setAttribute("aria-modal", "true");
        dialog.setAttribute("aria-labelledby", "concept-dialog-title");

        var headerBar = document.createElement("div");
        headerBar.className = "concept-dialog-header";

        var title = document.createElement("h3");
        title.id = "concept-dialog-title";
        title.className = "concept-dialog-title";

        closeBtn = document.createElement("button");
        closeBtn.className = "concept-close-btn";
        closeBtn.setAttribute("type", "button");
        closeBtn.setAttribute("aria-label", "Close concept popup");
        closeBtn.innerHTML = "&times;";

        headerBar.appendChild(title);
        headerBar.appendChild(closeBtn);

        contentEl = document.createElement("div");
        contentEl.className = "concept-dialog-content";

        dialog.appendChild(headerBar);
        dialog.appendChild(contentEl);
        overlay.appendChild(dialog);
        document.body.appendChild(overlay);

        overlay.addEventListener("click", function (e) {
            if (e.target === overlay) close();
        });
        closeBtn.addEventListener("click", close);
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && isOpen) {
                e.stopPropagation();
                close();
            }
        });
        dialog.addEventListener("keydown", function (e) {
            if (e.key === "Tab") trapFocus(e);
        });

        var terms = document.querySelectorAll(".concept-term[data-concept]");
        for (var i = 0; i < terms.length; i++) {
            (function (term) {
                term.setAttribute("tabindex", "0");
                term.setAttribute("role", "button");
                term.setAttribute("aria-label", "Open explanation: " + term.textContent.trim());
                term.addEventListener("click", function (e) {
                    e.preventDefault();
                    open(term);
                });
                term.addEventListener("keydown", function (e) {
                    if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        open(term);
                    }
                });
            })(terms[i]);
        }
    }

    function trapFocus(e) {
        var focusable = dialog.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
        }
    }

    function open(term) {
        var conceptId = term.getAttribute("data-concept");
        var template = document.getElementById("concept-" + conceptId);
        if (!template) return;

        var titleText = term.textContent.trim();
        dialog.querySelector(".concept-dialog-title").textContent = titleText;

        contentEl.innerHTML = "";
        contentEl.appendChild(template.content.cloneNode(true));

        lastFocused = term;
        isOpen = true;
        overlay.classList.add("is-open");
        overlay.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";

        closeBtn.focus();

        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise([contentEl]).catch(function () {});
        }
    }

    function close() {
        if (!isOpen) return;
        isOpen = false;
        overlay.classList.remove("is-open");
        overlay.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
        if (lastFocused) lastFocused.focus();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
