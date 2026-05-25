# 03 — Skills et Learning Loop

## Skill mère existante

```text
/opt/data/skills/hermes-audit-remediation-learning-loop.md
```

Rôle annoncé :

```text
Audit → Diagnostic → Plan → Exécution → Vérification → Capitalisation
```

Elle existe déjà et doit être **étendue**, pas remplacée.

## Skill spécialisée Discord

```text
/opt/data/skills/hermes-discord-communication-guard.md
```

Rôle : règles opérationnelles Discord inter-agents.

Sections obligatoires :

- mentions numériques ;
- `allowed_mentions.users` ;
- `MISSION-ID` ;
- `TASK-ID` ;
- interdiction traces outils ;
- interdiction ACK texte ;
- séparation Hermes/OpenClaw ;
- `thread_id` validé explicitement ;
- dry-run obligatoire avant test réel ;
- modes linter.

## Mémoire curée

```text
/opt/data/workspace/memory/curated/LESSONS_LEARNED_MANDATORY.md
```

Doit contenir des records sous forme :

```md
## LEARNING LOOP RECORD — <incident>

Date:
Incident:
Symptôme:
Cause:
Skill créée/modifiée:
Mémoire curée:
Guardrail:
Test ajouté:
Healthcheck:
Critère de non-régression:
Date de révision:
```

## Patch SOUL minimal

Chaque SOUL.md doit seulement contenir :

```md
## LEÇONS DISCORD OBLIGATOIRES
Avant toute action Discord, appliquer skill:hermes-discord-communication-guard.
Si la skill est absente ou non chargée : BLOCKED.
```

Pas de règles détaillées dans les SOUL.md. Les règles détaillées vivent dans la skill.

## Chemins canoniques

| Élément | Chemin canonique |
|---|---|
| Linter | `/opt/data/workspace/scripts/hermes_discord_payload_lint.py` |
| Healthcheck | `/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh` |
| Rapport | `/opt/data/workspace/healthchecks/lessons_latest.md` |

`/usr/local/bin` est optionnel et non validé dans l’état actuel.
