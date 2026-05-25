# Hermes Agents Online Repair - 2026-05-25

## Problem

Discord agents were not visible online in their channels.

The default Hermes gateway was running, but the named profiles were configured only as profile directories. Docker Compose had no services for the named agent gateways.

## Findings

Existing Compose services before repair:

- `gateway` -> default Hermes gateway only
- `dashboard`

Profile state before repair:

- `hermes-ariane`: gateway stopped
- `hermes-vulcain`: gateway stopped
- `hermes-argus`: gateway stopped
- `hermes-atlas`: gateway stopped

`hermes gateway start` is not applicable inside the Docker container:

```text
Service start is not applicable inside a Docker container.
The gateway runs as the container's main process.
```

Therefore each agent needs its own Docker Compose service running `gateway run` with `HERMES_HOME` pointing at that profile directory.

## Action

Backed up Compose file:

```text
/docker/hermes/docker-compose.yml.bak.20260525_160257
```

Added four Compose services:

- `ariane` -> `HERMES_HOME=/opt/data/profiles/hermes-ariane`
- `vulcain` -> `HERMES_HOME=/opt/data/profiles/hermes-vulcain`
- `argus` -> `HERMES_HOME=/opt/data/profiles/hermes-argus`
- `atlas` -> `HERMES_HOME=/opt/data/profiles/hermes-atlas`

Started only the four new agent services:

```bash
docker compose -f /docker/hermes/docker-compose.yml up -d --no-deps ariane vulcain argus atlas
```

The default gateway and dashboard were not recreated during this step.

## Verification

Docker containers after repair:

```text
hermes-ariane   Up
hermes-vulcain  Up
hermes-argus    Up
hermes-atlas    Up
hermes-agent-1  Up
hermes-dashboard Up
```

Profile status from inside each agent container:

- Ariane: `Gateway Service: running`, model `openrouter/owl-alpha`
- Vulcain: `Gateway Service: running`, model `openrouter/owl-alpha`
- Argus: `Gateway Service: running`, model `poolside/laguna-m.1:free`
- Atlas: `Gateway Service: running`, model `nvidia/nemotron-3-super-120b-a12b:free`

Discord connection evidence from gateway logs:

- Ariane connected as `Ariane PM/UX#8941`
- Vulcain connected as `Vulcain Full Stack#9135`
- Argus connected as `Argus QA (Hermes)#3095`
- Atlas connected as `Atlas DevOps (Hermes)#2038`

## Caveats

`hermes gateway list` and `hermes profile list` still report named gateways as stopped from the default container. In this Docker deployment that output is misleading because the named gateways now run as separate Compose containers, not as internal service-managed processes.

Several agent profile `.env` files still have `DISCORD_REACTIONS=true`. This was not changed in this intervention.
