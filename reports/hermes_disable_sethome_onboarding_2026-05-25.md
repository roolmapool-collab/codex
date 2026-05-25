# Report: Disable /sethome Onboarding Noise

Date: 2026-05-25
Operator: Codex
Scope: Hermes principal, Ariane, Vulcain, Argus, Atlas

## Issue

The gateway posted noisy onboarding messages in Discord channels:

`Type /sethome to make this chat your home channel, or ignore to skip.`

This polluted operational channels and agent context.

## Root Cause

`/opt/hermes/gateway/run.py` sent a one-time platform notice whenever a first
message arrived and no home channel environment variable was configured.

## Correction

The onboarding notice is now opt-in. It is disabled by default and can only be
restored by setting:

`HERMES_SHOW_HOME_ONBOARDING=true`

The `/sethome` command itself was not removed.

## Deployment

Patched and compiled:

- `hermes-agent-1`
- `hermes-ariane`
- `hermes-vulcain`
- `hermes-argus`
- `hermes-atlas`

Backups were created in each container as:

`/opt/hermes/gateway/run.py.bak.no-sethome-notice-20260525T2038Z`

## Verification

- All patched `run.py` files compile with Python.
- All five gateway containers restarted successfully.
- Post-restart logs showed no `Traceback`, `failed`, `error`,
  `No home channel`, or `Type /sethome` entries in the checked window.
- No Discord test message was sent.

## Remaining Note

The patch is applied inside running container filesystems. It survives normal
`docker restart`, but may be lost if containers are recreated from the image
without rebuilding or mounting the patched source.
