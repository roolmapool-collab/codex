# 06 — Commandes hôte VPS

## Corriger permissions healthcheck

```bash
docker exec -u 0 hermes-agent-1 sh -lc '
mkdir -p /opt/data/workspace/healthchecks &&
chown -R 10000:10000 /opt/data/workspace/healthchecks &&
chmod 755 /opt/data/workspace/healthchecks &&
ls -ld /opt/data/workspace/healthchecks
'
```

## Relancer healthcheck comme hermes

```bash
docker exec -u 10000:10000 hermes-agent-1 sh -lc '
bash /opt/data/workspace/scripts/hermes_lessons_healthcheck.sh &&
ls -lah /opt/data/workspace/healthchecks/lessons_latest.md &&
cat /opt/data/workspace/healthchecks/lessons_latest.md
'
```

## Inspect Docker env

```bash
docker inspect hermes-agent-1 --format '{{json .HostConfig.RestartPolicy}}'

docker inspect hermes-agent-1 --format '{{json .Config.Entrypoint}} {{json .Config.Cmd}}'

docker inspect hermes-agent-1 --format '{{range .Config.Env}}{{println .}}{{end}}' \
| sort \
| grep -E "DISCORD_REACTIONS|DISCORD_ALLOWED_CHANNELS|DISCORD_FREE_RESPONSE_CHANNELS|1505129251232546858|HERMES|PROFILE" || true
```

## Inspect config.yaml

```bash
docker exec hermes-agent-1 sh -lc 'nl -ba /opt/data/config.yaml | sed -n "315,335p"'
```

## Inspect runtime PID env filtré

```bash
docker exec hermes-agent-1 sh -lc '
for p in 1 6 7; do
  if [ -r /proc/$p/environ ]; then
    echo "=== PID $p ==="
    tr "\0" "\n" < /proc/$p/environ | sort | grep -E "DISCORD_REACTIONS|DISCORD_ALLOWED_CHANNELS|DISCORD_FREE_RESPONSE_CHANNELS|HERMES|PROFILE" || true
  fi
done
'
```

## Tester linter sans Discord

```bash
docker exec -u 10000:10000 hermes-agent-1 sh -lc '
python3 -m py_compile /opt/data/workspace/scripts/hermes_discord_payload_lint.py &&
/opt/data/workspace/scripts/hermes_discord_payload_lint.py --help
'
```
