# 05 — Prompts prêts à coller pour Codex / Hermes

## Prompt 1 — Démarrage Codex

```text
Codex, tu reprends la réparation Hermes Discord / skills.
Lis AGENTS.md puis README_PASSATION_CODEX_HERMES.md.
Tu dois travailler en mode audit → preuve → proposition → validation.
Ne modifie rien avant d’avoir produit un rapport d’état.
Priorité 1 : corriger le healthcheck lessons au chemin canonique.
Priorité 2 : auditer les réactions Discord stale.
Aucun message Discord réel.
Aucun restart.
Aucun kill.
Aucune modification .env/config.yaml.
```

## Prompt 2 — Audit healthcheck lessons

```text
Audit le système apprentissage permanent Hermes.
Vérifie les fichiers, les scripts, les fixtures, et le rapport healthcheck.
Ne corrige rien.
Rapporte les permissions du dossier /opt/data/workspace/healthchecks.
```

## Prompt 3 — Correction permissions validée

```text
VALIDER CORRECTION PERMISSIONS healthcheck lessons.
Depuis hôte/root uniquement, corriger owner de /opt/data/workspace/healthchecks vers 10000:10000.
Ne change pas le chemin du rapport.
Relance ensuite le healthcheck.
Rapport attendu : lessons_latest.md généré au chemin canonique.
```

## Prompt 4 — Audit réactions Discord

```text
Audit les réactions Discord Hermes.
Ne modifie rien.
Vérifie Docker Config.Env depuis l’hôte, /opt/data/.env, /opt/data/config.yaml et l’environnement runtime PID.
Objectif : expliquer pourquoi DISCORD_REACTIONS=true persiste.
```

## Prompt 5 — Dry-run payload Ariane

```text
Prépare uniquement un dry-run payload Ariane.
Ne l’envoie pas.
Canal : 1505129251232546858
Bot/User ID Ariane : 1505112142792097872
Mention : <@1505112142792097872>
Linter mode : outbound_mission
Attendre validation humaine avant tout envoi réel.
```
