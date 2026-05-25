# 01 — Contexte et architecture Hermes

## Philosophie Hermes / Nous Agent IA

Hermes est conçu comme un agent qui apprend par expérience : il crée ou améliore ses skills, persiste la connaissance utile, recherche dans ses conversations passées, et devient plus capable au fil des sessions.

La réparation actuelle doit respecter cette philosophie :

```text
Incident → Learning Loop Record → Skill update → Mémoire curée → Lint/Test → Healthcheck → Révision
```

## Profiles Hermes

Les profils Hermes sont isolés : chacun possède son propre répertoire, `config.yaml`, `.env`, `SOUL.md`, mémoire, sessions, skills et gateway state.

| Profil | Rôle | Chemin |
|---|---|---|
| default | Hermes Orchestrateur | `/opt/data` |
| hermes-ariane | PM/UX | `/opt/data/profiles/hermes-ariane` |
| hermes-vulcain | Full Stack | `/opt/data/profiles/hermes-vulcain` |
| hermes-argus | QA | `/opt/data/profiles/hermes-argus` |
| hermes-atlas | DevOps | `/opt/data/profiles/hermes-atlas` |

## Architecture attendue

- Hermes orchestre.
- Les agents spécialisés ne se parlent pas directement.
- Toute consultation passe par Hermes via `REQUEST-CONSULT`.
- Discord doit être un canal de mission propre, pas une console d’outils.

## Séparation Hermes / OpenClaw

OpenClaw et Hermes sont deux périmètres distincts.

Dans un incident Hermes Discord multi-agents, sources prioritaires :

```text
DISCORD_* / AGENTS_* / discord_inventory.md / skills Hermes
```

Les docs OpenClaw sont interdites comme source principale sauf si le ticket mentionne explicitement OpenClaw.
