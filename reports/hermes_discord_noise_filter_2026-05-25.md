# Hermes Discord noise filter - 2026-05-25

## Status

DONE - deployed on:

- hermes-agent-1
- hermes-ariane
- hermes-vulcain
- hermes-argus
- hermes-atlas
- hermes-dashboard

## Problem

Discord agent channels were polluted by operational/tool chatter:

- `Type /sethome to make this chat your home channel, or ignore to skip.`
- `A home channel is where Hermes delivers cron job results and cross-platform messages.`
- `💻 terminal: "..."`
- `🔎 search_files: "..."`
- `📖 read_file: "..."`
- French preflight line: `Je dois d'abord vérifier ...`

The prior `/sethome` source was disabled in `gateway/run.py`, but stale prompt/context
and tool status delivery could still leak those lines through the Discord adapter or
through `send_message_tool`.

## Fix

Added a Discord outbound sanitizer in both delivery paths:

- `/opt/hermes/gateway/platforms/discord.py`
- `/opt/hermes/tools/send_message_tool.py`

Behavior:

- removes known noise lines from outbound Discord content;
- keeps legitimate message lines around the removed noise;
- skips the Discord send entirely when the remaining content is empty;
- keeps the existing textual agent mention guard intact.

## Validation

- `py_compile` passed for both patched files in the Hermes runtime.
- `test_discord_noise_filter.py` passed in `hermes-agent-1`, `hermes-ariane`, and `hermes-vulcain`.
- The test covers sanitizer-only and `send_message_tool(action="send", target="discord:...", message="💻 terminal: ...")`, confirming it returns `skipped=true` before any Discord delivery.
- Containers restarted successfully.
- Recent logs checked after restart for:
  - `Traceback`
  - `error`
  - `failed`
  - `sethome`
  - `terminal:`
  - `search_files:`
  - `read_file:`

No matching post-restart log noise was found in checked agent logs.

## Backups

Each container received backups:

- `/opt/hermes/gateway/platforms/discord.py.bak.no-discord-noise-20260525T2115Z`
- `/opt/hermes/tools/send_message_tool.py.bak.no-discord-noise-20260525T2115Z`

## Note

This prevents new noise. Existing Discord messages were not deleted because that is a destructive channel action.
