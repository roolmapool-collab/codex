# Hermes Lessons Healthcheck Repair - 2026-05-25

## Context

Hermes reported that `/opt/data/workspace/healthchecks/lessons_latest.md`
could not be generated because `/opt/data/workspace/healthchecks/` was owned by
`root:root` with mode `755`.

No Discord message was sent. No gateway was restarted. No `.env` or
`config.yaml` file was modified.

## Actions

### 1. Permissions

Fixed canonical healthcheck directory ownership inside the container as root:

```text
/opt/data/workspace/healthchecks -> hermes:hermes mode 755
```

### 2. Healthcheck Script Fixes

The lessons healthcheck script itself had three execution bugs:

- `set -e` combined with `((PASS++))`, `((FAIL++))`, `((WARN++))` exited after
  the first pass/fail/warn.
- `SOUL.md` paths pointed under `/opt/data/workspace/...` instead of the real
  profile paths under `/opt/data/...`.
- Expected-failure linter fixtures exited the script before their expected KO
  status could be evaluated.

Backups were created before each patch:

```text
/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh.bak.counter-fix-20260525T191721Z
/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh.bak.soul-paths-20260525T191758Z
/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh.bak.fixture-sete-20260525T191829Z
/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh.bak.accent-20260525T191920Z
```

### 3. Accent/Pattern Fix

The guard skill contains `Mention numérique`, while the healthcheck searched
for `Mention numerique`. The check was aligned with the actual section title.

## Verification

Canonical report generated:

```text
/opt/data/workspace/healthchecks/lessons_latest.md
owner=hermes:hermes
mode=644
size=788
```

Final healthcheck result:

```text
PASS=27
FAIL=0
WARN=0
Healthcheck: SUCCES
Conclusion: TOUT OK
```

## Safety Notes

- No secrets were printed or committed.
- No Discord test was executed.
- The remaining runtime/Discord validation steps still require explicit human
  approval before any real message is sent.
