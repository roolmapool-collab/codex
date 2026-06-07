# Xiaomi/MiMo Resource Card

> **Version:** 1.0
> **Date:** 2026-06-07
> **Source:** P32.1 MiMo Premium Classification + P33 Resource Cards
> **Owner:** Hermes Orchestrateur
> **Classification:** PREMIUM_SECURED_DOC_ONLY

---

## Status

| Item | Value |
|------|-------|
| **Runtime configured** | NO (CANARY_LEVEL_2_PASS) |
| **Default model** | NO |
| **Human validation required** | YES (canary Level 3+ required) |
| **Provider** | token-plan-ams (Xiaomi) |
| **Token type** | Paid dedicated subscription |
| **Classification** | PREMIUM_SECURED_DOC_ONLY |
| **Canary status** | CANARY_LEVEL_2_PASS — Niveau 1-2 PASS, Niveau 3 (coding) en attente |

---

## Trust Level

**PREMIUM_SECURED** — Ressource payante dédiée, pas un brouillon gratuit.

**MiMo ≠ OpenRouter free. MiMo ≠ brouillon gratuit. MiMo ≠ opportuniste.**

MiMo est un **plan payant premium** avec quota mensuel important (11B credits). Son usage doit être justifié et intelligent.

---

## Primary Role

MiMo exécute l'**offload premium sécurisé** pour valoriser le quota mensuel de 11B crédits. Après validation canary, MiMo peut gérer des tâches seriesues non prod-critical quand MiniMax doit être préservé.

**Règle:** MiMo exécute l'offload premium sécurisé et valorise le quota mensuel après canary.

**NOT a free resource.** MiMo est une ressource premium à utiliser intelligemment.

---

## Best For (after CANARY_PASS — Niveau 1-3)

| Usage | Description |
|-------|-------------|
| **Premium offload coding** | Tâches coding interactives sérieuses (compatible AI coding tools) |
| **Serious work analysis** | Analyse non secrète, évaluation approfondie |
| **Long tasks preservation** | Tâches longues pour préserver M2.7/M3 pour tâches critiques |
| **Monthly quota intelligent** | Valoriser le quota mensuel (11B credits) intelligemment |
| **Coding agent tools** | Tâches compatibles avec MiMo API |
| **Interactive work** | Usage interactif uniquement (pas automated scripts) |

---

## Not For

| Usage | Raison |
|-------|--------|
| **Automated scripts** | ❌ Violation terms of service |
| **Application backends** | ❌ Violation terms of service |
| **Cron jobs** | ❌ Violation terms of service |
| **Backend app** | ❌ Violation terms of service |
| **Automatique répétitive** | ❌ Violation terms of service |
| **Secrets / sécurité** | ❌ Niveau sensibilité maximum (sans validation) |
| **Prod / release** | ❌ Risque irréversible |
| **Brainstorming non critique** | ❌ Gaspillage — utiliser OpenRouter free |
| **Free offload** | ❌ MiMo n'est pas gratuit — quota mensuel |
| **OpenRouter substitute** | ❌ MiMo ≠ OpenRouter free |

---

## Counters / Quotas

| Counter | Value | Monitoring | Action |
|---------|-------|------------|--------|
| **Monthly remaining** | 11,000,000,000 credits | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard |
| **Usage %** | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard | STOP si proche limite |
| **Days left in month** | Manual | Stéphane track | STOP si fin de mois |
| **Off-peak benefit** | Not monitored | Observation | Utiliser off-peak pour benefit |

**COUNTER_MANUAL_REQUIRED:** MiMo ne fournit pas de compteur automatique accessible. Stéphane doit vérifier le dashboard token-plan-ams pour suivre l'usage.

**Règle:** Valoriser le quota sur le mois sans gaspiller. Ne pas utiliser MiMo pour des tâches que OpenRouter free peut faire.

---

## Decision Rules

### Quand choisir MiMo (après canary)

1. Tâche coding interactive sérieuse
2. Analyse non secrète non prod-critical
3. Tâche longue où M2.7 doit être préservé
4. Offload premium quand OpenRouter insuffisant mais M2.7 pas nécessaire
5. Valorisation intelligente du quota mensuel

### Quand éviter MiMo

1. Tâche non critique → OpenRouter free
2. Tâche prod/secrets → M2.7
3. Tâche technique → Codex
4. Brainstorming → OpenRouter free
5. Automated scripts → INTERDIT (ToS)
6. Cron jobs → INTERDIT (ToS)

### Quand demander validation humaine

1. Tâche sensible (non secrets mais sensitive)
2. Usage significatif du quota (>10% mensuel estimé)
3. Première utilisation après canary
4. Incertitude sur appropriateness

---

## Security Rules

| Action | Autorisé | Notes |
|--------|----------|-------|
| Secrets manipulation | ❌ INTERDIT | Niveau sensibilité maximum |
| Secrets en docs | ❌ INTERDIT ABSOLU | Jamais, sécurité absolue |
| Clé en Discord | ❌ INTERDIT ABSOLU | Jamais |
| Clé indexée OpenViking | ❌ INTERDIT ABSOLU | Jamais |
| Prod / release | ❌ INTERDIT | Risque irréversible |
| Code prod | ⚠️ Après canary + validation | M2.7 approve final |
| Logs | ✅ Non sensitifs | Debugging allowed |

**Règle absolue:** La clé MiMo ne doit jamais apparaître en clair dans aucun document, logs, Discord, ou index OpenViking.

---

## Output Rules

| Format | MiMo |
|--------|------|
| Code | ✅ (interactive, after canary) |
| Markdown report | ✅ |
| Analysis | ✅ (non secret) |
| JSON strict | ⚠️ Avec caution |
| Shell/tool calls | ⚠️ Avec caution |
| Secrets output | ❌ INTERDIT |

---

## Canary / Validation

> **⚠️ Règle contexte:** Les canaries MiMo **doivent** être exécutés depuis le contexte Hermes/VPS canonique (`/opt/data/.env`). Ne jamais généraliser un résultat de canary d'un contexte à l'autre.

| Contexte | Résultat | Cause |
|----------|----------|-------|
| Tests locaux Codex/Windows | ❌ HTTP 401 | Clé refusée dans ce contexte |
| Contexte Hermes/VPS | ✅ HTTP 200 | Config env effective, 9 modèles |

**Status:** CANARY_LEVEL_2_PASS — Niveau 1-2 PASS, Niveau 3 (coding non sensitif) en attente validation humaine

### Canary Status

| Niveau | Test | Résultat |
|--------|------|----------|
| 1 | Découverte modèles (`/v1/models`) | ✅ PASS (P35 — HTTP 200, 9 modèles) |
| 2 | Prompt simple non sensible | ✅ PASS (P39 — mimo-v2.5 + P39.2 — mimo-v2.5-pro) |
| 3 | Coding interactif simple non sensitif | ⬜ EN ATTENTE validation humaine |
| 4 | JSON strict | ⬜ EN ATTENTE |
| 5 | Latence / usage dashboard | ⬜ EN ATTENTE |
| 6 | Usage complet prod | ⬜ INTERDIT |

**Prochaine validation:** Niveau 3 coding non sensitif — Stéphane doit autoriser.

---

## Fallback Policy

| Situation | Fallback vers | Interdit |
|-----------|---------------|----------|
| MiMo unavailable | M2.7 ou OpenRouter selon criticité | M3 (reasoning only) |
| Quota épuisé | OpenRouter free → STOP_AND_ASK | MiMo sans quota |
| Erreur canary | STOP_AND_ASK | Aucun usage sans canary |

**STOP_AND_ASK:** Si MiMo non disponible et tâche urgente → demander Stéphane.

---

## Reporting Template

```
Resource: Xiaomi/MiMo
Model: MiMo (token-plan-ams)
Why: <justification premium offload>
Why not M2.7: <M2.7 doit être préservé pour tâches critiques>
Why not Codex: <pas une tâche technique complexe>
Why not M3: <M3 reasoning only, pas exécution>
Why not OpenRouter free: <tâche trop sérieuse pour free/non fiable>
Quota impact: <estimation credits>
Risk: <LOW|MEDIUM|HIGH>
Fallback: <si applicable>
Human validation: <oui/non>
```

---

## Base URLs

| Type | URL |
|------|-----|
| OpenAI-compatible | `https://token-plan-ams.xiaomimimo.com/v1` |
| Anthropic-compatible | `https://token-plan-ams.xiaomimimo.com/anthropic` |

**Models disponibles:** `mimo-v2.5-pro`, `mimo-v2.5`, `mimo-v2.5-asr`, `mimo-v2.5-tts-voiceclone`, `mimo-v2.5-tts-voicedesign`, `mimo-v2.5-tts`, `mimo-v2-pro`, `mimo-v2-omni`, `mimo-v2-tts`

---

## Reference

- `/opt/data/workspace/MODEL_RESOURCE_GOVERNANCE.md` (section MiMo)
- `/opt/data/workspace/runbooks/ai_model_routing.md` (section Xiaomi/MiMo)
- `/opt/data/workspace/AGENTS_GOVERNANCE.md` (tableau modèles)
- `/opt/data/skills/hermes-sysop-config/SKILL.md` (section Xiaomi/MiMo)
- `LEDGER_2026-06-07_P32_1_MIMO_PREMIUM_CLASSIFICATION_FIX.md`