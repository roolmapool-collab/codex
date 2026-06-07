# Model Availability & Quota Probe — Runbook

> **Version:** 1.0
> **Date:** 2026-06-07
> **Source:** P34 Model Availability Quota Probe
> **Owner:** Hermes Orchestrateur
> **Classification:** DOC_ONLY — Procédure opérationnelle

---

## Objectif

Avant toute tâche importante, Hermes doit répondre à cette question :

> **"Quel modèle est pertinent ET disponible maintenant, selon les compteurs 5h, hebdo, mensuels, latence, statut canary et risque ?"**

Ce runbook définit :
- Les probes par ressource (disponibilité, compteur)
- Les seuils green/yellow/red
- Les règles de décision dynamique
- La procédure canary MiMo (PREPARE ONLY — NE PAS EXÉCUTER sans validation)

---

## Règle absolue

**Aucune clé n'est exposée, écrite, ou indexée. Aucune modification runtime. Aucune automatisation MiMo.**

---

## Section 1 — Model Resource Probe

### A. MiniMax

#### Probe disponible ?

| Probe | Méthode | Fréquence | Sécurité |
|-------|---------|----------|----------|
| `/v1/models` accessible | curl read-only | Par session | Aucune clé exposée |
| M2.7 disponible | Probe /v1/models | Par session | Aucune clé exposée |
| M3 disponible | Probe /v1/models | Par session | Aucune clé exposée |
| Erreurs provider récentes | Session observation | Continu | Aucune |
| Latence moyenne | Session observation | Continu | Aucune |
| Usage quota 5h | COUNTER_MANUAL_REQUIRED | Dashboard Stéphane | MANUAL |
| Usage hebdo | COUNTER_MANUAL_REQUIRED | Dashboard Stéphane | MANUAL |

#### Commande probe (read-only)

```bash
# Probe MiniMax models (read-only, pas de clé en clair)
curl -s "https://api.minimax.io/v1/models" \
  -H "Authorization: Bearer sk-cp-***MASKED***" \
  --max-time 10
```

**Note:** La clé n'est jamais affichée. Utiliser `***MASKED***` en output.

#### Seuils

| Statut | Condition | Action |
|--------|-----------|--------|
| **GREEN** | models OK + pas de 429/529 récent + quota OK | USE |
| **YELLOW** | Latence haute (>15s) ou 529 sporadique | PRESERVE + WARN |
| **RED** | 429 / quota EXHAUSTED / endpoint KO | STOP_AND_ASK |

#### Compteurs

| Counter | Type | Comment |
|---------|------|---------|
| Quota 5h | MANUAL_REQUIRED | Stéphane check dashboard |
| Quota hebdo | MANUAL_REQUIRED | Stéphane check dashboard |
| Quota mensuel | MANUAL_REQUIRED | Stéphane check dashboard |
| Latence | AUTOMATIC | Session observation |
| Erreurs 429/529 | AUTOMATIC | Session observation |

#### Comportement si indisponible

| Situation | Action |
|-----------|--------|
| 529 × 2 | STOP, fallback OpenRouter ou STOP_AND_ASK |
| 429 | STOP_AND_ASK (quota épuisé) |
| Latence >15s × 3 | STOP |
| Endpoint KO | STOP_AND_ASK |

---

### B. Codex OAuth

#### Probe disponible ?

| Probe | Méthode | Fréquence | Sécurité |
|-------|---------|----------|----------|
| OAuth connecté | Check Nous/Codex status | Par session | Aucune clé exposée |
| Codex tool/runtime disponible | Test tool call | Par session | Aucune |
| Capacité shell/git/fichiers | Observation | Continu | Aucune |
| Usage restant | COUNTER_MANUAL_REQUIRED | Dashboard Nous | MANUAL |

#### Commande probe

```bash
# Probe Codex OAuth (ne jamais lire auth.json)
# Vérification via session ou test tool
echo "Codex OAuth: vérifier via session Hermes"
```

**Règle:** Ne jamais lire/afficher `auth.json`. La clé OAuth est gérée par Nous/Codex.

#### Seuils

| Statut | Condition | Action |
|--------|-----------|--------|
| **GREEN** | OAuth OK + tool disponible | USE |
| **YELLOW** | Usage inconnu mais tool OK | PRESERVE + MANUEL |
| **RED** | OAuth KO / tool inaccessible | STOP_AND_ASK |

#### Compteurs

| Counter | Type | Comment |
|---------|------|---------|
| OAuth status | AUTOMATIC | Nous/Codex |
| Usage remaining | MANUAL_REQUIRED | Dashboard Nous |
| Session limits | MANUAL_REQUIRED | Dashboard Nous |

#### Comportement si indisponible

| Situation | Action |
|-----------|--------|
| OAuth KO | STOP_AND_ASK |
| Rate limit 429 | STOP, fallback M2.7 si non critique |
| Tool inaccessible | STOP_AND_ASK si tech requise |

---

### C. Xiaomi/MiMo

#### Probe disponible ?

| Probe | Méthode | Fréquence | Sécurité |
|-------|---------|----------|----------|
| Statut canary | COUNTER_MANUAL_REQUIRED | Stéphane validation | MANUAL |
| Base URLs documentées | DOC_ONLY | N/A | N/A |
| Modèle listé dans plan | COUNTER_MANUAL_REQUIRED | Stéphane | MANUAL |
| Quota mensuel | MANUAL_REQUIRED | Dashboard token-plan | MANUAL |
| /v1/models | SEULEMENT après validation Stéphane (canary Niveau 1) | N/A | N/A |

**Status actuel:** CANARY_LEVEL_2_PASS — Niveau 1-2 PASS, Niveau 3 (coding) en attente

#### Seuils

| Statut | Condition | Action |
|--------|-----------|--------|
| **DOC_ONLY** | CANARY_PENDING | NO_RUNTIME_USE |
| **YELLOW** | Clé disponible mais non testée | CANARY_ALLOWED (Niveau 1) |
| **RED** | Clé absente / règles usage non acceptées | STOP_AND_ASK |

#### Compteurs

| Counter | Type | Comment |
|---------|------|---------|
| Monthly quota | MANUAL_REQUIRED | Dashboard token-plan (11B credits) |
| Usage % | MANUAL_REQUIRED | Dashboard token-plan |
| Days left | MANUAL_REQUIRED | Stéphane track |
| Canary status | MANUAL_REQUIRED | Stéphane validation |

#### Règles de sécurité MiMo

| Action | Autorisé |
|--------|----------|
| Appeler avec vraie clé | ❌ INTERDIT sans canary Niveau 1-3 |
| Écrire clé en doc | ❌ INTERDIT ABSOLU |
| Indexer clé OpenViking | ❌ INTERDIT ABSOLU |
| Clé en Discord | ❌ INTERDIT ABSOLU |
| /v1/models canary | ⚠️ Après validation Stéphane ONLY |

---

### D. OpenRouter Free / Owl Alpha

#### Probe disponible ?

| Probe | Méthode | Fréquence | Sécurité |
|-------|---------|----------|----------|
| Modèle disponible | OpenRouter API | Par session | Aucune clé requise |
| Erreurs récentes | Session observation | Continu | Aucune |
| Latence | Session observation | Continu | Aucune |
| Qualité récente | Session observation | Continu | Aucune |
| Rate limit | AUTOMATIC | Observation | Aucune |

#### Commande probe

```bash
# Probe OpenRouter model availability (free tier)
curl -s "https://openrouter.ai/api/v1/models" --max-time 10
```

#### Seuils

| Statut | Condition | Action |
|--------|-----------|--------|
| **GREEN** | Modèle disponible + pas d'erreur | DRAFT_ONLY |
| **YELLOW** | Instable mais disponible | DRAFT_ONLY + CAUTION |
| **RED** | Erreurs / rate limit × 3 | AVOID / STOP_AND_ASK |

**Règle:** OpenRouter GREEN = brouillon uniquement. Pas authoritative même si GREEN.

#### Compteurs

| Counter | Type | Comment |
|---------|------|---------|
| Model availability | AUTOMATIC | OpenRouter API |
| Rate limits | AUTOMATIC | Session observation |
| Latence | AUTOMATIC | Session observation |
| Output quality | AUTOMATIC | Session observation |

---

## Section 2 — Règles de Décision Dynamique

### Avant toute tâche importante

**Step 1 — Classifier tâche**

| Dimension | Options |
|-----------|---------|
| Task Type | ORCHESTRATION / TECHNICAL_ACTION / LONG_CONTEXT_REASONING / DRAFT_OR_BRAINSTORM / STRUCTURED_OUTPUT / SECURITY_OR_SECRET / PROD_RELEASE_ROLLBACK / SIMPLE_SUMMARY |
| Risk | LOW / MEDIUM / HIGH / CRITICAL |
| Output Format | FREE_TEXT / JSON_STRICT / MARKDOWN_REPORT / CODE_PATCH / SHELL_ACTION / DISCORD_MESSAGE |
| Expected Duration | SHORT (<60s) / MEDIUM (60s-5min) / LONG (>5min) |
| Technical Action | YES / NO |

**Step 2 — Lire/proposer probe status**

| Situation | Action |
|-----------|--------|
| Status récent existe (<1h) | Utiliser ce status |
| Status absent/stale | Lancer probes read-only autorisées |
| Quota manuel nécessaire | Demander à Stéphane |
| MiMo requise sans canary | STOP_AND_ASK |

**Step 3 — Choisir modèle selon matrice + disponibilité**

| Scénario | Decision |
|---------|----------|
| M2.7 pertinent mais quota 5h LOW | M3 si reasoning long-context, MiMo si canary PASS, sinon STOP_AND_ASK |
| Codex pertinent mais usage LOW | MiMo si canary PASS + coding interactif, sinon M2.7 pour analyse, sinon STOP_AND_ASK |
| OpenRouter GREEN | Uniquement brouillon |
| MiMo quota élevé fin de mois + canary PASS | Proposer MiMo pour offload premium |
| M3 pertinent mais output JSON strict | M2.7 ou STOP_AND_ASK |

**Step 4 — Reporter le choix**

Format obligatoire dans toute justification :

```
Task:
Risk:
Output:
Probe freshness: <timestamp ou "UNKNOWN">
Selected resource:
Why:
Why not MiniMax:
Why not Codex:
Why not MiMo:
Why not OpenRouter:
Quota impact:
Fallback:
Human validation:
```

---

## Section 3 — Fichier Status Standard

### Schema JSON

```json
{
  "generated_at": "2026-06-07T00:00:00Z",
  "scope": "Model Resource Availability & Quota Probe",
  "probe_freshness": "<timestamp ou UNKNOWN>",
  "resources": {
    "minimax": {
      "status": "GREEN|YELLOW|RED|UNKNOWN",
      "models_available": ["MiniMax-M2.7", "MiniMax-M3", "MiniMax-M2.1", "MiniMax-M2.5"],
      "quota_5h": "OK|LOW|EXHAUSTED|UNKNOWN|MANUAL_REQUIRED",
      "quota_weekly": "OK|LOW|EXHAUSTED|UNKNOWN|MANUAL_REQUIRED",
      "quota_monthly": "OK|LOW|EXHAUSTED|UNKNOWN|MANUAL_REQUIRED",
      "latency": "OK|HIGH|UNKNOWN",
      "last_error": null,
      "decision": "USE|PRESERVE|STOP_AND_ASK"
    },
    "codex_oauth": {
      "status": "GREEN|YELLOW|RED|UNKNOWN",
      "oauth": "OK|KO|UNKNOWN",
      "usage_remaining": "OK|LOW|UNKNOWN|MANUAL_REQUIRED",
      "session_limits": "OK|LIMITED|UNKNOWN|MANUAL_REQUIRED",
      "decision": "USE|PRESERVE|STOP_AND_ASK"
    },
    "mimo": {
      "status": "DOC_ONLY|CANARY_PENDING|GREEN|YELLOW|RED",
      "monthly_quota": "11B credits",
      "usage_percent": "0.0%|MANUAL_REQUIRED",
      "days_left": "MANUAL_REQUIRED",
      "canary": "PENDING|PASS|FAIL",
      "canary_level": "0|1|2|3|4|5|6",
      "decision": "NO_RUNTIME_USE|CANARY_ALLOWED|USE_LIMITED|STOP_AND_ASK"
    },
    "openrouter_free": {
      "status": "GREEN|YELLOW|RED|UNKNOWN",
      "authoritative": false,
      "model_available": true,
      "rate_limit_ok": true,
      "decision": "DRAFT_ONLY|AVOID|STOP_AND_ASK"
    }
  }
}
```

---

## Section 4 — Procédure Canary MiMo (PREPARE ONLY — NE PAS EXÉCUTER)

### Règle absolue

**Cette procédure est DOCUMENTÉE uniquement. Aucune exécution sans validation humaine explicite de Stéphane.**

**Chaque niveau indique :**
- Prérequis
- Commande/pseudo-commande
- Données interdites
- Succès/échec
- Quoi faire après

---

### Niveau 1 — Découverte Modèles

**Prérequis:** Validation Stéphane pour commencer canary

**Commande:**
```bash
# CANARY NIVEAU 1 — Modèles discovery (read-only, pas de prompt)
curl -s "https://token-plan-ams.xiaomimimo.com/v1/models" \
  -H "Authorization: Bearer sk-cp-***MASKED***" \
  --max-time 15
```

**Données interdites:** Aucune donnée réelle, aucune clé exposée, pas de prompt production

**Succès:** Response 200, liste modèles visible, pas d'erreur auth

**Échec:** 401 (clé invalide), 403 (accès refusé), timeout

**Après succès:** Reporter à Stéphane, attendre validation Niveau 2

---

### Niveau 2 — Prompt Simple Non Sensible

**Prérequis:** Niveau 1 validé + validation Stéphane

**Commande:**
```bash
# CANARY NIVEAU 2 — Prompt simple (non sensible)
curl -s "https://token-plan-ams.xiaomimimo.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-cp-***MASKED***" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role": "user", "content": "Quelle est la capitale de la France?"}],
    "max_tokens": 50
  }' \
  --max-time 30
```

**Données interdites:** Secrets, credentials, données personnelles, code production, noms de domaine réels

**Succès:** Response 200, réponse cohérente, latence acceptable

**Échec:** 401, 429, latence >30s, réponse incohérente

**Après succès:** Reporter à Stéphane, attendre validation Niveau 3

---

### Niveau 3 — Usage Coding Interactif Simple

**Prérequis:** Niveau 2 validé + validation Stéphane

**Commande:**
```bash
# CANARY NIVEAU 3 — Coding simple (non sensible)
curl -s "https://token-plan-ams.xiaomimimo.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-cp-***MASKED***" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role": "user", "content": "Écris une fonction Python qui calcule la factorielle."}],
    "max_tokens": 200
  }' \
  --max-time 30
```

**Données interdites:** Secrets, credentials, code production réel, fichiers système

**Succès:** Code fonctionnel, pas d'erreur, latence acceptable

**Échec:** 401, 429, code non fonctionnel, timeout

**Après succès:** Classification → LIMITED_ACTIVE, reporter à Stéphane

---

### Niveau 4 — JSON Strict

**Prérequis:** Niveau 3 validé + validation Stéphane

**Commande:**
```bash
# CANARY NIVEAU 4 — JSON strict (test contamination)
curl -s "https://token-plan-ams.xiaomimimo.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-cp-***MASKED***" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role": "user", "content": "Donne-moi un objet JSON avec name et age."}],
    "max_tokens": 100,
    "response_format": {"type": "json_object"}
  }' \
  --max-time 30
```

**Données interdites:** Secrets, credentials, données réelles

**Succès:** JSON valide sans contamination `<thinking>` tags

**Échec:** JSON invalide, contamination tags, 429

**Après succès:** Classification → ACTIVE_LIMITED, reporter à Stéphane

---

### Niveau 5 — Latence + Usage Dashboard Manuel

**Prérequis:** Niveau 4 validé + validation Stéphane

**Action:** Stéphane vérifie dashboard token-plan pour usage et latence

**Données interdites:** Aucune (dashboard only)

**Succès:** Quota usage visible, latence acceptable, pas d'erreur

**Échec:** Dashboard inaccessible, quota vide, latence >30s

**Après succès:** Classification → ACTIVE_PREMIUM_MONTHLY, reporter à Stéphane

---

### Niveau 6 — Validation Complète

**Prérequis:** Niveau 5 validé + validation Stéphane

**Action:** Test complet usage réel non prod avec monitoring

**Données interdites:** Secrets, prod, release, rollback

**Succès:** Usage stable, pas d'erreur, quota préservé, latence OK

**Échec:** Erreurs récurrentes, latence haute, quota gaspillé

**Après succès:** Classification → ACTIVE_FULL, canary COMPLETE

---

## Section 5 — Reference

- `/opt/data/workspace/MODEL_RESOURCE_GOVERNANCE.md`
- `/opt/data/workspace/model_resources/minimax.md`
- `/opt/data/workspace/model_resources/codex_oauth.md`
- `/opt/data/workspace/model_resources/mimo.md`
- `/opt/data/workspace/model_resources/openrouter_free.md`
- `/opt/data/workspace/runbooks/ai_model_routing.md`
- `/opt/data/workspace/AGENTS_GOVERNANCE.md`
- `/opt/data/workspace/LEDGER_2026-06-07_P34_MODEL_AVAILABILITY_QUOTA_PROBE.md`