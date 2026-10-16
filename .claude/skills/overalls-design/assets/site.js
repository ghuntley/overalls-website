// Overalls website: progressive enhancement only. Every page reads and works
// without this file; the theme then follows the operating system.
//
// 1. Appearance: System / Light / Dark via <select data-appearance>. An
//    explicit choice persists in localStorage when storage is available.
// 2. Copy buttons on command blocks (<pre data-copy>).
(() => {
  const KEY = "overalls:theme";
  const root = document.documentElement;
  const media = window.matchMedia("(prefers-color-scheme: dark)");
  let preference = "system";
  try { preference = localStorage.getItem(KEY) || "system"; } catch {}

  const apply = () => {
    if (!["system", "light", "dark"].includes(preference)) preference = "system";
    root.dataset.theme = preference === "system" ? (media.matches ? "dark" : "light") : preference;
    document.querySelectorAll("select[data-appearance]").forEach(select => { select.value = preference; });
  };

  // Runs from <head>, so the theme is set before first paint.
  apply();
  media.addEventListener("change", apply);
  window.addEventListener("storage", event => {
    if (event.key === KEY || event.key === null) {
      preference = event.newValue || "system";
      apply();
    }
  });
  document.addEventListener("change", event => {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement) || !target.matches("[data-appearance]")) return;
    preference = target.value;
    try {
      if (preference === "system") localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, preference);
    } catch {}
    apply();
  });

  const copyText = pre => {
    // Lines beginning with a muted prompt or output span are not copied.
    const clone = pre.cloneNode(true);
    clone.querySelectorAll(".prompt, .out, .copy-button").forEach(node => node.remove());
    return clone.textContent.replace(/^\n+|\s+$/g, "") + "\n";
  };

  // Newsletter: subscribe through the Ghost members API on ghuntley.com, the same
  // two calls Ghost's own embeddable signup form makes. Without JS the form falls
  // back to opening ghuntley.com/newsletter/.
  //
  // ghuntley.com is on Ghost(Pro), whose Fastly edge sits in front of the members
  // API. Ghost itself answers every origin with CORS headers, including its 4xx
  // errors, but the edge refuses some networks (VPNs, shared and datacenter
  // addresses, addresses that signed up repeatedly) with a 429 that has none, and
  // the browser reports that only as "Failed to fetch". The same requests succeed
  // from other networks, so that case is explained and the visitor is pointed at
  // Portal on ghuntley.com, which can show them the real reason.
  const newsletter = form => {
    const site = form.dataset.ghostSite;
    const status = form.parentElement.querySelector(".newsletter-status");
    const input = form.querySelector("input[type=email]");
    const button = form.querySelector("button");
    // Server messages are untrusted, so status text is set as text, never as HTML.
    const say = (state, text, link) => {
      status.dataset.state = state;
      status.textContent = text;
      if (link) {
        const a = document.createElement("a");
        a.href = `${site}/#/portal/signup`;
        a.textContent = "ghuntley.com ↗";
        status.append(a, ".");
      }
    };
    form.addEventListener("submit", async event => {
      event.preventDefault();
      if (form.dataset.state === "sending") return;
      form.dataset.state = "sending";
      button.disabled = true;
      say("sending", "Sending…");
      try {
        const token = await fetch(`${site}/members/api/integrity-token/`).then(r => {
          if (!r.ok) throw Object.assign(new Error(`HTTP ${r.status}`), { fromServer: true });
          return r.text();
        });
        const response = await fetch(`${site}/members/api/send-magic-link/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: input.value.trim(), emailType: "signup", integrityToken: token }),
        });
        if (!response.ok) {
          // HTTP/2 has no status text, so fall back to the status code.
          const body = await response.json().catch(() => ({}));
          throw Object.assign(new Error(body.errors?.[0]?.message || `HTTP ${response.status}`), { fromServer: true });
        }
        form.reset();
        say("done", "Check your inbox and click the link to confirm your subscription.");
      } catch (error) {
        if (error?.fromServer) {
          // Ghost answered, so its message is worth showing (e.g. "Email is not valid").
          say("error", `Couldn't subscribe. ${error.message.replace(/\.$/, "")}. Try again, or sign up at `, true);
        } else if (navigator.onLine === false) {
          say("error", "You're offline. Reconnect and try again.");
        } else {
          say("error", "Couldn't reach ghuntley.com. Its spam protection refuses sign-ups from some networks, such as VPNs and shared addresses, without saying so. Try another network, or sign up at ", true);
        }
      } finally {
        form.dataset.state = "";
        button.disabled = false;
      }
    });
  };

  const enhance = () => {
    apply();
    document.querySelectorAll("form[data-ghost-site]").forEach(newsletter);
    if (!navigator.clipboard) return;
    document.querySelectorAll("pre[data-copy]").forEach(pre => {
      pre.classList.add("copyable");
      const button = document.createElement("button");
      button.type = "button";
      button.className = "copy-button";
      button.textContent = "copy";
      button.setAttribute("aria-label", "Copy command");
      button.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(copyText(pre));
          button.textContent = "copied ■";
        } catch {
          button.textContent = "copy failed";
        }
        setTimeout(() => { button.textContent = "copy"; }, 1600);
      });
      pre.appendChild(button);
    });
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", enhance);
  else enhance();
})();
