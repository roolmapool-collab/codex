# MiniMax Resource Card

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
| **Default model** | YES (M2.7) |
| **Human validation required** | NO (routine ops) / YES (prod/release/secrets) |
| **Provider** | minimax |
| **Token type** | Subscription (sk-cp- prefix) |

---

## Trust Level

**PAID_SHARED** — Ressource partagée payante avec quota. Pas de garantie exclusive.

---

## Primary Role

MiniMax est le **cerveau central** de l'orchestration Hermes. M2.7 est le modèle par défaut pour toute décision, coordination, mémoire, et exécution. Les autres modèles (M3, M2.1/M2.5) sont des ressources spécialisées qui ne remplacent pas M2.7.

**M2.7 = Modèle par défaut** — stabilisé, éprouvé, décisionnel.
**M3 = Reasoning long contexte** — utile pour analyse, pas pour exécution finale.
**M2.1/M2.5 = Auxiliaires** — tâches simples pour préserver M2.7.

---

## Models

### M2.7 — Default Stable (PRIMARY)

**Rôle:** Décision, orchestration, coordination, mémoire, JSON strict, tool calls, sécurité, prod.

**Quand choisir:**
- Orchestration multi-agents
- Coordination live monitoring
- Écriture mémoire durable (MEMORY.md, curated)
- JSON strict / protocoles structurés
- Tool calls / exécution
- Sécurité / secrets
- Prod / release / rollback
- Validation finale
- Messages structurés

**Quand éviter:**
- Brouillon / brainstorming → OpenRouter free
- Tâche technique complexe → Codex
- Contexte >100K tokens → M3 (reasoning only)
- Résumé simple → M2.1/M2.5

### M3 — Long Context Reasoning

**Rôle:** Analyse approfondie multi-docs, stratégie, audit, migration.

**Quand choisir:**
- Contexte >100K tokens
- Audit >5 documents simultanés
- Analyse stratégique >3 options
- Plan migration multi-composants
- Synthèse corpus volumineux
- session_search insuffisant

**INTERDIT:**
- JSON strict (contamination `<thinking>` tags)
- Tool calls / exécution
- Commandes opérationnelles
- Décision finale prod
- Sécurité / secrets
- Release / rollback
- Discord automatique
- Tâches courtes (gaspillage)

**Règle:** M3 réfléchit, M2.7 arbitre.

### M2.1/M2.5 — Auxiliary

**Rôle:** Tâches simples pour préserver M2.7.

**Quand choisir:**
- Résumé court non sensitif
- Classification simple
- Extraction simple
- Titres / nettoyage texte

**Quand éviter:**
- Décision projet
- Sécurité / code complexe
- Production

### TTS — Text-to-Speech

**Endpoint canonique:** `https://api.minimax.io/v1/t2a_v2`

**Modèle:** `speech-2.8-hd` (pas `speech-02-hd` — bug 2056)

**Quand choisir:**
- Synthèse vocale (notifications, alerts)
- Voice clone Stéphane

**INTERDIT:**
- Vidéo / multimodal (M2.7 non multimodal)
- Endpoints OpenAI-like TTS

---

## Counters / Quotas

### M2.7 / M3 / M2.1/M2.5 (shared quota)

| Counter | Value | Monitoring | Action |
|---------|-------|------------|--------|
| **5-hour window** | 4 500 req/5h | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard |
| **Weekly allowance** | Variable | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard |
| **Monthly budget** | Token Plan Plus (20$/mois) | COUNTER_MANUAL_REQUIRED | Stéphane check dashboard |
| **Provider errors (529)** | HTTP 529 = overload | Log monitoring | STOP + fallback M2.1 ou OpenRouter |
| **Latence** | Variable (target <10s) | Session observation | Si >15s × 3 → STOP |
| **Cache hit rate** | Target 95-100% | Session logs | Si <80% → investigate |

### TTS

| Counter | Value | Monitoring |
|---------|-------|------------|
| **Usage** | Within plan quota | COUNTER_MANUAL_REQUIRED |
| **Model** | speech-2.8-hd ONLY | Config |
| **Endpoint** | /v1/t2a_v2 ONLY | Config |

---

## Decision Rules

### Quand choisir M2.7

1. Orchestration / coordination / arbitrage
2. Mémoire durable (MEMORY, curated)
3. JSON strict / protocoles
4. Tool calls / exécution
5. Sécurité / secrets
6. Prod / release / rollback
7. Validation finale
8. Contexte <100K tokens

### Quand choisir M3

1. Contexte >100K tokens
2. Audit multi-docs (>5)
3. Analyse stratégique
4. Migration architecture
5. Recherche approfondie (session_search insuffisant)
6. Synthèse gros corpus

### Quand choisir M2.1/M2.5

1. Résumé court non sensitif
2. Classification simple
3. Extraction simple
4. Tâche <60s

### Quand éviter MiniMax (utiliser OpenRouter)

1. Brouillon non critique
2. Brainstorming
3. Première passe exploration

### Règle STOP

- Erreur 529 × 2 → STOP, fallback OpenRouter ou STOP_AND_ASK
- Latence >15s × 3 → STOP
- Cache <80% → investigate avant STOP

---

## Security Rules

| Action | Autorisé | Notes |
|--------|----------|-------|
| Secrets manipulation | ✅ M2.7 only | Jamais M3, jamais OpenRouter |
| Secrets en docs | ❌ INTERDIT | Mémoire, curations, docs |
| Prod/release/rollback | ✅ M2.7 only | M3 interdit |
| Clé API en mémoire | ❌ INTERDIT | Ne jamais écrire clés |
| Indexation OpenViking secrets | ❌ INTERDIT | secret scan OK requis |
| Discord messages | ✅ M2.7 only | Structure |
| Telegram messages | ✅ M2.7 only | Structure |

---

## Output Rules

| Format | M2.7 | M3 | M2.1/M2.5 |
|--------|------|----|-----------|
| JSON strict | ✅ | ❌ | ❌ |
| Markdown report | ✅ | ✅ | ✅ |
| Code patch | ✅ | ❌ | ❌ |
| Shell/tool calls | ✅ | ❌ | ❌ |
| Long-context (>80K) | ✅ | ✅ | ❌ |
| Voice/TTS/ASR | ✅ | ❌ | ❌ |
| Discord messages | ✅ | ❌ | ❌ |

---

## Canary / Validation

**Status:** ACTIVE — Validated via prod session P27-P33

| Test | Result | Date |
|------|--------|------|
| M2.7 prod session P27 | ✅ 36 API calls, cache 95-100% | 2026-06-07 |
| M3 reasoning session P31-P32 | ✅ Useful, with limits | 2026-06-07 |
| TTS /v1/t2a_v2 | ✅ Canonical endpoint | 2026-06-07 |
| M3 contamination lesson v0.16 | ✅ Documented | 2026-06-07 |

**M3 Lesson v0.16:** M3 had prédit `WAIT_UPSTREAM` pour blockers v0.15. Reality: blockers were s6 lock + path issues. M3 reasoning useful but NOT authoritative. Always validate with M2.7.

---

## Fallback Policy

| Situation | Fallback vers | Interdit |
|-----------|---------------|----------|
| M2.7 overload | M2.1/M2.5 → OpenRouter free | M3 (reasoning only) |
| M3 contamination risk | M2.7 | M3 pour décision |
| TTS fail | M2.7 (text only) | Pas de retry TTS auto |
| 529 × 2 | OpenRouter free → STOP_AND_ASK | Retry infini |

**STOP_AND_ASK:** Si aucun fallback disponible et tâche critique → demander Stéphane.

---

## Reporting Template

```
Resource: MiniMax
Model: <M2.7|M3|M2.1|M2.5|TTS>
Why: <justification courte>
Why not others: <M3 reasoning, Codex tech, OpenRouter free>
Quota impact: <estimation req/5h>
Risk: <LOW|MEDIUM|HIGH>
Fallback: <si applicable>
Human validation: <oui/non>
```

---

## Reference

- `/opt/data/workspace/MODEL_RESOURCE_GOVERNANCE.md`
- `/opt/data/workspace/runbooks/ai_model_routing.md`
- `/opt/data/skills/hermes-sysop-config/SKILL.md`
- `/opt/data/skills/hermes-sysop/hermes-orchestrator-operating-rules/SKILL.md`
- `LEDGER_2026-06-07_P32B_MINIMAX_M3_DOC_AUDIT.md`