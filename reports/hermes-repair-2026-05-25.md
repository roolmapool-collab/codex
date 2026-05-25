# Hermes Repair Report - 2026-05-25

## Context

Hermes default gateway was running with stale Discord environment values inside Docker.

Observed before repair:

- Docker `Config.Env` had `DISCORD_REACTIONS=true`.
- Docker `Config.Env` still included Ariane channel `1505129251232546858` in `DISCORD_ALLOWED_CHANNELS`.
- `/root/hermes/data/.env` already had `DISCORD_REACTIONS=false`.
- `/root/hermes/data/.env` no longer included Ariane channel `1505129251232546858`.
- `/root/hermes/data/config.yaml` still had `discord.reactions: true`.

Root cause:

`hermes-agent-1` was created on 2026-05-20, while `/root/hermes/data/.env` was corrected on 2026-05-24. Docker container environment was therefore stale until the service was recreated.

Decision:

`DOCKER_ENV_STALE`, with a secondary stale config value in `config.yaml`.

## Actions Performed

Backup created:

```text
/root/hermes/data/config.yaml.bak.20260525_152238
```

Patch applied:

```diff
-  reactions: true
+  reactions: false
```

Gateway service recreated:

```bash
docker compose -f /docker/hermes/docker-compose.yml up -d --force-recreate --no-deps gateway
```

No Telegram test was sent.
No Discord test was sent.
Ariane gateway was not started.

## Verification

Container after recreate:

```text
hermes-agent-1 Up
```

New gateway process inside container:

```text
PID 8 /opt/hermes/.venv/bin/hermes gateway run
```

Docker environment after recreate:

```text
DISCORD_REACTIONS=false
DISCORD_FREE_RESPONSE_CHANNELS=
DISCORD_ALLOWED_CHANNELS=1504231713813958656,1505129245733687347,1505129257297383465,1505129262708162570,1505129268324077618
```

Config files after repair:

```text
/opt/data/.env: DISCORD_REACTIONS=false
/opt/data/config.yaml: discord.reactions=false
```

The Ariane channel `1505129251232546858` is absent from `DISCORD_ALLOWED_CHANNELS`.

## Remaining Work

1. Observe Hermes behavior without sending agent tests.
2. Treat Ariane gateway startup as a separate operation.
3. If approved later, run a minimal Telegram or Discord route test with a mission ID.
4. Add a runbook for future Docker env drift diagnosis.
