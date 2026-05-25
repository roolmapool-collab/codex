# 04 — Plan d’action Codex

## Phase 0 — No send

Avant tout :

```text
Discord no-send
pas de test réel
pas de restart
pas de kill
pas de modification .env/config.yaml
```

## Phase 1 — Audit état fichiers

```bash
ls -lah \
/opt/data/skills/hermes-discord-communication-guard.md \
/opt/data/skills/hermes-audit-remediation-learning-loop.md \
/opt/data/workspace/memory/curated/LESSONS_LEARNED_MANDATORY.md \
/opt/data/workspace/scripts/hermes_discord_payload_lint.py \
/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh \
/opt/data/workspace/healthchecks \
/opt/data/workspace/healthchecks/lessons_latest.md 2>&1 || true
```

## Phase 2 — Corriger permissions healthcheck

Depuis hôte/root :

```bash
docker exec -u 0 hermes-agent-1 sh -lc '
mkdir -p /opt/data/workspace/healthchecks &&
chown -R 10000:10000 /opt/data/workspace/healthchecks &&
chmod 755 /opt/data/workspace/healthchecks &&
ls -ld /opt/data/workspace/healthchecks
'
```

Puis :

```bash
docker exec -u 10000:10000 hermes-agent-1 sh -lc '
bash /opt/data/workspace/scripts/hermes_lessons_healthcheck.sh &&
ls -lah /opt/data/workspace/healthchecks/lessons_latest.md
'
```

## Phase 3 — Vérifier runtime Discord env

Depuis hôte :

```bash
docker inspect hermes-agent-1 --format '{{json .HostConfig.RestartPolicy}}'

docker inspect hermes-agent-1 --format '{{json .Config.Entrypoint}} {{json .Config.Cmd}}'

docker inspect hermes-agent-1 --format '{{range .Config.Env}}{{println .}}{{end}}' \
| sort \
| grep -E "DISCORD_REACTIONS|DISCORD_ALLOWED_CHANNELS|DISCORD_FREE_RESPONSE_CHANNELS|1505129251232546858|HERMES|PROFILE" || true
```

## Phase 4 — Vérifier config fichier

```bash
docker exec hermes-agent-1 sh -lc 'nl -ba /opt/data/config.yaml | sed -n "315,335p"'

docker exec hermes-agent-1 sh -lc 'grep -nE "DISCORD_REACTIONS|DISCORD_ALLOWED_CHANNELS|DISCORD_FREE_RESPONSE_CHANNELS|reactions:|allowed_channels:|free_response_channels:" /opt/data/.env /opt/data/config.yaml 2>/dev/null || true'
```

## Phase 5 — Proposer correction

Ne pas appliquer tant que Stéphane n’a pas validé.

Cas possibles :

| Cause | Correction proposée |
|---|---|
| `DOCKER_ENV_STALE` | corriger config Docker/Hostinger ou recréer container |
| `CONFIG_YAML_STALE` | backup + patch `discord.reactions: false` |
| `PID_RUNTIME_STALE` | restart contrôlé après vérification Docker env clean |
| `UNKNOWN` | stop |

## Phase 6 — Test Discord réel seulement après validation

Préconditions :

- healthcheck lessons OK ;
- linter OK ;
- reactions runtime corrigées ;
- dry-run payload validé ;
- validation Stéphane.

Ensuite seulement : un message Discord réel, puis silence.
