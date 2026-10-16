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
  // calls Ghost's own embeddable signup form makes. Without JS the form falls
  // back to opening ghuntley.com/newsletter/.
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
        a.href = `${site}/newsletter/`;
        a.textContent = "ghuntley.com/newsletter ↗";
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
          if (!r.ok) throw new Error(r.statusText);
          return r.text();
        });
        const response = await fetch(`${site}/members/api/send-magic-link/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: input.value.trim(), emailType: "signup", integrityToken: token }),
        });
        if (!response.ok) {
          const body = await response.json().catch(() => ({}));
          const failure = new Error(body.errors?.[0]?.message || response.statusText);
          failure.fromServer = true;
          throw failure;
        }
        form.reset();
        say("done", "Check your inbox and click the link to confirm your subscription.");
      } catch (error) {
        // Rate limits and outages arrive without CORS headers and surface as a bare
        // network error, so only Ghost's own validation messages are shown verbatim.
        const reason = error?.fromServer && error.message
          ? `${error.message.replace(/\.$/, "")}. `
          : "The newsletter service didn't respond, possibly because it's limiting sign-ups from your network. Wait a while and ";
        say("error", `Couldn't subscribe. ${reason}${error?.fromServer ? "Try" : "try"} again, or sign up at `, true);
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
