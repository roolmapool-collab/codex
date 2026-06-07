# 📑 DOC_INDEX.md — Index de la Documentation Hermes

> **Version:** 1.8
> **Emplacement :** `/opt/data/workspace/DOC_INDEX.md`
> ⚠️ MAJ après chaque ajout/suppression de document

---

## 🚨 SÉQUENCE BOOT (OBLIGATOIRE)

| Fichier | Rôle |
|---------|------|
| `BOOT.md` | **À lire en premier** — Séquence boot obligatoire + structure mémoire hybride |
| `_current_state.md` | WAL snapshot — État courant Hermes root |
| `MEMORY.md` | Base connaissances long terme curée |

---

## 🏗️ INFRASTRUCTURE & SYSTÈME

| Fichier | Synthèse |
|---------|----------|
| `SHARED_KNOWLEDGE.md` | Wikisystème Hermes + OpenClaw (infra, modèles, Caddy, workflow deploy, alertes) | `DOC-SHARED-KNOWLEDGE-20260526` |
| `docker_inventory.md` | **NOUVEAU** — Inventaire complet Docker (9 containers, réseaux, commands diagnostic) |
| `TOOLS.md` | Référence commandes SysOp (Docker, SSH, Caddy, Hermes CLI) |
| `HEARTBEAT.md` | Standing Orders — déclenchement, rôles, alertes, monitoring |
| `IDENTITY.md` | Identité technique Hermes Root (mission, périmètre, modèle) | `DOC-IDENTITY-HERMES-ROOT` |
| `SOUL.md` | Identité et comportement de l'agent | `SOUL-HERMES-MAIN` |

---

## 🤖 MULTI-AGENT DISCORD — AI Delivery Team

| Fichier | Synthèse |
|---------|----------|
| `AGENTS_GOVERNANCE.md` | **Gouvernance v2.0** — Canaux, règles mention, format réponse, anti-boucle (518 lignes) |
| `DISCORD_MULTI_AGENT_SETUP.md` | Guide installation complet v2.0 — 4 agents + orchestrateur | `DOC-DISCORD-SETUP-20260518` |
| `DISCORD_COLLABORATION_PROCESS.md` | Processus collaboration v1.0 — Workflows, statuts, RACI | `DOC-DISCORD-COLLAB-20260526` |
| `DISCORD_COMPLIANCE_REPORT.md` | Rapport conformité v1.0 — Audit permissions | `DOC-DISCORD-COMPLIANCE-20260518` |
| `DOC_FONCTIONNELLE_DISCORD.md` | Documentation fonctionnelle v1.0 (1332 lignes) |
| `RAPPORT_CONFORMITE_DOC.md` | Comparaison DOC vs réalité (262 lignes) |
| `RAPPORT_FINAL_AGENTS.md` | Configuration agents v1.0 (197 lignes) |
| `discord_inventory.md` | **NOUVEAU** — Inventaire complet (6 bots, 10 canaux, 5 gateways, config .env) |
| `runbooks/restart_agent_gateway.md` | Runbook restart gateway par profil |
| `runbooks/ai_model_routing.md` | **MAJ v1.8** — Routage modèle : M3 intégré, Xiaomi/MiMo CANARY_PENDING, probe dispo/quotas, règles décision. P34: ref probe. | `P31-P32-P32.1-P33-P34` |
| `runbooks/model_availability_quota_probe.md` | **NOUVEAU** — Probe dispo + quotas modèles. Probes par ressource, seuils GREEN/YELLOW/RED, règles décision, canary MiMo (PREPARE ONLY). P34. | `P34` |
| `runbooks/model_resource_live_counters.md` | **NOUVEAU** — Live Counter Gate. Concept A→D, counters auto/manuels, routing rules 4 catégories, probe commands, demande compteurs manuels. P37. | `P37` |
| `MODEL_RESOURCE_GOVERNANCE.md` | **MAJ v1.3** — Table centrale + ref probe + corrections Codex/M2.7. P34: probe dispo/quotas. | `P32-P32.1-P33-P34` |
| `model_resources/minimax.md` | **NOUVEAU** — Fiche ressource MiniMax (M2.7, M3, M2.1/M2.5, TTS). Status, counters, decision rules, security, canary, fallback, reporting template. | `P33` |
| `model_resources/codex_oauth.md` | **NOUVEAU** — Fiche ressource Codex OAuth. Status, counters, decision rules, security, OAuth no OPENAI_API_KEY, fallback, reporting template. | `P33` |
| `model_resources/mimo.md` | **NOUVEAU** — Fiche ressource Xiaomi/MiMo (CANARY_PENDING). Status premium secured, counters 11B credits, security rules, canary 6 niveaux, reporting template. | `P33` |
| `model_resources/openrouter_free.md` | **NOUVEAU** — Fiche ressource OpenRouter free (Owl Alpha). Status FREE_UNTRUSTED, counters, decision rules, security, non authoritative, fallback, reporting template. | `P33` |
| `LEDGER_2026-06-07_P32_1_MIMO_PREMIUM_CLASSIFICATION_FIX.md` | **NOUVEAU** — Correction classification MiMo : premium monthly secured resource, paid dedicated token plan (11B credits), NOT free, NOT opportunistic. | `P32.1` |
| `LEDGER_2026-06-07_P37_MODEL_RESOURCE_LIVE_COUNTERS.md` | **NOUVEAU** — Live Counter Gate. Script probe, runbook, JSON status. Routing rules 4 catégories. Auto vs manual counters. Hermes ne route plus à l'aveugle. | `P37` |
| `LEDGER_2026-06-07_P37_1_LIVE_COUNTERS_FIX.md` | **MAJ** — Fix P37.1: DR Git → DR_PUSH_PENDING, MiMo days_left_in_month → automatic. | `P37.1` |
| `LEDGER_2026-06-07_P37_2_COUNTER_KEY_CONTEXT_FIX.md` | **NOUVEAU** — Correction détection clés: check_key_presence(), credentials block, KEY_PRESENT_ENV_FILE vs KEY_NOT_FOUND. MiMo CANARY_LEVEL_2_PASS. MANUAL_REQUIRED avec reason. | `P37.2` |
| `LEDGER_2026-06-07_P37_3_DR_GIT_PUSH_CONTEXT_FIX.md` | **MAJ** — Classification SSH DR Git: host/root canonique = PUSH_OK, subcontext hermes = AUTH_FAILED. Overall = OK_WITH_SUBCONTEXT_LIMITATION. Action Stéphane = AUCUNE requise. Ne pas ajouter clé hQR7Ik77... à GitHub. | `P37.3` |
| `LEDGER_2026-06-07_P38_DYNAMIC_AGENT_MODEL_ROUTING_ALIGNMENT.md` | **MAJ** — 4 corrections CANARY_PENDING → CANARY_LEVEL_1_PASS. Règle "agents do not own models" renforcée. Exemples routage par agent (Hermes/Ariane/Vulcain/Argus/Atlas). | `P38` |
| `LEDGER_2026-06-07_P39_2_MIMO_PRO_LEVEL_2_RETRY.md` | **NOUVEAU** — mimo-v2.5-pro Level 2 PASS (500 tokens, latence 6.0s, MIMO_LEVEL_2_OK). MiMo global → CANARY_LEVEL_2_PASS. 5 fichiers mis à jour. | `P39.2` |
| `LEDGER_2026-06-07_P39_MIMO_CANARY_LEVEL_2.md` | **NOUVEAU** — MiMo Level 2 PASS. Prompt simple non sensitif: 3 lignes, LAST=MIMO_LEVEL_2_OK. CANARY_LEVEL_2_PASS. Coding/JSON INTERDIT. | `P39` |
| `LEDGER_2026-06-07_P32B_MINIMAX_M3_DOC_AUDIT.md` | **NOUVEAU** — Audit cohérence docs MiniMax/M3. 6 problèmes corrigés (base_url canonique /v1, leçon M3 v0.16, TTS payload, reference P32) | `P32B` |

---

## 📋 ÉTAT & MÉMOIRE

| Fichier | Synthèse |
|---------|----------|
| `_current_state.md` | WAL snapshot — État temps réel (mis à jour 2026-05-19) |
| `MEMORY.md` | Base connaissances long terme curée (erreurs résolues, leçons, configs) |
| `events.jsonl` | **NOUVEAU** — WAL append-only (8 événements initiaux) |

---

## 📂 DÉCISIONS & RISQUES

| Fichier | Synthèse |
|---------|----------|
| `decisions/DECISIONS.md` | **NOUVEAU** — Archive décisions validées (6 décisions) |
| `risks/RISKS.md` | **NOUVEAU** — Suivi risques ouverts (6 risques) |

---

## 🎯 MISSIONS

| Fichier | Synthèse |
|---------|----------|
| `missions/MISSION-2026-05-19-SYSCOM-001/MISSION.md` | **NOUVEAU** — Mission architecture mémoire hybride (EN COURS) |
| `missions/MISSION-2026-05-19-SYSCOM-001/TASKS.md` | Tâches planifiées (21 tâches) |
| `missions/MISSION-2026-05-19-SYSCOM-001/EVENTS.jsonl` | Événements mission (9 événements) |
| `missions/MISSION-2026-05-19-SYSCOM-001/DECISIONS.md` | Décisions de la mission |
| `missions/MISSION-2026-05-19-SYSCOM-001/RISKS.md` | Risques de la mission |
| `missions/MISSION-2026-05-19-SYSCOM-001/DELIVERABLES.md` | Livrables attendus (18 livrables) |
| `missions/MISSION-2026-05-19-SYSCOM-001/VALIDATIONS.md` | Journal de validation |
| `missions/MISSION-2026-05-19-SYSCOM-001/final_report.md` | Rapport final (EN COURS) |

---

## 👥 AGENTS

| Fichier | Synthèse |
|---------|----------|
| `agents/ariane/_current_state.md` | **NOUVEAU** — État courant Ariane PM/UX |
| `agents/vulcain/_current_state.md` | **NOUVEAU** — État courant Vulcain Full Stack |
| `agents/argus/_current_state.md` | **NOUVEAU** — État courant Argus QA |
| `agents/atlas/_current_state.md` | **NOUVEAU** — État courant Atlas DevOps |
| `agents/devops/AGENTS.md` | Agents DevOps (ancien) |
| `agents/full-stack/AGENTS.md` | Agents Full Stack (ancien) |
| `agents/product-manager/AGENTS.md` | Agents PM (ancien) |
| `agents/qa/AGENTS.md` | Agents QA (ancien) |
| `agents/AGENTS_TEMPLATE.md` | Template agent |

---

## 💾 MEMORY CURATED

| Fichier | Synthèse |
|---------|----------|
| `memory/curated/LESSONS_LEARNED_MANDATORY.md` | **MIS À JOUR** — Learning Loop Records obligatoires + clôture Memory Kernel v1 |
| `memory/curated/known_errors.md` | **NOUVEAU** — Erreurs connues + fix (12 erreurs) |
| `memory/curated/stable_config.md` | **NOUVEAU** — Configurations stables validées |
| `memory/curated/agent_contracts.md` | **NOUVEAU** — Contrats inter-agents |
| `memory/2026-05-13.md` | Journal quotidien (ancien) |

---

## 🧠 MEMORY KERNEL v1 (EN PRODUCTION — 2026-05-26)

| Fichier | Synthèse |
|---------|----------|
| `memory/curated/negative_memory.md` | **NOUVEAU** — Mémoire négative testable : interdits, anti-patterns et tests associés |
| `memory/curated/LESSONS_LEARNED_MANDATORY.md` | **MIS À JOUR** — Learning Loop Records obligatoires + clôture Memory Kernel v1 |
| `scripts/hermes_memory_router.py` | **NOUVEAU** — Routeur canonique d'écriture mémoire : dry-run, verrou fcntl, écriture atomique, nettoyage content-file |
| `scripts/hermes_memory_healthcheck.py` | **MIS À JOUR** — Healthcheck mémoire enrichi : Memory Kernel v1 + correction chemin SOUL Orchestrateur |
| `scripts/hermes_lessons_healthcheck.sh` | Healthcheck Learning Loop / Discord guard |
| `healthchecks/model_resource_status.example.json` | **NOUVEAU** — Template statut probe dispo/quotas modèles. Schema JSON par ressource (MiniMax, Codex, MiMo, OpenRouter). P34. |

---

## 📒 LEDGERS

|| Fichier | Synthèse |
|---------|----------|
| `LEDGER_2026-05-19.md` | Ledger session — Architecture mémoire hybride |
| `LEDGER_2026-05-18.md` | Ledger session — Multi-agent Discord |
| `LEDGER_2026-05-16.md` | Ledger session — Outils |
| `LEDGER_2026-05-15.md` | Ledger session — Migration VPS |
| `LEDGER_2026-05-13.md` | Ledger session — Setup initial |
| `LEDGER_2026-05-27_PROCESS_DIAG.md` | **MIS À JOUR** — Audit conformite + VRF-004 cronjob alignment (6 jobs actifs) | `VRF-004-CRONJOB-ALIGN-20260527` |

---

## 📚 OPENVIKING (POC à venir)

| Fichier | Synthèse |
|---------|----------|
| `openviking_index_policy.md` | **À CRÉER** — Politique d'indexation POC |
| `skills/openviking_context_recall/` | **À CRÉER** — Skill recall sémantique |

---

## 🔒 SKILLS

| Skill | Rôle |
|-------|------|
| `skills/hermes-sysop-ledger/` | Framework LEDGER + exécution technique |
| `skills/hermes-doc-system/` | Documentation système vivante |
| `skills/hermes-sysop-config/` | Référence technique complète |
| `skills/context_hydration/` | **À CRÉER** — Hydratation contexte au boot |
| `skills/memory_curator/` | **À CRÉER** — Curation mémoire longue |
| `skills/openviking_context_recall/` | **À CRÉER** — Recall sémantique |

---

## 🛡️ GOUVERNANCE (depuis 2026-05-30)

| Fichier | Synthèse |
|---------|----------|
| `GOVERNANCE_MASTER_REGISTER.md` | **NOUVEAU** — Registre maître de gouvernance P0-P9, rules canonical, open reserves, do-not-reopen list, maintenance cadence |
| `HERMES_V015_UPGRADE_READINESS_PLAN.md` | **NOUVEAU** — Runbook upgrade v0.14.0→v0.15.0, STATUS NEEDS_INFO, validation Stéphane requise |
| `HERMES_V015_BLOCKER_NEXT_MOVE.md` | **BLOCKED / NEXT MOVE** — Diagnostic v0.15.x Docker multi-agent : s6-log lock, gateway.lock global, sources upstream, issue GitHub à ouvrir, prod migration interdite |
| `LEDGER_2026-05-30_P10_HERMES_RUNTIME_VERSION_AND_UPGRADE_READINESS.md` | **P10_VALIDÉ_AVEC_CORRECTIONS** — Preuve runtime v0.14.0 inside hermes-agent-1, 6 containers, image locale vs Docker Hub distant NON vérifié |
| `LEDGER_2026-05-30_P11_GOVERNANCE_REGISTER_P10_UPDATE.md` | **MIS À JOUR** — Intégration P10 dans registre maître |
| `GOVERNANCE_MAINTENANCE_RUNBOOK.md` | **NOUVEAU** — Runbook maintenance gouvernance légère (12 sections), checks read-only hebdomadaires |
| `LEDGER_2026-05-30_P12_GOVERNANCE_MAINTENANCE_RUNBOOK.md` | **P12_VALIDÉ** — Création runbook maintenance, vérifications 4/4 PASS, 0 runtime modifié |
| `LEDGER_2026-05-30_P13_CREATE_HERMES_VERSION_UPGRADE_SKILL.md` | **P13_VALIDÉ** — Skill hermes-version-upgrade créée, 17 sections, OC 8/8 |
| `HERMES_VERSION_UPGRADE_LOG.md` | **NOUVEAU** — Log structuré pour upgrades versions futures |

---

## 🗂️ ARCHIVES

| Fichier | Raison |
|---------|--------|
| `workspace/skills_backup_20260519_201541/` | Backup 87 skills — à intégrer ou archiver |
| `workspace/queues/` | Historique inbox/outbox agents — à curer |

---

## RÈGLES D'INDEX

1. Tout nouveau fichier `.md` dans `workspace/` → ajouter dans ce fichier
2. Tout fichier supprimé → retirer de ce fichier
3. Révision mensuelle pour nettoyer les obsolete references
4. Pas de secrets, tokens ou clés API dans les documents indexés

## Validations operationnelles

- VALIDATION_ARIANE_DISCORD_2026-05-24.md - validation live Ariane Discord post-restauration; supersede les diagnostics headless du 2026-05-24.

| `LEDGER_2026-06-06_P24_HERMES_V016_PROD_MIGRATION_RUNBOOK.md` | **NOUVEAU** — P24 Runbook migration PROD DOC_ONLY: preflight A-H, compose v016, rollback, gate phrase | `P24_RUNBOOK_20260606` |


| `LEDGER_2026-06-06_P24_1_PROD_RUNBOOK_SAFETY_FIX.md` | **P24.1** — Safety fix runbook: 6 corrections (PATH compose, UID/GID hardcodés, port 9119, docker rm différé, rollback docker start, backup no-loss check) | `P24_1_FIX_20260606` |
| `LEDGER_2026-06-06_P24_2_PROD_RUNBOOK_ACTIVE_COMPOSE_FIX.md` | **P24.2** — Correction critique: compose actif réel = `/docker/hermes/docker-compose.yml`; `/root/hermes/data/hermes-agent/docker-compose.yml` est un template non actif; rollback via `docker start` des containers préservés | `P24_2_ACTIVE_COMPOSE_FIX_20260606` |
| `LEDGER_2026-06-06_P24_3_MIGRATION_VERIFICATION.md` | **P24.3** — Vérification migration: image v0.16 dispo (9ad3b04ec916), 6 containers UP, compose `/docker/hermes/docker-compose.yml` actif, PATH runbook corrigé, backup gate BLOCKED (archive 10j) | `P24_3_MIGRATION_VERIF_20260606` |
| `LEDGER_2026-06-06_P24_4_BACKUP_GATE_VERIFICATION.md` | **P24.4** — Backup gate verification: archive DR May 27 = 10 jours >7j limite, BLOCKED_NEEDS_BACKUP. Intégrité archive VERIFIED OK. Script backup dispo: `hermes_full_data_archive.sh --force` | `P24_4_BACKUP_GATE_20260606` |
| `LEDGER_2026-06-06_P24_5_FRESH_DR_ARCHIVE.md` | **P24.5** — Fresh DR archive created: SHA256=327db44b0d32a35b8091901d219e6de606ae6353b347bc7bdc05c9bc3cef72b9, Verify OK, BACKUP_GATE_PASS_DR_ARCHIVE. Script patché: `--ignore-failed-read` (race condition) | `P24_5_BACKUP_PASS_20260606` |
| `LEDGER_2026-06-07_P26_USER_MD_COMPACTION.md` | **P26** — Compaction USER.md sub-agents (Ariane/Vulcain/Argus/Atlas) | `P26_USER_COMPACT_20260607` |
| `LEDGER_2026-06-07_P27_HEALTHCHECK_REMAINING_FIXES.md` | **P27** — Corrections healthcheck P27 (Learning Loop + Discord Guard restaurés) | `P27_HC_FIX_20260607` |
| `LEDGER_2026-06-07_P28_WARNINGS_AND_LATENCY_TRIAGE.md` | **P28** — Diagnostic lenteur + triage warnings (7→3) + patches healthcheck | `P28_LATENCY_20260607` |
| `LEDGER_2026-06-07_P33_MODEL_RESOURCE_CARDS.md` | **P33** — Fiches ressources modèles IA (MiniMax, Codex, MiMo, OpenRouter) + table centrale | `P33_MODEL_RESOURCE_CARDS` |
| `LEDGER_2026-06-07_P36_1_GOVERNANCE_RAILS_FALSE_POSITIVES_FIX.md` | **P36.1** — Correction faux positifs DR Git + healthcheck dans governance_rails_check.py | `P36.1_VALIDÉ` |
| `governance_rails_check.py` | **NOUVEAU** — Script auto-contrôle gouvernance : 9 sections, dry-run + write |
| `runbooks/governance_rails_autocontrol.md` | **NOUVEAU** — Runbook auto-contrôle gouvernance : quand lancer, lecture JSON, stop conditions |
| `healthchecks/governance_rails_status.example.json` | **NOUVEAU** — Template JSON statut gouvernance rails |
| `healthchecks/governance_rails_status.json` | **NOUVEAU** — Résultat exécution gouvernance rails (PASS_WITH_WARNINGS) |
| `LEDGER_2026-06-07_P36_GOVERNANCE_RAILS_AUTOCONTROL.md` | **P36** — Ledger gouvernance rails auto-control : 9 sections, script Python, runbook, résultats | `P36_GOVERNANCE_RAILS_20260607` |
| `LEDGER_2026-06-07_P35_MIMO_CANARY_LEVEL_1.md` | **P35** — Canary MiMo Niveau 1 : HTTP 200, 9 modèles, CANARY_LEVEL_1_PASS (retry après HTTP 401) | `P35_MIMO_CANARY_L1_PASS` |
| `LEDGER_2026-06-07_P29_DOC_ALIGNMENT_V016_FINAL.md` | **P29** — Alignement documentaire v0.16 final (17 docs, 6 STALE→OK, 4 HISTORICAL) | `P29_DOC_ALIGN_20260607` |
| `HERMES_V016_CORRECTIFS_RAPPORT.md` | **MIS À JOUR** — C-01-C-10 statuses actualisés post-v0.16 | `V016_CORRECTIFS_20260607` |
| `LEDGER_2026-06-07_P31_MODEL_ROUTING_STRATEGY.md` | **P31** — Stratégie routage IA post-v0.16: M2.7/M3/Codex/OpenRouter/MiMo, matrice 20 tâches, plan canary Xiaomi/MiMo | `P31_MODEL_ROUTING_20260607` |
