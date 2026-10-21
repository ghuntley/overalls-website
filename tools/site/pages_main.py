from layout import ADR, DOCS, MARK, SOURCE, page


def status(tone):
    return f'<span class="status-label" data-tone="{tone}">{tone.upper()}</span>'


FEATURES = [
    ("Persistent microVMs", "stable",
     "Each machine is a Firecracker guest with its own kernel and a ZFS disk. Stopping it keeps the disk. "
     "Disks go up to 500 GiB."),
    ("NixOS", "stable",
     "The default guest. Declarative and reproducible, with Nix and devenv ready for per-project "
     "environments. You can build your own variant with extra NixOS modules."),
    ("Ubuntu 26.04 LTS", "stable",
     "Built with Nix from pinned package snapshots, so every build of the image is identical. Add your own "
     "packages with a lockfile."),
    ("Windows Server 2025", "stable",
     "Booted from firmware under a patched Firecracker, with guest agents for readiness, SSH and the terminal."),
    ("AlmaLinux", "experimental",
     "A RHEL-compatible guest for teams that build, package and test against Red Hat Enterprise Linux and "
     "its rebuilds. Being built now."),
    ("FreeBSD", "experimental",
     "FreeBSD guests, so BSD software gets developed and tested on a real FreeBSD kernel rather than "
     "emulated in Linux. Being built now."),
    ("illumos", "experimental",
     "illumos guests, the open-source descendant of OpenSolaris, for work on Solaris-heritage systems. "
     "Being built now."),
    ("Tools already installed", "stable",
     "Linux guests come with Podman (Docker-compatible), git and the GitHub CLI, tmux, Neovim, ripgrep, jq, direnv and devenv "
     "installed."),
    ("Browser terminal", "stable",
     "Run many persistent terminals per machine from a browser tab. People you share with start "
     "in watch mode and can take control and hand it back."),
    ("Clients for macOS, Linux and Windows", "stable",
     "The <code>overalls</code> client runs on macOS (Apple Silicon and Intel), Linux (x86_64 and arm64) and "
     "Windows. A one-line installer sets up SSH, and you can connect to any machine, whether it runs NixOS, "
     "Ubuntu or Windows."),
    ("SSH management", "stable",
     "<code>ssh &lt;gateway&gt; new</code>, <code>ls</code>, <code>start</code>, <code>stop</code> "
     "and <code>rm</code>, with <code>--json</code> and retry-safe request IDs for scripts. "
     "One wildcard SSH profile connects you to every guest."),
    ("Share with coworkers", "stable",
     "Give a coworker access to one machine with an access-control role. <strong>Viewers</strong> watch "
     "the terminal, <strong>operators</strong> can also take control of it, and <strong>managers</strong> "
     "can also start, stop, delete and re-share the machine. The owner can't be removed. Cedar checks "
     "every action when it runs, so revoking access takes effect even on pages that are already open."),
    ("Teams", "stable",
     "Owners, admins and members share a pool of machines, integrations and secrets, so a team's "
     "environments don't belong to whoever happened to create them."),
    ("Clone, resize, relocate", "stable",
     "Clone a machine into an independent copy. Resize CPU and memory up or down, and grow the disk. "
     "Move a stopped machine to another host; it keeps its name, identity and address."),
    ("Caching HTTP proxy", "stable",
     "Guest downloads from apt, Nix, pip, npm and the like go through Brady. It fetches only from verified upstreams "
     "and caches public, anonymous responses, so the second machine to install a package gets it from the cache."),
    ("Locked-down profile", "stable",
     "For customer material: no outbound network, no sharing, no web exposure, and SSH for the "
     "owner only."),
    ("Repo launch links", "stable",
     "<code>https://&lt;your-domain&gt;/#https://github.com/OWNER/REPO</code> creates a new machine "
     "with that repo cloned into <code>/workspace/REPO</code>. Add <code>/tree/BRANCH</code>, "
     "<code>/commit/SHA</code> or <code>/pull/N</code> to start from exactly that code. If you aren't signed in, the launch "
     "picks up again after you sign in."),
    ("Browser extension", "stable",
     "The Gitpod workflow on your own hardware. Click the toolbar button on a GitHub, GitLab, Codeberg or "
     "Bitbucket Cloud page (a repository, branch, commit or pull request) and you get a new machine with that "
     "code already cloned. Use one machine per piece of work and delete it when you're done. It works in Chrome, "
     "Firefox and Chromium browsers such as Edge, Brave and Arc, and sends only the page's origin and path."),
    ("Public web apps", "stable",
     "Each machine can serve HTTPS on its own subdomain under <code>apps.&lt;your-domain&gt;</code>. "
     "Audi runs DNS and ingress for this."),
    ("Agent threads", "stable",
     "Overalls' built-in agent works in threads on each machine. Sending a prompt wakes a stopped machine, the "
     "agent's tools run inside the guest, and the work carries on after you close your laptop. It's the Amp orbs "
     "workflow on your own hardware. You can also prompt from your terminal after approving it in the browser."),
    ("Browser editor", "preview",
     "A personal editor built from Microsoft's official Code OSS source, with Open VSX extensions, running as "
     "you inside the guest. It is verified on NixOS; Ubuntu support is partial."),
    ("Claude Code and Codex", "stable",
     "Pre-installed on every guest image that supports them, and ready to use. They're already pointed at "
     "Ziggy, so there's nothing to configure: no API keys or credentials are installed on the machine."),
    ("Inference without keys", "stable",
     "Guests call <code>https://llm.internal</code> for OpenAI and Anthropic models. Ziggy adds the provider "
     "credentials outside the guest and records usage per account, so no API key ever lives in a VM."),
    ("AI usage accounting", "stable",
     "Inference usage is recorded for each user, down to the machine and agent thread. Everyone can keep an "
     "eye on their own usage. Administrators get fleet-wide reports on AI adoption, utilisation and estimated cost, "
     "and can export them to reconcile against their inference provider's bills. Usage that wasn't measured "
     "shows as unknown, never as zero."),
    ("Integrations without keys", "stable",
     "Named integrations at <code>&lt;name&gt;.integration.internal</code> let guests call external APIs and peer "
     "VMs. Galileo adds the credentials at the edge, so a machine can use a secret without being able to read it."),
    ("Node maintenance", "stable",
     "Take a Lilly host out of service without losing anyone's work. Evacuation moves its machines to other "
     "Lilly hosts one at a time; each keeps its identity, disk, sharing and address, and you approve any long "
     "downtime first. A drain stops machines in place instead. When the host is empty you can bring it back "
     "or retire it."),
    ("Hosts near your developers", "stable",
     "Keep the control plane in one region and put Lilly hosts in Washington DC, London, Singapore or wherever "
     "your team works."),
    ("Off-site backups", "stable",
     "Restic backs up to any S3-compatible bucket: guest disks from native ZFS snapshots, a dump of Marshall's "
     "PostgreSQL, host identities and keys. Running guests sync first and are never paused. Built-in checks "
     "read the backups back to prove they restore."),
    ("Inception", "experimental",
     "A 16 vCPU guest that runs a whole Overalls stack inside itself, including nested Firecracker guests. "
     "Useful for developing Overalls within Overalls."),
    ("Multi-host fleet and HA", "stable",
     "Run multiple Marshall instances behind HAProxy against a shared PostgreSQL, and as many Lilly "
     "hosts as you need. If a Marshall instance is lost, running machines keep running and terminal sessions "
     "and sharing recover on the others. Each host keeps itself up to date from Git."),
]

CATEGORIES = [
    ("Machines", ["Persistent microVMs", "Clone, resize, relocate", "Tools already installed", "Caching HTTP proxy", "Locked-down profile"]),
    ("Operating systems", ["NixOS", "Ubuntu 26.04 LTS", "Windows Server 2025", "AlmaLinux", "FreeBSD", "illumos"]),
    ("Working on a machine", ["Browser terminal", "Clients for macOS, Linux and Windows", "SSH management", "Public web apps", "Browser editor"]),
    ("Collaboration", ["Share with coworkers", "Teams"]),
    ("Starting from a repository", ["Repo launch links", "Browser extension"]),
    ("AI", ["Claude Code and Codex", "Inference without keys", "AI usage accounting", "Integrations without keys", "Agent threads"]),
    ("Running the platform", ["Hosts near your developers", "Multi-host fleet and HA", "Node maintenance", "Off-site backups", "Inception"]),
]

REGIONS_DIAGRAM = """\
          ┌─ control plane · one region ───────────────────────────────┐
          │                                                            │
          │  HAProxy ─▶ Marshall · Marshall · Marshall ◀─▶ PostgreSQL  │
          │  several Marshall instances for high availability          │
          │                                                            │
          └──────────────────────────────┬─────────────────────────────┘
                                         ▲
                                         │  HTTPS, dialled out by every host
                                         │
            ┌────────────────────────────┼────────────────────────────┐
 ┌──────────┴──────────┐      ┌──────────┴──────────┐      ┌──────────┴──────────┐
 │ WASHINGTON DC       │      │ LONDON              │      │ SINGAPORE           │
 │ Lilly  Lilly  Lilly │      │ Lilly  Lilly        │      │ Lilly  Lilly        │
 │ guests on ZFS       │      │ guests on ZFS       │      │ guests on ZFS       │
 │ Audi: SSH, web apps │      │ Audi: SSH, web apps │      │ Audi: SSH, web apps │
 └─────────────────────┘      └─────────────────────┘      └─────────────────────┘
            ▲                            ▲                            ▲
      developers in                developers in                developers in
      the Americas                    Europe                    Asia-Pacific"""

PATHS_DIAGRAM = """\
      ┌─ control plane · one region ─────────────────────────────────────────┐
      │  HAProxy ─▶ Marshall · Marshall · Marshall ◀─▶ PostgreSQL            │
      └───────▲──────────────────────────────────────────────────────▲───────┘
              │ web terminal and                  relay over HTTPS,  │
              │ browser editor                 dialled out by Lilly  │
              │                                                      │
 ┌────────────┴────────────┐                          ┌──────────────┴─────────────┐
 │ DEVELOPER IN SINGAPORE  │                          │ HOST IN SINGAPORE          │
 │ browser                 │                          │                            │
 │ ssh, VS Code,           │   direct, same region    │                            │
 │ shared web apps ────────┼─────────────────────────▶│ Audi ─▶ Lilly ─▶ guest     │
 └─────────────────────────┘                          └────────────────────────────┘"""

# Outbound sponsor links carry UTM tags so sponsors can attribute visits to ghuntley.
UTM = "utm_source=ghuntley&amp;utm_medium=referral&amp;utm_campaign=overalls"

LANDING_DIAGRAM = """\
                                ┌───────────────┐ ◀──▶ PostgreSQL
      browser ─HTTPS─▶ proxy ─▶ │    Marshall   │
     ssh ──manage──▶ Porsche ─▶ │ control plane │
                                └───────▲───────┘
                         HTTPS, dialled out by every host
            ┌───────────────────────────┼───────────────────────────┐
 ┌──────────┴─────────┐      ┌──────────┴─────────┐      ┌──────────┴─────────┐
 │ Lilly · host 1     │      │ Lilly · host 2     │      │ Lilly · host N     │
 │ ┌────┐┌────┐┌────┐ │      │ ┌────┐┌────┐       │      │ ┌────┐┌────┐┌────┐ │
 │ │ vm ││ vm ││ vm │ │      │ │ vm ││ vm │       │  ··  │ │ vm ││ vm ││ vm │ │
 │ └────┘└────┘└────┘ │      │ └────┘└────┘       │      │ └────┘└────┘└────┘ │
 │ Firecracker · ZFS  │      │ Firecracker · ZFS  │      │ Firecracker · ZFS  │
 └──────────▲─────────┘      └──────────▲─────────┘      └──────────▲─────────┘
            └───────────────────────────┬───────────────────────────┘
                                        │
ssh · web ────────────────────▶ Audi ───┘  routes each request to the
                                           host running that guest"""


def landing():
    by_name = {name: (name, tone, text) for name, tone, text in FEATURES}
    listed = [n for _, names in CATEGORIES for n in names]
    assert sorted(listed) == sorted(by_name), set(listed) ^ set(by_name)
    order = ["stable", "preview", "experimental"]
    groups = []
    for title, names in CATEGORIES:
        cards = "\n".join(
            f"""<article class="panel">
<header><h4>{name}</h4>{status(tone)}</header>
<p>{text}</p>
</article>"""
            for name, tone, text in sorted((by_name[n] for n in names), key=lambda f: order.index(f[1]))
        )
        groups.append(f'<div class="feature-group">\n<h3>{title}</h3>\n<div class="cols feature-grid">\n{cards}\n</div>\n</div>')
    cards = "\n".join(groups)
    body = f"""<main id="main-content">
<div class="hero">
<div>
<h1>An AI-first developer platform <span class="line">that you own.</span></h1>
<p class="lede">Overalls is a self-hosted platform for development machines and the AI agents that work on them. Every machine is a persistent Firecracker microVM running NixOS, Ubuntu or Windows, and it keeps its disk, name and address when you stop, start, resize, clone or move it.</p>
<p class="lede">Overalls has its own agent built in: start a thread on any machine from the browser or the CLI, and it keeps working after you close your laptop, waking the machine if it was stopped. It's the Amp orbs workflow on hardware you own.</p>
<p class="lede">Claude Code and Codex come pre-installed too, with no API keys on the machine and every token accounted for. Open any repository, branch or pull request in a fresh machine with one click, share it with your coworkers, and work from the browser, SSH, VS Code or the <code>overalls</code> CLI. Put hosts in every region your team works in.</p>
<p class="lede">It's open source under the MIT licence. There is no hosted version to sign up for: you install it and run it yourself.</p>
<div class="row actions">
<a class="console-button primary" href="self-host/index.html">Self-host it →</a>
<a class="console-button" href="{SOURCE}">Source on GitHub <span aria-hidden="true">↗</span></a>
</div>
</div>
<figure>
<pre class="mark" aria-hidden="true">{MARK}</pre>
<figcaption>made to get dirty</figcaption>
</figure>
</div>

<section aria-labelledby="what">
<h2 id="what">What you get</h2>
<p class="legend"><span class="status-label" data-tone="stable">STABLE</span> built and covered by acceptance tests · <span class="status-label" data-tone="preview">PREVIEW</span> works, with rough edges · <span class="status-label" data-tone="experimental">EXPERIMENTAL</span> still being built</p>
{cards}
</section>

<section aria-labelledby="how">
<h2 id="how">How it fits together</h2>
<p>Marshall is the web app and control plane, a Phoenix and Ash application backed by PostgreSQL. Lilly runs on each host. It starts Firecracker guests on ZFS and connects to Marshall over HTTPS to report capacity and receive commands. Porsche handles management over SSH, and Audi serves DNS, guest SSH and web apps. Each guest gets an isolated network, and traffic between guests is blocked.</p>
<figure class="diagram">
<pre role="img" aria-label="Browsers reach Marshall through a TLS proxy and SSH management goes through Porsche. Marshall uses PostgreSQL. Several hosts each run Lilly, which dials out to Marshall over HTTPS and runs Firecracker guests on ZFS. Audi routes guest SSH and web traffic to whichever host runs the guest.">{LANDING_DIAGRAM}</pre>
<figcaption>One control plane, many hosts. Add a host and Marshall starts placing machines on it. <a href="architecture.html">Full architecture →</a></figcaption>
</figure>
</section>

<section aria-labelledby="regions">
<h2 id="regions">Close to your developers</h2>
<p>Run the control plane in one region and put Lilly hosts wherever your developers are. Marshall and PostgreSQL stay together, with several Marshall instances for high availability. Lilly hosts can go anywhere, for example Washington DC, London and Singapore, and each one dials out to the control plane over HTTPS.</p>
<figure class="diagram">
<pre role="img" aria-label="The control plane runs in one region: HAProxy in front of several Marshall instances and one PostgreSQL. Lilly hosts in Washington DC, London and Singapore each dial out to it over HTTPS. Each region's hosts run guests on ZFS and Audi for SSH and web apps, serving developers in the Americas, Europe and Asia-Pacific.">{REGIONS_DIAGRAM}</pre>
<figcaption>Centralise the control plane; distribute the hosts.</figcaption>
</figure>
<p>There are two ways into a machine. <strong>SSH and shared web apps go direct</strong>: <code>ssh</code>, VS Code over Remote-SSH, and the web apps a machine shares connect to Audi on the machine's own host, so they stay in the region and get local latency. <strong>The web interface goes through the control plane</strong>: the browser terminal and the browser editor are relayed by Marshall, so they cross regions when the control plane is far away.</p>
<figure class="diagram">
<pre role="img" aria-label="A developer in Singapore uses a machine on a host in Singapore. The browser terminal and browser editor go up to the control plane, which relays to the host over a connection Lilly dialled out. SSH, VS Code and shared web apps connect directly to Audi on the Singapore host.">{PATHS_DIAGRAM}</pre>
<figcaption>For the lowest latency, use SSH, VS Code or a shared web app. The browser terminal is there for when you're away from your laptop.</figcaption>
</figure>
</section>

<section aria-labelledby="taste">
<h2 id="taste">A taste</h2>
<p>Every management command works in the browser, at an interactive SSH prompt or as a one-off <code>ssh</code> command. Add <code>--json</code> when a script (or agent) is reading the output.</p>
<pre class="term" data-copy><span class="prompt">$ </span>ssh &lt;gateway&gt; new --name scratch
<span class="prompt">$ </span>ssh &lt;gateway&gt; ls
<span class="prompt">$ </span>ssh &lt;gateway&gt; resize scratch --cpu 4 --memory 8192
<span class="prompt">$ </span>ssh &lt;gateway&gt; clone scratch --name scratch-copy --request-id copy-1 --no-wait
<span class="prompt">$ </span>ssh &lt;gateway&gt; share add scratch colleague@example.com operator
<span class="prompt">$ </span>overalls open https://github.com/OWNER/REPO</pre>
<p class="muted"><code>&lt;gateway&gt;</code> is your own deployment's domain: Porsche listens on port 22 of your Marshall hosts. See <a href="self-host/first-machine.html">your first machine</a>.</p>
</section>

<section aria-labelledby="run">
<h2 id="run">Run it yourself</h2>
<p>Overalls is a set of NixOS modules plus tools for installing and enrolling bare-metal hosts. Your fleet is defined in a Git repository: you fork Overalls, declare your hosts, and each host keeps itself up to date from your <code>main</code> branch. You can start with one server and add hosts later. To make the installation your own (patch a component, pin a package, add tools to the guest images), use <a href="https://ghuntley.com/nix/?{UTM}">Nix overlays <span aria-hidden="true">↗</span></a> in your fork.</p>
<ol class="steps">
<li data-state="current"><span class="step-marker" aria-hidden="true"></span><a href="self-host/index.html">Read the requirements and fork the repo</a></li>
<li><span class="step-marker" aria-hidden="true"></span><a href="self-host/provision.html">Install NixOS on a bare-metal host</a></li>
<li><span class="step-marker" aria-hidden="true"></span><a href="self-host/deploy.html">Deploy Marshall, PostgreSQL, email and TLS</a></li>
<li><span class="step-marker" aria-hidden="true"></span><a href="self-host/dns.html">Point your domain and delegate apps.&lt;your-domain&gt; to Audi</a></li>
<li><span class="step-marker" aria-hidden="true"></span><a href="self-host/enroll.html">Enroll Lilly hosts and publish guest images</a></li>
<li><span class="step-marker" aria-hidden="true"></span><a href="self-host/first-machine.html">Sign in and create your first machine</a></li>
<li><span class="step-marker" aria-hidden="true"></span><a href="self-host/operations.html">Updates, drains, backups and logs</a></li>
</ol>
<dl class="kv">
<div><dt>Hardware</dt><dd>x86_64 bare metal with a working <code>/dev/kvm</code>. The bootstrap tool can discover Hetzner dedicated and EC2 bare-metal servers.</dd></div>
<div><dt>Operating system</dt><dd>NixOS 26.05, installed for you from a rescue or Ubuntu system</dd></div>
<div><dt>Storage</dt><dd>ZFS, which holds the guest disks</dd></div>
<div><dt>Services</dt><dd>PostgreSQL with TLS, and an authenticated SMTP relay for sign-in links</dd></div>
<div><dt>Network</dt><dd>A domain you control, with <code>apps.&lt;your-domain&gt;</code> delegated to Audi. Certificates come from ACME.</dd></div>
<div><dt>Your laptop</dt><dd>Nix with flakes, and a Git server your hosts can read from</dd></div>
</dl>
</section>

<section aria-labelledby="who">
<h2 id="who">Who is behind Overalls</h2>
<p>Overalls is built by <a href="https://ghuntley.com/?{UTM}">Geoffrey Huntley <span aria-hidden="true">↗</span></a>, a software engineer who writes about AI-assisted software development. He created the <a href="https://ghuntley.com/ralph/?{UTM}">Ralph loop <span aria-hidden="true">↗</span></a>, which runs a coding agent in a loop until the work is done and is the technique <a href="https://ghuntley.com/loop/?{UTM}">loop engineering <span aria-hidden="true">↗</span></a> grew out of. He also defined <a href="https://ghuntley.com/pressure/?{UTM}">agent back pressure <span aria-hidden="true">↗</span></a>: letting compilers, tests and type checkers push back on an agent's output so it corrects itself.</p>
</section>

<section aria-labelledby="newsletter">
<h2 id="newsletter">Stay in the loop</h2>
<p>Get updates on new features, integrations and security fixes, by email.</p>
<form class="newsletter-form" action="https://ghuntley.com/newsletter/" method="get" data-ghost-site="https://ghuntley.com">
<label for="newsletter-email" class="sr-only">Email address</label>
<input id="newsletter-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
<button type="submit" class="console-button primary">Subscribe</button>
</form>
<p class="newsletter-status muted" role="status" aria-live="polite">Unsubscribe any time. Sent from <a href="https://ghuntley.com/?{UTM}">ghuntley.com <span aria-hidden="true">↗</span></a>.</p>
</section>

<section aria-labelledby="sponsors">
<h2 id="sponsors">Donors and sponsors</h2>
<p>Overalls is built with support from these organisations. Thank you.</p>
<dl class="kv sponsors">
<div><dt><a href="https://antithesis.com/?{UTM}">Antithesis <span aria-hidden="true">↗</span></a></dt><dd>Autonomous, deterministic testing that finds <a href="https://antithesis.com/blog/2026/time-traveling-agents/?{UTM}">the bugs that AI misses <span aria-hidden="true">↗</span></a>.</dd></div>
<div><dt><a href="https://www.cachix.org/?{UTM}">Cachix <span aria-hidden="true">↗</span></a></dt><dd>Binary Nix caching, so installation is fast.</dd></div>
<div><dt><a href="https://namespace.so/?{UTM}">Namespace Labs <span aria-hidden="true">↗</span></a></dt><dd>Fast CI that builds Overalls and publishes the results to Cachix.</dd></div>
</dl>
</section>

<section aria-labelledby="faq" class="faq">
<h2 id="faq">Questions</h2>
<details>
<summary>Is there a hosted Overalls I can sign up for?</summary>
<p>No. Overalls is software you run on your own machines, and this site is the project's home page. Any "sign in" mentioned in these docs is your own deployment's sign-in page.</p>
</details>
<details>
<summary>What does it cost?</summary>
<p>Nothing. It's MIT-licensed; you pay for your own hardware, bandwidth, email relay and inference. Ziggy forwards model calls to OpenAI and Anthropic using your own provider accounts. If you'd rather not pay per token, <a href="https://github.com/ghuntley/underclass">Underclass <span aria-hidden="true">↗</span></a> lets you pool your team's OpenAI subscriptions instead.</p>
</details>
<details>
<summary>Can I run it on a single server?</summary>
<p>Yes. A single Marshall instance with local PostgreSQL is a supported deployment, though it has no redundancy (<a href="{ADR}0048-single-host-service-deployment.md">ADR-0048 ↗</a>). You can add Lilly hosts later. A resilient deployment needs independent hosts and a tested plan for database recovery.</p>
</details>
<details>
<summary>Why Firecracker rather than containers?</summary>
<p>Each machine gets its own kernel, its own disk and an isolated network, so you can run Podman, systemd services or anything else that expects a real Linux machine. A machine with a working setup stays that way between sessions.</p>
</details>
<details>
<summary>Does it need Kubernetes?</summary>
<p>No. It's NixOS modules, systemd units and a few Elixir and Rust services. Hosts install from a reviewed plan and then poll your Git repository for updates.</p>
</details>
<details>
<summary>Why "Overalls"?</summary>
<p>They're workwear: what you put on before getting your hands dirty. The first production host was also called <code>overalls</code>, and its sibling is <code>dungarees</code>.</p>
</details>
</section>
</main>
"""
    return page(
        "Overalls",
        "Overalls is an open-source, self-hosted platform for persistent Firecracker development machines and the AI agents that work on them.",
        body,
        path="",
    )


ARCH_CONTROL = """\
                 ┌──────────────────────────────────────────┐
 browser ─HTTPS─▶│ HAProxy  TLS, ACME, verified backends    │
                 └────────────────────┬─────────────────────┘
                                      ▼
 ssh ──────────▶ Porsche ───▶ ┌────────────────┐     ┌────────────┐
 overalls CLI ──────────────▶ │ Marshall × 1…N │◀───▶│ PostgreSQL │
                              │ Phoenix · Ash  │     └────────────┘
                              │ Cedar · Oban   │
                              └───────▲────────┘
                                      │ HTTPS, per-host credential
                                      │ reports up · commands down
                        ┌─────────────┴─────────────┐
                 ┌──────┴──────┐             ┌──────┴──────┐
                 │ Lilly host  │     · · ·   │ Lilly host  │
                 │ ZFS · KVM   │             │ ZFS · KVM   │
                 └─────────────┘             └─────────────┘"""

ARCH_LIFECYCLE = """\
  new ─▶ [pending] ─▶ [running] ◀─── start ─── [stopped]
                        │    │                    ▲  │
                        │    └─── stop ───────────┘  │
                        │                            ├─ relocate ─▶ another host
                     resize                          ├─ clone ────▶ new machine
           stop · apply · restart                    ├─ resize ───▶ at next boot
                                                     └─ rm ───────▶ disk deleted"""

ARCH_GUEST = """\
  ┌─ guest ──────────────────────────┐
  │  apt · nix · pip · npm ──────────┼──▶ Brady    proxy, cache ──▶ internet
  │  git clone ──────────────────────┼──▶ Enrico   GitHub mirror
  │  https://llm.internal ───────────┼──▶ Ziggy    ──▶ OpenAI, Anthropic
  │  https://x.integration.internal ─┼──▶ Galileo  adds credentials
  └──────────────────────────────────┘
    secrets stay outside the guest; usage is recorded per account"""

COMPONENTS = [
    ("Marshall", "marshall/", "Web app and control plane (Elixir, Phoenix, Ash)",
     "Accounts with magic links and passkeys, Cedar authorization, machine lifecycle, scheduling, sharing, teams, the browser terminal and agent threads."),
    ("Lilly", "lilly/", "Host provisioner (Elixir)",
     "Runs Firecracker guests on ZFS behind jailed, isolated networks, with a durable actor for each VM. Guests keep running when Lilly restarts."),
    ("Porsche", "porsche/", "SSH management gateway",
     "<code>ssh &lt;gateway&gt; &lt;command&gt;</code> manages machines with the same account and permissions as the web."),
    ("Audi", "audi/", "DNS and ingress",
     "Authoritative DNS, guest SSH, and public HTTPS for each machine's web apps."),
    ("Brady", "brady/", "Egress proxy and cache",
     "Guest downloads go through verified upstreams, and public anonymous responses are cached."),
    ("Enrico", "enrico/", "Private GitHub mirror",
     "Speeds up checkouts and powers the repository browser."),
    ("Galileo", "galileo/", "Integration gateway",
     "Named integrations at <code>&lt;name&gt;.integration.internal</code>; credentials are added at the edge."),
    ("Ziggy", "ziggy/", "Inference proxy",
     "<code>llm.internal</code> for guests, with no provider keys inside the VM and usage recorded per account."),
    ("Lyra", "lyra/", "CLI and guest tools (Rust)",
     "The <code>overalls</code> CLI: wildcard SSH, <code>open</code> for repos, <code>agent</code> prompts. It also runs the agent's tools inside the guest."),
    ("Marvin", "marvin/", "Browser extension",
     "Opens the repository page you're on in your Overalls deployment."),
    ("Mila", "mila/", "Desktop and mobile client (Flutter)",
     "Manages machines over one SSH connection to Porsche, signs in by approving a device key in the browser, and opens <code>overalls://</code> links on iOS, Android, macOS and Windows."),
    ("Susan", "susan/", "Push notification relay",
     "Relays end-to-end encrypted Mila notifications to APNs, FCM and WNS without seeing their content."),
    ("Peach", "peach/", "Guest reflection service",
     "Serves <code>reflection.internal</code>: a secret-free view of the integrations a running guest may use, authorized by Marshall. Opt-in for each host, with a credential issued by Marshall; the private-services certificate must also cover <code>reflection.internal</code>."),
    ("Protocol", "protocol/", "Shared wire schemas",
     "Validates the messages services exchange, so their interfaces stay consistent."),
    ("Fleet and Nix", "fleet/ nix/", "Declarative infrastructure",
     "NixOS modules, host inventory, guest images, secrets, and the host install and enroll tools."),
]

ADRS = [
    ("0018-persisted-sharing-and-user-machine-access.md", "Persisted sharing and machine access"),
    ("0022-browser-terminal-and-live-login-checks.md", "Browser terminal and live login checks"),
    ("0030-nixos-deployment-and-tls.md", "NixOS deployment and TLS"),
    ("0036-automatic-host-updates.md", "Automatic host updates"),
    ("0043-declarative-host-provisioning.md", "Declarative host provisioning"),
    ("0048-single-host-service-deployment.md", "Single-host service deployment"),
    ("0055-queued-machine-cloning.md", "Queued machine cloning"),
    ("0077-teams-and-shared-resources.md", "Teams and shared resources"),
    ("0128-repository-launch-links.md", "Repository launch links"),
    ("0153-official-source-browser-editor.md", "Official-source browser editor"),
    ("0155-stopped-only-relocation.md", "Stopped-only relocation"),
    ("0161-monospace-web-presentation.md", "Monospace Web presentation"),
]


def architecture():
    rows = "\n".join(
        f'<tr><td class="width-min" data-label="Name:"><strong>{n}</strong><br><code class="muted">{d}</code></td>'
        f'<td data-label="Role:">{role}</td><td class="width-auto" data-label="Gives you:">{gives}</td></tr>'
        for n, d, role, gives in COMPONENTS
    )
    adrs = "\n".join(
        f'<li><a href="{ADR}{f}">ADR-{f[:4]} · {t} <span aria-hidden="true">↗</span></a></li>' for f, t in ADRS
    )
    body = f"""<main id="main-content">
<div class="prose">
<h1>Architecture</h1>
<p>Overalls is a monorepo of small services, each named after something or someone, with one NixOS deployment that wires them together. Marshall holds the record of what should exist. Lilly hosts make it physically true and report back. The other services sit at the edges: SSH, DNS, egress, inference, integrations, clients and notifications.</p>
</div>

<section aria-labelledby="components">
<h2 id="components">Components</h2>
<table class="table-stack">
<thead><tr><th>Name</th><th>Role</th><th>What it gives you</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</section>

<section aria-labelledby="planes">
<h2 id="planes">Control plane and hosts</h2>
<div class="prose">
<p>You can run multiple Marshall instances against a shared PostgreSQL. Machine capacity is admitted atomically, so concurrent requests can't overbook a host. Every lifecycle change is a durable operation with an audit trail. Each host's Lilly dials out to Marshall with its own revocable credential, sends capacity reports and receives commands. A generation fence stops a delayed launch from starting a guest after a stop has already been requested.</p>
</div>
<figure class="diagram">
<pre role="img" aria-label="Browsers go through HAProxy to one or more Marshall instances. SSH and the CLI go through Porsche. Marshall uses PostgreSQL. Several Lilly hosts each connect to Marshall over HTTPS to send reports and receive commands.">{ARCH_CONTROL}</pre>
<figcaption>Marshall decides; Lilly does the work and reports back.</figcaption>
</figure>
</section>

<section aria-labelledby="arch-regions">
<h2 id="arch-regions">Regions</h2>
<div class="prose">
<p>We recommend running Marshall in a single region. Its instances share one PostgreSQL, and admission, sharing and lifecycle decisions all depend on that database, so keep them close to it. Run several instances in that region for high availability.</p>
<p>Lilly hosts have no such constraint. Each one only needs to reach Marshall over HTTPS, so you can put hosts in every region where your developers work.</p>
<p>Where the traffic goes depends on how you connect. SSH, VS Code over Remote-SSH, and the web apps a machine shares enter through Audi on the machine's own host and stay in that region. The browser terminal and browser editor are relayed through Marshall, over the connection the host dialled out, so they pay the round trip to the control-plane region.</p>
</div>
<figure class="diagram">
<pre role="img" aria-label="The control plane runs in one region: HAProxy in front of several Marshall instances and one PostgreSQL. Lilly hosts in Washington DC, London and Singapore each dial out to it over HTTPS. Each region's hosts run guests on ZFS and Audi for SSH and web apps, serving developers in the Americas, Europe and Asia-Pacific.">{REGIONS_DIAGRAM}</pre>
<figcaption>One control-plane region, hosts wherever they're needed.</figcaption>
</figure>
<figure class="diagram">
<pre role="img" aria-label="A developer in Singapore uses a machine on a host in Singapore. The browser terminal and browser editor go up to the control plane, which relays to the host over a connection Lilly dialled out. SSH, VS Code and shared web apps connect directly to Audi on the Singapore host.">{PATHS_DIAGRAM}</pre>
<figcaption>SSH and shared web apps go direct; the web interface goes by way of the control plane.</figcaption>
</figure>
</section>

<section aria-labelledby="lifecycle">
<h2 id="lifecycle">A machine's life</h2>
<div class="prose">
<p>A machine is an identity first and a process second. Its UUID, name, private address, sharing and disk outlive any particular Firecracker process, so stopping, resizing and relocating it don't create a new machine. Cloning does: the copy is private, gets a fresh address and starts without the source's RAM.</p>
</div>
<figure class="diagram">
<pre role="img" aria-label="A new machine goes from pending to running. Running machines can be stopped or resized. Stopped machines can be started, relocated to another host, cloned into a new private machine, or deleted.">{ARCH_LIFECYCLE}</pre>
<figcaption>Every transition is a durable request with an ID you can retry.</figcaption>
</figure>
</section>

<section aria-labelledby="guest">
<h2 id="guest">From inside a guest</h2>
<div class="prose">
<p>Guests reach the outside world only through services that can check, cache and record the traffic. Lateral traffic between guests and to private address ranges is blocked by Lilly's nftables policy. The locked-down customer profile removes outbound networking entirely.</p>
</div>
<figure class="diagram">
<pre role="img" aria-label="Package downloads from a guest go through Brady, git clones through Enrico, inference calls through Ziggy, and integration calls through Galileo, which adds credentials so the guest never sees them.">{ARCH_GUEST}</pre>
<figcaption>Credentials are added at the edge, never handed to the guest.</figcaption>
</figure>
</section>

<section aria-labelledby="principles">
<h2 id="principles">Principles</h2>
<div class="prose">
<ul>
<li><strong>Declared, reviewed, then applied.</strong> Hosts, images, users and secret recipients live in Git. Hosts install from a reviewed plan and update from a pinned branch.</li>
<li><strong>Make it your own.</strong> Your fork is yours to change. Patch a component, pin a package or add tools to the guest images with a <a href="https://ghuntley.com/nix/?{UTM}">Nix overlay <span aria-hidden="true">↗</span></a> rather than carrying a long-lived fork of the code.</li>
<li><strong>Secrets never travel in the clear.</strong> SOPS and age documents are encrypted to each host's SSH-derived key and to named recovery users. Private keys are generated where they're used.</li>
<li><strong>Authority is checked at execution time.</strong> Cedar policies are evaluated when each action runs, not when a page was loaded, so revoked access takes effect on pages that are already open.</li>
<li><strong>Uncertainty is explicit.</strong> If a request might not have reached a host, the system asks for deliberate reconciliation rather than guessing.</li>
</ul>
</div>
</section>

<section aria-labelledby="adrs">
<h2 id="adrs">Decision records</h2>
<div class="prose">
<p>Every design decision is written up as an architecture decision record (ADR), with a review recording the evidence. There are over 170 of them. Some good places to start:</p>
<ul>
{adrs}
</ul>
<p><a href="{SOURCE}/tree/main/docs/architecture/decisions">All decision records <span aria-hidden="true">↗</span></a> · <a href="{DOCS}architecture/README.md">Implementation status <span aria-hidden="true">↗</span></a></p>
</div>
</section>
</main>
"""
    return page(
        "Architecture",
        "How Overalls fits together: Marshall, Lilly, Porsche, Audi and the guest-edge services.",
        body,
        current="architecture",
        path="architecture.html",
    )


def not_found():
    body = f"""<main id="main-content" class="error-page">
<pre class="mark" aria-hidden="true">{MARK}</pre>
<h1>Not found</h1>
<p>There's nothing at this address. It may have moved while we were tidying the workshop.</p>
<p><a class="console-button primary" href="/index.html">← Back home</a></p>
</main>
"""
    return page("Not found", "Page not found.", body, r="/")
