/* ==========================================================================
   Progressive enhancement only. Without this file every page is complete and
   readable: the loops show their poster, the slider shows its starting value,
   the tripwire map shows its homes and its rule. With it:

     1. the nav gets a background once the page scrolls
     2. silent loops play while on screen, with a Pause button
     3. the email Copy button
     4. the 64 KiB slider
     5. the tripwire map

   Motion is decided once, before first paint, by the inline script in
   <head>: it sets .motion when prefers-reduced-motion is "no-preference".
   ========================================================================== */
(() => {
  "use strict";

  const root = document.documentElement;
  const motion = root.classList.contains("motion");
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ---- 1. Nav background ---------------------------------------------------- */
  const nav = $("[data-nav]");
  if (nav) {
    let raf = 0;
    const set = () => { raf = 0; nav.classList.toggle("is-scrolled", window.scrollY > 24); };
    window.addEventListener("scroll", () => { if (!raf) raf = requestAnimationFrame(set); }, { passive: true });
    set();
  }

  /* ---- 2. Silent loops --------------------------------------------------------
     Nothing loads until a loop is at least 40% on screen. It pauses when it
     leaves. Anything that moves for more than five seconds needs a way to stop
     it, so the button is always there; once someone pauses a loop it stays
     paused. With reduced motion nothing plays until the button is pressed. */
  const loops = $$("[data-loop]");
  if (loops.length) {
    const io = "IntersectionObserver" in window ? new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        const l = e.target._loop;
        if (e.isIntersecting && e.intersectionRatio >= 0.4) {
          l.onScreen = true;
          if (!l.userPaused && motion) l.play();
        } else {
          l.onScreen = false;
          l.pause();
        }
      });
    }, { threshold: [0, 0.4] }) : null;

    loops.forEach((el) => {
      const video = $("video", el);
      const btn = $("[data-loop-btn]", el);
      if (!video || !btn) return;
      const l = {
        onScreen: false,
        userPaused: !motion,
        play() {
          const p = video.play();
          if (p && p.catch) p.catch((err) => {
            // Blocked by the browser: wait for the button. (An AbortError just
            // means a pause came first, which is fine.)
            if (err && err.name === "NotAllowedError") { l.userPaused = true; label(); }
          });
          label();
        },
        pause() { video.pause(); label(); },
      };
      const label = () => {
        const playing = !video.paused && !l.userPaused;
        btn.textContent = playing ? "Pause" : "Play";
        btn.setAttribute("aria-label", (playing ? "Pause" : "Play") + " the clip");
      };
      video.addEventListener("playing", () => el.classList.add("is-playing"));
      btn.addEventListener("click", (ev) => {
        ev.preventDefault();
        if (video.paused) { l.userPaused = false; l.play(); }
        else { l.userPaused = true; l.pause(); }
      });
      el._loop = l;
      btn.hidden = false;
      label();
      if (io) io.observe(el);
    });
  }

  /* ---- 3. Copy the email address ---------------------------------------------- */
  const copyBtn = $("[data-copy]");
  const copyStatus = $("[data-copy-status]");
  if (copyBtn && navigator.clipboard && window.isSecureContext) {
    copyBtn.hidden = false;
    copyBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(copyBtn.dataset.copy);
        copyBtn.textContent = "Copied";
        if (copyStatus) copyStatus.textContent = "Email address copied.";
      } catch (_) {
        if (copyStatus) copyStatus.textContent = "Couldn't copy. Select the address instead.";
      }
      setTimeout(() => {
        copyBtn.textContent = "Copy";
        if (copyStatus) copyStatus.textContent = "";
      }, 2400);
    });
  }

  /* ---- 4. The 64 KiB slider ----------------------------------------------------- */
  $$("[data-trunc]").forEach((box) => {
    const limit = Number(box.dataset.limit);
    const max = Number(box.dataset.max);
    const range = $("input[type=range]", box);
    const bar = $(".trunc-bar", box);
    const printed = $("[data-t-printed]", box);
    const kept = $("[data-t-kept]", box);
    const lost = $("[data-t-lost]", box);
    const verdict = $("[data-t-verdict]", box);
    const update = () => {
      const v = Number(range.value);
      const k = Math.min(v, limit);
      printed.textContent = `${v} KiB`;
      kept.textContent = `${k} KiB`;
      lost.textContent = `${v - k} KiB`;
      bar.style.setProperty("--p", `${(100 * v / max).toFixed(2)}%`);
      verdict.textContent = v > limit
        ? `${v - k} KiB gone, and nothing said so.`
        : "Under 64 KiB, nothing is lost.";
    };
    range.addEventListener("input", update);
    update();
  });

  /* ---- 5. The tripwire ------------------------------------------------------------
     The project's rule, in the same plain code the real system uses: it fires
     on three different homes, every pair within 250 m, all reported within
     72 hours. Then every enrolled home within 250 m of the three is warned.
     Each report moves the clock on 3 hours. */
  $$("[data-trip]").forEach((box) => {
    const W = Number(box.dataset.w), H = Number(box.dataset.h);
    const RADIUS = 250, WINDOW = 72, STEP = 3, START = 8;
    const homes = $$(".home", box).map((b) => ({ b, id: Number(b.dataset.home), x: Number(b.dataset.x), y: Number(b.dataset.y) }));
    const byId = new Map(homes.map((h) => [h.id, h]));
    const ring = $("[data-trip-ring]", box);
    const clockEl = $("[data-trip-clock]", box);
    const statusEl = $("[data-trip-status]", box);
    const waitBtn = $("[data-trip-wait]", box);
    const resetBtn = $("[data-trip-reset]", box);
    const intro = statusEl.textContent;

    let now = 0;            // hours since Day 1, 08:00
    let reports = [];       // { id, t }
    let fired = false;

    const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
    const live = () => reports.filter((r) => now - r.t <= WINDOW);
    const clock = () => {
      const h = START + now;
      clockEl.textContent = `Day ${Math.floor(h / 24) + 1}, ${String(h % 24).padStart(2, "0")}:00`;
    };
    const say = (html) => { statusEl.innerHTML = html; };
    const name = (h) => `home ${h.id}`;

    const paint = () => {
      const liveIds = new Set(live().map((r) => r.id));
      homes.forEach((h) => {
        const reported = reports.some((r) => r.id === h.id);
        const isLive = liveIds.has(h.id);
        h.b.classList.toggle("is-reported", isLive);
        h.b.classList.toggle("is-old", reported && !isLive);
        let label = `Home ${h.id}`;
        if (isLive) label += ", reported";
        else if (reported) label += ", report too old to count";
        if (h.b.classList.contains("is-warned")) label += ", warned";
        h.b.setAttribute("aria-label", label);
      });
      clock();
    };

    // Any three different homes among the live reports, every pair within
    // RADIUS, that include the newest report.
    const findTrio = (newest) => {
      const others = live().map((r) => byId.get(r.id)).filter((h) => h !== newest && dist(h, newest) <= RADIUS);
      for (let i = 0; i < others.length; i++) {
        for (let j = i + 1; j < others.length; j++) {
          if (dist(others[i], others[j]) <= RADIUS) return [newest, others[i], others[j]];
        }
      }
      return null;
    };

    const fire = (trio) => {
      fired = true;
      const cx = trio.reduce((s, h) => s + h.x, 0) / 3;
      const cy = trio.reduce((s, h) => s + h.y, 0) / 3;
      const warned = homes.filter((h) => Math.hypot(h.x - cx, h.y - cy) <= RADIUS);
      warned.forEach((h) => h.b.classList.add("is-warned"));
      ring.style.setProperty("--x", `${(100 * cx / W).toFixed(3)}%`);
      ring.style.setProperty("--y", `${(100 * cy / H).toFixed(3)}%`);
      ring.classList.add("is-on");
      const quiet = warned.filter((h) => !trio.includes(h)).length;
      say(`<b>Third report: the tripwire fires.</b> ${warned.length} homes within 250 m are warned, ` +
          `${quiet} of them never complained. In the real system a volunteer approves it first. ` +
          `Start again to try another.`);
    };

    const report = (h) => {
      if (fired) { say("This warning has gone out. Start again to try another."); return; }
      if (live().some((r) => r.id === h.id)) {
        say(`${name(h)[0].toUpperCase() + name(h).slice(1)} has already reported. The rule counts <b>different</b> homes.`);
        return;
      }
      reports = reports.filter((r) => r.id !== h.id);   // an expired report is replaced
      reports.push({ id: h.id, t: now });
      paint();
      const trio = findTrio(h);
      if (trio) { fire(trio); paint(); }
      else explain(h);
      now += STEP;
      clock();
    };

    const explain = (h) => {
      const l = live().map((r) => byId.get(r.id));
      if (l.length === 1) {
        say(`1 report, from ${name(h)}. The rule needs three different homes.`);
      } else if (l.length === 2) {
        const d = Math.round(dist(l[0], l[1]));
        say(d <= RADIUS
          ? `2 reports, ${d} m apart. One more home within 250 m of both, inside 72 hours, fires it.`
          : `2 reports, but ${d} m apart. <b>Every pair</b> has to be within 250 m.`);
      } else {
        say(`${l.length} reports in the last 72 hours, but no three of them are all within 250 m of each other.`);
      }
    };

    const wait = () => {
      const before = live().length;
      now += 24;
      paint();
      const dropped = before - live().length;
      say(dropped
        ? `A day passes. ${dropped === 1 ? "1 report is" : dropped + " reports are"} now older than 72 hours and ${dropped === 1 ? "no longer counts" : "no longer count"}.`
        : `A day passes. Reports count for 72 hours from when they were made.`);
    };

    const reset = () => {
      now = 0; reports = []; fired = false;
      homes.forEach((h) => h.b.classList.remove("is-warned"));
      ring.classList.remove("is-on");
      paint();
      say(intro);
    };

    homes.forEach((h) => {
      h.b.disabled = false;
      h.b.addEventListener("click", () => report(h));
    });
    waitBtn.disabled = false;
    resetBtn.disabled = false;
    waitBtn.addEventListener("click", wait);
    resetBtn.addEventListener("click", reset);
    paint();
  });
})();
