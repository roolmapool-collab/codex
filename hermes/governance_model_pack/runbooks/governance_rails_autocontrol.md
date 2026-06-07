# Runbook: Governance Rails Auto-Control

> **Version:** 1.1
> **Date:** 2026-06-07
> **Scope:** Auto-control governance rails for Hermes v0.16
> **Type:** Read-only operational procedure
> **P37.3:** DR Git Push SSH classification — AUTH_FAILED, DNS_FAIL, SUBCONTEXT_PUSH_LIMITATION, NETWORK_FAIL, HOST_KEY_FAILED

---

## Objectif

Routine d'auto-contrôle qui vérifie régulièrement qu'Hermes reste sur les bons rails :
- procédures cohérentes
- documentation alignée
- sources de vérité respectées
- pas de retour de règles obsolètes
- pas de secrets exposés
- pas de cron/LLM parasite
- modèle routing conforme
- v0.16 stable
- mémoire/WAK/DR Git sains

**Principe:** Éviter le ferraillage documentaire. Rapports courts, anomalies seulement.

---

## Quand lancer

| Contexte | Fréquence | Commande |
|----------|-----------|----------|
| Avant mission lourde (P37+) | Manual | `python3 /opt/data/workspace/scripts/governance_rails_check.py --dry-run` |
| Après upgrade runtime | Manual | `python3 /opt/data/workspace/scripts/governance_rails_check.py --write` |
| Incident suspecté | Manual | `python3 /opt/data/workspace/scripts/governance_rails_check.py --write` |
| Cron OS (futur, après validation) | daily/weekly | avec `no_agent=true` + deliver=origin si FAIL |

**Ne pas lancer sur cron par défaut** — seulement si Stéphane valide l'installation OS cron.

---

## Commandes de test

```bash
# Dry-run — aperçu sans écriture
python3 /opt/data/workspace/scripts/governance_rails_check.py --dry-run

# Exécution + écriture JSON
python3 /opt/data/workspace/scripts/governance_rails_check.py --write

# Lecture du statut
cat /opt/data/workspace/healthchecks/governance_rails_status.json | python3 -m json.tool
```

---

## Structure du JSON de sortie

```json
{
  "generated_at": "2026-06-07T...",
  "decision": "PASS|PASS_WITH_WARNINGS|FAIL",
  "critical": 0,
  "warnings": 0,
  "errors_count": 5,
  "checks": {
    "runtime": {...},
    "health": {...},
    "cron": {...},
    "dr_git": {...},
    "docs": {...},
    "model_routing": {...},
    "security": {...},
    "skills": {...},
    "ownership": {...}
  },
  "next_actions": [
    {"priority": "CRITICAL", "action": "..."}
  ]
}
```

---

## Comment lire le JSON

### Champs principaux

| Champ | Signification |
|-------|---------------|
| `decision` | PASS / PASS_WITH_WARNINGS / FAIL |
| `critical` | Nombre de problèmes critiques (secret, v0.15 actif, etc.) |
| `warnings` | Anomalies non bloquantes |
| `errors_count` | Total des erreurs détectées |

### Décisions

| Decision | Signification | Action |
|----------|---------------|--------|
| `PASS` | Aucun problème détecté | Aucune action requise |
| `PASS_WITH_WARNINGS` | Anomalies mineures | Documenter, corriger si simple |
| `FAIL` | Problème critique détecté | STOP — corriger avant prochaine opération |

---

## Classification des anomalies

### CRITICAL (bloquantes)

| Anomalie | Seuil | Action |
|----------|-------|--------|
| Secret détecté | > 0 | STOP_AND_ASK — corriger immédiatement |
| v0.15 container actif | > 0 | STOP_AND_ASK — arrêt requis |
| Healthcheck critical > 0 | > 0 | STOP_AND_ASK — corriger santé |
| DR Git remote credentials | > 0 | STOP_AND_ASK — nettoyage requis |
| OpenRouter free pour prod/final | > 0 | STOP_AND_ASK — routage invalide |

### HIGH (à corriger rapidement)

| Anomalie | Action |
|----------|--------|
| DR Git dirty | Commit + push si scan OK |
| WAK vieux (>48h) | Lancer WAK manuellement |
| Healthcheck absent | Lancer healthcheck canonique |
| Doc manquante | Créer si critique, sinon noter |

### WARN (non bloquantes)

| Anomalie | Action |
|----------|--------|
| v0.15 migration pending |Indexer en HISTORICAL |
| Modèles P31-P36 pas indexés | Ajouter entrées register |
| Cron bruit (deliver=origin) | Corriger si excessif |

---

## Corrections automatiques vs validation

### Corrections AUTOMATIQUES (typo documentaire, non risqué)

- Orthographe dans runbook/ledger (non procédural)
- Mise à jour version number dans header
- Index DOC_INDEX après création nouveaux fichiers
- Ajout entrée P-N dans GOVERNANCE_MASTER_REGISTER après création ledger

### Corrections REQUISANT validation humaine

- Toute modification runtime
- Toute modification container
- Toute modification cron
- Toute modification modèle default
- Toute modification clé/secret
- Correction de fichier .env/config.yaml
- Promotion de MiMo (canary → active)
- Activation feature v0.15
- DR Git push avec secret scan FAIL

### STOP_AND_ASK immédiatement

- Secret détecté dans workspace/skills
- v0.15 container actif
- Runtime non v0.16
- DR Git remote contient credentials
- OpenRouter free autorisé pour prod/décision finale
- MiMo activé sans canary passé
- LLM cronjob bruyant réactivé
- Docs source de vérité manquantes

---

## Comment éviter le bruit

**Règle:** Rapport court = anomalies seules. Silence si PASS.

- PASS → Aucun rapport Discord/Telegram. Silencieux.
- PASS_WITH_WARNINGS → Rapport court : "WARN: X anomalies, voir JSON".
- FAIL → Rapport structuré : problème + next_action + STOP.

**Pas de:** ✅, 👍, "OK", "confirmé", "noté" — silencieux ou structuré.

---

## Installation cron OS (optionnel, après validation)

Si Stéphane valide l'installation :

```bash
# Ne pas utiliser no_agent=true pour ce script (analyse LLM requise)
# Mais garder deliver=origin uniquement si FAIL
# dry-run daily enough

# Exemple cron OS (NE PAS installer sans validation)
# 0 8 * * * cd /opt/data && python3 workspace/scripts/governance_rails_check.py --write
```

**Règle:** deliver=origin uniquement si FAIL. Silence si PASS.

---

## Intégration future

### Phase 1 (maintenant)
- Script Python read-only
- Lancement manuel
- Rapport dans JSON

### Phase 2 (après validation)
- Cron OS quotidien (dry-run)
- deliver=origin uniquement si FAIL
- Pas de notification si PASS

### Phase 3 (après stabilité)
- Intégration healthcheck canonique
- WAK inclut governance_rails dans score
- Alerte Discord uniquement si FAIL

---

## Stop Conditions

**Hermes doit STOP_AND_ASK si :**

| Condition | Seuil | Raison |
|-----------|-------|--------|
| Secret détecté | > 0 | Sécurité — exposition possible |
| Healthcheck critical > 0 | > 0 | Santé système compromise |
| v0.15 container actif | > 0 | Migration non complétée |
| Runtime non v0.16 | > 0 | Version non conforme |
| DR Git remote contient credential | > 0 | Exposition token |
| OpenRouter free pour prod/final | > 0 | Routage non conforme |
| MiMo activé sans canary | > 0 | Procédure non respectée |
| LLM cronjob bruyant réactivé | > 0 | Bruit excessif |
| Docs source de vérité manquantes | > 0 | Gouvernance incomplète |

---

## Vérifications détaillées

### A. Runtime / version

| Check | Attendu | KO si |
|-------|---------|-------|
| hermes_version | 0.16.x | autre version |
| container | hermes-v016-prod-s6 | v0.15 actif |
| v0.14 containers | NONE | encore présents |
| v0.15 containers | NONE | encore actifs |

### B. Health / mémoire

| Check | Attendu | KO si |
|-------|---------|-------|
| healthcheck_exists | true | absent |
| healthcheck critical | 0 | > 0 |
| healthcheck warnings | 0 ou classifié | non classifié |
| wak_exists | true | absent |
| wak_age_hours | < 48h | > 48h |
| current_state_exists | true | absent |
| curated_memory_exists | true | absent |

### C. Cron / bruit

| Check | Attendu | KO si |
|-------|---------|-------|
| os_cron_entries | ≤ nombre validé | excessif |
| wak_10_wrapper | true | absent |
| wak_15_direct | false | true |
| deliver_origin_count | minimal | excessif |
| cron_registry_exists | true | absent |

### D. DR Git / backup

|| Check | Attendu | KO si |
|-------|---------|-------|
| git_repo | true | false (non initialisé) |
| git_dirty | false | true (push non fait) |
| remote_has_credentials | false | true |
| last_commit | récent (<7j) | > 7j ou absent |
| dr_git_push_classification | PUSH_OK / OK_WITH_SUBCONTEXT_LIMITATION | AUTH_FAILED / DNS_FAIL / NETWORK_FAIL / HOST_KEY_FAILED / SUBCONTEXT_AUTH_FAILED |

#### DR Git Push — Classification SSH (P37.3)

Quand le push échoue, SSH retourne une erreur qu'il faut correctement interpréter :

| Code | Signification | Cause | Action |
|------|---------------|-------|--------|
| `PUSH_OK` | Push réussi | — | Aucune |
| `AUTH_FAILED` | Clé SSH non autorisée | Clé non enregistrée sur GitHub, révoquée, ou clé publique manquante | Stéphane : vérifier clé SSH sur GitHub |
| `DNS_FAIL` | Résolution DNS échoue | Alias SSH non résolu (sans -F ~/.ssh/config) ou réseau | Vérifier avec `ssh -F ~/.ssh/config` ; si OK → SSH config non chargé |
| `OK_WITH_SUBCONTEXT_LIMITATION` | Push OK dans host/root canonique, AUTH_FAILED dans subcontext hermes | Canonique PUSH_OK, subcontext limité. Action Stéphane = AUCUNE requise. |
| `SUBCONTEXT_AUTH_FAILED` | Canonique inaccessible + subcontext AUTH_FAILED | Impossible de vérifier — classification conservatrice |
| `NETWORK_FAIL` | Connexion réseau impossible | Firewall, proxy, réseau down | Vérifier connectivité réseau |
| `HOST_KEY_FAILED` | Host key GitHub a changé | known_hosts corrompu ou attaque MITM | Vérifier known_hosts |

**Règle critique:** Le message "Could not resolve hostname" de git n'est PAS le vrai diagnostic SSH. SSH resolve correctement l'alias `github.com-hermes-dr` → `github.com`. Le vrai diagnostic est le message SSH après connexion TCP (visible avec `-F ~/.ssh/config`).

**Diagnostic canonique:**
```bash
# 1. Vérifier SSH config chargeable
ssh -F ~/.ssh/config -o BatchMode=yes -T github.com-hermes-dr 2>&1

# 2. Parser le vrai message
# - "Permission denied (publickey)" → AUTH_FAILED
# - "Success" / pas de sortie → PUSH_OK
# - "Could not resolve hostname" après -F → vérifier config SSH

# 3. Si AUTH_FAILED: vérifier clé
ssh-keygen -lf ~/.ssh/id_ed25519
# → fingerprint doit correspondre à la clé enregistrée sur GitHub

# 4. Vérifier depuis contexte host/root canonique
# /root/hermes/data/DR_Backup/hermes_IA
# cd /root/hermes/data/DR_Backup/hermes_IA && git push origin main
```

**Nouvelle classification (P37.3):**
- P37.1/P37.2 avaient classé DR_PUSH_PENDING avec message "hostname non résolu"
- En réalité: SSH config non chargé dans le subprocess → false DNS error
- Le vrai problème: AUTH_FAILED (clé SSH non autorisée par GitHub)
- Classification corrigée: DR_GIT_PUSH = AUTH_FAILED

### E. Documentation rails

| Check | Attendu | KO si |
|-------|---------|-------|
| required_docs | tous présents | un absent |
| model_resources | ≥ 4 | < 4 |
| p31_p36_indexed | tous | partiels |
| v015_pending | NONE | présent |
| v014_v016_contradiction | none | présente |

### F. Model routing

| Check | Attendu | KO si |
|-------|---------|-------|
| mimo_status | CANARY_PENDING ou canary passé | ACTIVE sans canary |
| openrouter_non_auth | count > 0 | count = 0 |
| codex_routing | TECHNICAL_ONLY | autre |
| m3_routing_rules | count > 0 | absent |

### G. Security / secrets

| Check | Attendu | KO si |
|-------|---------|-------|
| secrets_found | 0 | > 0 |
| real_keys_in_examples | NONE | présent |

### H. Skills / operating contracts

| Check | Attendu | KO si |
|-------|---------|-------|
| critical_skills | tous présents | un absent |
| skill_headers_check | OK | FAIL |

### I. File ownership

| Check | Attendu | KO si |
|-------|---------|-------|
| workspace | hermes:hermes | root |
| healthchecks | hermes:hermes | root |
| curated_memory | hermes:hermes | root |
| agents_state | hermes:hermes | root |

---

## Sortie attendue

```
=== Governance Rails Check ===
Mode: EXECUTE

A. Runtime / version...
B. Health / mémoire...
C. Cron / bruit...
D. DR Git / backup...
E. Documentation rails...
F. Model routing...
G. Security / secrets...
H. Skills / operating contracts...
I. File ownership...

=== RESULT: PASS ===
Critical: 0
Warnings: 0
Errors: 0
Next actions: []

JSON written to: /opt/data/workspace/healthchecks/governance_rails_status.json
```

---

**Version:** 1.0
**Auteur:** Hermes Orchestrateur
**Date:** 2026-06-07