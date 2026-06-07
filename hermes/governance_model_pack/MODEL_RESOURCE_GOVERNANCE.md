# MODEL_RESOURCE_GOVERNANCE.md

## Gouvernance Active des Ressources Modèles IA — Hermes Orchestrateur

|| **Version:** 1.3
| **Date:** 2026-06-07
| **Source:** P32 Active Model Resource Governance + P32.1 MiMo + P33 Resource Cards + P34 Availability Probe
| **Owner:** Hermes Orchestrateur
| **Status:** ACTIVE

---

## Probe Disponibilité & Quotas

Avant toute tâche importante, Hermes applique la procédure **Model Availability & Quota Probe** :
- **Runbook:** `/opt/data/workspace/runbooks/model_availability_quota_probe.md`
- **Template JSON:** `/opt/data/workspace/healthchecks/model_resource_status.example.json`

**Question clé:** *"Quel modèle est pertinent ET disponible maintenant, selon les compteurs 5h, hebdo, mensuels, latence, statut canary et risque ?"*

---

## Vue d'ensemble — Fiches Ressources

Chaque ressource modèle est documentée dans une fiche dédiée :

| Ressource | Fiche | Trust | Default Role |
|-----------|-------|-------|--------------|
| MiniMax (M2.7, M3, M2.1/M2.5, TTS) | `model_resources/minimax.md` | PAID_SHARED | Cerveau central, décision, orchestration |
| Codex OAuth | `model_resources/codex_oauth.md` | OAUTH_LOCAL | Mains techniques, code, git, shell |
| Xiaomi/MiMo | `model_resources/mimo.md` | PREMIUM_SECURED | Offload premium, CANARY_LEVEL_2_PASS |
| OpenRouter free (Owl Alpha) | `model_resources/openrouter_free.md` | FREE_UNTRUSTED | Brouillonnage, première passe |

---

## Table Centrale des Ressources

| Resource | Trust | Default Role | Counters | Can Decide? | Can Execute? | Secrets? | Prod? | Status |
|---------|-------|--------------|----------|-------------|-------------|---------|------|--------|
| MiniMax-M2.7 | PAID_SHARED | Orchestration, décision, JSON, tool calls | 4500 req/5h, weekly, monthly | ✅ YES | ✅ ORCHESTRATE_ONLY | ✅ YES | ✅ YES | ACTIVE |
| MiniMax-M3 | PAID_SHARED | Long-context reasoning | Quota partagé | ❌ NO (reasoning only) | ❌ NO | ❌ NO | ❌ NO | ACTIVE |
| MiniMax-M2.1/M2.5 | PAID_SHARED | Tâches auxiliaires simples | Quota partagé | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ACTIVE |
| MiniMax-TTS | PAID_SHARED | Text-to-Speech | Within plan | N/A | ✅ YES (TTS only) | ❌ NO | ❌ NO | ACTIVE |
| Codex OAuth | OAUTH_LOCAL | Code, git, shell, debug | COUNTER_MANUAL | ⚠️ TECHNICAL_ONLY | ✅ YES | ✅ Via fichiers | ⚠️ WITH VALIDATION | ACTIVE |
| Xiaomi/MiMo | PREMIUM_SECURED | Offload premium, monthly quota | 11B credits/month | ❌ NO | ⚠️ AFTER CANARY_L3 | ❌ NO | ❌ NO | CANARY_LEVEL_2_PASS |
| OpenRouter free | FREE_UNTRUSTED | Brouillonnage, exploration | Rate limits | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ACTIVE |

**Can Decide:** Autorisé pour décision finale sans validation humaine supplémentaire.
**Can Execute:** Autorisé pour exécution technique (tool calls, shell, git, etc.).
**Secrets:** Manipulation de secrets/credentials.
**Prod:** Usage pour prod/release/rollback.

---

## Classification des Ressources

Ce document établit la **gouvernance active** des ressources modèles IA dans l'écosystème Hermes.

**Principe fondamental :** Hermes n'est pas un simple routeur passif de modèles. Il est un **gestionnaire stratégique de ressources** qui optimise l'utilisation de chaque modèle selon le besoin, le risque, le format, les ressources disponibles, les quotas, et la criticité métier.

---

## Classification des Ressources

### Vue d'ensemble

| Ressource | Provider | Capacité | Quota | Status |
|-----------|----------|----------|-------|--------|
| MiniMax-M2.7 | minimax | Modèle par défaut | 4 500 req/5h | ACTIVE |
| MiniMax-M3 | minimax | Long-context reasoning | Quota partagé | ACTIVE |
| MiniMax-M2.1/M2.5 | minimax | Tâches auxiliaires | Quota partagé | ACTIVE |
| Codex OAuth | nous | Expertise technique | Usage limité | ACTIVE |
| OpenRouter free | openrouter | Brouillon gratuit | Illimité | ACTIVE |
| Xiaomi/MiMo | token-plan-ams | Premium monthly secured offload | 11B credits/month | CANARY_LEVEL_2_PASS |

---

## Modèle de Décision Obligatoire

Avant toute tâche significative, Hermes classifie selon 4 dimensions :

### A. Task Type

| Type | Définition | Modèle par défaut |
|------|------------|-------------------|
| **ORCHESTRATION** | Coordination, arbitrage, décision finale, mémoire | M2.7 |
| **TECHNICAL_ACTION** | Code, shell, git, serveur, debug, fichiers | Codex |
| **LONG_CONTEXT_REASONING** | Audit multi-docs, migration, analyse stratégique | M3 |
| **DRAFT_OR_BRAINSTORM** | Première passe, exploration, test non critique | OpenRouter free |
| **STRUCTURED_OUTPUT** | JSON strict, protocoles structurés | M2.7 |
| **SECURITY_OR_SECRET** | Secrets, sécurité, credentials | M2.7 |
| **PROD_RELEASE_ROLLBACK** | Release, rollback, déploiement | M2.7 |
| **SIMPLE_SUMMARY** | Résumé court, classification, extraction | M2.1/M2.5 ou OpenRouter free |
| **AUDIO_TTS_ASR** | Synthèse vocale, transcription | MiniMax TTS |
| **MULTIMODAL** | Image, audio, vidéo | MiniMax |
| **UNKNOWN** | Flou, risqué, coûteux | STOP_AND_ASK |

### B. Risk Level

| Level | Définition | Exemples |
|-------|-----------|----------|
| **LOW** | Non critique, réversible, sans secrets | Brouillon, test, exploration |
| **MEDIUM** | Sensible mais réversible | Coding, analyse, documentation |
| **HIGH** | Critique, irréversible | Prod, release, rollback, secrets |
| **CRITICAL** | Impact business majeur | Sécurité, mémoire durable, infra |

### C. Output Format

| Format | Modèle optimal | Interdit |
|--------|----------------|----------|
| **FREE_TEXT** | M2.7, M3, OpenRouter free | — |
| **JSON_STRICT** | M2.7 UNIQUEMENT | M3 (contamination) |
| **MARKDOWN_REPORT** | M2.7, M3 | — |
| **CODE_PATCH** | Codex, M2.7 | OpenRouter free (prod) |
| **SHELL_ACTION** | Codex, M2.7 | — |
| **DISCORD_MESSAGE** | M2.7 | OpenRouter, M3 |
| **LEDGER** | M2.7 | OpenRouter, M3 |
| **RUNBOOK** | M2.7, M3 | — |

### D. Resource Class

| Class | Définition | Modèle |
|-------|-----------|--------|
| **FREE_OK** | Gratuit, illimité | OpenRouter free |
| **MONTHLY_BUDGET_PREFERRED** | Quota mensuel à valoriser | MiMo (après canary) |
| **FIVE_HOUR_QUOTA_OK** | Quota 5h MiniMax | M2.7, M3 |
| **WEEKLY_QUOTA_OK** | Quota hebdo partagé | M2.1/M2.5 |
| **PREMIUM_REQUIRED** | Expertise technique | Codex |
| **STOP_AND_ASK** | Trop cher, risqué, flou | → Stéphane |

---

## Hiérarchie d'Utilisation

### Règle prioritaire absolue

**MiniMax-M2.7 est le modèle par défaut.** Il est utilisé pour :
- Décision finale (orchestration, projet, mémoire)
- JSON strict / protocoles structurés
- Tool calls / exécution
- Sécurité / secrets
- Prod / release / rollback

**M2.7 est préservé quand :**
- Brouillon suffit
- OpenRouter free peut faire le travail
- MiMo peut offloader après canary
- M3 reasoning suffirait pour la partie non-exécutive

**Règle courte validée**

```
M2.7 décide.
M3 réfléchit en long contexte.
Codex agit techniquement.
MiMo exécute l'offload premium sécurisé et valorise le quota mensuel après canary.
OpenRouter brouillonne gratuitement.
Hermes arbitre selon risque, quota, format et criticité.
```

---

## Matrice de Routage par Modèle

### 1. MiniMax-M2.7 — Cerveau Hermes

**UTILISER pour :**

| Catégorie | Exemples |
|-----------|----------|
| Orchestration | Coordination multi-agents, arbitrage, décision projet |
| Coordination | Live monitoring, diagnostic, gouvernance |
| Mémoire | Écriture mémoire durable, MEMORY.md, curated memory |
| JSON strict | Protocoles structurés, API responses, config formats |
| Tool calls | Exécution d'outils, delegation, kron jobs |
| Sécurité | Secrets, credentials, audit sécurité |
| Prod | Release, rollback, déploiement, infrastructure |
| Validation | Validation finale, vérification, approbation |
| Discord | Messages structurés vers agents ou humains |
| Fallback | Après erreur sur autre modèle (sauf si M2.7 déjà utilisé) |

**PRÉSERVER pour les tâches où il est vraiment nécessaire.**

### 2. MiniMax-M3 — Raison Pure

**UTILISER pour :**

| Catégorie | Exemples |
|-----------|----------|
| Long-context reasoning | Contexte >100K tokens, analyse de sessions géantes |
| Audit multi-docs | Comparaison >5 documents simultanément |
| Analyse stratégique | Évaluation de >3 options avec critères |
| Migration architecture | Plan de migration multi-composants |
| Synthèse gros corpus | Synthèse de documentation volumineuse |
| Recherche approfondie | Quand session_search insuffisant |
| Analyse de risques | Évaluation risques complexes |

**INTERDIT pour :**

| Catégorie | Raison |
|-----------|--------|
| JSON strict | Tags `<thinking>` contaminent le output |
| Tool calls | Contamination, exécution non fiable |
| Commandes opérationnelles | Reasoning ≠ exécution |
| Décision finale prod | Pas de validation humaine intégrée |
| Sécurité / secrets | Niveau sensibilité maximum |
| Release / rollback | Risque irréversible |
| Discord automatique | Perturbation protocole |
| Tâches courtes | Gaspillage de la capacité reasoning |

**RÈGLE :** M3 réfléchit, M2.7 arbitre.

### 3. Codex OAuth — Mains Techniques

**UTILISER pour :**

| Catégorie | Exemples |
|-----------|----------|
| Code | Python, JS, Bash, etc. (réel, pas simulation) |
| Repo / git | Clone, push, pull, merge, conflicts |
| Shell / serveur | Commandes système, scripts, debugging |
| Debugging | Stack traces, logs, config, pdb |
| Review technique | PR review, diff analysis, architecture |
| Modifications fichiers | patch, write, edit (pas juste lecture) |
| Validation technique | Compilation, tests, lint |

**PRÉSERVER quand :**
- Pas d'action technique réelle
- Simple synthèse / résumé
- Brainstorming non technique
- Tâche de coordination pure

**RÈGLE :** Codex agit, mais ne gaspille pas sur des tâches non techniques.

### 4. OpenRouter Free — Brouillonnage

**UTILISER pour :**

| Catégorie | Exemples |
|-----------|----------|
| Brainstorming | Génération d'idées, exploration |
| Première passe | Analyse initiale non critique |
| Exploration | Test de concept, prototypage |
| Reformulation | Refactoring texte non critique |
| Résumé non sensitif | Résumé de document non sensible |
| Test de concept | Validation idée avant engagement |

**LIMITES :**
- MAX 10 tool calls par tâche
- Livrables <20 lignes ou <10 tool calls

**INTERDIT pour :**

| Catégorie | Raison |
|-----------|--------|
| Secrets / sécurité | Niveau sensibilité |
| Prod / release | Risque irréversible |
| Décision finale | Non authoritatif |
| Livrables longs | >20 lignes, >10 tool calls |
| JSON strict | Fiabilité insuffisante |
| Code complexe | Non fiable pour prod |
| Mémoire durable | Pas assez stable |
| Configuration infra | Trop critique |

**RÈGLE :** OpenRouter brouillonne, ne décide pas.

### 5. Xiaomi/MiMo — Premium Monthly Secured Offload

**STATUS:** CANARY_LEVEL_2_PASS — PREMIUM_SECURED_DOC_ONLY
**Classification:** Paid dedicated token plan (11B credits/month) — NOT free, NOT opportunistic.

**UTILISER après canary validé (Niveau 1-3 minimum) :**

|| Catégorie | Exemples |
|-----------|----------|
| Premium offload coding | Tâches coding interactives sérieuses (compatible AI coding tools) |
| Serious work analysis | Analyse non secrète, évaluation approfondie |
| Tâches longues non prod-critical | Quand MiniMax doit être préservé pour tâches critiques |
| Monthly quota intelligent consumption | Valoriser le quota mensuel (11B credits) intelligemment |
| Coding agent tools | Tâches compatibles avec MiMo |

**INTERDIT (règles MiMo) :**

| Contrainte | Raison |
|-----------|--------|
| Automated scripts | Violation terms of service |
| Application backends | Violation terms of service |
| Cron jobs | Violation terms of service |
| Backend app | Violation terms of service |
| Automatisation répétitive | Violation terms of service |
| Secrets / sécurité | Niveau sensibilité |
| Prod / release | Risque irréversible |

**INTERDIT (règles canary) :**

| Condition | Action |
|-----------|--------|
| Canary non validé Niveau 1-3 | Aucune exécution |
| Validation sécurité non faite | Aucune exécution |
| Sans consentement humain | Aucune exécution |
| Clé en docs | Jamais — sécurité absolue |

**RÈGLE :** MiMo exécute l'offload premium sécurisé et valorise le quota mensuel après canary. MiMo ≠ OpenRouter free, ≠ brouillon gratuit, ≠ opportuniste.

**Reporting obligatoire — Quand Hermes choisit MiMo :**

```
Pourquoi MiMo plutôt que M2.7: <justification>
Pourquoi MiMo plutôt que Codex: <justification>
Pourquoi MiMo plutôt que M3: <justification>
Pourquoi pas OpenRouter free: <justification>
Impact quota mensuel: <estimation credits>
Niveau de risque: <LOW|MEDIUM|HIGH>
Validation humaine nécessaire: <oui/non>
```

---

## Politique de Budget

### Règle de préservation MiniMax

**Principe :** MiniMax-M2.7 est la ressource la plus précieuse. Chaque appel doit être justifié.

| Situation | Action |
|-----------|--------|
| Tâche non critique | OpenRouter free ou M2.1/M2.5 |
| Tâche reasoning long | M3 (pas M2.7) |
| Tâche technique | Codex (pas M2.7) |
| Tâche simple résumé | M2.1/M2.5 ou OpenRouter free |
| Contexte >80K tokens | Compression proactive |
| >20 tool calls | Scinder en sous-tâches |
| Erreur 1 | Log + continuer |
| Erreur 2 | STOP → rapporter immédiatement |

### Règle MiMo Monthly Budget

**Principe :** Le quota MiMo (11B crédits) doit être valorisé intelligemment.

| Situation | Action |
|-----------|--------|
| Quota MiMo élevé + fin de mois | Proposer utilisation pour tâches adaptées |
| Quota MiMo bas | Préserver pour tâches critiques |
| Quota MiMo non testé | Demander validation canary |
| MiMo non configuré | Rester DOC_ONLY |

### Seuils d'alerte

| Trigger | Action |
|---------|--------|
| MiniMax >3000 req/5h | Alerte : quota à 67% |
| MiniMax >4000 req/5h | STOP non essentiel |
| MiMo usage >50% mensuel | Revoir stratégie offload |
| 2 agents simultanément | Évaluer nécessité |

---

## Reporting Obligatoire

Pour toute tâche significative, Hermes documente :

```
Mode: <mode>
Modèle choisi: <model>
Pourquoi ce modèle: <justification>
Pourquoi pas M2.7: <si non choisi>
Pourquoi pas Codex: <si non choisi>
Pourquoi pas OpenRouter: <si non choisi>
Pourquoi pas MiMo: <si non choisi>
Risque: <LOW|MEDIUM|HIGH|CRITICAL>
Quota impact: <estimation>
Fallback: <plan B>
Validation humaine requise: <oui/non>
```

**Quand utiliser ce reporting :**
- Tâches critiques (HIGH/CRITICAL)
- Tâches coûtant >1000 tokens
- Tâches >60s estimées
- Tâches impliquant plusieurs modèles
- Tâches prod/release/security
- Demandes de Stéphane

---

## Fallbacks Corrigés

| Tâche | Default | Alternative | Fallback | Interdit |
|-------|---------|-------------|----------|----------|
| Orchestration Hermes | M2.7 | M3 (reasoning long sans décision) | STOP_AND_ASK | OpenRouter free |
| Long-context reasoning | M3 | M2.7 | MiMo (canary) ou STOP | OpenRouter (non authoritative) |
| Coding technique | Codex | MiMo (canary) + coding tools | M2.7 (analyse, pas shell) | OpenRouter (code prod) |
| Brouillon non critique | OpenRouter free | MiMo (quota à valoriser) | M2.1/M2.5 | M2.7 (gaspillage) |
| JSON strict | M2.7 | — | STOP_AND_ASK | M3 (contamination) |
| Security/secrets | M2.7 | — | STOP_AND_ASK | TOUT free |
| Tâche simple résumé | M2.1/M2.5 | OpenRouter free | — | M2.7 (gaspillage) |
| Analyse stratégique | M3 | M2.7 | STOP_AND_ASK | OpenRouter |
| TTS/ASR | MiniMax TTS | — | — | OpenRouter, MiMo |
| Image generation | MiniMax | — | — | OpenRouter free |
| Multi-agent coordination | M2.7 | — | STOP_AND_ASK | M3 (tool calls) |

---

## Canary MiMo — Protocole

### Niveaux de test

| Niveau | Test | Classification | Status |
|--------|------|----------------|--------|
| 1 | Découverte modèles `/v1/models` | READ_ONLY | ⬜ EN ATTENTE |
| 2 | Prompt simple non sensible | SAFE_CANARY | ⬜ EN ATTENTE |
| 3 | Test coding court non sensitif | SAFE_CANARY | ⬜ EN ATTENTE |
| 4 | Test JSON strict | NEEDS_HUMAN_KEY | ⬜ EN ATTENTE |
| 5 | Test latence | NEEDS_HUMAN_KEY | ⬜ EN ATTENTE |
| 6 | Usage dashboard / coût | NEEDS_HUMAN_KEY | ⬜ EN ATTENTE |

### Statuts canary

| Status | Signification | Actions autorisées |
|--------|--------------|-------------------|
| CANARY_PENDING | Non testé | Aucune exécution, DOC_ONLY |
| CANARY_READY | Niveau 1-3 validé | Usage limité non sensitif |
| ACTIVE_LIMITED | Tests OK | Coding interactif non prod |
| ACTIVE_PREMIUM_MONTHLY | Validation complète | Usage selon budget mensuel |

**RÈGLE :** Exécuter sans validation humaine explicite = INTERDIT.

---

## Sécurité — Règles Absolues

### Clés et secrets

1. **Clé MiMo** : Jamais affichée, jamais en docs, jamais indexée OpenViking, jamais push Git
2. **Token MiniMax** : Jamais affiché en clair (sk-cp-***, sk-api-***)
3. **auth.json** : Jamais affiché, jamais copié
4. **.env** : Jamais modifié sans validation humaine explicite

### Usage interdit

1. **OpenRouter free** : Jamais pour secrets, prod, release, rollback, sécurité, décision finale
2. **M3** : Jamais pour JSON strict, tool calls, sécurité, prod, release
3. **MiMo non canary** : Jamais sans validation humaine explicite
4. **Génération vidéo** : Jamais (aucun endpoint vidéo supporté)

### Configuration

- Clés uniquement via .env / secret store
- Jamais de clé en Markdown ou documentation
- Vérification systématique après toute modification

---

## Multi-Agent — Coordination

### Règle simple

```
Priorité 1 : Orchestrateur (Hermes) → M2.7
Priorité 2 : Agent actif → selon tâche (M3, Codex, M2.7)
Priorité 3 : NE PAS lancer tous les agents en parallèle sur MiniMax
```

### Exemple concret

```
Situation : Ariane analyse marché + Atlas fait DevOps

FAUX : Lancer les 2 agents en parallèle sur MiniMax
       → Dépassement budget, latence, conflit

BON : Hermes orchestre Ariane sur M2.7/M3 selon longueur
       Atlas fait DevOps sur Codex ou attend son tour
       OU Atlas utilise OpenRouter free si non critique
```

---

## Vérifications

### Checklist avant tâche

```
[ ] La tâche nécessite vraiment M2.7 ou un modèle plus léger suffit ?
[ ] M3 est-il pertinent (reasoning long-context) ou M2.7 suffit ?
[ ] Je peux utiliser OpenRouter free pour cette tâche non critique ?
[ ] M2.1/M2.5 est-il suffisant pour cette tâche auxiliaire ?
[ ] MiMo peut-il offloader après canary ?
[ ] Je n'ai pas déjà fait 2 erreurs consécutives sur ce type de tâche ?
[ ] Le budget remaining est-il suffisant ?
```

### Checklist après tâche

```
[ ] Aucun token/API key exposé
[ ] Le bon modèle selon la hiérarchie
[ ] M3 pas pour JSON strict / tool calls
[ ] OpenRouter respecté (MAX 10 tool calls, pas de secrets)
[ ] Budget respecté
[ ] Si erreur : règles de stop appliquées
[ ] Mission folder mis à jour si livrable produit
```

---

## Fichiers de Référence

| Fichier | Usage |
|---------|-------|
| `LEDGER_2026-06-07_P32_ACTIVE_MODEL_RESOURCE_GOVERNANCE.md` | Ledger P32 |
| `runbooks/ai_model_routing.md` | Runbook v1.5 (mise à jour) |
| `AGENTS_GOVERNANCE.md` | Gouvernance v1.6 (mise à jour) |
| `hermes-sysop-config/SKILL.md` | Infrastructure + section modèles |
| `LEDGER_2026-06-07_P31_MODEL_ROUTING_STRATEGY.md` | Stratégie P31 |
| `LEDGER_2026-06-02_MINIMAX_M3_CANARY.md` | Tests M3 |
| `LEDGER_2026-06-07_P30_LATENCY_AUDIT_AND_V014_CLEANUP_PLAN.md` | Correctifs C-01-C-05 |

---

**Version:** 1.1
**Date:** 2026-06-07
**Auteur:** Hermes Orchestrateur
**Règle courte:** M2.7 décide, M3 réfléchit, Codex agit, MiMo offload premium après canary, OpenRouter brouillonne gratuitement.