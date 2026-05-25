# 02 — Discord incidents et garde-fous attendus

## Incidents majeurs

### 1. Discord tool trace leak

Hermes a envoyé dans Discord des traces internes :

```text
send_message
skill_view
search_files
read_file
terminal
tool_call
exit_code
Traceback
DEBUG
```

### 2. Bad mention format

Hermes a utilisé des mentions textuelles (`@Ariane`) ou confondu :

```text
Bot/User ID = 1505112142792097872
Channel ID = 1505129251232546858
```

### 3. OpenClaw/Hermes confusion

Hermes a cherché des règles Hermes Discord dans une skill OpenClaw.

### 4. ACK/ping-pong agents

Les agents ont généré des boucles d’ACK / Roger / emoji.

### 5. thread_id non validé

Hermes a proposé un `thread_id` sans validation explicite.

### 6. PID/ENV stale Docker

PID 6 / PID 7 a conservé des variables runtime stale :

```text
DISCORD_REACTIONS=true
DISCORD_ALLOWED_CHANNELS contient le canal Ariane
```

## Format Discord valide Hermes → agent

```json
{
  "channel_id": "1505129251232546858",
  "content": "<@1505112142792097872>\nMISSION-ID: TEST-ARIANE-ROUTING-001\nTASK-ID: TEST-ARIANE-ROUTING-001\nSOURCE: Hermes\nTARGET: Ariane\nOBJECTIF: Répondre uniquement DONE ARIANE ROUTING.\nSTATUT ATTENDU: DONE",
  "allowed_mentions": {
    "users": ["1505112142792097872"]
  }
}
```

## Linter attendu

Modes minimum :

### `outbound_mission`

Hermes → agent.

Obligatoire :

- `channel_id`
- `content`
- mention numérique `<@BOT_USER_ID>`
- `allowed_mentions.users` contenant le même Bot/User ID
- `MISSION-ID`
- `TASK-ID`

Interdit :

- trace outil
- mention textuelle
- ACK seul
- DONE seul sans contexte
- `thread_id` sans `metadata.thread_validated=true`

### `agent_reply`

Agent → Hermes.

Autorisé :

- `DONE`
- `BLOCKED`
- `NEEDS_VALIDATION`
- `RISK_DETECTED`

Interdit :

- trace outil
- ACK inutile
- emoji ACK

## Fixtures requises

| Fixture | Mode | Résultat attendu |
|---|---|---|
| payload valide | outbound_mission | OK |
| trace outil | outbound_mission | KO |
| mention textuelle | outbound_mission | KO |
| channel ID comme mention | outbound_mission | KO |
| thread_id non validé | outbound_mission | KO |
| ACK seul | outbound_mission | KO |
| réponse DONE structurée | agent_reply | OK |
| DONE seul en outbound | outbound_mission | KO |
