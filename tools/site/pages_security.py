from layout import SOURCE, page

ADVISORY = SOURCE + "/security/advisories/new"
BASE = "https://overalls.dev/"

# Expires is a required field in RFC 9116, so it's set far in the future instead of omitted.
# The RFC recommends less than a year ahead; some scanners will warn about this date.
EXPIRES = "2099-12-31T23:59:59Z"

# Researchers credited on the hall of fame, newest first:
# (date "YYYY-MM-DD", name, profile URL or "", advisory URL or "", one-line finding)
HALL_OF_FAME = []


def security_txt():
    return f"""Contact: {ADVISORY}
Expires: {EXPIRES}
Preferred-Languages: en
Canonical: {BASE}.well-known/security.txt
Policy: {BASE}security/
Acknowledgments: {BASE}security/hall-of-fame/
"""


def policy():
    body = f"""<main id="main-content">
<div class="prose">
<h1>Security</h1>
<p>Overalls runs other people's code on other people's hardware, so we take reports of security problems seriously. This is our vulnerability disclosure policy: what's in scope, how to report, and what you can expect from us.</p>
<dl class="kv">
<div><dt>Report to</dt><dd><a href="{ADVISORY}">GitHub private security advisory <span aria-hidden="true">↗</span></a></dd></div>
<div><dt>Reward</dt><dd>Public thanks on the <a href="hall-of-fame/">hall of fame</a> and credit in the advisory. There is no cash bounty.</dd></div>
<div><dt>Machine-readable</dt><dd><a href="../.well-known/security.txt">/.well-known/security.txt</a></dd></div>
</dl>
</div>

<section aria-labelledby="scope">
<h2 id="scope">In scope</h2>
<div class="prose">
<ul>
<li>The Overalls source code at <a href="{SOURCE}">{SOURCE.removeprefix("https://")} <span aria-hidden="true">↗</span></a>: Marshall, Lilly, Porsche, Audi, Brady, Enrico, Galileo, Ziggy, the <code>overalls</code> CLI, the browser extension, the NixOS modules, the host tools and the guest images.</li>
<li>Anything that lets one tenant reach another: escaping a guest, crossing the guest network isolation, reading another account's machines, terminals or usage, or reading secrets that are supposed to stay at the edge.</li>
<li>This website, <code>overalls.dev</code>.</li>
</ul>
</div>
</section>

<section aria-labelledby="out">
<h2 id="out">Out of scope</h2>
<div class="prose">
<ul>
<li><strong>Other people's deployments.</strong> There is no hosted Overalls. Every deployment belongs to whoever runs it, and only they can authorise testing it. If you find a problem in someone's deployment that comes from Overalls itself, reproduce it on your own and report it here.</li>
<li>Third-party services, including GitHub, Ghost and ghuntley.com, Cachix, and AI model providers. Report those to the service.</li>
<li>Denial of service, load or volumetric testing, spam, social engineering and physical attacks.</li>
<li>Scanner output without a working proof of concept, and missing headers or best-practice notes on this static site with no demonstrable impact.</li>
</ul>
</div>
</section>

<section aria-labelledby="how">
<h2 id="how">How to report</h2>
<div class="prose">
<ol>
<li>Open a <a href="{ADVISORY}">private security advisory <span aria-hidden="true">↗</span></a> on the Overalls repository. Please don't open a public issue or pull request.</li>
<li>Include the commit or release you tested, how it was deployed, step-by-step reproduction, and what an attacker gains.</li>
<li>Keep any data you came across private, and don't include other people's data in the report.</li>
</ol>
</div>
</section>

<section aria-labelledby="rules">
<h2 id="rules">Rules of engagement</h2>
<div class="prose">
<ul>
<li>Test against a deployment you own and run.</li>
<li>Don't access, change or delete data that isn't yours. Stop and report as soon as you've shown the problem.</li>
<li>Don't degrade a service for other people.</li>
<li>Give us a reasonable time to fix the problem before you talk about it publicly. We aim to agree a disclosure date with you, normally within 90 days of the report.</li>
</ul>
</div>
</section>

<section aria-labelledby="commitments">
<h2 id="commitments">What you can expect</h2>
<div class="prose">
<ul>
<li>We'll confirm we've received your report and keep you updated as we investigate and fix it.</li>
<li>We'll publish a GitHub security advisory for confirmed problems, request a CVE where one applies, and credit you unless you'd rather stay anonymous.</li>
<li>With your permission, we'll add you to the <a href="hall-of-fame/">hall of fame</a>.</li>
</ul>
</div>
</section>

<section aria-labelledby="harbor">
<h2 id="harbor">Safe harbour</h2>
<div class="prose">
<p>If you research and report in good faith and follow this policy, we consider your research authorised. We won't pursue or support legal action against you for it, and if someone else does, we'll make it clear you acted under this policy. This covers only what we control: the Overalls project and this website. We can't authorise testing of deployments or services that belong to anyone else.</p>
</div>
</section>
</main>
"""
    return page(
        "Security",
        "The Overalls vulnerability disclosure policy: scope, how to report, and safe harbour.",
        body,
        r="../",
    )


def hall_of_fame():
    if HALL_OF_FAME:
        rows = "\n".join(
            f'<tr><td class="width-min" data-label="Date:">{date}</td>'
            f'<td data-label="Researcher:">{f"<a href=\"{url}\">{name} <span aria-hidden=\"true\">↗</span></a>" if url else name}</td>'
            f'<td class="width-auto" data-label="Finding:">{f"<a href=\"{advisory}\">{finding}</a>" if advisory else finding}</td></tr>'
            for date, name, url, advisory, finding in HALL_OF_FAME
        )
        listing = f"""<table class="table-stack">
<thead><tr><th>Date</th><th>Researcher</th><th>Finding</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>"""
    else:
        listing = f"""<div class="empty-state">
<h2>No one yet</h2>
<p>Be the first. Read the <a href="../">disclosure policy</a>, then open a <a href="{ADVISORY}">private security advisory <span aria-hidden="true">↗</span></a>.</p>
</div>"""
    body = f"""<main id="main-content">
<div class="prose">
<h1>Hall of fame</h1>
<p>Thank you to the people who have found and responsibly reported security problems in Overalls. Everyone listed here reported under our <a href="../">vulnerability disclosure policy</a>, and every finding was confirmed and fixed.</p>
</div>
{listing}
</main>
"""
    return page(
        "Hall of fame",
        "Security researchers who have responsibly reported vulnerabilities in Overalls.",
        body,
        r="../../",
    )
