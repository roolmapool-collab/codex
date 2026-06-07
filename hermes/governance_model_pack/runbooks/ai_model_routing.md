# ai_model_routing — Runbook v1.8

Runbook opérationnel pour le routage des modèles IA dans Hermes.

**Objectif :** Aider Hermes à choisir le bon modèle au bon moment, respecter le budget, et appliquer les règles de sécurité.

**Version :** 1.8
**Date :** 2026-06-07
**Source :** P32 Active Model Resource Governance + P32.1 MiMo + P33 Resource Cards + P34 Availability Probe
**Référence fiches :** `/opt/data/workspace/model_resources/` (minimax.md, codex_oauth.md, mimo.md, openrouter_free.md)
**Référence probe :** `/opt/data/workspace/runbooks/model_availability_quota_probe.md`

**Règle prioritaire absolue :** Hermes orchestre activement les ressources modèles IA selon besoin, risque, format, quota et criticité. Pas de réflexe "tout sur MiniMax".

---

## Hiérarchie des modèles

**Règle prioritaire absolue :** Hermes orchestre activement les ressources modèles IA.

| Priorité | Modèle | Rôle |
|---|---|---|
| 1 | **MiniMax-M2.7** | Cerveau Hermes — décision finale, JSON, tool calls, sécurité |
| 2 | **MiniMax-M3** | Raison pure — reasoning long-context uniquement, interdit JSON/tool calls |
| 3 | **Codex OAuth** | Mains techniques — code, git, shell, serveur |
| 4 | **OpenRouter free** | Brouillonnage — brainstorming, première passe, non critique |
| 5 | **MiniMax M2.1/M2.5** | Tâches auxiliaires — résumé simple, classification |
| 6 | **Xiaomi/MiMo** | Premium monthly secured offload — CANARY_PENDING, paid dedicated token plan (11B credits), serious work after canary |

**Règle courte :**
```
M2.7 décide.
M3 réfléchit en long contexte.
Codex agit techniquement.
OpenRouter brouillonne gratuitement.
MiMo valorise le quota mensuel en offload premium interactif après canary.
Hermes orchestre les ressources, pas seulement les réponses.
```

---

## Modèle de Décision Obligatoire

Avant toute tâche significative, Hermes classifie selon 4 dimensions :

### A. Task Type

| Type | Définition | Modèle par défaut |
|------|------------|-------------------|
| ORCHESTRATION | Coordination, arbitrage, décision finale, mémoire | M2.7 |
| TECHNICAL_ACTION | Code, shell, git, serveur, debug | Codex |
| LONG_CONTEXT_REASONING | Audit multi-docs, migration, analyse stratégique | M3 |
| DRAFT_OR_BRAINSTORM | Première passe, exploration, test non critique | OpenRouter free |
| STRUCTURED_OUTPUT | JSON strict, protocoles structurés | M2.7 |
| SECURITY_OR_SECRET | Secrets, sécurité, credentials | M2.7 |
| PROD_RELEASE_ROLLBACK | Release, rollback, déploiement | M2.7 |
| SIMPLE_SUMMARY | Résumé court, classification, extraction | M2.1/M2.5 ou OpenRouter |
| AUDIO_TTS_ASR | Synthèse vocale, transcription | MiniMax TTS |
| MULTIMODAL | Image, audio, vidéo | MiniMax |
| UNKNOWN | Flou, risqué, coûteux | STOP_AND_ASK |

### B. Risk Level

| Level | Définition | Exemples |
|-------|-----------|----------|
| LOW | Non critique, réversible, sans secrets | Brouillon, test, exploration |
| MEDIUM | Sensible mais réversible | Coding, analyse, documentation |
| HIGH | Critique, irréversible | Prod, release, secrets |
| CRITICAL | Impact business majeur | Sécurité, infra |

### C. Output Format

| Format | Modèle optimal | Interdit |
|--------|----------------|----------|
| FREE_TEXT | M2.7, M3, OpenRouter free | — |
| JSON_STRICT | M2.7 UNIQUEMENT | M3 |
| MARKDOWN_REPORT | M2.7, M3 | — |
| CODE_PATCH | Codex, M2.7 | OpenRouter free (prod) |
| SHELL_ACTION | Codex, M2.7 | — |
| DISCORD_MESSAGE | M2.7 | OpenRouter, M3 |
| LEDGER | M2.7 | OpenRouter, M3 |

### D. Resource Class

| Class | Définition | Modèle |
|-------|-----------|--------|
| FREE_OK | Gratuit, illimité | OpenRouter free |
| MONTHLY_BUDGET_PREFERRED | Premium monthly secured resource (11B credits) | MiMo (after canary) |
| FIVE_HOUR_QUOTA_OK | Quota 5h MiniMax | M2.7, M3 |
| WEEKLY_QUOTA_OK | Quota hebdo partagé | M2.1/M2.5 |
| PREMIUM_REQUIRED | Expertise technique | Codex |
| STOP_AND_ASK | Trop cher, risqué, flou | → Stéphane |

---

## Modes de routage obligatoires

Avant chaque tâche, Hermes choisit un mode :

| Mode | Quand utiliser | Modèle |
|---|---|---|
| **CRITICAL** | Décision projet, orchestration, synthèse finale, mémoire, sécurité, release | MiniMax-M2.7 |
| **LONG_REASONING** | Analyse stratégique, audit multi-docs, migration, comparaison options | MiniMax-M3 |
| **TECHNICAL_ACTION** | Code, repo, git, shell, serveur, debugging, review technique | Codex OAuth |
| **OPPORTUNISTIC** | Brainstorming, première passe, synthèse non critique, brouillon court | OpenRouter free |
| **AUXILIARY** | Résumé court, classification, extraction simple, titre, nettoyage texte | M2.1/M2.5 |
| **STOP_AND_ASK** | Tâche floue, coûteuse, sensible, risquée | → Demander à Stéphane |

**Hermes doit toujours justifier son choix de mode dans le rapport.**

---

## Matrice de routage par tâche

| Tâche | Modèle recommandé | Fallback | Interdit | Justification |
|-------|-------------------|----------|----------|---------------|
| **Hermes orchestration quotidienne** | MiniMax-M2.7 | — | OpenRouter free, M3 (tool calls) | Décision, coordination, mémoire |
| **Décision finale prod** | MiniMax-M2.7 | — | OpenRouter free, M3 (JSON strict) | Stabilité, pas de contamination |
| **Sécurité / secrets** | MiniMax-M2.7 | — | TOUT free, M3 (tool calls) | Niveau sensibilité maximum |
| **Release / rollback** | MiniMax-M2.7 | — | OpenRouter free, M3 | Pas de risque |
| **Long-context reasoning** | MiniMax-M3 | MiniMax-M2.7 | OpenRouter free | 1M tokens M3 vs ~100K M2.7 |
| **Audit multi-docs** | MiniMax-M3 | MiniMax-M2.7 | OpenRouter free | Analyse stratégique |
| **Migration architecture** | MiniMax-M3 | MiniMax-M2.7 | OpenRouter free | Raisonnement complexe |
| **Coding technique** | Codex OAuth | MiniMax-M2.7 | OpenRouter free (complexe) | Expertise technique |
| **Shell / git / repo / debug** | Codex OAuth | MiniMax-M2.7 | OpenRouter free | Mains sur le système |
| **Brouillon non critique** | OpenRouter free | MiniMax-M2.7 | — | Économie quota |
| **Résumé simple** | MiniMax-M2.1/M2.5 | OpenRouter free | — | Tâche triviale |
| **Extraction / classification** | MiniMax-M2.5 | MiniMax-M2.7 | OpenRouter free (si critique) | Simple mais sensitif |
| **JSON strict / structured output** | MiniMax-M2.7 | — | MiniMax-M3 (tags contaminent) | Pas de contamination |
| **Tool calls** | MiniMax-M2.7 | — | MiniMax-M3 (tags contaminent) | Exécution, pas de contamination |
| **Discord automatique** | MiniMax-M2.7 | — | OpenRouter free, MiniMax-M3 | Stabilité |
| **TTS (speech)** | MiniMax speech-2.8-hd | — | OpenRouter, M3 | Endpoint `/v1/t2a_v2` MiniMax only |
| **ASR** | MiniMax-M2.5 | OpenRouter free | — | Transcription simple |
| **Image generation** | MiniMax (MiniMax Image) | — | OpenRouter free | Livrable le justifie |
| **Tasks longues >60s** | MiniMax-M2.7 + ACK initial | MiniMax-M3 (reasoning) | OpenRouter free | Évite perception freeze |
| **Tasks très longues >20 tool calls** | MiniMax-M2.7 + scinder | — | OpenRouter free | Évite sessions géantes |

---

## MiniMax-M2.7 — Cerveau Hermes

**Quand utiliser :**
```
Orchestration Hermes → M2.7
Coordination multi-agents → M2.7
Décisions projet → M2.7
Synthèse finale → M2.7
Arbitrage mémoire → M2.7
Analyse longue → M2.7
Tâches critiques → M2.7
Fallback après erreur autre modèle → M2.7
JSON strict → M2.7
Tool calls → M2.7
```

---

## MiniMax-M3 — Raison pure (2026-06-02 — PROMOTE_FOR_SPECIFIC_TASKS)

**Disponibilité :** Créé 2026-05-25. Disponible via provider `minimax`.

### Quand utiliser M3 :
```
Raisonnement complexe → M3
Analyse stratégique → M3
Synthèse longue → M3
Audit multi-docs → M3
Comparaison d'options → M3
Migration architecture → M3
Long-context (contexte >100K tokens) → M3
```

### Interdits stricts pour M3 :
```
JSON strict / structured output → INTERDIT (tags contaminent)
Tool calls → INTERDIT (tags contaminent)
Commandes opérationnelles → INTERDIT
Décisions finales de prod → INTERDIT
Sécurité / secrets → INTERDIT
Release / rollback → INTERDIT
Messages Discord automatiques → INTERDIT
Workflows où les balises <thinking> cassent la sortie → INTERDIT
```

**Raison :** M3 utilise chain-of-thought reasoning (tags `<thinking>`) qui pollue le output JSON strict.
Test canary 2026-06-02 : Test A (reasoning) = PASS, Test B (JSON) = BEHAVIOR_FAIL (contamination).
M2.7 reste meilleur pour JSON/protocoles structurés.

**M3 ne remplace pas M2.7.** M2.7 = modèle par défaut général. M3 = reasoning only, validation humaine requise.

---

## Codex OAuth — Mains techniques

**Quand utiliser :**
```
Code réel → Codex
Repo / git → Codex
Shell / serveur → Codex
Debugging → Codex
Review technique → Codex
Modifications fichiers → Codex
```

**Vérification avant usage :**
1. Vérifier status Codex OAuth (`hermes status`)
2. Ne jamais afficher `/opt/data/auth.json`
3. Confirmer logged in avant routage

---

## OpenRouter free — Opportunité utile

**Quand utiliser :**
```
Brainstorming non critique → OpenRouter free
Première passe d'analyse → OpenRouter free
Synthèse non sensible → OpenRouter free
Brouillon court → OpenRouter free
Test non critique → OpenRouter free
```

**Règles strictes :**
- MAX 10 tool calls par tâche
- **INTERDIT pour :** secrets, décision finale, release, infra critique, sécurité, **livrables longs**, prod, release/rollback, décisions finales
- **Fallback vers M2.7 après 2 erreurs** → STOP, puis proposer fallback M2.7 si utile
- Pas de retry loop

---

## MiniMax M2.1/M2.5 — Petites tâches auxiliaires

**Quand utiliser :**
```
Résumé court → M2.1/M2.5
Classification → M2.1/M2.5
Extraction simple → M2.1/M2.5
Titres → M2.1/M2.5
Nettoyage texte → M2.1/M2.5
```

**Interdit pour :** décision projet, sécurité, code complexe, production, mémoire durable.

---

## Xiaomi/MiMo — Premium Monthly Secured Offload — CANARY_LEVEL_2_PASS (2026-06-07)

**Classification:** PREMIUM_SECURED_DOC_ONLY
**Type:** Paid dedicated token plan — 11B credits/month
**Status:** CANARY_PENDING — NOT free, NOT opportunistic, NOT a free resource.

**MiMo ≠ OpenRouter free. MiMo ≠ brouillon gratuit. MiMo ≠ opportuniste.**

### Caractéristiques

| Caractéristique | Valeur |
|----------------|--------|
| Plan | Token Plan Plus — 11B crédits (0 utilisé) |
| Base URL OpenAI-compatible | `https://token-plan-ams.xiaomimimo.com/v1` |
| Base URL Anthropic-compatible | `https://token-plan-ams.xiaomimimo.com/anthropic` |
| Modèles | `mimo-v2.5-pro`, `mimo-v2.5`, `mimo-v2.5-asr`, `mimo-v2.5-tts-voiceclone`, `mimo-v2.5-tts-voicedesign`, `mimo-v2.5-tts`, `mimo-v2-pro`, `mimo-v2-omni`, `mimo-v2-tts` |
| Usage autorisé | Interactive use with compatible AI coding and agent tools only |

### Contraintes strictes

| Contrainte | Règle |
|------------|-------|
| Automated scripts | ❌ INTERDIT |
| Application backends | ❌ INTERDIT |
| Cron jobs | ❌ INTERDIT |
| Clé en docs | ❌ INTERDIT |
| Clé indexée (OpenViking) | ❌ INTERDIT |
| Promotion runtime | ❌ INTERDIT sans canary explicite |
| Usage secrets | ❌ INTERDIT sans validation sécurité |

### Rôle possible

|| Usage | Évaluation | Status |
|-------|------------|--------|
| Premium offload coding interactif longues tâches | ✅ Serious work candidate | CANARY_PENDING |
| Monthly quota intelligent consumption | ✅ Valoriser les 11B credits intelligemment | CANARY_PENDING |
| Serious work analysis non prod-critical | ✅ Pertinent après canary | CANARY_PENDING |
| Tâches longues pour préserver MiniMax | ✅ Altérnatif sérieux à OpenRouter | CANARY_PENDING |
| TTS/ASR | ✅ `mimo-v2.5-tts`, `mimo-v2.5-asr` | CANARY_PENDING |
| Modèle omni | ✅ `mimo-v2-omni` | CANARY_PENDING |

**Note:** MiMo est un **plan payant premium**, pas un substitut gratuit à OpenRouter. Son usage doit être justifié et intelligent.

### Plan canary

| Niveau | Test | Classification |
|--------|------|-----------------|
| 1 | Découverte modèles (`/v1/models`) | READ_ONLY |
| 2 | Prompt simple non sensible | SAFE_CANARY |
| 3 | Test coding court | SAFE_CANARY |
| 4 | Test JSON strict | NEEDS_HUMAN_KEY |
| 5 | Test latence | NEEDS_HUMAN_KEY |
| 6 | Test coût/usage dashboard | NEEDS_HUMAN_KEY |

**Statut actuel :** Aucun test exécuté. Clé non utilisée. Validation Stéphane requise avant tout test.

---

## Reporting Obligatoire (Tâches significatives)

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

## Règles de sécurité

### Interdits absolus

```
1. Token/API en clair → JAMAIS
2. auth.json affiché → INTERDIT
3. Secrets (.env, credentials) → OpenRouter free → INTERDIT
4. Génération vidéo MiniMax → INTERDIT
5. Voice clone sans consentement → INTERDIT
6. Codex owner Kanban → INTERDIT
7. Retry loop → INTERDIT
8. OPENAI_API_KEY si OAuth suffit → INTERDIT
9. M3 pour JSON strict / tool calls → INTERDIT
10. Xiaomi/MiMo sans canary → INTERDIT
```

### Ce qui est autorisé

```
→ MiniMax-M2.7 : orchestration, décisions, analyse, coding Hermes, fallback stable, JSON, tool calls
→ MiniMax-M3 : reasoning long-context, audit multi-docs, migration, analyse stratégique. INTERDIT : JSON strict, tool calls
→ Codex OAuth : code, repo, git, shell, serveur, debugging, review
→ OpenRouter free : brainstorming, brouillon, première passe, non critique. MAX 10 tool calls. INTERDIT : secrets, prod, release
→ M2.1/M2.5 : résumé simple, classification, extraction simple
→ MCP web_search : recherche factuelle vérifiable
→ MCP understand_image : analyse visuelle
→ MiniMax image generation : livrable le justifie
→ MiniMax speech : audio si livrable le justifie
→ Xiaomi/MiMo : CANARY_PENDING — usage interactif coding après canary validé
```

---

## Règles anti-latence (P30 — 2026-06-07)

Basées sur LEDGER_2026-06-07_P30_LATENCY_AUDIT_AND_V014_CLEANUP_PLAN.md.

| Règle | Action | Source |
|-------|--------|--------|
| Seuil compression 80K tokens | Compression proactive quand contexte >80K tokens | C-01 validé |
| Tâche >20 tool calls | Scinder en sous-tâches avec livrables intermédiaires | C-05 validé |
| Tâche >60s estimated | ACK initial + progression | C-02 validé |
| Cache <50% | Signaler latence potentielle | P30 |
| HTTP 529 | Retry 1x, puis fallback M2.7 si tâche critique | P30 |

---

## Budget — Comment préserver les 4500 requests/5h

### Checklist avant une tâche

```
[ ] La tâche nécessite vraiment M2.7 ou un modèle plus léger suffit ?
[ ] M3 est-il pertinent (reasoning long-context) ou M2.7 suffit ?
[ ] Je peux utiliser OpenRouter free pour cette tâche non critique ?
[ ] M2.1/M2.5 est-il suffisant pour cette tâche auxiliaire ?
[ ] Je n'ai pas déjà fait 2 erreurs consécutives sur ce type de tâche ?
```

### Si erreur se produit

```
Erreur 1 : Log + continuer (peut être transient)
Erreur 2 : STOP, puis proposer fallback M2.7 si la tâche n'utilisait pas déjà M2.7 ; sinon rapporter
→ Rapporter à Stéphane immédiatement
```

---

## Cost reporting

Pour toute tâche coûteuse ou longue, Hermes indique :

```
Mode : CRITICAL | LONG_REASONING | TECHNICAL_ACTION | OPPORTUNISTIC | AUXILIARY | STOP_AND_ASK
Modèle : <choix>
Pourquoi : <justification>
Appels : <nombre estimé>
Fallback : <plan B si échec>
Risque budget : LOW | MEDIUM | HIGH
```

**Checklist avant appel modèle :**
```
[ ] La tâche est-elle vraiment critique ou peut-elle être opportuniste/auxiliaire ?
[ ] M3 reasoning est-il pertinent ou M2.7 suffit ?
[ ] Ai-je déjà 1 erreur sur cette tâche ?
[ ] Puis-je grouper cette tâche avec une autre ?
[ ] Le budget remaining est-il suffisant ?
```

---

## Multi-agent — Comment gérer les 1-2 agents max

### Règle simple

```
Priorité 1 : Orchestrateur (Hermes) → M2.7
Priorité 2 : Agent actif → selon tâche (M3 pour reasoning, Codex pour technique, M2.7 pour analyse)
Priorité 3 : NE PAS lancer tous les agents en parallèle sur MiniMax
```

### Exemple concret

```
Situation : Ariane fait analyse marché + Atlas fait DevOps

FAUX : Lancer les 2 agents en parallèle sur MiniMax
       → Dépassement budget, latence, conflit

BON : Hermes orchestre Ariane sur l'analyse marché (M2.7 ou M3 selon longueur)
       Atlas fait son DevOps sur Codex ou attend son tour
       OU Atlas utilise OpenRouter free si c'est non critique
```

---

## Seuils d'alerte

| Trigger | Action |
|---|---|
| Plusieurs agents veulent utiliser MiniMax en même temps | Alerter Stéphane |
| Tâche longue ou répétitive | Demander validation |
| Rate limit / 429 / 402 / provider error | STOP + plan de réduction |
| Besoin vidéo | Refuser → vidéo exclue |
| 2 erreurs consécutives | STOP → rapporter |
| Contexte >80K tokens | Compression proactive |

---

## Résolution des cas ambigus

### "Je ne sais pas quel modèle utiliser"

```
Règle par défaut : MiniMax-M2.7
Sauf si la tâche est clairement :
  - reasoning long-context (audit/migration/analyse) → M3
  - technique (code/git/shell/serveur) → Codex
  - non critique et opportuniste → OpenRouter free
  - auxiliaire simple → M2.1/M2.5 ou OpenRouter free
```

### "La tâche combine plusieurs choses"

```
Décomposer :
  1. Partie technique (code/git) → Codex
  2. Partie raisonnement long-context → M3
  3. Partie décision/analytique → MiniMax-M2.7
  4. Partie simple (résumé) → M2.1/M2.5 ou OpenRouter free

Utiliser le modèle le plus puissant requis par l'une des parties.
```

### "OpenRouter free est instable aujourd'hui"

```
1. Vérifier disponibilité
2. Si indisponible ou réponses médiocres → fallback MiniMax-M2.7
3. Ne pas insister avec retry loop
```

---

## Checklist de vérification

Après toute tâche utilisant un modèle IA :

```
[ ] Aucun token/API key exposé dans les logs ou outputs
[ ] Le bon modèle a été utilisé selon la hiérarchie
[ ] M3 pas utilisé pour JSON strict / tool calls
[ ] OpenRouter free respecté (MAX 10 tool calls, pas de secrets)
[ ] Le budget a été respecté (pas d'appels inutiles)
[ ] Si erreur : règles de stop appliquées
[ ] Aucune génération vidéo MiniMax effectuée
[ ] Voice clone : consentement validé avant utilisation
[ ] Codex n'a pas été owner officiel d'une tâche Kanban
[ ] auth.json jamais affiché
[ ] Xiaomi/MiMo pas utilisé sans canary validé
[ ] Mission folder mis à jour si livrable produit
```

---

## Fichiers de référence

| Fichier | Usage |
|---|---|
| `LEDGER_2026-06-07_P32_ACTIVE_MODEL_RESOURCE_GOVERNANCE.md` | Analyse complète P32 |
| `MODEL_RESOURCE_GOVERNANCE.md` | Gouvernance principale v1.0 |
| `LEDGER_2026-06-07_P31_MODEL_ROUTING_STRATEGY.md` | Analyse complète P31 |
| `LEDGER_2026-06-02_MINIMAX_M3_CANARY.md` | Tests M3, décision PROMOTE |
| `LEDGER_2026-06-07_P30_LATENCY_AUDIT_AND_V014_CLEANUP_PLAN.md` | Correctifs C-01-C-05 |
| `AGENTS_GOVERNANCE.md` | Gouvernance v1.6 |
| `hermes-sysop-config/SKILL.md` | Infrastructure + section Xiaomi/MiMo |

**Version :** 1.5
**Date :** 2026-06-07
**Auteur :** Hermes Orchestrateur
**Source :** P32 Active Model Resource Governance