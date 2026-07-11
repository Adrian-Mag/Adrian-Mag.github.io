/*
 * hero.js — homepage hero seismogram trace + scroll-reveal.
 * The animated trace over the nebula is the visual thesis: reading
 * structure from faint, noisy signals. Both effects are disabled
 * under prefers-reduced-motion.
 */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- scroll reveal --- */
  var items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.16 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* --- hero seismogram trace --- */
  var canvas = document.getElementById("seismo");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W = 0, H = 0;
  function accent() {
    return getComputedStyle(document.documentElement).getPropertyValue("--accent-bright").trim() || "#9BC1E8";
  }
  function resize() {
    var r = canvas.getBoundingClientRect();
    W = r.width; H = r.height;
    canvas.width = Math.floor(W * dpr); canvas.height = Math.floor(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();
  window.addEventListener("resize", resize);

  // recurring gaussian "events" along the trace
  function envelope(x) {
    var bursts = [0.16, 0.42, 0.68, 0.88];
    var amp = 0.16;
    for (var i = 0; i < bursts.length; i++) {
      var d = (x - bursts[i]);
      amp += (0.7 + 0.25 * i) * Math.exp(-(d * d) / 0.0016);
    }
    return Math.min(amp, 1.1);
  }
  function trace(t) {
    var mid = H * 0.52;
    ctx.clearRect(0, 0, W, H);
    var col = accent();
    ctx.lineWidth = 1.4; ctx.strokeStyle = col;
    ctx.shadowColor = col; ctx.shadowBlur = 6;
    ctx.beginPath();
    for (var px = 0; px <= W; px += 2) {
      var u = px / W;
      var phase = (u * 5.5 + t * 0.12);
      var env = envelope((u + t * 0.02) % 1);
      var y = mid
        + Math.sin(phase * 6.283) * 6 * env
        + Math.sin(phase * 2.7 * 6.283 + 1.3) * 10 * env
        + Math.sin(phase * 11.0 * 6.283) * 3 * env;
      if (px === 0) ctx.moveTo(px, y); else ctx.lineTo(px, y);
    }
    ctx.stroke();
    ctx.shadowBlur = 0; ctx.globalAlpha = 0.25; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, mid); ctx.lineTo(W, mid); ctx.stroke();
    ctx.globalAlpha = 1;
  }
  if (reduce) {
    trace(0);
  } else {
    var start = performance.now();
    (function loop(now) { trace((now - start) / 1000); requestAnimationFrame(loop); })(start);
  }
})();
