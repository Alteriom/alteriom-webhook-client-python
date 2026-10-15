---
verified_at: 2026-10-15
verified_commit: 337bb90fc61fd822113654f550d491de4e76aa38
---

# Documents — what this repository has for people

The agent-facing files are the root `AGENTS.md` (the entry) and this `.github/icm/` folder. The one user document restates facts the code owns, and the code is right when they disagree.

| Document | What it answers | Owner of the facts |
|---|---|---|
| [README.md](../../../README.md) | install, the FastAPI quick start, manual and low-level use, configuration, the models | `src/alteriom_webhook_client/` |

There is no changelog, contributing guide or security policy file; the GitHub release notes record what changed, and private vulnerability reporting is enabled on the repository.

## Known drift

None found at the commit above: the README's defaults (five-minute age, 10 MB) match `WebhookReceiver` (`src/alteriom_webhook_client/receiver.py:51`).
