# Incident Report: Discord Text Mention Guard

Date: 2026-05-25
Operator: Codex
Scope: Ariane, Vulcain, Argus, Atlas

## Incident

Ariane sent a Discord message containing the textual mention `@Hermes` in
`#hermes-orchestrateur`. The expected form is the numeric Discord mention
`<@1504184998075306005>` with `allowed_mentions.users` explicitly scoped.

## Root Cause

The Discord communication guard existed in agent documentation and SOUL
instructions, but it was not enforced at the final Discord send boundary.
The linter also did not reject the plain-text `@Hermes` case in `agent_reply`
mode. A second contributing factor was a missing shared workspace path:
agents looked for `/opt/hermes/workspace/discord_inventory.md`, while the
canonical file was at `/opt/data/workspace/discord_inventory.md`.

## Corrections Applied

- Updated `/opt/data/workspace/scripts/hermes_discord_payload_lint.py` to reject
  textual agent mentions in both `outbound_mission` and `agent_reply` modes.
- Added a healthcheck fixture reproducing the incident text:
  `@Hermes demande les liens livrables.md`.
- Added a runtime guard in `/opt/hermes/gateway/platforms/discord.py` before
  Discord text sends, forum posts, edits, and attachment captions.
- Deployed the runtime guard to `hermes-ariane`, `hermes-vulcain`,
  `hermes-argus`, `hermes-atlas`, and available Hermes gateway containers.
- Created `/opt/hermes/workspace -> /opt/data/workspace` symlink in the four
  agent containers.
- Fixed `auth.json` ownership and mode for all four agent profiles:
  `hermes:hermes 600`.
- Restarted the four specialized agent containers to load the runtime guard.

## Verification

- `hermes_lessons_healthcheck.sh`: `PASS=28 FAIL=0 WARN=0`.
- Linter dry-run rejects the exact bad case with:
  `FORBIDDEN_TEXT_MENTION`.
- Linter dry-run accepts a valid numeric mention payload.
- Runtime guard dry-run in Ariane, Vulcain, Argus, and Atlas blocks `@Hermes`
  and accepts a valid numeric mention string.
- `/opt/hermes/workspace/discord_inventory.md` is visible in all four agents.
- `auth.json` is now `hermes:hermes 600` for all four agents.
- Post-restart logs showed no `Permission denied`, `failed to parse`,
  `Traceback`, or `failed to send` entries in the checked window.

## Remaining Note

The gateway patch is currently applied to running container filesystems. It will
survive normal `docker restart`, but may be lost if containers are recreated from
the image without rebuilding or mounting the patched source.
