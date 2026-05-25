# SPEC — hermes_lessons_healthcheck.sh

## Objectif

Vérifier que le système d’apprentissage permanent Hermes est installé et fonctionnel.

## Rapport canonique

```text
/opt/data/workspace/healthchecks/lessons_latest.md
```

## Contrôles obligatoires

- skill Discord présente ;
- skill Discord lisible et non vide ;
- sections obligatoires présentes ;
- skill mère learning loop patchée ;
- `LESSONS_LEARNED_MANDATORY.md` présent ;
- linter présent et exécutable ;
- fixtures lint exécutées réellement ;
- 5 SOUL.md référencent la skill ;
- aucun SOUL.md ne réfère OpenClaw comme source Discord Hermes ;
- rapport généré au chemin canonique.

## Interdictions

- ne corrige rien ;
- n’envoie pas Discord ;
- ne modifie pas .env/config.yaml ;
- ne redémarre rien.
