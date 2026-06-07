# Codex OAuth Resource Card

> **Version:** 1.0
> **Date:** 2026-06-07
> **Source:** P32 Model Resource Governance + P33 Resource Cards
> **Owner:** Hermes Orchestrateur
> **Classification:** RUNTIME_ACTIVE

---

## Status

| Item | Value |
|------|-------|
| **Runtime configured** | YES (OAuth via Nous) |
| **Default model** | NO (specialized) |
| **Human validation required** | NO (routine technical) / YES (infra changes) |
| **Auth type** | OAuth (NO OPENAI_API_KEY required) |
| **Provider** | Nous Research |

---

## Trust Level

**OAUTH_LOCAL** — Authentification OAuth locale. Ressources techniques spécialisées.

---

## Primary Role

Codex est le **bras technique** de l'écosystème Hermes. Il exécute les actions réelles sur le système : code, git, shell, serveur, fichiers, debugging, review technique.

**Règle:** Codex agit techniquement. Il ne raisonne pas (raisonnement → M3), il n'orchestre pas (orchestration → M2.7), il n'est pas un brouillon gratuit (brouillon → OpenRouter).

---

## Best For

| Usage | Description |
|-------|-------------|
| **Code Python/JS/Bash** | Écriture réelle, pas simulation |
| **Repo / Git** | Clone, push, pull, merge, conflicts |
| **Shell / Serveur** | Commandes système, scripts, debugging |
| **Debugging** | Stack traces, logs, config, pdb |
| **Review technique** | PR review, diff analysis, architecture |
| **Modifications fichiers** | patch, write, edit (pas lecture seule) |
| **Validation technique** | Compilation, tests, lint |
| **Fichiers système** | Config, scripts, scripts CI/CD |

---

## Not For

| Usage | Raison |
|-------|--------|
| **Brainstorming non technique** | Gaspillage — utiliser OpenRouter free |
| **Simple résumé** | Gaspillage — utiliser M2.1/M2.5 |
| **Coordination pure** | M2.7 only |
| **Reasoning long contexte** | M3 only |
| **Décision projet** | M2.7 only |
| **Mémoire durable** | M2.7 only |
| **Sécurité / secrets** | M2.7 only |
| **Prod / release / rollback** | M2.7 only (codex peut aider prep, M2.7 approve) |

---

## Counters / Quotas

| Counter | Value | Monitoring | Action |
|---------|-------|------------|--------|
| **Usage remaining** | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard | STOP si épuisé |
| **Session limits** | Variable par plan | Observation | STOP si rate limit |
| **Context window** | Local compute | Observation | STOP si contexte overflow |
| **Cost/quotas** | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard | STOP si budget |
| **Rate limit** | Variable | Observation | STOP si 429 |

**COUNTER_MANUAL_REQUIRED:** Codex ne fournit pas de compteur automatique. Stéphane doit vérifier le dashboard Nous ou Codex pour suivre l'usage.

---

## Decision Rules

### Quand choisir Codex

1. Tâche nécessite modification de fichier (write, patch, edit)
2. Commande shell à exécuter
3. Git operation (clone, push, pull, merge)
4. Debugging stack trace / logs
5. Code review / PR analysis
6. Compilation / test / lint
7. Script execution (bash, python)
8. Configuration système

### Quand éviter Codex

1. Simple lecture / résumé → M2.1/M2.5 ou OpenRouter free
2. Brainstorming → OpenRouter free
3. Coordination / décision → M2.7
4. Reasoning long contexte → M3
5. Mémoire durable → M2.7

### Règle STOP

- Rate limit 429 → STOP, attendre ou fallback M2.7
- Contexte overflow → STOP, scinder la tâche
- Erreur compilation → STOP, rapporter erreur technique

---

## Security Rules

| Action | Autorisé | Notes |
|--------|----------|-------|
| Manipulation secrets | ✅ Via fichiers/runtime | Ne jamais afficher auth.json |
| OPENAI_API_KEY demande | ❌ INTERDIT | OAuth suffit, pas de clé requise |
| Code prod | ✅ Avec validation | M2.7 approve final |
| Config système | ✅ Avec validation | M2.7 approve final |
| Git operations | ✅ | Auth via OAuth |
| Secrets en output | ❌ INTERDIT | Ne jamais afficher clés |
| Logs système | ✅ | Debugging allowed |
| Docker exec | ✅ Si autorisé | Vérifier permissions |

---

## Output Rules

| Format | Codex |
|--------|-------|
| Code patch | ✅ |
| Shell command | ✅ |
| Git operation | ✅ |
| Review technique | ✅ |
| JSON strict | ❌ (pas son rôle) |
| Markdown report | ⚠️ Limité (output technique) |
| Decision finale | ❌ (M2.7 only) |

---

## Canary / Validation

**Status:** ACTIVE — Validated via usage sessions P27-P33

| Test | Result | Date |
|------|--------|-------|
| Code execution P27-P33 | ✅ | 2026-06-07 |
| Git operations | ✅ | 2026-06-07 |
| OAuth no OPENAI_API_KEY | ✅ | 2026-06-07 |

**Note:** Codex n'a pas besoin de "canary" comme MiMo. Il est validé par usage quotidien.

---

## Fallback Policy

| Situation | Fallback vers | Interdit |
|-----------|---------------|----------|
| Codex rate limit | M2.7 (read-only) → STOP_AND_ASK si modification requise | OpenRouter (non fiable pour tech) |
| Codex unavailable | M2.7 (read-only) → STOP_AND_ASK | OpenRouter pour modifications |
| Tâche non technique | M2.7 / OpenRouter selon criticité | Codex pour non-tech |

**STOP_AND_ASK:** Si tâche technique urgente et Codex indisponible → demander Stéphane.

**Règle critique:** Si une tâche est TECHNIQUE mais pas critique (pas prod, pas infra), OpenRouter peut être utilisé comme fallback temporaire. Pour tout ce qui touche à prod/infra, STOP_AND_ASK.

---

## Reporting Template

```
Resource: Codex OAuth
Model: Codex (Nous)
Why: <action technique requise (code, git, shell, etc.)>
Why not M2.7: <M2.7 n'exécute pas, Codex exécute>
Why not M3: <M3 reasoning only, pas exécution>
Why not OpenRouter: <OpenRouter non fiable pour tech prod>
Quota impact: <estimation usage>
Risk: <LOW|MEDIUM|HIGH>
Fallback: <si applicable>
Human validation: <oui/non> (requis pour infra/prod changes)
```

---

## Reference

- `/opt/data/workspace/MODEL_RESOURCE_GOVERNANCE.md`
- `/opt/data/workspace/runbooks/ai_model_routing.md`
- `/opt/data/workspace/AGENTS_GOVERNANCE.md` (section Codex)