/* ==========================================================================
   Progressive enhancement only. Delete this file and the page is complete,
   readable and navigable — you lose motion, the ⌘K menu, the live clock and
   copy-to-clipboard, nothing else.

   Motion is decided once, before first paint, by the inline script in
   <head>: it sets .motion when prefers-reduced-motion is "no-preference".
   ========================================================================== */
(() => {
  "use strict";

  const root = document.documentElement;
  const motion = root.classList.contains("motion");
  const hasIO = "IntersectionObserver" in window;
  const finePointer = window.matchMedia("(pointer: fine)").matches;
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /** Run `fn(el)` once, the first time `el` is mostly on screen. */
  const onceVisible = (els, fn, opts = { threshold: 0.25 }) => {
    if (!hasIO) { els.forEach(fn); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        fn(e.target);
      });
    }, opts);
    els.forEach((el) => io.observe(el));
  };

  /* ---- 1. Scroll reveal ---------------------------------------------------- */
  if (root.classList.contains("reveal-armed")) {
    onceVisible($$(".rv"), (el) => el.classList.add("is-in"),
      { rootMargin: "0px 0px -6% 0px", threshold: 0.04 });
  }

  /* ---- 2. Nav scroll spy --------------------------------------------------- */
  const navLinks = $$(".nav-link");
  if (hasIO && navLinks.length) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        navLinks.forEach((l) =>
          l.setAttribute("aria-current", l.dataset.nav === e.target.id ? "true" : "false"));
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    navLinks.forEach((l) => { const s = document.getElementById(l.dataset.nav); if (s) spy.observe(s); });
    const hero = $("#top");
    if (hero) spy.observe(hero);   // clears the highlight back at the top
  }

  /* ---- 3. Hero crosshair ---------------------------------------------------
     A CAD-style cursor: two hairlines and a coordinate readout. Fine pointers
     with motion on only; a phone gets the static Mumbai coordinates. */
  const hero = $("#top");
  const readout = $("[data-coords]");
  if (hero && readout && finePointer && motion) {
    const chX = $(".ch-x", hero), chY = $(".ch-y", hero);
    const resting = readout.textContent;
    const pad = (n) => String(Math.max(0, Math.round(n))).padStart(4, "0");
    let px = 0, py = 0, raf = 0;
    const draw = () => {
      raf = 0;
      chX.style.transform = `translate3d(0, ${py}px, 0)`;
      chY.style.transform = `translate3d(${px}px, 0, 0)`;
      readout.textContent = `x ${pad(px)} · y ${pad(py)}`;
    };
    hero.addEventListener("pointermove", (e) => {
      const r = hero.getBoundingClientRect();
      px = e.clientX - r.left; py = e.clientY - r.top;
      hero.classList.add("is-tracking");
      if (!raf) raf = requestAnimationFrame(draw);
    }, { passive: true });
    hero.addEventListener("pointerleave", () => {
      hero.classList.remove("is-tracking");
      readout.textContent = resting;
    });
  }

  /* ---- 4. The system drawing -------------------------------------------------
     Each wire carries a packet during its own slice of a looping cycle
     (data-t0..data-t1, computed in drawings.py), so a request visibly travels
     client → edge → app and fans out. A node lights up as a packet lands.
     On narrow screens the wires are hidden but the lights still run down the
     stacked boxes. Runs only while on screen; has a pause control (WCAG
     2.2.2); with reduced motion it starts paused and the button offers Play. */
  const sys = $("[data-sys]");
  if (sys) {
    const svg = $(".sys-wires", sys);
    const wires = $$(".wire", sys);
    const nodes = {};
    $$("[data-node]", sys).forEach((n) => { nodes[n.dataset.node] = n; });

    // Hover: trace a box's connections.
    const link = (id, on) => {
      if (nodes[id]) nodes[id].classList.toggle("is-linked", on);
      wires.forEach((w) => {
        if (w.dataset.from !== id && w.dataset.to !== id) return;
        w.classList.toggle("is-linked", on);
      });
    };
    Object.keys(nodes).forEach((id) => {
      nodes[id].addEventListener("pointerenter", () => link(id, true));
      nodes[id].addEventListener("pointerleave", () => link(id, false));
    });

    const NS = "http://www.w3.org/2000/svg";
    const group = $(".packets", svg);
    const packets = wires.map(() => {
      const r = document.createElementNS(NS, "rect");
      r.setAttribute("class", "packet");
      r.setAttribute("x", "-6"); r.setAttribute("y", "-6");
      r.setAttribute("width", "12"); r.setAttribute("height", "12");
      r.style.opacity = "0";
      group.appendChild(r);
      return r;
    });
    const lengths = wires.map((w) => w.getTotalLength());
    const spans = wires.map((w) => [parseFloat(w.dataset.t0), parseFloat(w.dataset.t1)]);
    const CYCLE = 4600;
    const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
    const hotState = {};
    let running = motion, visible = false, raf = 0, origin = performance.now(), pausedAt = 0;

    const frame = (now) => {
      raf = 0;
      const t = ((now - origin) % CYCLE) / CYCLE;
      const hot = new Set();
      if (t < 0.06) hot.add("client");
      wires.forEach((w, i) => {
        const [t0, t1] = spans[i];
        const p = packets[i];
        if (t >= t0 && t <= t1) {
          const k = ease((t - t0) / (t1 - t0));
          const pt = w.getPointAtLength(k * lengths[i]);
          p.setAttribute("transform", `translate(${pt.x.toFixed(1)} ${pt.y.toFixed(1)})`);
          p.style.opacity = "1";
          if (k > 0.92) hot.add(w.dataset.to);
        } else {
          p.style.opacity = "0";
          if (t > t1 && t < t1 + 0.07) hot.add(w.dataset.to);
        }
        if (t >= t0 && t < t0 + 0.05) hot.add(w.dataset.from);
      });
      Object.keys(nodes).forEach((id) => {
        const h = hot.has(id);
        if (hotState[id] !== h) { hotState[id] = h; nodes[id].classList.toggle("is-hot", h); }
      });
      svg.classList.toggle("runtime-hot", hot.has("runtime"));
      if (running && visible) raf = requestAnimationFrame(frame);
    };
    const kick = () => { if (running && visible && !raf) raf = requestAnimationFrame(frame); };
    const clear = () => {
      packets.forEach((p) => { p.style.opacity = "0"; });
      Object.keys(nodes).forEach((id) => { hotState[id] = false; nodes[id].classList.remove("is-hot"); });
      svg.classList.remove("runtime-hot");
    };

    const btn = $("[data-sys-toggle]", sys);
    const label = () => {
      btn.textContent = running ? "Pause flow" : "Play flow";
      btn.setAttribute("aria-pressed", running ? "false" : "true");
    };
    if (btn) {
      btn.hidden = false;
      label();
      btn.addEventListener("click", () => {
        const now = performance.now();
        if (running) { running = false; pausedAt = now; cancelAnimationFrame(raf); raf = 0; }
        else { running = true; origin += pausedAt ? now - pausedAt : 0; kick(); }
        label();
      });
    }

    if (hasIO) {
      new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting;
        if (visible) kick(); else { cancelAnimationFrame(raf); raf = 0; }
      }, { threshold: 0.15 }).observe(sys);
    } else { visible = true; kick(); }
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) { cancelAnimationFrame(raf); raf = 0; } else kick();
    });
    if (!running) clear();
  }

  /* ---- 5. Flow pipeline sweep -----------------------------------------------
     One sweep through the steps when it scrolls into view (≈2.5 s, so no
     pause control is needed), and again on hover. */
  if (motion) {
    $$("[data-pipeline]").forEach((fig) => {
      const steps = $$(".pipe-step", fig);
      let timer = 0, busy = false;
      const sweep = () => {
        if (busy) return;
        busy = true;
        let i = 0;
        const tick = () => {
          steps.forEach((s, k) => s.classList.toggle("is-active", k === i));
          i += 1;
          if (i <= steps.length) timer = setTimeout(tick, 380);
          else { steps.forEach((s) => s.classList.remove("is-active")); busy = false; }
        };
        clearTimeout(timer);
        tick();
      };
      onceVisible([fig], sweep, { threshold: 0.5 });
      fig.addEventListener("pointerenter", sweep);
    });
  }

  /* ---- 6. Figure draw-in (chart, ring) + counters --------------------------------------- */
  if (root.classList.contains("reveal-armed")) {
    onceVisible($$("[data-draw]"), (el) => el.classList.add("is-drawn"), { threshold: 0.35 });
  }

  if (motion) {
    onceVisible($$("[data-count]"), (el) => {
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || "";
      if (Number.isNaN(target)) return;
      const dur = 1100;
      let start = null;
      const step = (ts) => {
        if (start === null) start = ts;
        const p = Math.min((ts - start) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      el.textContent = "0" + suffix;
      requestAnimationFrame(step);
    }, { threshold: 0.6 });
  }

  /* ---- 7. Copy email ------------------------------------------------------ */
  const status = $("[data-copy-status]");
  const say = (msg) => {
    if (!status) return;
    status.textContent = msg;
    clearTimeout(say.t);
    say.t = setTimeout(() => { status.textContent = ""; }, 4000);
  };
  const copy = (text) => {
    if (!navigator.clipboard) { window.location.href = "mailto:" + text; return; }
    navigator.clipboard.writeText(text)
      .then(() => say("Copied " + text + " to the clipboard."))
      .catch(() => say("Couldn't copy — it's " + text));
  };
  $$("[data-copy]").forEach((b) => {
    if (!navigator.clipboard) return;
    b.hidden = false;
    b.addEventListener("click", () => copy(b.dataset.copy));
  });

  /* ---- 8. Live local time ---------------------------------------------- */
  const clock = $("[data-clock]");
  if (clock && window.Intl) {
    try {
      const fmt = new Intl.DateTimeFormat("en-GB", {
        timeZone: clock.dataset.tz, hour: "2-digit", minute: "2-digit", hour12: false,
      });
      const tz = clock.dataset.tzLabel || "";
      const tick = () => {
        const s = fmt.format(new Date());
        const h = parseInt(s.slice(0, 2), 10);
        const note = h >= 8 && h < 24 ? "probably at the keyboard" : "probably asleep — replies by morning";
        clock.textContent = `${s} ${tz} · ${note}`;
      };
      tick();
      setInterval(tick, 20000);
    } catch (e) { /* unknown time zone: keep the static label */ }
  }

  /* ---- 9. ⌘K command menu ------------------------------------------------- */
  const pal = $("#palette");
  if (pal && typeof pal.showModal === "function") {
    const input = $("#pal-input", pal);
    const items = $$(".pal-item", pal);
    const groups = $$(".pal-group", pal);
    const empty = $(".pal-empty", pal);
    const email = ($("[data-copy]") || {}).dataset?.copy || "";
    let sel = 0;

    const shown = () => items.filter((i) => !i.hidden);
    const select = (n) => {
      const v = shown();
      items.forEach((i) => i.setAttribute("aria-selected", "false"));
      if (!v.length) { input.removeAttribute("aria-activedescendant"); return; }
      sel = (n + v.length) % v.length;
      v[sel].setAttribute("aria-selected", "true");
      input.setAttribute("aria-activedescendant", v[sel].id);
      v[sel].scrollIntoView({ block: "nearest" });
    };
    const filter = () => {
      const q = input.value.trim().toLowerCase();
      items.forEach((i) => {
        const hay = (i.textContent + " " + (i.dataset.keywords || "")).toLowerCase();
        i.hidden = q !== "" && !hay.includes(q);
      });
      // hide a group heading when everything under it is filtered out
      groups.forEach((g) => {
        let n = g.nextElementSibling, any = false;
        while (n && !n.classList.contains("pal-group")) { if (!n.hidden) any = true; n = n.nextElementSibling; }
        g.hidden = !any;
      });
      empty.hidden = shown().length > 0;
      select(0);
    };
    const open = () => {
      if (pal.open) return;
      input.value = "";
      filter();
      pal.showModal();
      input.focus();
    };
    const close = () => { if (pal.open) pal.close(); };
    const run = (item) => {
      const href = item.dataset.href;
      close();
      if (item.dataset.action === "copy") { copy(email); return; }
      if (!href) return;
      if (href.startsWith("#")) {
        const target = document.getElementById(href.slice(1));
        if (!target) return;
        target.scrollIntoView({ behavior: motion ? "smooth" : "auto", block: "start" });
        target.focus({ preventScroll: true });
        history.replaceState(null, "", href);
      } else if ("external" in item.dataset) {
        window.open(href, "_blank", "noopener");
      } else {
        window.location.href = href;
      }
    };

    const typing = (el) => el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
    document.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        pal.open ? close() : open();
      } else if (e.key === "/" && !pal.open && !typing(e.target)) {
        e.preventDefault();
        open();
      }
    });
    input.addEventListener("input", filter);
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); select(sel + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); select(sel - 1); }
      else if (e.key === "Enter") { e.preventDefault(); const v = shown()[sel]; if (v) run(v); }
    });
    items.forEach((i) => {
      i.addEventListener("click", () => run(i));
      i.addEventListener("pointermove", () => { const k = shown().indexOf(i); if (k !== sel) select(k); });
    });
    pal.addEventListener("click", (e) => { if (e.target === pal) close(); });   // backdrop
    $$("[data-palette-open]").forEach((b) => b.addEventListener("click", open));

    const mac = /Mac|iPhone|iPad/.test(navigator.userAgentData?.platform || navigator.platform || "");
    $$("[data-kbd]").forEach((k) => { k.textContent = mac ? "⌘K" : "Ctrl K"; });
  }

  /* ---- 10. Housekeeping --------------------------------------------------- */
  const year = $("#year");
  if (year) year.textContent = new Date().getFullYear();

  /* The site was once a React bundle with a service worker caching /assets/*.
     Left registered, returning visitors could be served that old app from
     cache. Delete this block if a service worker is ever reintroduced. */
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.getRegistrations()
      .then((regs) => regs.forEach((r) => r.unregister())).catch(() => {});
    if (window.caches && caches.keys) {
      caches.keys().then((keys) => keys.forEach((k) => caches.delete(k))).catch(() => {});
    }
  }
})();
