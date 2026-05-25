# PASSATION CODEX — Réparation Hermes Discord, Skills et Learning Loop

**Date de passation :** 2026-05-25  
**Responsable humain :** Stéphane  
**Cible :** Codex, reprise contrôlée de la réparation Hermes / Discord / skills  
**Statut global :** `PARTIEL — architecture d’apprentissage installée, mais Discord runtime encore à corriger`

---

## 0. Résumé exécutif

Hermes a été amélioré pour apprendre durablement de ses erreurs via une logique conforme à la philosophie Hermes / Nous Agent IA :

```text
Incident → Learning Loop Record → Skill update → Mémoire curée → Lint/Test → Healthcheck → Révision
```

L’architecture cible est en place partiellement :

- skill mère existante trouvée : `hermes-audit-remediation-learning-loop.md` ;
- skill spécialisée créée : `hermes-discord-communication-guard.md` ;
- mémoire curée créée : `LESSONS_LEARNED_MANDATORY.md` ;
- linter payload Discord créé côté workspace ;
- healthcheck lessons créé côté workspace ;
- patch minimal ajouté dans les SOUL.md des 5 agents ;
- fixtures lint annoncées OK ;
- **blocage restant** : le dossier canonique `healthchecks/` est `root:root`, donc Hermes uid `10000` ne peut pas générer `/opt/data/workspace/healthchecks/lessons_latest.md`.

Par ailleurs, le problème Discord runtime persiste :

- Hermes default continue potentiellement à réagir aux messages Discord ;
- `PID 6` ou `PID 7` a conservé un environnement runtime stale ;
- `/opt/data/config.yaml` contient encore `discord.reactions: true` ;
- il faut vérifier depuis l’hôte Docker si `Config.Env` contient encore `DISCORD_REACTIONS=true` ou le canal Ariane dans `DISCORD_ALLOWED_CHANNELS`.

**Codex ne doit pas envoyer de message Discord réel tant que les guards et le healthcheck ne sont pas verts.**

---

## 1. Objectif de Codex

Codex doit reprendre la réparation proprement, sans bricolage Discord en live.

### Objectif principal

Stabiliser la communication Discord Hermes multi-agents et rendre l’apprentissage permanent vraiment vérifiable.

### Objectifs secondaires

1. Vérifier l’état réel des fichiers installés.
2. Corriger les permissions du dossier healthcheck canonique.
3. Valider le healthcheck lessons au bon chemin.
4. Auditer et corriger les réactions Discord persistantes.
5. Vérifier que les SOUL.md référencent correctement la skill Discord guard.
6. Vérifier que le linter Discord empêche les erreurs déjà observées.
7. Proposer uniquement des corrections avant application, sauf validation explicite de Stéphane.

---

## 2. Règles absolues pour Codex

```text
NE PAS envoyer de message Discord réel.
NE PAS tester Discord sans validation humaine.
NE PAS redémarrer de gateway sans validation.
NE PAS kill PID 6 / PID 7 / PID 1 sans validation.
NE PAS modifier .env sans validation.
NE PAS modifier config.yaml sans validation.
NE PAS afficher de token ou secret.
NE PAS mélanger OpenClaw et Hermes.
NE PAS créer une nouvelle skill mère si hermes-audit-remediation-learning-loop existe déjà.
NE PAS contourner healthchecks/ par healthchecks_lessons_latest.md comme chemin final.
```

Codex doit travailler en mode :

```text
audit → preuve → proposition → validation humaine → exécution limitée → vérification
```

Pas de “j’ai compris, j’applique tout”. On a déjà vu le film, la fin est idiote.

---

## 3. Architecture Hermes concernée

### Agents Hermes

| Agent | Rôle | Profil | Modèle annoncé | Canal Discord |
|---|---|---|---|---|
| Hermes | Orchestrateur | `default` | MiniMax 2.7 | `#hermes-orchestrateur` |
| Ariane | PM/UX | `hermes-ariane` | `openrouter/owl-alpha` | `#pm-ux-ariane` |
| Vulcain | Full Stack | `hermes-vulcain` | `openrouter/owl-alpha` | `#fullstack-vulcain` |
| Argus | QA | `hermes-argus` | `poolside/laguna-m.1:free` | `#qa-argus` |
| Atlas | DevOps | `hermes-atlas` | `nvidia/nemotron-3-super-120b-a12b:free` | `#devops-atlas` |

### IDs connus

| Élément | ID |
|---|---:|
| Ariane Bot/User ID | `1505112142792097872` |
| Canal `#pm-ux-ariane` | `1505129251232546858` |
| Canal `#hermes-orchestrateur` | vérifier dans `discord_inventory.md` |

**Règle critique :**

```text
Bot/User ID ≠ Channel ID
Mention Ariane = <@1505112142792097872>
Channel Ariane = 1505129251232546858
```

---

## 4. Règles Discord attendues

### Format obligatoire Hermes → agent

```text
<@BOT_USER_ID>
MISSION-ID: MISSION-YYYY-MM-DD-XXX
TASK-ID: TASK-YYYY-MM-DD-XXX
SOURCE: Hermes
TARGET: Agent
OBJECTIF: ...
CONTRAINTES:
- ...
RÉPONSE ATTENDUE:
- Statut final : DONE / BLOCKED / NEEDS_VALIDATION / RISK_DETECTED
```

Avec payload Discord :

```json
{
  "channel_id": "1505129251232546858",
  "content": "<@1505112142792097872>\nMISSION-ID: ...\nTASK-ID: ...",
  "allowed_mentions": {
    "users": ["1505112142792097872"]
  }
}
```

### Interdictions absolues Discord

- Pas de `@Ariane` textuel.
- Pas de Channel ID utilisé comme mention.
- Pas de `thread_id` sans validation explicite.
- Pas d’ACK texte : `Roger`, `acknowledged`, `✅`, `🟢`, `👍`, `✓`.
- Pas de traces outils : `send_message`, `skill_view`, `search_files`, `read_file`, `terminal`, `tool_call`, `exit_code`, `Traceback`, `DEBUG`, `Result:`, `Output:`.
- Pas de message sans `MISSION-ID` + `TASK-ID` en mode outbound mission.
- Pas de test Discord réel sans validation humaine.

---

## 5. Incidents déjà appris

Le fichier `LESSONS_LEARNED_MANDATORY.md` doit contenir au minimum ces 6 Learning Loop Records :

1. `Discord tool trace leak`  
   Hermes a envoyé dans Discord des traces internes (`send_message`, `skill_view`, `terminal`, etc.).

2. `Bad mention format`  
   Hermes a utilisé des mentions textuelles ou confondu Bot/User ID et Channel ID.

3. `OpenClaw/Hermes confusion`  
   Hermes a cherché dans des docs OpenClaw pour un problème Hermes multi-agents Discord.

4. `ACK/ping-pong agents`  
   Hermes et les agents ont généré une boucle d’ACK / Roger / emoji.

5. `thread_id non validé`  
   Hermes a proposé ou utilisé `thread_id` sans validation du thread parent.

6. `PID/ENV stale Docker`  
   PID 6/PID 7 a gardé `DISCORD_REACTIONS=true` et des canaux stale en mémoire après modification `.env`.

---

## 6. État réel observé avant passation

### État learning loop

| Élément | État |
|---|---|
| `hermes-discord-communication-guard.md` | présent, ~4.4K, OK annoncé |
| `hermes-audit-remediation-learning-loop.md` | présent, ~12K, patch Discord annoncé OK |
| `LESSONS_LEARNED_MANDATORY.md` | présent, ~8.1K, OK annoncé |
| `hermes_discord_payload_lint.py` | présent dans `/opt/data/workspace/scripts/`, exécutable, py_compile OK annoncé |
| `hermes_lessons_healthcheck.sh` | présent dans `/opt/data/workspace/scripts/`, exécutable, bash -n OK annoncé |
| `/usr/local/bin/*` | absent, permission denied, ne pas considérer comme chemin canonique |
| `SOUL.md` des 5 agents | référence skill présente, annoncé OK |
| `healthchecks/lessons_latest.md` | absent à cause permissions root |

### Problème healthcheck restant

```text
/opt/data/workspace/healthchecks/
owner = root:root
mode = 755
Hermes uid = 10000
=> Hermes ne peut pas écrire lessons_latest.md
```

Chemin final obligatoire :

```text
/opt/data/workspace/healthchecks/lessons_latest.md
```

Chemin fallback à ne pas valider comme final :

```text
/opt/data/workspace/healthchecks_lessons_latest.md
```

---

## 7. État Discord runtime à corriger

### Symptôme

Les agents réagissent encore aux messages Discord. Hermes default poste ou réagit dans les canaux agents, notamment `#pm-ux-ariane`.

### Diagnostic antérieur

Deux processus ont été observés dans le canal Ariane :

| PID | Process | Profil | Problème |
|---:|---|---|---|
| 7 ou 6 | Hermes default | `/opt/data` ou `/opt/hermes` selon log | `DISCORD_REACTIONS=true`, canal Ariane dans env runtime |
| 23760 | Ariane | `hermes-ariane` | répond aux messages parasites Hermes |

### Config fichier observée

`/opt/data/.env` annoncé correct :

```text
DISCORD_REACTIONS=false
Canal Ariane absent de DISCORD_ALLOWED_CHANNELS
```

`/opt/data/config.yaml` observé stale :

```yaml
discord:
  free_response_channels: '1505129245733687347'
  allowed_channels: ''
  reactions: true
```

La ligne importante :

```yaml
reactions: true
```

Elle doit probablement devenir :

```yaml
reactions: false
```

Mais uniquement après backup et validation.

### Docker env encore inconnu

Docker n’est pas accessible depuis l’intérieur du container. Il faut vérifier depuis l’hôte VPS :

```bash
docker inspect hermes-agent-1 --format '{{range .Config.Env}}{{println .}}{{end}}' \
| sort \
| grep -E "DISCORD_REACTIONS|DISCORD_ALLOWED_CHANNELS|DISCORD_FREE_RESPONSE_CHANNELS|1505129251232546858" || true
```

Si cette commande retourne encore :

```text
DISCORD_REACTIONS=true
```

ou :

```text
1505129251232546858
```

alors la source Docker/Hostinger est stale. Un simple restart risque de réinjecter le poison.

---

## 8. Plan d’action recommandé pour Codex

### Phase 1 — Stabiliser le healthcheck lessons

1. Depuis l’hôte/root, corriger permissions :

```bash
docker exec -u 0 hermes-agent-1 sh -lc '
mkdir -p /opt/data/workspace/healthchecks &&
chown -R 10000:10000 /opt/data/workspace/healthchecks &&
chmod 755 /opt/data/workspace/healthchecks &&
ls -ld /opt/data/workspace/healthchecks
'
```

2. Relancer :

```bash
docker exec -u 10000:10000 hermes-agent-1 sh -lc '
bash /opt/data/workspace/scripts/hermes_lessons_healthcheck.sh &&
ls -lah /opt/data/workspace/healthchecks/lessons_latest.md
'
```

3. Vérifier que `lessons_latest.md` est généré au bon chemin.

### Phase 2 — Vérifier Docker env côté hôte

```bash
docker inspect hermes-agent-1 --format '{{json .HostConfig.RestartPolicy}}'

docker inspect hermes-agent-1 --format '{{json .Config.Entrypoint}} {{json .Config.Cmd}}'

docker inspect hermes-agent-1 --format '{{range .Config.Env}}{{println .}}{{end}}' \
| sort \
| grep -E "DISCORD_REACTIONS|DISCORD_ALLOWED_CHANNELS|DISCORD_FREE_RESPONSE_CHANNELS|1505129251232546858|HERMES|PROFILE" || true
```

### Phase 3 — Décider correction runtime Discord

Décision selon résultats :

| Résultat | Décision |
|---|---|
| Docker env contient stale values | `DOCKER_ENV_STALE` : corriger config Hostinger/container avant restart |
| Docker env clean mais PID runtime stale | restart contrôlé possible après backup |
| config.yaml contient `reactions: true` | proposer patch `reactions: false` avec backup |
| source inconnue | stop, diagnostic supplémentaire |

### Phase 4 — Ne tester Discord qu’après healthcheck vert

Quand seulement tout est vert :

1. dry-run payload ;
2. lint `outbound_mission` ;
3. validation Stéphane ;
4. un seul envoi Discord réel ;
5. silence ;
6. lecture logs.

---

## 9. Critères d’acceptation

### Learning loop validée

- `lessons_latest.md` existe au chemin canonique.
- Healthcheck indique OK.
- Les 8 fixtures lint passent.
- Les 5 SOUL.md référencent la skill.
- Aucun SOUL.md n’utilise OpenClaw comme source Discord Hermes.

### Discord reactions corrigées

- Docker Config.Env ne contient pas `DISCORD_REACTIONS=true`.
- Docker Config.Env ne contient pas le canal Ariane dans `DISCORD_ALLOWED_CHANNELS` du default.
- `/opt/data/.env` contient `DISCORD_REACTIONS=false`.
- `/opt/data/config.yaml` contient `discord.reactions: false` si validé.
- Après restart contrôlé, le PID runtime contient `DISCORD_REACTIONS=false`.
- Hermes default ne réagit plus dans les canaux agents.

### Communication Ariane validée

- Message test validé par linter.
- Envoi unique.
- Mention numérique Ariane correcte : `<@1505112142792097872>`.
- `allowed_mentions.users = ["1505112142792097872"]`.
- Canal correct : `1505129251232546858`.
- Pas d’ACK de suivi.
- Ariane répond seulement à la mission.

---

## 10. Décisions interdites à Codex sans accord Stéphane

```text
Modifier .env
Modifier config.yaml
Redémarrer hermes-agent-1
Tuer PID 6 / PID 7 / PID 1
Envoyer message Discord
Lancer test Discord
Afficher secrets/tokens
Changer les modèles agents
Écraser la skill mère
Supprimer des backups
Changer le chemin canonique healthcheck
```

---

## 11. Prompt initial à donner à Codex

Voir `05_PROMPTS_PRETS_A_COLLER.md`.
