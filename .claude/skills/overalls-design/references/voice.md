# Voice and tone

## Who's talking

An experienced operator who built the thing, explaining it to a peer over coffee. They're plain,
specific and a little dry. They're proud of the engineering and honest about what isn't finished.
The workwear brand comes through lightly ("made to get dirty", "tidying the workshop"), never as a
pun in every line.

## Rules

1. **Lead with what it does, then why you'd care.** "Each machine keeps its disk, name and address
   when you stop, start, resize, clone or move it." Not "Experience seamless persistence."
2. **Be concrete.** Name the real thing: Firecracker, ZFS, NixOS 26.05, `/dev/kvm`, 500 GiB,
   `llm.internal`, Washington DC, London, Singapore. Numbers and nouns beat adjectives.
3. **Second person, active voice, present tense.** "You run it." "Each host dials out to Marshall."
4. **Short sentences.** One idea each. Use semicolons sparingly and avoid em-dash chains; colons
   and full stops are fine.
5. **Sentence case** for headings and card titles. CSS uppercases h1 and h2; don't type capitals.
6. **British spelling** where it differs: licence (noun), utilisation, centralise.
7. **No hype words.** These are banned: seamless, blazing, revolutionary, effortless, unlock,
   empower, leverage, cutting-edge, next-gen, game-changing, magic.
8. **No hedging filler.** Avoid "simply", "just", "easily", "basically" and "very".
9. **Say what it isn't.** "There is no hosted version to sign up for: you install it and run it
   yourself." "It's MIT-licensed; you pay for your own hardware, bandwidth, email relay and inference."
10. **Credit and cite.** Link ADRs and repo docs (`Full reference: docs/nixos.md ↗`), and credit
    The Monospace Web and JetBrains Mono in the footer.

## Positioning lines (approved)

- **Tagline:** "An AI-first developer platform that you own."
- **Elevator pitch:** "Overalls runs persistent Firecracker microVMs on hardware you control. Each
  machine keeps its disk, name and address when you stop, start, resize, clone or move it. You use it
  from a browser terminal, over SSH or with the `overalls` CLI."
- **Ownership:** "It's open source under the MIT licence. There is no hosted version to sign up for:
  you install it and run it yourself."
- **Topology:** "Centralise the control plane; distribute the hosts." Marshall runs in one region,
  with several instances for HA. Lilly hosts go wherever your developers are.
- **Workflow:** "The Gitpod workflow on your own hardware." Use one machine per piece of work and
  delete it when you're done.
- **AI:** Claude Code and Codex come pre-installed and already pointed at Ziggy. No API keys or
  credentials live on the machine.
- **Mark caption:** "made to get dirty"
- **404:** "There's nothing at this address. It may have moved while we were tidying the workshop."

## Status labels: how to choose

| Label | Means | Use when |
|---|---|---|
| `STABLE` | Built and covered by acceptance tests | The owner says so, or the repo marks it done with passing acceptance |
| `PREVIEW` | Works, with rough edges | It ships, but coverage is partial (e.g. Browser editor: verified on NixOS, partial on Ubuntu) |
| `EXPERIMENTAL` | Still being built | Spikes and in-progress work (e.g. Inception) |

- The product owner's call on status wins over the repo docs. If the docs disagree, update the card
  text so it doesn't contradict the label. Don't keep "acceptance still open" on a STABLE card.
  Then tell the owner which repo doc still disagrees.
- Never invent a capability to fill a card. Check `~/src/kittens` on `origin/main` with `git grep`.
  If the code doesn't support a claim (for example per-region placement), leave the claim out and
  say so.

## Naming

- The product is **Overalls**: one word, capital O. The wordmark is `OVERALLS.` with a muted dot.
- The CLI is shown as `overalls`. Module, option and unit names that still say `kittens` (for example
  `services.kittensAutoUpdate`) are written exactly as they are in the code, with a one-line note
  that the codename remains.
- Components keep their code names and are introduced by role the first time they appear:
  - Marshall: control plane
  - Lilly: host provisioner
  - Porsche: SSH gateway
  - Audi: DNS and ingress
  - Brady: caching HTTP proxy
  - Enrico: GitHub mirror
  - Galileo: integrations
  - Ziggy: inference
  - Lyra: CLI
- Use placeholders for anything deployment-specific: `<your-domain>`, `<gateway>`, `OWNER/REPO`,
  `<machine-uuid>`. Never write `overalls.dev` as a service someone can use.

## Card copy formula

`<What it is/does, concretely>. <The consequence for the reader>. <Limit or caveat, if any>.`

Keep it to two or three sentences and roughly 30 to 60 words. Example:

> Guest downloads from apt, Nix, pip, npm and the like go through Brady. It fetches only from
> verified upstreams and caches public, anonymous responses, so the second machine to install a
> package gets it from the cache.
