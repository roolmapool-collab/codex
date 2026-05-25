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

## Follow-Up: Send Message Tool Bypass

After the first correction, Ariane repeated the same textual mention through a
different path:

```json
{"target":"discord:#hermes-orchestrateur","message":"@Hermes ..."}
```

Evidence was found in Ariane's session log:
`/opt/data/profiles/hermes-ariane/sessions/20260525_162437_f878150c.jsonl`.

The root cause was that `tools/send_message_tool.py` contains a direct Discord
REST sender. That path posts Discord JSON payloads directly and did not pass
through the patched gateway adapter. The first patch therefore protected normal
adapter sends, but not the `send_message` tool call used by Ariane.

Additional corrections applied:

- Added textual mention rejection at the start of `_handle_send()` when
  `target` is Discord.
- Added a second guard inside `_send_discord()` before any REST request.
- Replaced raw `{"content": message}` Discord payloads with explicit
  `allowed_mentions` payloads:
  `parse=[]`, scoped `users=[...]`, `roles=[]`, `replied_user=false`.
- Added `send_message` mode to `hermes_discord_payload_lint.py`.
- Added a healthcheck fixture for the exact bypass class.
- Deployed `send_message_tool.py` to Ariane, Vulcain, Argus, Atlas,
  Hermes principal, and dashboard containers.
- Restarted Ariane, Vulcain, Argus, Atlas, and Hermes principal.

Follow-up verification:

- Direct bad tool call in Ariane:
  `send_message(target="discord:#hermes-orchestrateur", message="@Hermes ...")`
  returns `FORBIDDEN_TEXT_MENTION` before config resolution or send.
- Same bad tool call returns `FORBIDDEN_TEXT_MENTION` in Vulcain, Argus, and
  Atlas.
- Healthcheck now reports `PASS=29 FAIL=0 WARN=0`.
- No Discord message was sent during these verification tests.
