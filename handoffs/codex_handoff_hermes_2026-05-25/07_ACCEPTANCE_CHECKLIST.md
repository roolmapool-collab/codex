# 07 — Checklist d’acceptation

## Apprentissage permanent Hermes

- [ ] `hermes-discord-communication-guard.md` présent et lisible.
- [ ] `hermes-audit-remediation-learning-loop.md` patché, pas écrasé.
- [ ] `LESSONS_LEARNED_MANDATORY.md` présent avec 6 records.
- [ ] Linter présent dans `/opt/data/workspace/scripts/`.
- [ ] Healthcheck présent dans `/opt/data/workspace/scripts/`.
- [ ] `healthchecks/` writable par uid 10000.
- [ ] Rapport généré : `/opt/data/workspace/healthchecks/lessons_latest.md`.
- [ ] 8 fixtures lint passent.
- [ ] Les 5 SOUL.md référencent la skill Discord guard.
- [ ] Aucun SOUL.md ne réfère OpenClaw comme source principale Discord Hermes.

## Discord reactions

- [ ] Docker Config.Env ne contient pas `DISCORD_REACTIONS=true`.
- [ ] Docker Config.Env ne contient pas le canal Ariane dans `DISCORD_ALLOWED_CHANNELS` default.
- [ ] `/opt/data/.env` contient `DISCORD_REACTIONS=false`.
- [ ] `/opt/data/config.yaml` a `discord.reactions: false`, si correction validée.
- [ ] Après restart contrôlé, PID runtime a `DISCORD_REACTIONS=false`.
- [ ] Hermes default ne réagit plus dans les canaux agents.

## Ariane routing

- [ ] Ariane gateway running.
- [ ] Token conflict absent.
- [ ] api_server conflict absent.
- [ ] Dry-run payload validé par linter.
- [ ] Envoi réel validé humainement.
- [ ] Un seul message envoyé.
- [ ] Pas d’ACK de suivi.
- [ ] Ariane répond selon consigne.

## Décision finale

- [ ] `APPRENTISSAGE PERMANENT HERMES VALIDÉ`
- [ ] `DISCORD REACTIONS CORRIGÉES`
- [ ] `ARIANE ROUTING VALIDÉ`
