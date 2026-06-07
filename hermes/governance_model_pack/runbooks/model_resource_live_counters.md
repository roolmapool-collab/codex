# runbooks/model_resource_live_counters.md

## Live Counters Gate — Runbook v1.1

**Purpose:** Before routing any task, Hermes must know the real state of model resources.

**Version:** 1.1
**Date:** 2026-06-07
**Source:** P37 + P37.2 Model Resource Live Counters + Credential Key Context Fix
**Owner:** Hermes Orchestrateur

---

## Le concept "Live Counter Gate"

Before routing a model (for Hermes or for sub-agents), Hermes MUST:

### A. Classifier la tâche

| Dimension | Question | Détecte |
|-----------|----------|---------|
| `task_type` | Orchestration / Technical / Reasoning / Draft | Quel modèle par défaut |
| `risk` | LOW / MEDIUM / HIGH / CRITICAL | STOP_AND_ASK si rouge |
| `output_format` | JSON / Markdown / Code / Shell | Qui peut produire |
| `expected_duration` | Court / Moyen / Long | Qui préserve les quotas |
| `technical_action` | Yes / No | Codex vs M2.7 |
| `secrets/prod/release` | Yes / No | M2.7 only, pas OpenRouter |

### B. Vérifier le statut des ressources

1. Lire `/opt/data/workspace/healthchecks/model_resource_status.json` si récent (< 1h)
2. Si absent ou stale → lancer `model_resource_probe.py --dry-run`
3. Si compteur manuel requis → demander à Stéphane
4. **Ne jamais inventer un quota**

### C. Choisir le modèle

Selon besoin + statut réel + quota + risque.

### D. Reporter brièvement

**Format obligatoire:**

```
Task: [description]
Risk: [LOW|MEDIUM|HIGH|CRITICAL]
Output: [format]
Selected model/resource: [name]
Counters used: [automatic|manual|unknown]
Unavailable resources: [list or NONE]
Why not MiniMax: [reason or N/A]
Why not Codex: [reason or N/A]
Why not MiMo: [reason or N/A]
Why not OpenRouter: [reason or N/A]
Fallback: [fallback model or STOP_AND_ASK]
Human validation: [YES/NO]
```

---

## Compteurs par ressource

### MiniMax

| Counter | Comment | Status |
|---------|---------|--------|
| Models available | `/v1/models` via API | **AUTOMATIC** |
| Provider health | Last errors/logs | **AUTOMATIC** |
| 5h quota | Dashboard MiniMax | **MANUAL_REQUIRED** |
| Weekly quota | Dashboard MiniMax | **MANUAL_REQUIRED** |
| Monthly quota | Dashboard MiniMax | **MANUAL_REQUIRED** |
| Latence récente | gateway.log probe | **AUTOMATIC** |

**Status possibles:** GREEN / YELLOW / RED / UNKNOWN

**Règle:** Ne jamais supposer "quota OK" sans preuve ou indication récente.

### Codex OAuth

| Counter | Comment | Status |
|---------|---------|--------|
| OAuth status | Nous probe via API | **AUTOMATIC** |
| Tool availability | Hermes status | **AUTOMATIC** |
| Usage remaining | Dashboard Nous | **MANUAL_REQUIRED** |
| Session limits | Dashboard Nous | **MANUAL_REQUIRED** |

**Status possibles:** GREEN / YELLOW / RED / UNKNOWN

**Règle:** Codex réservé actions techniques. Si usage inconnu mais tool OK → YELLOW, pas GREEN.

### MiMo

| Counter | Comment | Status |
|---------|---------|--------|
| Canary status | mimo.md fiche | **AUTOMATIC** |
| Models available | `/v1/models` via API | **AUTOMATIC** (read-only discovery) |
| Monthly credits | Dashboard token-plan | **MANUAL_REQUIRED** |
| Usage % | Dashboard token-plan | **MANUAL_REQUIRED** |
| Days left in month | Calculation | **AUTOMATIC** |
| Off-peak benefit | Doc-only | **DOC_ONLY** |

**Status possibles:** CANARY_LEVEL_1_PASS / CANARY_LEVEL_2_PASS / ACTIVE_LIMITED_PREMIUM

**Règle:** Pas de routing réel tant que Level 2+ non validé. Level 1 = découverte modèles uniquement.

### OpenRouter free

| Counter | Comment | Status |
|---------|---------|--------|
| Availability | API probe | **AUTOMATIC** |
| Recent errors/rate limits | gateway.log | **AUTOMATIC** |
| Quality | Observation | **DOC_ONLY** |

**Status possibles:** GREEN_FOR_DRAFT / YELLOW / RED

**Règle:** Même GREEN, OpenRouter reste non-authoritative.

---

## Règles de routing obligatoires

### Si tâche CRITICAL / PROD / SECRETS / RELEASE

```
Models: MiniMax-M2.7
Condition: Si compteur inconnu/rouge → STOP_AND_ASK
Never: OpenRouter, MiMo (sauf ACTIVE_LIMITED+ avec validation sécurité)
```

### Si tâche LONG-CONTEXT NON CRITICAL

```
Models: M3 si MiniMax disponible
MiMo si Level 2+ et quota mensuel à valoriser
Sinon: M2.7 ou STOP_AND_ASK
```

### Si tâche TECHNICAL ACTION

```
Models: Codex si disponible
MiMo après canary coding (Level 2+)
M2.7 pour analyse
OpenRouter: INTERDIT pour code prod
```

### Si tâche DRAFT / EXPLORATION

```
Models: OpenRouter free si GREEN_FOR_DRAFT
MiMo si quota mensuel doit être valorisé et canary OK
Sinon: Modèle auxiliaire
```

---

## Pourquoi un compteur est manuel

Un compteur est MANUAL_REQUIRED quand :

| Raison | Exemple |
|--------|---------|
| API absente | MiniMax ne expose pas d'endpoint quota usage |
| API non documentée | Aucune doc Hermes ne confirme un endpoint usage |
| Dashboard only | MiniMax quota只能通过 dashboard 检查 |
| OAuth non lisible | Codex: auth.json interdit de lecture |
| Risque secret | Appeler un endpoint non documenté = risque exposure |
| Contexte host/container | .env present but not loaded in runtime environment |

**Règle:** MANUAL_REQUIRED ne signifie pas "inconnu". Ça signifie "accessible uniquement par humain via dashboard".

---

## Ne pas confondre clé absente et clé non chargée

| Situation | Classification | Action |
|-----------|---------------|--------|
| Key in /opt/data/.env but not exported in runtime | KEY_PRESENT_ENV_FILE | Ne pas dire "clé absente" — utiliser la clé depuis .env si possible, sinon demander à Stéphane |
| No key in .env files | KEY_NOT_CONFIGURED | STOP_AND_ASK — clé manquante |
| Key in .env but Hermes context différent | KEY_PRESENT_ENV_FILE (risque) | Vérifier canary avant usage |
| auth.json existe mais forbidden to inspect | OAUTH_STATUS_UNKNOWN | Ne pas dire "token absent" — dire "OAUTH_STATUS_UNKNOWN (auth.json forbidden)" |
| Clé présente dans env runtime | KEY_PRESENT_ENV | Probe OK |
| Clé présente dans .env seulement | KEY_PRESENT_ENV_FILE | Canary ou Stéphane validation requis |

**Exemples concrets:**

```
# MINIMAX — clé dans .env mais pas dans env runtime
Status: YELLOW
credentials: {key_present: true, key_source: "ENV_FILE"}
→ Ne PAS dire "clé absente"
→ Dire "clé présente dans .env mais pas chargée. Stéphane doit fournir quota ou reload."

# CODEX — auth.json non lisible
Status: UNKNOWN
credentials: {key_present: false, key_source: "NOT_FOUND"}
oauth: "OAUTH_STATUS_UNKNOWN"
→ Ne PAS dire "token absent"
→ Dire "OAUTH_STATUS_UNKNOWN — auth.json non inspectable. Stéphane doit valider Codex."

# MiMo — clé dans .env, canary L1 PASS
Status: CANARY_LEVEL_1_PASS
credentials: {key_present: true, key_source: "ENV_FILE"}
→ Canaries L1 PASS confirmer clé valide dans contexte Hermes
→ Ne pas rétrograder à UNKNOWN
```

---

## Credential Status — Classification

Chaque ressource a un `credentials` block dans son status :

```json
"credentials": {
  "key_present": true|false,
  "key_source": "ENV|ENV_FILE|NOT_FOUND",
  "key_type": "token_plan|oauth|subscription|unknown",
  "secret_exposed": false,
  "runtime_note": "..."  // optional, quand key_source = ENV_FILE
}
```

**Classification des clés:**

- `ENV`: Clé chargée dans l'environnement courant (os.environ)
- `ENV_FILE`: Clé présente dans fichier .env canonique mais pas dans env runtime
- `NOT_FOUND`: Clé absente de tout fichier/environnement connu

---

## Probe — Commandes

```bash
# Dry-run (simulation, ne modifie rien)
python3 /opt/data/workspace/scripts/model_resource_probe.py --dry-run

# Live probe (écrit model_resource_status.json)
python3 /opt/data/workspace/scripts/model_resource_probe.py --write

# Probe resource spécifique
python3 /opt/data/workspace/scripts/model_resource_probe.py --resource minimax
python3 /opt/data/workspace/scripts/model_resource_probe.py --resource mimo
```

---

## Demande de compteurs manuels

Quand Hermes ne peut pas lire les compteurs automatiquement :

```
J'ai besoin des compteurs actuels :
- MiniMax : usage 5h / weekly ?
- Codex : usage restant ?
- MiMo : usage mensuel % ?
Sinon je route en mode conservateur.
```

**Fallback:** Mode conservateur → M2.7 only, préserver les autres.

---

## Intégration governance rails

Le script `governance_rails_check.py` peut vérifier :

- Existence/fraîcheur de `model_resource_status.json`
- Ne pas exiger GREEN partout
- Alerter si status absent/stale avant opération lourde
- Ne pas bloquer si compteurs manuels absents
- STOP_AND_ASK pour tâches CRITICAL si compteur rouge/inconnu

---

## Fichiers de référence

- `/opt/data/workspace/MODEL_RESOURCE_GOVERNANCE.md` — Gouvernance modèles
- `/opt/data/workspace/runbooks/ai_model_routing.md` — Routage IA
- `/opt/data/workspace/healthchecks/model_resource_status.json` — Status live
- `/opt/data/workspace/healthchecks/model_resource_status.example.json` — Template
- `/opt/data/workspace/model_resources/minimax.md` — Fiche MiniMax
- `/opt/data/workspace/model_resources/codex_oauth.md` — Fiche Codex
- `/opt/data/workspace/model_resources/mimo.md` — Fiche MiMo
- `/opt/data/workspace/model_resources/openrouter_free.md` — Fiche OpenRouter
- `/opt/data/workspace/scripts/model_resource_probe.py` — Script probe