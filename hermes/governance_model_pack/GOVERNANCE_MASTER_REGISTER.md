# Governance Master Register — Hermes

> **Statut :** ACTIVE — Point d'entrée officiel pour les audits de gouvernance
> **Version :** 1.8
> **Date :** 2026-06-07
> **Scope :** Infrastructure, skills, docs, runtime classification, Discord anti-bruit, model resource governance + P32.1 MiMo Premium Classification + P33 Resource Cards + P34 Availability Probe + P35 MiMo Canary + P36 Governance Rails Auto-Control + P37 Live Counters + P37.1 Live Counters Fix + P37.2 Counter Key Context Fix
> **Global_status :** OPÉRATIONNEL — v0.16 PROD_ACTIVE, P11 à P36 complétés
> **Last verified by :** Hermes (P0-P36 audit cycles)
> **Runtime caveat :** v0.16.0 mono-container s6 (hermes-v016-prod-s6) — v0.14 containers préservés pour rollback

---

## Phase Summary P0-P9

| Phase | Objectif | Décision | Evidence ledger | Réserve |
|-------|----------|----------|----------------|---------|
| P0 | Freeze risky features | P0_VALIDÉ | `LEDGER_2026-05-29_P0_FREEZE_RISKY_ACTIVATIONS.md` | Aucune |
| P1 | Docs/runtime alignment | P1_VALIDÉ_AVEC_RÉSERVES | `LEDGER_2026-05-29_P1_DOCS_RUNTIME_ALIGNMENT.md` | v0.15 runtime non confirmé |
| P2 | Cron registry créé | P2_VALIDÉ + correction | `LEDGER_2026-05-29_P2_CRON_REGISTRY.md` + addendum Codex | Close |
| P3 | Cron registry durable | P3_VALIDÉ | `LEDGER_2026-05-29_P3_CRON_REGISTRY_AUTOMATION_AND_SKILL_HARDENING.md` | Aucune |
| P4 | Skills governance | P4_VALIDÉ_AVEC_RÉSERVES | `LEDGER_2026-05-29_P4_SKILLS_GOVERNANCE_HARDENING.md` | Aucune |
| P5 | OC priority 1 adoption | P5_VALIDÉ | `LEDGER_2026-05-29_P5_SKILL_HEADER_ADOPTION_AND_DOC_WORKFLOW_CLARIFICATION.md` | Aucune |
| P6 | OC priority 2 skills | P6_VALIDÉ | `LEDGER_2026-05-29_P6_SKILL_HEADER_PRIORITY2_ADOPTION.md` | Aucune |
| P7 | Behavioral audit | P7_VALIDÉ_AVEC_RÉSERVES → addendum Codex | `LEDGER_2026-05-30_P7_BEHAVIORAL_CONFORMANCE_AUDIT.md` | Cron cross-env — levé |
| P8 | Ambiguities cleanup | P8_VALIDÉ | `LEDGER_2026-05-30_P8_DOC_RUNTIME_AMBIGUITY_CLEANUP.md` | Close |
| P9 | Clôture globale | P9_VALIDÉ | `LEDGER_2026-05-30_P9_GOVERNANCE_MASTER_REGISTER.md` | Aucune |
| P10 | Runtime Hermes version + upgrade readiness | P10_VALIDÉ_AVEC_CORRECTIONS | `LEDGER_2026-05-30_P10_HERMES_RUNTIME_VERSION_AND_UPGRADE_READINESS.md` | Réserve v0.15 maintenue |
| P11 | Governance Master Register update after P10 | P11_VALIDÉ | `LEDGER_2026-05-30_P11_GOVERNANCE_REGISTER_P10_UPDATE.md` | Aucune |
| P12 | Governance Maintenance Runbook | P12_VALIDÉ | `LEDGER_2026-05-30_P12_GOVERNANCE_MAINTENANCE_RUNBOOK.md` | Aucune |
| P13 | Hermes Version Upgrade skill | P13_VALIDÉ | `LEDGER_2026-05-30_P13_CREATE_HERMES_VERSION_UPGRADE_SKILL.md` | Aucune |
| P14 | Hermes v0.15 Upgrade Preflight Gate | P14_VALIDÉ | `LEDGER_2026-05-30_P14_HERMES_V015_UPGRADE_PREFLIGHT_GATE.md` | Aucune |
| P15a | Upgrade abort/recovery v0.15 | P15_RECOVERY_VALIDATED | `LEDGER_2026-05-30_P15_HERMES_UPGRADE_ABORT_RECOVERY.md` | Aucune |
| P15b | Normalisation profils sub-agents Discord | P15_VALIDÉ | `LEDGER_2026-05-30_P15_PROFILS_SUB_AGENTS_NORMALISATION.md` | Aucune |
| P16 | Gel upgrade v0.15 | P16_VALIDÉ | `LEDGER_2026-05-30_P16_UPGRADE_V015_FREEZE.md` | Aucune |

---

| P32 | Active Model Resource Governance | P32_VALIDÉ | `LEDGER_2026-06-07_P32_ACTIVE_MODEL_RESOURCE_GOVERNANCE.md` | Aucune |
| P32.1 | MiMo Premium Classification Fix | P32.1_VALIDÉ | `LEDGER_2026-06-07_P32_1_MIMO_PREMIUM_CLASSIFICATION_FIX.md` | Aucune |
| P33 | Model Resource Cards | P33_VALIDÉ | `LEDGER_2026-06-07_P33_MODEL_RESOURCE_CARDS.md` | Aucune |
| P34 | Model Availability Quota Probe | P34_VALIDÉ | `LEDGER_2026-06-07_P34_MODEL_AVAILABILITY_QUOTA_PROBE.md` | Aucune (canary MiMo en attente Stéphane) |
| P35 | MiMo Canary Niveau 1 | P35_CANARY_LEVEL_1_PASS | `LEDGER_2026-06-07_P35_MIMO_CANARY_LEVEL_1.md` | Niveau 1 PASS — 9 modèles découverts ; Niveau 2 en attente validation humaine |
| P36 | Governance Rails Auto-Control | P36_VALIDÉ | `LEDGER_2026-06-07_P36_GOVERNANCE_RAILS_AUTOCONTROL.md` | Script + runbook créés ; 2 HIGH actions en attente (DR Git + healthcheck) |
| P36.1 | Governance Rails False Positives Fix | P36.1_VALIDÉ | `LEDGER_2026-06-07_P36_1_GOVERNANCE_RAILS_FALSE_POSITIVES_FIX.md` | Corrections appliquées → PASS 0/0/0 |
| P37 | Model Resource Live Counters | P37_VALIDÉ | `LEDGER_2026-06-07_P37_MODEL_RESOURCE_LIVE_COUNTERS.md` | Script probe + runbook + JSON status créés. Routing rules 4 catégories. Auto vs manual counters. MiMo L1 PASS only. |
| P37.1 | Live Counters DR Git + MiMo Fix | P37.1_VALIDÉ | `LEDGER_2026-06-07_P37_1_LIVE_COUNTERS_FIX.md` | DR Git → DR_PUSH_PENDING (hostname github.com-hermes-dr non résolu). Corrigé par P37.3 → OK_WITH_SUBCONTEXT_LIMITATION (canonique host/root PUSH_OK, subcontext hermes AUTH_FAILED). MiMo days_left_in_month → automatic (integer 23). monthly_quota → MANUAL_REQUIRED. Governance rails PASS (0/0/0). |
| P37.2 | Counter Key Context Fix | P37.2_VALIDÉ | `LEDGER_2026-06-07_P37_2_COUNTER_KEY_CONTEXT_FIX.md` | Correction détection clés: check_key_presence() vérifie ENV puis .env. credentials block avec key_source (ENV/ENV_FILE/NOT_FOUND). MiMo CANARY_LEVEL_2_PASS. MANUAL_REQUIRED avec reason explicite. Aucun secret exposé. Governance rails PASS (0/0/0). |
| P37.3 | DR Git Push SSH Classification | P37.3_VALIDÉ | `LEDGER_2026-06-07_P37_3_DR_GIT_PUSH_CONTEXT_FIX.md` | Classification SSH DR Git: host/root canonique = PUSH_OK (dry-run Everything up-to-date), subcontext hermes = AUTH_FAILED. Overall = OK_WITH_SUBCONTEXT_LIMITATION. Action Stéphane = AUCUNE requise. Règle: ne pas ajouter clé hQR7Ik77... à GitHub — modèle host/root avec deploy key dédiée plus sûr. |
| P38 | Dynamic Agent Model Routing Alignment | P38_VALIDÉ | `LEDGER_2026-06-07_P38_DYNAMIC_AGENT_MODEL_ROUTING_ALIGNMENT.md` | 4 corrections CANARY_PENDING → CANARY_LEVEL_1_PASS (AGENTS_GOVERNANCE.md, MODEL_RESOURCE_GOVERNANCE.md, ai_model_routing.md, model_availability_quota_probe.md). Règle "agents do not own models" renforcée. Exemples routage par agent ajoutés (Hermes/Ariane/Vulcain/Argus/Atlas). Aucun secret exposé. Governance rails PASS (0/0/0). |
| P39 | MiMo Canary Level 2 (mimo-v2.5) | P39_VALIDÉ | `LEDGER_2026-06-07_P39_MIMO_CANARY_LEVEL_2.md` | Level 2 PASS (mimo-v2.5, 180 tokens, finish_reason=stop, content="Backup Git..."). CANARY_LEVEL_2_PASS. Coding/JSON INTERDIT. mimo-v2.5-pro FAIL (reasoning_only, finish_reason=length, 180 tokens insuffisant). |
| P39.2 | MiMo mimo-v2.5-pro Level 2 Retry | P39.2_VALIDÉ | `LEDGER_2026-06-07_P39_2_MIMO_PRO_LEVEL_2_RETRY.md` | mimo-v2.5-pro Level 2 PASS (500 tokens, 6.0s, finish_reason=stop, MIMO_LEVEL_2_OK). MiMo global → CANARY_LEVEL_2_PASS. 5 fichiers mis à jour (mimo.md, MODEL_RESOURCE_GOVERNANCE.md, AGENTS_GOVERNANCE.md, ai_model_routing.md, model_availability_quota_probe.md). |

## Current Source of Truth

| Outil / Document | Path | Commande / Usage |
|-----------------|------|-----------------|
| Skill header compliance checker | `/opt/data/workspace/scripts/check_skill_headers.py` | `python3 .../check_skill_headers.py` |
| Cron registry generator | `/opt/data/workspace/scripts/generate_cron_registry.py` | `python3 .../generate_cron_registry.py --dry-run` (host/container) |
| Cron registry JSON (canonique) | `/opt/data/workspace/healthchecks/cron_registry.json` | Schema 1.0, 5 jobs, `divergences_detected: 0` |
| Skill header standard | `/opt/data/workspace/SKILL_HEADER_STANDARD.md` | 8 champs obligatoires |
| Skills governance matrix | `/opt/data/workspace/SKILLS_GOVERNANCE_MATRIX.md` | 143 skills, 138 actifs, 5 archives |
| Current state WAL | `/opt/data/workspace/_current_state.md` | Dernier update 2026-05-29T07:01 |
| CHANGES_REQUIRED v0.15 | `/opt/data/workspace/CHANGES_REQUIRED_v0.15.0.md` | **WORKING DRAFT / HISTORICAL** — 0 feature active |
| v0.15 runtime status | `_current_state.md` ligne 32 | `v0.15.0 : DOC_ONLY / NON DÉPLOYÉE (2026-05-29)` |
| **Plan upgrade v0.15** | `/opt/data/workspace/HERMES_V015_UPGRADE_READINESS_PLAN.md` | **NEEDS_INFO** — runbook prêt, validation Stéphane requise |
| **Ledger P10 (runtime proof)** | `LEDGER_2026-05-30_P10_HERMES_RUNTIME_VERSION_AND_UPGRADE_READINESS.md` | Preuve runtime v0.14.0 inside hermes-agent-1 | |

---

## Rules Now Canonical

1. **Preuve runtime avant statut ACTIF** — toute claim `ACTIF` exige `generated_at` + commande/log/PID
2. **Ledger avant conclusion** — "not in ledger = not done"
3. **Discord silence réel** — zéro output, pas de marqueur `"---"`, pas d'emoji protocolaire
4. **Cron source of truth = host crontab** — `ssh root@187.77.161.196 "crontab -l"` — CRONJOBS LLM/APP = INACTIFS, OS CRON = source vérité
5. **Logs v0.16 primary** — `/opt/data/profiles/<profile>/logs/gateway.log` — ne pas utiliser `/opt/data/logs/gateways/` (legacy v0.14)
6. **Context chemins** — HOST root = `/root/hermes/data`, CONTAINER = `/opt/data`, vérifier avant diagnostic
5. **cron_registry.json = registre canonique** — cron_status.json = legacy WAK-only
6. **session_search Niveau 0** — ~20ms, gratuit, pré-check obligatoire
7. **OpenViking sans secrets** — pas de token GH, key SSH, Azerty2405 dans les fichiers
8. **WAK/current_state = guide contexte** — pas preuve runtime
9. **v0.15 features non activées** — sans validation humaine explicite (ntfy, OpenHands, Swarm, code-wiki, allow_any_attachment)
10. **Swarm = expérimental** — validation humaine obligatoire avant usage
11. **Docker socket absent = NON_VÉRIFIÉ** — pas "DOWN". Vérifier via SSH host.
12. **ACK texte = interdit** — ✅, 👍, roger, acknowledged, confirmé, etc. entre missions
13. **Operating Contract = obligatoire** — champs 8/8, propagation systématique

---

## Open Reserves

| Réserve | Contexte | Preuve | Prochaine action |
|---------|---------|--------|-----------------|
| **UPGRADE_V015_FROZEN** | Tentative upgrade avortée (hermes-agent-1 exit 137, P15 abort) — image avortée supprimée — runtime stable v0.14.0 — 6/6 containers UP — rollback restauré | `hermes --version` → v0.14.0 (2026.5.16) inside container ; rollback tag présent ; P15 abort ledger | Chantier v0.15 gelé — à reprendre avec plan dédié (disque, digest image, rollback, fenêtre maintenance, gate phrase) |

**Image locale vs tag distant Docker Hub :**
- Image locale déployée : `nousresearch/hermes-agent:latest` → v0.14.0 (2026.5.16)
- Tag distant Docker Hub `latest` : **NON VÉRIFIÉ** — impossible sans pull

**Aucune autre réserve ouverte.** P0-P16 closes. Chantier v0.15 gelé (UPGRADE_V015_FROZEN).
| **P17** | Lab v0.16 isolated (P22) — Gateway lock CORRIGÉ, s6-log collision CORRIGÉE | P17_LAB_PASS | `LEDGER_2026-06-06_P22_HERMES_V016_LAB_RUN.md` | 0 blocking issues |
| **P18** | Staging v0.16 isolated (P23) — STAGING_PASS, 0 blocking, mono-container viable | P18_STAGING_PASS | `LEDGER_2026-06-06_P23_HERMES_V016_STAGING_RUN.md` | Gateway lock CORRIGÉ, dashboard INSECURE works |
| **P24** | Prod migration runbook v0.16 (P24.2) — DOC_ONLY, PROD_MIGRATION_READY_AFTER_P24_2_FIX, gate phrase en attente | P24_2_RUNBOOK_READY | `LEDGER_2026-06-06_P24_2_PROD_RUNBOOK_ACTIVE_COMPOSE_FIX.md` | Gate phrase requise: GO PROD MIGRATION V016 EXECUTE — compose actif réel `/docker/hermes/docker-compose.yml`, template `/root/hermes/data/hermes-agent/docker-compose.yml` interdit comme rollback source |
| **P24.4** | Backup gate verification (P24.4) — Archive DR May 27 = 10 jours, BLOCKED_NEEDS_BACKUP | P24_4_BACKUP_GATE_BLOCKED | `LEDGER_2026-06-06_P24_4_BACKUP_GATE_VERIFICATION.md` | Archive DR trop ancienne (10j > 7j limite). Integrité VERIFIED OK. Script backup dispo: `hermes_full_data_archive.sh --force`. |
| **P24.5** | Fresh DR archive created (P24.5) — SHA256=327db44b0d32a35b8091901d219e6de606ae6353b347bc7bdc05c9bc3cef72b9, BACKUP_GATE_PASS_DR_ARCHIVE | P24_5_BACKUP_GATE_PASS | `LEDGER_2026-06-06_P24_5_FRESH_DR_ARCHIVE.md` | Archive fraîche20260606T084241Z. Verify OK. Script patché: `--ignore-failed-read` (race condition .skills_prompt_snapshot.json). |
| P25 | Prod migration v0.16 executed — mono-container s6, 5 gateways UP, dashboard public restored, rollback v0.14 containers preserved | P25_PROD_V016_STABLE_INITIAL | `LEDGER_2026-06-06_P25_HERMES_V016_PROD_MIGRATION_EXECUTION.md` | Do not remove old v0.14 containers until longer stabilization window accepted. |
| P26 | USER.md compaction sub-agents — Ariane/Vulcain/Argus/Atlas compacted | P26_VALIDÉ | `LEDGER_2026-06-07_P26_USER_MD_COMPACTION.md` | USER.md sub-agents sous 1,800 chars |
| P27 | Healthcheck P27 corrections — Learning Loop + Discord Guard restored | P27_VALIDÉ | `LEDGER_2026-06-07_P27_HEALTHCHECK_REMAINING_FIXES.md` | Skills restored, _current_state agents refresh |
| P28 | Warnings triage + latency diagnosis — 7→3 warnings | P28_VALIDÉ | `LEDGER_2026-06-07_P28_WARNINGS_AND_LATENCY_TRIAGE.md` | Healthcheck script patched, 3 warnings restants |
| P29 | Doc alignment v0.16 — 17 docs audited, 6 STALE → OK, 4 HISTORICAL | P29_VALIDÉ | `LEDGER_2026-06-07_P29_DOC_ALIGNMENT_V016_FINAL.md` | Critical=0, Warnings=0, DR Git clean |
| P30 | Latency audit post-v0.16 + v0.14 cleanup plan — C-01/C-02/C-04/C-05 validés, seuil compression 80K, threshold mis à jour | P30_VALIDÉ | `LEDGER_2026-06-07_P30_LATENCY_AUDIT_AND_V014_CLEANUP_PLAN.md` | Context drift = cause principale, v0.14 containers STOPPED, suppression J+2 |
| P31 | Stratégie routage IA post-v0.16 — M2.7/M3/Codex/OpenRouter/MiMo, matrice 20 tâches, Xiaomi/MiMo CANARY_PENDING | P31_DOC_ONLY | `LEDGER_2026-06-07_P31_MODEL_ROUTING_STRATEGY.md` | Aucune clé exposée, validation Stéphane requise |

---

## Do Not Reopen

Les sujets suivants sont **clôturés** — toute réouverture sans nouveau signal de Stéphane = violation de ce registre :

| Sujet | Preuve |
|-------|--------|
| P0 risky features freeze | `LEDGER_2026-05-29_P0_FREEZE_RISKY_ACTIVATIONS.md` — P0_VALIDÉ |
| Cron registry cross-env | P7 Addendum Codex — `generate_cron_registry.py --dry-run` OK host + container, 5 jobs, 0 divergence |
| Skill headers 6/6 non conformes | `check_skill_headers.py` — 6/6 OK, exit 0 |
| DOC/RUNTIME ambiguities (6 AMBIGUOUS P8) | `LEDGER_2026-05-30_P8_DOC_RUNTIME_AMBIGUITY_CLEANUP.md` — P8_VALIDÉ |
| DISCORD_REACTIONS historical incident | Identifié DOC_ONLY en P7 Phase 3 |
| Docker socket refused | MKV1 ledger `09d62c5` + _current_state.md |
| CHANGES_REQUIRED v0.15 = working draft | Header ligne 8-12 du fichier |
| Operating Contract gaps priority 1 | P5 ledger — P5_VALIDÉ |
| Operating Contract gaps priority 2 | P6 ledger — P6_VALIDÉ |
| Memory Kernel v1 production | `LEDGER_2026-05-26_MEMOIRE_REMÉDIATION.md` — commit `09d62c5` |
| **Docker Hub `latest` tag = v0.14** | **NE PAS AFFIRMER** — le tag distant Docker Hub n'a pas été vérifié. L'image locale déployée est v0.14.0 mais le digest distant `latest` n'est pas confirmé comme v0.14.0. Affirmer le contraire = hors périmètre. |
| **`generate_cron_registry` permission denied cross-env** | **CLOS** — P10 Addendum Codex : script OK host + container, divergences_detected=0. L'erreur `Permission denied` initiale a été résolue (pas de divergence). |
| **v0.15 feature activation** | **INTERDIT** sans validation humaine explicite — ntfy, OpenHands, Swarm, code-wiki, allow_any_attachment restent RUNTIME_DISABLED. Aucune activation implicite. |
| **v0.15 blockers résolus v0.16** | s6-log collision + gateway.lock global CORRIGÉS en v0.16 (P22/P23 validés). Ne pas rouvrir. |
| **Cron LLM actifs vs OS cron** | LLM cronjobs = INACTIFS (pausés). OS cron root = source vérité. |
| **v0.16 PROD active** | mono-container s6 hermes-v016-prod-s6. Ne pas présenter v0.14 comme actif. |

---

## Verification Commands

```bash
# Skill headers compliance (6 skills critiques)
python3 /opt/data/workspace/scripts/check_skill_headers.py
# → attendu : 6/6 OK, exit 0

# Cron registry coherence (host)
python3 /root/hermes/data/workspace/scripts/generate_cron_registry.py --dry-run
# → attendu : 5 jobs, 0 divergence

# Cron registry coherence (container)
python3 /opt/data/workspace/scripts/generate_cron_registry.py --dry-run
# → attendu : 5 jobs, 0 divergence

# Hermes runtime version (inside container)
docker exec hermes-v016-prod-s6 /opt/hermes/.venv/bin/hermes --version
# → attendu : Hermes Agent v0.16.0 (v2026.6.5)

# CHANGES_REQUIRED v0.15 status
grep -n "WORKING DRAFT\|HISTORICAL\| aucune.*active" /opt/data/workspace/CHANGES_REQUIRED_v0.15.0.md | head -5
# → attendu : STATUS WORKING DRAFT, 0 feature active

# Skills governance matrix
grep -n "143\|138\|5 archives\|hermes-sysop-ledger\|hermes-doc-system" /opt/data/workspace/SKILLS_GOVERNANCE_MATRIX.md | head -10
# → attendu : inventaire complet

# Current state WAL (last update)
grep -n "<last_updated\|v0.15\|DOC_ONLY" /opt/data/workspace/_current_state.md | head -5
# → attendu : timestamp récent, v0.15 DOC_ONLY

# Shared knowledge (HISTORICAL markers)
grep -n "HISTORICAL" /opt/data/workspace/SHARED_KNOWLEDGE.md
# → attendu : 2 occurrences (lignes 220, 236)
```

---

## Maintenance Cadence

| Trigger | Action |
|---------|--------|
| Every week | `check_skill_headers.py` + `generate_cron_registry.py --dry-run` |
| After every Hermes runtime upgrade | Rebuild CHANGES_REQUIRED status + vérifier skills OC headers |
| After every new skill created | Header compliance check (`check_skill_headers.py`) |
| After Discord/gateway config change | P7 Discord anti-bruit audit pattern check |
| After cron install/remove/modify | `generate_cron_registry.py --write` + vérifier `cron_registry.json` |
| After major mission closure | Curation memory + update `_current_state.md` |
| Cycle Pair→N closure | Créer registre maître synthétique (cette leçon) |

---

## CHANGES_REQUIRED v0.15 — Statut Officiel

```
STATUS: WORKING DRAFT / HISTORICAL
 Aucune des 7 sections n'a été exécutée.
Aucune feature listée (ntfy, allow_any_attachment, OpenHands, code-wiki, Swarm) n'est active.
Ce fichier est un plan de travail, pas une trace d'exécution.
```

**Absolument aucune activation implicite.** Swarm = validation humaine obligatoire.

---

## Learnings From Pair→N Audit Cycle

1. **Anti-hallucination** — toute claim sans `generated_at` ou preuve = AMBIGUOUS
2. **Cross-context debugging** — script qui marche dans 1 contexte (host) ≠ erreur totale ; vérifier container aussi
3. **Correction Codex autonome** — Codex peut lever des réserves sans intervention humaine ; merger le addendum
4. **Cycle closure** — quand Pair→N cycle clot, centraliser dans un registre maître pour éviter réouverture
5. **Skill header OC propagation** — OC headers sont un contrat, pas une case à cocher ; Monitorer compliance

---

*Ce registre est le point d'entrée officiel. Mis à jour après chaque cycle Pair→N.*
*Ledger de référence : `LEDGER_2026-05-30_P9_GOVERNANCE_MASTER_REGISTER.md`*
