# AGENTS.md — Instructions Codex pour réparation Hermes

Tu es Codex et tu reprends une réparation Hermes / Discord / skills. Lis ce fichier avant toute action.

## Mission

Stabiliser Hermes multi-agents Discord et finaliser l’apprentissage permanent Hermes.

## Priorités

1. Corriger le blocage permissions du healthcheck lessons.
2. Vérifier que le rapport canonique est généré : `/opt/data/workspace/healthchecks/lessons_latest.md`.
3. Auditer Docker env côté hôte pour les réactions Discord stale.
4. Proposer la correction Discord reactions sans appliquer sans validation.
5. Ne jamais envoyer de message Discord réel sans validation humaine.

## Interdictions absolues

- Ne pas envoyer Discord.
- Ne pas tester Discord.
- Ne pas redémarrer.
- Ne pas kill PID 6 / PID 7 / PID 1.
- Ne pas modifier `.env`.
- Ne pas modifier `config.yaml`.
- Ne pas afficher de token ou secret.
- Ne pas mélanger OpenClaw et Hermes.
- Ne pas remplacer la skill mère `hermes-audit-remediation-learning-loop.md`.
- Ne pas changer le chemin canonique du rapport healthcheck.

## Chemins clés

- Skill mère : `/opt/data/skills/hermes-audit-remediation-learning-loop.md`
- Skill Discord : `/opt/data/skills/hermes-discord-communication-guard.md`
- Mémoire curée : `/opt/data/workspace/memory/curated/LESSONS_LEARNED_MANDATORY.md`
- Linter : `/opt/data/workspace/scripts/hermes_discord_payload_lint.py`
- Healthcheck : `/opt/data/workspace/scripts/hermes_lessons_healthcheck.sh`
- Rapport canonique : `/opt/data/workspace/healthchecks/lessons_latest.md`
- Config Discord : `/opt/data/config.yaml`
- Env default : `/opt/data/.env`

## Style d’action attendu

Toujours suivre :

```text
audit → preuve → proposition → validation humaine → action limitée → vérification
```

Jamais d’action opportuniste.

## Format des réponses Codex attendues

- Toujours donner un statut : `OK`, `KO`, `PARTIEL`.
- Toujours citer les preuves : sortie commande, chemin, taille, owner, exit code.
- Si permission denied : STOP et demander action root/hôte.
- Si secret détecté : masquer et STOP si risque.

## Règle Discord centrale

Discord n’est pas un terminal, pas un log, pas une console de debug. Discord reçoit uniquement des messages validés.

Tout message Hermes → agent doit être validé par le linter en mode `outbound_mission` avant envoi réel.

## Mention Ariane

- Bot/User ID Ariane : `1505112142792097872`
- Canal Ariane : `1505129251232546858`
- Mention Ariane : `<@1505112142792097872>`

Ne jamais confondre channel ID et user ID.
