# OpenRouter Free Resource Card

> **Version:** 1.0
> **Date:** 2026-06-07
> **Source:** P32 Model Resource Governance + P33 Resource Cards
> **Owner:** Hermes Orchestrateur
> **Classification:** RUNTIME_ACTIVE

---

## Status

| Item | Value |
|------|-------|
| **Runtime configured** | YES |
| **Default model** | NO (supplementary) |
| **Human validation required** | NO (non critical) / YES (if output used for decisions) |
| **Provider** | OpenRouter |
| **Model** | Owl Alpha (free tier) |
| **Cost** | FREE (rate limited) |

---

## Trust Level

**FREE_UNTRUSTED** — Ressource gratuite avec fiabilité variable. Pas authoritative.

**Règle:** OpenRouter brouillonne gratuitement. Il ne décide pas, il ne valide pas, il ne certifie pas.

---

## Primary Role

OpenRouter free (Owl Alpha) est le **brouillonnage gratuit** de l'écosystème Hermes. Il sert pour les premières passes non critiques, explorations, et tâches où la fiabilité n'est pas critique.

**Règle:** OpenRouter brouillonne gratuitement. Il n'est PAS authoritative.

---

## Best For

| Usage | Description |
|-------|-------------|
| **Brainstorming** | Génération d'idées, exploration |
| **Première passe** | Analyse initiale non critique |
| **Exploration** | Test de concept, prototypage |
| **Reformulation** | Refactoring texte non critique |
| **Résumé non sensitif** | Résumé de document non sensible |
| **Test de concept** | Validation idée avant engagement |
| **Non critique drafts** | Brouillons à raffiner après |

---

## Not For

| Usage | Raison |
|-------|--------|
| **Secrets / sécurité** | ❌ Niveau sensibilité maximum |
| **Prod / release** | ❌ Risque irréversible |
| **Décision finale** | ❌ Non authoritative |
| **Livrables longs** | ❌ >20 lignes, >10 tool calls |
| **JSON strict** | ❌ Fiabilité insuffisante |
| **Code complexe prod** | ❌ Non fiable pour prod |
| **Mémoire durable** | ❌ Pas assez stable |
| **Configuration infra** | ❌ Trop critique |
| **Release / rollback** | ❌ Risque irréversible |
| **Décision projet** | ❌ Non authoritative |

---

## Counters / Quotas

| Counter | Value | Monitoring | Action |
|---------|-------|------------|--------|
| **Model availability** | Variable | Observation | Si modèle down → autre modèle ou M2.7 |
| **Rate limit errors** | Variable | Observation | STOP si 429 × 3 |
| **Latence** | Variable (peut être lent) | Observation | Si >30s × 3 → fallback |
| **Output quality** | Variable | Observation | Si output incohérent → M2.7 |
| **Tool calls** | MAX 10 par tâche | Strict | STOP si >10 calls |

**Règle:** MAX 10 tool calls par tâche OpenRouter. Livrables <20 lignes ou <10 tool calls.

---

## Decision Rules

### Quand choisir OpenRouter

1. Tâche non critique (brainstorming, exploration)
2. Première passe avant engagement M2.7
3. Résumé non sensitif
4. Test de concept rapide
5. Reformulation non critique

### Quand éviter OpenRouter

1. Tâche critique → M2.7
2. Secrets → M2.7
3. Prod → M2.7
4. Code complexe → Codex ou M2.7
5. Decision finale → M2.7
6. JSON strict → M2.7 (M3 interdit)

### Quand fallback vers M2.7

1. Output OpenRouter incohérent
2. Tâche devient critique après première passe
3. Rate limit 429 × 3
4. Latence >30s × 3
5. Livrable final requis (pas juste draft)

---

## Security Rules

| Action | Autorisé | Notes |
|--------|----------|-------|
| Secrets manipulation | ❌ INTERDIT | Niveau sensibilité maximum |
| Secrets en output | ❌ INTERDIT | Ne jamais exposer |
| Prod / release | ❌ INTERDIT | Risque irréversible |
| Code prod | ❌ INTERDIT | Non fiable pour prod |
| Confidential data | ❌ INTERDIT | Non assez sécurisé |
| Git operations | ⚠️ Limité (read-only suggéré) | Préférer Codex |
| Configuration infra | ❌ INTERDIT | Trop critique |

---

## Output Rules

| Format | OpenRouter |
|--------|------------|
| Markdown draft | ✅ (brainstorming) |
| Code draft | ⚠️ (exploration only) |
| Summary | ✅ (non sensitif) |
| JSON strict | ❌ INTERDIT |
| Decision finale | ❌ INTERDIT |
| Prod code | ❌ INTERDIT |
| Security output | ❌ INTERDIT |

---

## Canary / Validation

**Status:** ACTIVE — Validated via usage sessions P27-P33

| Test | Result | Date |
|------|--------|-------|
| Brainstorming sessions | ✅ Useful for first pass | 2026-06-07 |
| Exploration non critique | ✅ | 2026-06-07 |
| Rate limit behavior | ✅ Observed | 2026-06-07 |

**Note:** OpenRouter n'a pas besoin de canary formel. Il est validé par usage quotidien et ses limites sont bien comprises.

---

## Fallback Policy

| Situation | Fallback vers | Interdit |
|-----------|---------------|----------|
| Rate limit 429 × 3 | M2.7 | Retry infini |
| Latence >30s × 3 | M2.7 | Retry infini |
| Output quality poor | M2.7 | Utiliser output poor |
| Tâche devient critique | M2.7 | Continuer avec OpenRouter |
| Livrable final | M2.7 | OpenRouter comme final |

**STOP_AND_ASK:** Si aucune ressource disponible et tâche urgente → demander Stéphane.

**Règle:** OpenRouter est un brouillon. Il ne devient jamais un livrable final sans validation M2.7.

---

## Reporting Template

```
Resource: OpenRouter Free
Model: Owl Alpha (free)
Why: <tâche non critique (brainstorming, exploration, première passe)>
Why not M2.7: <M2.7 trop précieux pour cette tâche non critique>
Why not M3: <pas besoin reasoning long contexte>
Why not Codex: <pas une tâche technique>
Why not MiMo: <MiMo premium, pas pour brouillon gratuit>
Quota impact: <aucun (free)>
Risk: <LOW (non critique)>
Fallback: <M2.7 si tâche devient critique ou output poor>
Human validation: <non (non critique) / oui (si output utilisé pour décision)>
```

---

## Reference

- `/opt/data/workspace/MODEL_RESOURCE_GOVERNANCE.md` (section OpenRouter free)
- `/opt/data/workspace/runbooks/ai_model_routing.md` (section OpenRouter)
- `/opt/data/workspace/AGENTS_GOVERNANCE.md` (tableau modèles)