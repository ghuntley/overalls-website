import html
from layout import ADR, DOCS, SOURCE, SOURCE_BLOB, SOURCE_BRANCH, guide_page


def ref(doc, label=None):
    url = SOURCE_BLOB + doc[3:] if doc.startswith("../") else DOCS + doc
    return f'<p class="muted">Full reference: <a href="{url}">{label or doc} <span aria-hidden="true">↗</span></a></p>'


def facts(*pairs):
    rows = "\n".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in pairs)
    return f'<dl class="kv">\n{rows}\n</dl>\n'


def sh(text):
    lines = html.escape(text, quote=False).strip("\n").split("\n")
    out = []
    for line in lines:
        if line.startswith("# "):
            out.append(f'<span class="prompt out">{line}</span>')
        else:
            out.append(line)
    return '<pre data-copy>' + "\n".join(out) + "</pre>\n"


def code(text):
    return "<pre data-copy>" + html.escape(text, quote=False).strip("\n") + "</pre>\n"




def overview():
    body = f"""<h1>Self-host Overalls</h1>
<p>Overalls runs on hardware you control and nowhere else. This guide covers going from a bare-metal server to signing in and starting your first machine. It's a summary: each page links to the full operator documentation in the repository, which is the source of truth.</p>
{facts(
    ("Audience", "Operators who are comfortable with NixOS, SSH and PostgreSQL"),
    ("Time", "An afternoon for one host, if your DNS and email relay are ready"),
)}
<h2>What you're building</h2>
<ul>
<li><strong>Marshall</strong>: the web app and control plane, behind HAProxy with ACME certificates, using PostgreSQL and an SMTP relay.</li>
<li><strong>Lilly</strong> on every host: runs Firecracker guests on a ZFS pool.</li>
<li><strong>Porsche</strong>: the SSH management gateway. <strong>Audi</strong>: DNS, guest SSH and public web apps.</li>
<li>Optional edge services: Brady (egress cache), Enrico (GitHub mirror), Ziggy (inference) and Galileo (integrations).</li>
</ul>
<p>Every role can run on one host. A deployment with redundancy spreads Marshall across at least three hosts with a highly available database.</p>

<h2>Your fleet is a Git repository</h2>
<p>Each host polls the <code>{SOURCE_BRANCH}</code> branch of a Git repository you control, builds its own Buck2 deployment target, applies migrations, switches and checks its own health. So step one is to fork Overalls and make the fleet yours:</p>
<ol>
<li>Fork <a href="{SOURCE}">{SOURCE.removeprefix("https://")} <span aria-hidden="true">↗</span></a> to a Git server your hosts can reach over SSH.</li>
<li>Replace the example hosts in <code>fleet/hosts/</code> with your own. The <code>fleet/roles/control-plane/</code> modules and <code>fleet/hosts/panterloons/</code> show the control-plane configuration; <code>fleet/hosts/dungarees/</code> is a worker.</li>
<li>Put operators and recovery users in <code>nix/policy/identity/users.nix</code>. Declare host roles in <code>nix/policy/fleet/</code> and reviewed network sources in <code>nix/policy/network/allowed-hosts.nix</code>. Public addresses live in the encrypted <code>fleet-addresses</code> document, with logical names in <code>nix/policy/network/fleet-addresses.nix</code>.</li>
<li>Commit and push to <code>{SOURCE_BRANCH}</code>. Encrypted secrets live under <code>secrets/</code>; plaintext never goes in the repo.</li>
</ol>
<p>Buck2 is the build entry point. Nix supplies the pinned toolchains and dependencies and assembles the NixOS systems and guest images.</p>

<h2>Requirements</h2>
{facts(
    ("Hosts", "x86_64 bare metal with a working <code>/dev/kvm</code>. The bootstrap tool knows Hetzner dedicated and EC2 bare metal. The target needs root (or passwordless sudo), Python 3, OpenSSH, <code>lsblk</code> and <code>iproute2</code>."),
    ("Disks", "Two system disks on Hetzner, or the root EBS volume on EC2. Guest disks live on native ZFS."),
    ("Database", "PostgreSQL, reached over verified TLS"),
    ("Email", "An SMTP relay with authentication and verified TLS (implicit TLS or STARTTLS), for magic-link sign-in"),
    ("DNS", "A domain you control. The apex points at your Marshall hosts and <code>apps.&lt;your-domain&gt;</code> is delegated to Audi. See <a href=\"dns.html\">Set up DNS</a>."),
    ("Laptop", "Nix with flakes, a checkout of your fork, and an Ed25519 operator SSH key"),
)}

<h2>The path</h2>
<ol class="steps">
<li data-state="current"><span class="step-marker" aria-hidden="true"></span>Overview and requirements (this page)</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="provision.html">Provision a host</a>: discover, review, plan, install, enroll</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="deploy.html">Deploy the control plane</a>: modules, secrets, database, email, TLS</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="dns.html">Set up DNS</a>: apex records and the Audi delegation</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="enroll.html">Enroll hosts and images</a>: Lilly credentials, guest images, Porsche</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="first-machine.html">Your first machine</a>: sign in, SSH keys, CLI, terminal</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="operations.html">Day-two operations</a>: updates, drains, backups, logs</li>
</ol>
{ref("operations/deployment.md", "docs/operations/deployment.md")}
"""
    return guide_page("index.html", "Self-host", "How to run Overalls on your own bare-metal hardware.", body)


def provision():
    body = f"""<h1>Provision a host</h1>
<p>The bootstrap tool, <code>tools/buck2 run //:host</code>, turns a rented server in rescue mode into a NixOS host that installs from a reviewed plan and then updates itself. It never trusts a new SSH key automatically and never formats a disk you haven't approved.</p>
{facts(
    ("Commands", "<code>discover</code> · <code>plan</code> · <code>install</code> · <code>enroll</code> · <code>verify</code>"),
    ("Inventory", "<code>fleet/hosts/NAME/host.json</code> and <code>BUCK</code>, plus an optional <code>configuration.nix</code> for roles"),
)}
<h2>1. Discover</h2>
<p>Get the rescue system's Ed25519 host key through a trusted channel and put it in its own known-hosts file. Then record what the machine has:</p>
{sh('''tools/buck2 run //:host -- discover --platform hetzner --name example \\
  --target root@HOST --known-hosts /private/rescue-known-hosts \\
  --identity /private/operator-key --output /private/example.candidate.json''')}
<p>Use <code>--platform ec2</code> for EC2 bare metal. Discovery won't overwrite an existing file. It suggests a network configuration (DHCP on EC2, interface addresses on Hetzner) for you to review.</p>

<h2>2. Review and declare</h2>
<p>Copy the candidate to <code>fleet/hosts/NAME/host.json</code> and finish it by hand:</p>
<ul>
<li>Set <code>reviewed</code> to true once you've checked the hardware, firmware and networking.</li>
<li>Choose <code>storage.system</code> by disk ID: two physical disks on Hetzner, or the existing root EBS volume on EC2. On EC2, list the local NVMe IDs in <code>storage.guests</code>.</li>
<li>Give <code>identity.hostId</code> a persistent, nonzero eight-digit hex value. Leave <code>identity.sshKeys</code> empty for now.</li>
<li>Set <code>budgets.guestCpuCores</code>, <code>guestMemoryMiB</code> and <code>arcMaxMiB</code>, and on Hetzner a reviewed <code>storage.quotaBytes</code>.</li>
<li>Set <code>git.repository</code> to your fork's SSH URL and add your Git server's known-host lines to <code>git.knownHosts</code>. Private keys never go in the declaration.</li>
</ul>
<p>Add <code>fleet/hosts/NAME/BUCK</code> so the installer, enrollment tool and updater can build this host's targets:</p>
{code('''load("@root//buck:fleet.bzl", "fleet_host")

fleet_host()''')}
<p>If the host will run Lilly, declare that role now (see <a href="enroll.html">enroll hosts</a>), then commit and push to <code>{SOURCE_BRANCH}</code>. Planning only accepts a commit that has been pushed to <code>{SOURCE_BRANCH}</code>.</p>

<h2>3. Plan</h2>
<p>Use your fork's SSH URL for <code>&lt;repository-ssh-url&gt;</code>, matching <code>git.repository</code> in the declaration:</p>
{sh('''tools/buck2 run //:host -- plan --host example --revision FULL_COMMIT \\
  --repository <repository-ssh-url> \\
  --target root@HOST --known-hosts /private/rescue-known-hosts \\
  --identity /private/operator-key --output /private/example.plan.json''')}
<p>The plan pins the declaration, the authenticated target key, the firmware, the revision, the exact system, disk-layout and kexec paths, and the list of disks it will erase. Read it. Everything is built before anything destructive happens.</p>

<h2>4. Install</h2>
{sh('''tools/buck2 run //:host -- install --plan /private/example.plan.json --erase PLAN_SHA256 \\
  --target root@HOST --known-hosts /private/rescue-known-hosts \\
  --identity /private/operator-key''')}
<p>The installer kexecs into a pinned image, compares the disk inventory again and formats under a lock. It refuses if a device is mounted or a pool is imported. The new host key is generated on the host; only its public half comes back, recorded in <code>PLAN.installed.json</code>. <strong>Keep that file.</strong> An interrupted install never resumes formatting silently.</p>

<h2>5. Enroll and verify</h2>
<p>Record the installed public key in <code>identity.sshKeys</code> and in a new known-hosts file. Add <code>{{"name":"example-git","path":"secrets/example-git.enc.json"}}</code> to <code>credentials</code>. Prepare a JSON document at <code>/private/example-git.json</code>, outside the checkout and Nix store, readable only by you. Its structure is:</p>
{code('''{"overalls-git":{"production":{"GIT_DEPLOY_KEY":"<complete SSH deploy key>"}}}''')}
<p>Use the complete read-only deploy key, with its line breaks encoded as JSON string escapes. Encrypt the document to the authenticated host and recovery recipients:</p>
{sh('''tools/buck2 run //:secrets -- encrypt example-git --input /private/example-git.json''')}
<p>Push the updated declaration and ciphertext, then activate that exact commit and check it:</p>
{sh('''tools/buck2 run //:host -- enroll --host example --revision ENROLLED_FULL_COMMIT \\
  --repository <repository-ssh-url> \\
  --install-receipt /private/example.plan.json.installed.json \\
  --target YOU@HOST --known-hosts /private/installed-known-hosts \\
  --identity /private/operator-key
tools/buck2 run //:host -- verify --target YOU@HOST \\
  --known-hosts /private/installed-known-hosts --identity /private/operator-key''')}
<p><code>YOU</code> is your own account name from <code>nix/policy/identity/users.nix</code>. Remove the private plaintext document when encryption succeeds.</p>
<p>From here the host polls <code>{SOURCE_BRANCH}</code> every ten seconds, with jitter. Changes to the platform, firmware, disks or identity are rejected by ordinary updates; those need deliberate maintenance.</p>
{ref("operations/host-provisioning.md", "docs/operations/host-provisioning.md")}
"""
    return guide_page("provision.html", "Provision a host", "Install NixOS on a bare-metal Overalls host from a reviewed plan.", body)


def deploy():
    body = f"""<h1>Deploy the control plane</h1>
<p>Marshall and Lilly are NixOS modules exported by the flake. Enabling one doesn't enable the other. The host's <code>configuration.nix</code> chooses its roles, and secrets arrive as encrypted documents that are decrypted on the host.</p>
{facts(
    ("Modules", "<code>nixosModules.default</code>, or individual modules under <code>nixosModules.services</code>, <code>.network</code>, <code>.security</code> and <code>.storage</code>"),
    ("Target", "<code>x86_64-linux</code>, NixOS 26.05"),
)}
<h2>1. Build and check</h2>
{sh('''tools/buck2 build //:package-service-marshall //:package-service-lilly
tools/buck2 build //:check-marshall-release
tools/buck2 build //:check-lilly-release
tools/buck2 build //:check-module-configuration''')}
<p>Run these commands from your fork. The <code>tools/buck2</code> wrapper selects the pinned Buck2 and toolchains. Release compilation has no network access, and dependency hashes are pinned. No production secrets are needed to build.</p>

<h2>2. Enable Marshall</h2>
{code('''{
  imports = [ overalls.nixosModules.default ];
  services.marshall = {
    enable = true;
    publicHost = "example.com";
    replicaCount = 3;
    databaseConnectionBudget = 43;
    environmentFile = "/run/overalls-secrets/marshall.env";
    instances.node01 = {
      port = 4443;
      fleetPort = 5443;
      fleetBindAddress = "10.90.0.1";
      fleetLoopback = true;
      certificateFile = "/run/overalls-secrets/backend.crt";
      keyFile = "/run/overalls-secrets/backend.key";
    };
  };
}''')}
<p>Here <code>overalls</code> is your flake input for the fork. Import <code>overalls.nixosModules.services.marshall</code> or <code>overalls.nixosModules.services.lilly</code> when you want an individual service. For a single server, set <code>replicaCount = 1</code> and use local PostgreSQL; that's the supported nonredundant layout (<a href="{ADR}0048-single-host-service-deployment.md">ADR-0048 ↗</a>). With automatic updates enabled, budget at least <code>replicaCount × (poolSize + 3) + 10</code> database connections.</p>
<p>Marshall has separate browser and fleet HTTPS listeners. Point <code>control.internal.example</code> at your control plane's private address, replacing <code>10.90.0.1</code> above with that address. Lilly, Audi and Porsche use <code>https://control.internal.example:5443</code>; browsers use the public domain. The backend certificate must cover the private name as well as the public host, and each fleet client must trust its CA. Allow port 5443 only from fleet peers through your private network's firewall. The public browser listener refuses machine APIs. See the <a href="{DOCS}operations/fleet-network.md">fleet network reference ↗</a>.</p>

<h2>3. Secrets</h2>
<p><code>services.overallsSecrets</code> decrypts SOPS documents with the host's SSH-derived age key and publishes them under <code>/run/overalls-secrets/NAME</code>. Encrypt each document to the host and to your recovery users:</p>
{code('''services.overallsSecrets = {
  enable = true;
  bundles.marshall = {
    encryptedFile = "${./secrets/marshall.enc.json}";
    outputs.environment = {
      format = "environment";
      secrets = [
        "DATABASE_URL" "MARSHALL_CLOAK_KEYS" "SECRET_KEY_BASE"
        "TOKEN_SIGNING_SECRET" "MARSHALL_SMTP_HOST" "MARSHALL_SMTP_USERNAME"
        "MARSHALL_SMTP_PASSWORD" "MARSHALL_MAIL_FROM"
      ];
    };
  };
};
services.marshall = {
  environmentFile = "${config.services.overallsSecrets.bundles.marshall.directory}/environment";
  secretUnits = [ config.services.overallsSecrets.bundles.marshall.unit ];
};''')}
{sh('''tools/buck2 build //:package-security-user-recipients
tools/buck2 run //:secrets -- check''')}

<h2>4. Database and email</h2>
<table>
<thead><tr><th>Variable</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td><code>DATABASE_URL</code></td><td>PostgreSQL, reached over verified TLS, shared by every Marshall</td></tr>
<tr><td><code>SECRET_KEY_BASE</code>, <code>TOKEN_SIGNING_SECRET</code></td><td>Shared signing secrets</td></tr>
<tr><td><code>MARSHALL_CLOAK_KEYS</code></td><td>Encryption keyring. Keep old keys as long as data encrypted with them still exists.</td></tr>
<tr><td><code>MARSHALL_SMTP_HOST</code> · <code>_USERNAME</code> · <code>_PASSWORD</code></td><td>Your relay. Plaintext SMTP isn't supported.</td></tr>
<tr><td><code>MARSHALL_SMTP_TLS</code></td><td><code>implicit</code> (the default, port 465) or <code>starttls</code> (port 587)</td></tr>
<tr><td><code>MARSHALL_SMTP_PORT</code> · <code>MARSHALL_SMTP_CA_CERTFILE</code></td><td>Optional port override and private-CA bundle path; otherwise use the TLS mode's default port and bundled public roots</td></tr>
<tr><td><code>MARSHALL_MAIL_FROM</code></td><td>A verified sender, such as <code>noreply@your-domain.example</code></td></tr>
<tr><td><code>PHX_HOST</code></td><td>The public host name used in sign-in links</td></tr>
</tbody>
</table>
<p>Every name in a secret output's <code>secrets</code> list is required. If your relay needs STARTTLS, another port or a private CA, add the corresponding variables to both the encrypted document and the environment output above.</p>
<p>Marshall won't start if its SMTP configuration is missing or invalid. Send a test to a mailbox you control before you open the deployment to other people.</p>

<h2>5. TLS and certificates</h2>
<p><code>services.marshallProxy</code> runs HAProxy in front of Marshall and verifies each backend's certificate and host name. The ACME integration issues and renews the public certificate:</p>
{code('''services.marshallProxy.acme = {
  enable = true;
  email = "operator@example.com";
};
# Set only after accepting the selected CA's terms.
security.acme.acceptTerms = true;''')}
<p>HTTP-01 needs public DNS pointing at the frontend and port 80 reachable. Use <code>challengeType = "dns-01"</code> with Route 53 when port 80 can't be reachable. If several frontends share one host name, each lists the others as <code>http01.peers</code>.</p>

<h2>6. Migrate, then switch</h2>
<p>Serving instances never run migrations when they start. Instead, host enrollment and every automatic update run Marshall's migrations from the candidate release, under a PostgreSQL advisory lock, before the running services are stopped. Migrations must work with every release still serving, and a successful schema change is never rolled back automatically. Incompatible changes need a coordinated upgrade.</p>
{ref("operations/nixos.md", "docs/operations/nixos.md")}
{ref("operations/production-email.md", "docs/operations/production-email.md")}
"""
    return guide_page("deploy.html", "Deploy the control plane", "Enable Marshall, secrets, PostgreSQL, SMTP and TLS for a self-hosted Overalls.", body)


DNS_DIAGRAM = """\
┌─ your DNS provider · example.com ──────────────┐
│ example.com        A   one per Marshall host   │
│ ns1.example.com    A   Audi DNS host 1         │
│ ns2.example.com    A   Audi DNS host 2         │
│ ns3, ns4 …         A   optional, up to eight   │
│ apps.example.com   NS  ns1, ns2 (, ns3, ns4)   │
└───────────────────────┬────────────────────────┘
                        │  delegated
                        ▼
┌─ Audi DNS · authoritative for apps.example.com ─────────────┐
│ &lt;machine&gt;.apps.example.com       A    gateway on its host   │
│                                       TTL up to 20 s        │
│ _acme-challenge.apps.example.com TXT  wildcard DNS-01       │
└─────────────────────────────────────────────────────────────┘"""


def dns():
    body = f"""<h1>Set up DNS</h1>
<p>Overalls uses two kinds of DNS. Your domain's apex stays with your normal DNS provider and points at your Marshall hosts. A subzone, <code>apps.&lt;your-domain&gt;</code>, is delegated to Audi, which answers for every machine's hostname itself. That's what lets a machine move between hosts without you touching DNS. It also conserves scarce IPv4 addresses: you can create as many machines as you like, and they share the host's IPv4 address between them.</p>
{facts(
    ("You create", "One apex A record per Marshall host, two to eight <code>ns</code> A records, and one NS delegation"),
    ("Audi serves", "<code>&lt;machine&gt;.apps.&lt;your-domain&gt;</code>, and the wildcard certificate challenge"),
    ("Ports", "UDP and TCP 53 on each Audi DNS host; 22, 80 and 443 on each Audi gateway"),
)}
<figure class="diagram">
<pre role="img" aria-label="At your DNS provider, example.com has one A record per Marshall host, ns1 and ns2 (optionally up to eight) point at Audi DNS hosts, and apps.example.com is delegated to them with NS records. Audi DNS then answers for each machine's hostname under apps.example.com with the address of the gateway on the host running it, and serves the DNS-01 challenge for Marshall's wildcard certificate.">{DNS_DIAGRAM}</pre>
<figcaption>The apex stays with your provider; Audi answers for everything under <code>apps</code>.</figcaption>
</figure>

<h2>1. Choose where Audi DNS runs</h2>
<p>Audi doesn't need hosts of its own. Its DNS role can run on your Marshall control-plane hosts, and on Lilly hosts too. We recommend running it in several places: the module needs two to eight nameservers, and spreading them across hosts keeps DNS answering when one goes down. Each one needs a stable public IPv4 address that's reachable on UDP and TCP port 53. Every Lilly host also runs an Audi gateway, which carries SSH and web traffic to its own machines, but gateways don't need DNS records of their own.</p>

<h2>2. Create the records at your DNS provider</h2>
<table>
<thead><tr><th class="width-min">Name</th><th class="width-min">Type</th><th>Value</th></tr></thead>
<tbody>
<tr><td class="nowrap"><code>&lt;your-domain&gt;</code></td><td>A</td><td>One record per Marshall host, each with that host's public address. Browsers, sign-in links, HTTP-01 certificates and Porsche all use this name.</td></tr>
<tr><td class="nowrap"><code>ns1.&lt;your-domain&gt;</code></td><td>A</td><td>The first Audi DNS host</td></tr>
<tr><td class="nowrap"><code>ns2.&lt;your-domain&gt;</code></td><td>A</td><td>The second Audi DNS host</td></tr>
<tr><td class="nowrap"><code>ns3</code>, <code>ns4</code> …</td><td>A</td><td>Optional extra Audi DNS hosts, up to eight in total</td></tr>
<tr><td class="nowrap"><code>apps.&lt;your-domain&gt;</code></td><td>NS</td><td><code>ns1.&lt;your-domain&gt;</code>, <code>ns2.&lt;your-domain&gt;</code>, and any others</td></tr>
</tbody>
</table>
<p>Porsche, the SSH gateway, runs on the Marshall hosts and answers on port 22 of these same apex addresses, so <code>ssh &lt;your-domain&gt;</code> reaches it with no extra records. Keep the apex records at your provider. Audi serves only the delegated subzone and never answers for the apex. With several Marshall hosts behind one name, a certificate challenge can arrive at any of them, so list the other frontends as <code>services.marshallProxy.acme.http01.peers</code> on each one (see <a href="deploy.html">Deploy the control plane</a>).</p>

<h2>3. Enable Audi DNS</h2>
{code('''services.audiDns = {
  enable = true;
  zone = "apps.example.com";
  nameservers = [ "ns1.example.com" "ns2.example.com" ];
  mailbox = "hostmaster.example.com";
  controlPlane = "https://control.internal.example:5443";
  caFile = "/etc/overalls/service-ca.crt";
  credentialFile = "${config.services.overallsSecrets.bundles.audi-dns.directory}/token";
  secretUnits = [ config.services.overallsSecrets.bundles.audi-dns.unit ];
  openFirewall = true;
};''')}
<p>Every Audi DNS host lists the same zone and the same set of nameservers. <code>mailbox</code> is the SOA contact address, written in DNS form. The module refuses fewer than two or more than eight nameservers. <code>controlPlane</code> reaches Marshall's private fleet listener; install its CA at the <code>caFile</code> path.</p>

<h2>4. Enroll Audi with Marshall</h2>
<p>Each Audi DNS server and each gateway authenticates to Marshall with its own token. Gateways need an enrolled Lilly host; complete <a href="enroll.html">host enrollment</a> before issuing their tokens. Issue the tokens with the operator CLI and write them to private files outside your checkout:</p>
{sh('''bin/marshall eval 'Marshall.Operations.CLI.main()' audi-dns-rotate audi-host1-dns /private/host1-dns.token
bin/marshall eval 'Marshall.Operations.CLI.main()' audi-gateway-rotate audi-host1 HOST_UUID ADDRESS /private/host1.token''')}
<p>Check each file with <code>audi-dns-verify</code> or <code>audi-gateway-verify</code>. Then encrypt the tokens into each host's secret documents with <code>tools/buck2 run //:secrets -- encrypt</code> and run <code>tools/buck2 run //:secrets -- check</code>. <code>HOST_UUID</code> is the enrolled Lilly host's ID, and <code>ADDRESS</code> is the gateway's public address.</p>

<h2>5. Enable each Audi gateway</h2>
<p>On each enrolled Lilly host, enable the local connector and gateway. Move administrative SSH to port 2222 and verify access there before removing port 22, as described under <a href="enroll.html">Porsche setup</a>.</p>
{code('''services.openssh.ports = [ 2222 ];
services.lilly.ingress.enable = true;
services.audi = {
  enable = true;
  bindAddress = "192.0.2.11";
  hostId = config.services.lilly.hostId;
  controlPlane = "https://control.internal.example:5443";
  caFile = "/etc/overalls/service-ca.crt";
  credentialFile = "${config.services.overallsSecrets.bundles.audi.directory}/token";
  secretUnits = [ config.services.overallsSecrets.bundles.audi.unit ];
  openFirewall = true;
  tls = {
    enable = true;
    zone = "apps.example.com";
    browserOrigin = "https://example.com";
  };
};''')}
<p>Replace <code>192.0.2.11</code> with the public service address assigned to this host and enrolled as <code>ADDRESS</code> above. If Porsche shares the host, it needs a different explicit address, such as the primary <code>192.0.2.10</code> in the enrollment guide. Audi uses its service address for ports 22, 80 and 443. Its local Lilly identity and the enrolled gateway's <code>HOST_UUID</code> must match.</p>

<h2>6. Configure the wildcard issuer</h2>
<p>Set the same ingress zone on every Marshall host, Audi gateway and DNS replica. Configure one Marshall instance to request the fleet's Let's Encrypt wildcard:</p>
{code('''services.marshall.ingress = {
  zone = "apps.example.com";
  wildcardAcme = {
    issuerInstance = "node01";
    directory = "https://acme-v02.api.letsencrypt.org/directory";
    issuerCaFile = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
    certificateRootsFile = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
    # Set only after accepting the selected CA's terms.
    acceptTerms = true;
    nameservers = [
      { address = "192.0.2.11"; }
      { address = "198.51.100.11"; }
    ];
  };
};''')}
<p><code>node01</code> matches the local instance in the <a href="deploy.html">deployment example</a>. Put <code>wildcardAcme</code> on that issuer's host and replace the nameserver addresses with your two to eight authoritative Audi DNS replicas. Audi trusts Let's Encrypt's delivered chain through the public CA bundle by default; <code>caFile</code> above separately authenticates the private Marshall endpoint.</p>
<p>Marshall requests <code>*.apps.&lt;your-domain&gt;</code> using DNS-01. Every Audi DNS replica publishes the challenge record, so you don't need DNS provider credentials for it. Marshall installs the certificate on each gateway and waits for its installation receipt before publishing machine routes. Establish <a href="operations.html">database and Cloak-keyring backups</a> before relying on the wildcard, and configure Marshall's SSH host CA as described in <a href="enroll.html">gateway setup</a>.</p>

<h2>7. Validate</h2>
{sh('''dig @ns1.example.com apps.example.com SOA
dig @ns2.example.com apps.example.com SOA
dig +trace apps.example.com NS''')}
<p>Check that UDP and TCP 53 reach every Audi DNS host, and that 22, 80 and 443 reach every gateway, from a network outside your fleet. Then stop one <code>audi-dns</code> at a time and confirm the others keep answering. In <strong>Administrator audit → Certificates</strong>, check the active wildcard generation and an installation receipt from every gateway. Verify an actual machine hostname over HTTPS through each enrolled gateway address.</p>
{ref("services/audi.md", "docs/services/audi.md")}
{ref("operations/fleet-network.md", "docs/operations/fleet-network.md")}
"""
    return guide_page("dns.html", "Set up DNS", "Delegate apps.<your-domain> to Audi and create the DNS records a self-hosted Overalls needs.", body)


def enroll():
    body = f"""<h1>Enroll hosts and images</h1>
<p>A Lilly host only runs guests once Marshall knows about it. Enrolling registers the host as disabled, issues it a revocable credential encrypted to that host, and leaves it to you to enable scheduling.</p>
{facts(
    ("Needs", "An installed host with its receipt, and administrative SSH to both the host and a Marshall host"),
    ("Credential", "Five years by default, revocable at any time, rotated explicitly"),
)}
<h2>1. Declare the Lilly role</h2>
<p>Add this to the host's <code>host.json</code> <em>before</em> installing, so the base system includes the identity helper:</p>
{code('''"lilly": {
  "controlPlane": "https://control.internal.example:5443",
  "egressInterface": "eth0",
  "credentialTtlSeconds": 157680000,
  "overheads": {"cores": 1, "memoryBytes": 1073741824, "storageBytes": 1073741824}
}''')}
<p>Host names for Lilly hosts can be at most 26 characters. Don't set Lilly host or pool IDs by hand; they're generated.</p>
<p>The control-plane URL reaches Marshall's private fleet listener. If it uses your own CA, set <code>services.lilly.controlPlaneCAFile</code> in the host's <code>configuration.nix</code> to the installed CA bundle, such as <code>/etc/overalls/service-ca.crt</code>.</p>

<h2>2. Prepare the enrollment</h2>
<p>Deploy the Marshall release and its migration first. Then, from your checkout:</p>
{sh('''tools/buck2 run //:host -- prepare-enrollment --host NAME --root . \\
  --target admin@installed-host --marshall-target admin@marshall-host \\
  --identity /private/admin-key --known-hosts /private/known-hosts \\
  --install-receipt /private/host-plan.installed.json \\
  --recovery-key /private/recovery-key''')}
<p>This registers a disabled host and writes the <code>NAME-git</code> and <code>NAME-lilly</code> ciphertext, plus public registration data in <code>lilly.binding</code>. It doesn't commit, push or enable anything. If it's interrupted, run the identical command again; its journal resumes the work without issuing a second credential.</p>

<h2>3. Activate and enable</h2>
<p>Push the changes and activate the commit with <code>tools/buck2 run //:host -- enroll --revision …</code>, as in <a href="provision.html">provisioning</a>. Once the host reports ready, enable it from a Marshall host with the operator CLI:</p>
{sh('''bin/marshall eval 'Marshall.Operations.CLI.main()' show NAME
bin/marshall eval 'Marshall.Operations.CLI.main()' enable HOST_UUID''')}
<p>Operator commands run as a separate process with <code>PHX_SERVER=false</code>, never through a serving node's console. They print only public identities.</p>

<h2>4. Guest images</h2>
<p>Images have immutable <code>sha256:</code> identities. The shared catalog in <code>fleet/guest-images.nix</code> selects NixOS, Ubuntu, Arch Linux, AlmaLinux, Windows and the reviewed FreeBSD and OmniOS images, plus an experimental Android SDK variant of NixOS. Entries name packages from <code>overallsPackages</code>, for example:</p>
{code('''[
  { name = "NixOS"; package = overallsPackages.guest; }
  { name = "Ubuntu 26.04 LTS"; package = overallsPackages.ubuntuGuest; }
  { name = "Windows Server 2025"; package = overallsPackages.windowsGuestPublished; }
]''')}
<p>Use the same staged catalog on every Lilly host and register the selected manifests with Marshall. Lilly seals image templates within its configured budget and clones guest disks on demand. Set <code>services.marshall.defaultImageId</code> to a registered image to choose the default for new machines.</p>
<p>Build the standard Ubuntu image through Buck2:</p>
{sh('''image=$(cat "$(tools/buck2 build --show-full-simple-output //:package-guest-ubuntu)")
ls "$image"
# kernel  initrd  rootfs.ext4  manifest.json''')}
<p>For custom images, use <code>mkUbuntuGuest</code> with a reviewed APT lock, or the NixOS guest builder's <code>extraModules</code>. The <a href="{DOCS}guests/os-matrix.md">OS matrix ↗</a> records each family's capabilities and verification limits.</p>
<p>Windows installation isn't byte-identical from build to build. <code>windowsGuestPublished</code> selects one sealed <code>windows-v1</code> image through the signed Overalls cache and refuses a cache miss. To update it, build once with the source builder, retain the installation evidence, seal <code>disk.raw</code>, <code>firmware</code> and <code>manifest.json</code>, and review their digests and recursive NAR hash. Update the publication and manifest pins together. Publish that exact directory, verify signature-checked substitution on every host, then activate the catalog. Follow the <a href="{DOCS}guests/windows-guests.md#fleet-publication">Windows publication procedure ↗</a>.</p>

<h2>5. Porsche on your Marshall hosts</h2>
<p>Porsche, the SSH gateway, runs on the same hosts as Marshall and listens on port 22 of the same public addresses your apex domain points at. Port 443 on those addresses serves the browser and port 22 serves Porsche, so people manage machines with <code>ssh &lt;your-domain&gt;</code>. There's no separate gateway address or DNS record.</p>
<ol>
<li><strong>Move administrative SSH to port 2222 first.</strong> Activate OpenSSH on both 22 and 2222, check that you can log in on 2222 (with sudo if you need it), then activate a configuration without 22. The module refuses to start Porsche on port 22 until administrative SSH is on 2222. From then on, pass <code>--ssh-port 2222</code> to the bootstrap tool.</li>
<li><strong>Issue a gateway credential for each Porsche host.</strong> Each host gets its own token and gateway name:
{sh('''bin/marshall eval 'Marshall.Operations.CLI.main()' gateway-prepare /private/porsche-host1.token
bin/marshall eval 'Marshall.Operations.CLI.main()' gateway-configure porsche-host1 /private/porsche-host1.token''')}
Encrypt the token into that host's <code>porsche</code> secret bundle as <code>PORSCHE_GATEWAY_TOKEN</code>.</li>
<li><strong>Enable Porsche</strong> alongside Marshall:
{code('''services.openssh.ports = [ 2222 ];
services.porsche = {
  enable = true;
  bindAddress = "192.0.2.10";
  controlPlane = "https://control.internal.example:5443";
  publicOrigin = "https://example.com";
  caFile = "/etc/overalls/service-ca.crt";
  credentialFile = "${config.services.overallsSecrets.bundles.porsche.directory}/token";
  secretUnits = [ config.services.overallsSecrets.bundles.porsche.unit ];
  openFirewall = true;
};''')}
</li>
</ol>
<p>Replace <code>192.0.2.10</code> with the host's primary public address. When Audi shares this host, bind its gateway to a different explicit service address: both gateways listen on port 22, and Audi also needs ports 80 and 443. The modules reject overlapping SSH listeners. Keep <code>publicOrigin</code> on the public browser domain; <code>controlPlane</code> uses the private fleet endpoint.</p>
<p>Before starting either gateway, configure Marshall's dedicated SSH host CA with <code>services.marshall.sshHostCa.publicKey</code>, <code>keyFile</code> and <code>retirement</code>, alongside <code>services.marshall.ingress.zone</code>. Deliver the private signer only to Marshall through an encrypted secret output and list its preparation unit in <code>services.marshall.secretUnits</code>. Follow the <a href="{SOURCE_BLOB}secrets/README.md#ssh-host-ca">SSH host CA custody procedure ↗</a>.</p>
<p>Porsche presents a host certificate signed by that CA. The <code>overalls</code> installer adds that CA to people's <code>known_hosts</code>, so <code>ssh &lt;your-domain&gt;</code> verifies without trust-on-first-use. Porsche reports readiness on <code>/run/porsche/status.sock</code>, and automatic updates wait for it. Rotating a gateway credential ends that gateway's open sessions until it loads the new token.</p>
{ref("operations/provisioner-enrollment.md", "docs/operations/provisioner-enrollment.md")}
{ref("guests/ubuntu-guests.md", "docs/guests/ubuntu-guests.md")}
{ref("guests/windows-guests.md", "docs/guests/windows-guests.md")}
{ref("operations/porsche-operations.md", "docs/operations/porsche-operations.md")}
"""
    return guide_page("enroll.html", "Enroll hosts and images", "Register Lilly hosts, publish guest images and configure the Porsche SSH gateway.", body)


def first_machine():
    body = f"""<h1>Your first machine</h1>
<p>Everything on this page happens on <em>your</em> deployment. Replace <code>&lt;your-domain&gt;</code> with your deployment's domain. <code>&lt;gateway&gt;</code> is the same domain: Porsche listens on port 22 of your Marshall hosts.</p>
{facts(
    ("Sign in", "<code>https://&lt;your-domain&gt;/sign-in</code>, by magic link; passkeys are also supported"),
    ("Machines", "<code>https://&lt;your-domain&gt;/machines</code>"),
    ("SSH keys", "<code>https://&lt;your-domain&gt;/settings#ssh-keys</code>"),
)}
<h2>1. Sign in</h2>
<p>Enter your email address at <code>/sign-in</code> and follow the link you're sent. Registration is open, and an account is created the first time someone signs in.</p>

<h2>2. Create a machine in the browser</h2>
<p>On <code>/machines</code>, choose an image and a profile, then create. When the machine is running, its page opens a terminal straight away. Add as many terminals as you need; they stay open when you close the tab.</p>

<h2>3. Register an SSH key</h2>
<p>Paste one OpenSSH <em>public</em> key (Ed25519, ECDSA, or RSA with at least 2048 bits) on the SSH keys page. To approve a key from the terminal instead, keep an interactive <code>ssh &lt;gateway&gt;</code> session open and follow the short-lived approval link it prints.</p>

<h2>4. Manage machines over SSH</h2>
{sh('''ssh <gateway> whoami
ssh <gateway> images
ssh <gateway> new --name example-machine
ssh <gateway> ls
ssh <gateway> stop example-machine
ssh <gateway> start example-machine''')}
<p>Every command accepts <code>--json</code>. Commands that change something accept <code>--request-id ID</code>, so retrying after a dropped connection can't do the same thing twice. Stopping keeps the disk; <code>rm</code> deletes it.</p>

<h2>5. Install the CLI</h2>
<p>Each machine's page has a <strong>Connect from your computer</strong> section with a one-line installer for Linux and macOS (and a PowerShell one for Windows). It sets up wildcard SSH to every machine you can reach. After that:</p>
{sh('''overalls open https://github.com/OWNER/REPO
overalls agent --machine <machine-uuid>''')}
<p><code>open</code> creates a machine, waits for the clone into <code>/workspace/REPO</code>, then opens a shell. <code>agent</code> sends one prompt to the machine's agent threads, after you approve the CLI in the browser.</p>

<h2>6. Launch from a repository page</h2>
<p>Any supported repository URL, appended to your deployment's address after a <code>#</code>, starts a machine with that repository checked out:</p>
{code('''https://<your-domain>/#https://github.com/OWNER/REPO''')}
<p>The toolbar extension does the same with one click on GitHub, GitLab, Codeberg and Bitbucket Cloud. It sends only the repository's origin and path, and never page contents. Your deployment serves the unsigned developer packages at <code>/bin/chrome.zip</code> and <code>/bin/firefox.xpi</code>.</p>
{ref("../marshall/priv/docs/quickstart.md", "Getting started")}
{ref("../marshall/priv/docs/commands.md", "Command reference")}
{ref("../marshall/priv/docs/automation.md", "Automation")}
"""
    return guide_page("first-machine.html", "Your first machine", "Sign in to your own Overalls deployment, register a key and create a machine.", body)


def operations():
    body = f"""<h1>Day-two operations</h1>
<p>Once it's running, a fleet mostly looks after itself: hosts update from Git, back themselves up, and report health. These are the controls you'll use when it doesn't.</p>
{facts(
    ("Updates", f"<code>overalls-auto-update</code>, which every enrolled host runs from your <code>{SOURCE_BRANCH}</code> branch"),
    ("Hosts", "Drain, resume and retire with the Marshall operator CLI"),
    ("Backups", "<code>overalls-backup</code>, restic to S3-compatible storage"),
)}
<h2>Automatic updates</h2>
<p>Each host builds the candidate revision with <code>tools/buck2 build //fleet/hosts/NAME:deployment</code>, stages its secrets, applies compatible migrations, switches, and checks health twice, five seconds apart. A failing revision backs off from thirty seconds to fifteen minutes; pushing a fix skips the wait.</p>
{sh('''sudo overalls-auto-update status
sudo systemctl start overalls-auto-update.service
sudo journalctl -u overalls-auto-update.service
sudo systemctl stop overalls-auto-update.timer   # before manual recovery''')}
<p>Hosts don't coordinate their restarts with each other. Kernel changes and incompatible schema or protocol changes need planned maintenance.</p>

<h2>Drain a host for maintenance</h2>
{sh('''bin/marshall eval 'Marshall.Operations.CLI.main()' drain HOST_UUID REQUEST_UUID ops:ticket-123
bin/marshall eval 'Marshall.Operations.CLI.main()' drain-status REQUEST_UUID''')}
<p>Drain stops the host's guests and retains their disks and host assignments. Before maintenance, require <code>status=drained</code> and <code>currently_quiescent=true</code> from <code>drain-status</code>. Stopping Lilly's VM slice doesn't count as confirmed cleanup. Guests keep running when the Lilly daemon itself restarts.</p>
<p>After maintenance, wait for a fresh ready report, then resume admission:</p>
{sh('''bin/marshall eval 'Marshall.Operations.CLI.main()' resume-host REQUEST_UUID''')}
<p>Resume closes the drain and leaves guests stopped for their owners to start. For permanent retirement instead, keep the drain open, have owners delete retained machines, and wait for physical cleanup and fresh empty-pool reports. Then retire:</p>
{sh('''bin/marshall eval 'Marshall.Operations.CLI.main()' retire-host REQUEST_UUID''')}

<h2>Move machines between hosts</h2>
<p>Owners, managers and team admins can relocate a machine with <code>ssh &lt;gateway&gt; relocate NAME</code>. Running moves involve downtime. Marshall chooses the destination host and transfer method. The machine keeps its identity, name, sharing and private address.</p>

<h2>Backups</h2>
<p>First provision each host's encrypted backup document with an independently generated <code>RESTIC_PASSWORD</code> and the S3 provider's <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code>. The fleet profile publishes the password and S3 environment files under <code>/run/overalls-secrets/backup</code>. Keep recovery identities outside the node and verify recovery decryption before relying on the repository. Follow the <a href="{DOCS}operations/backups.md#secret-custody">secret custody procedure ↗</a>.</p>
{code('''services.overallsBackups = {
  enable = true;
  s3 = {
    endpoint = "https://objects.example.com";
    bucket = "node-recovery";
    region = "your-region";
  };
};''')}
{sh('''overalls-backup list
overalls-backup check
overalls-backup read-check''')}
<p>Only enabled roles add their state. By default that's the host identity and receipts; Lilly's journals, image templates and every ready guest disk (from native ZFS snapshots); a logical dump of PostgreSQL on Marshall hosts; Porsche and Audi keys; and ACME state. A stopped guest is never started just to back it up. A running guest is asked to <code>sync</code> first, but isn't paused.</p>
<h2>Logs and metrics</h2>
<p><code>services.overallsLogging</code> sends journals from Marshall, Lilly, Porsche, HAProxy and the system to CloudWatch, OTLP or a fleet log store, with a bounded on-disk queue. Ziggy and Galileo record usage per account.</p>

<h2>Credentials</h2>
<p>Rotate a Lilly credential with <code>tools/buck2 run //:host -- rotate-credential</code>, using the same arguments as <code>prepare-enrollment</code>. Rotation revokes the old credential immediately, so deploy the new ciphertext promptly. Signing secrets, the database URL and the active Cloak key can't change through automatic updates; rotating them needs the coordinated procedure.</p>
{ref("operations/host-maintenance.md", "docs/operations/host-maintenance.md")}
{ref("operations/backups.md", "docs/operations/backups.md")}
{ref("operations/observability.md", "docs/operations/observability.md")}
"""
    return guide_page("operations.html", "Day-two operations", "Updates, host drains, relocation, backups and logs for a self-hosted Overalls fleet.", body)
