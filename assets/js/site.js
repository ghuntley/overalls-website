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

  const enhance = () => {
    apply();
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
