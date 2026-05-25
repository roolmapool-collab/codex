---
name: minimax-token-plan
description: "MiniMax Token Plan Plus operational skill. M2.7 text/coding, MCP web_search+understand_image, Image T2I/I2I, Speech TTS, Voice clone/design/management, Music, File management. Video: INTERDIT. Heavy technical recipes in runbooks."
version: 1.1.1
author: Hermes Orchestrateur
license: MIT
platforms: [linux]
compatibility: "MiniMax Token Plan Plus. Token managed by Hermes auth (NEVER read/displayed/copied)."
prerequisites:
  commands: [curl, python3]
metadata:
  hermes:
    tags: [minimax, token-plan, tts, voice-clone, image-generation, music-generation, mcp, multi-agent]
    category: llm-providers
---

# minimax-token-plan

MiniMax Token Plan Plus — skill opérationnelle pour Hermes Orchestrateur.
Recipes techniques détaillées : voir runbooks.

## Plan Plus — Capacités et limites

| Paramètre | Valeur |
|---|---|
| Prix | 20$/mois |
| Model requests | 4 500 / 5 heures |
| Weekly allowance | 10× quota 5 heures (45 000 / semaine) |
| Modèle principal | MiniMax-M2.7 |
| TPS normal | ~50 |
| TPS off-peak | ~100 |
| OpenClaw agents | 1 à 2 max |
| TTS Audio | Speech 2.8 : 4 000 caractères / jour (Token Plan Plus) — quota quotidien |

**Budget rule :** STOP après 2 erreurs consécutives → rapporter à Stéphane.

---

## Quick Decision Table

| Je veux faire… | Utiliser… | Où stocker |
|---|---|---|
| Coding / raisonnement / orchestration | POST /v1/chat/completions (M2.7) | — |
| Recherche web vérifiable | MCP web_search | workspace/missions/<ID>/research/ |
| Analyse d'image | MCP understand_image | — |
| Générer une image | POST /v1/image_generation | workspace/missions/<ID>/assets/ |
| Transformer une image | POST /v1/image_generation + subject_reference | workspace/missions/<ID>/assets/ |
| Texte → audio court (<10k chars) | POST /v1/t2a_v2 | workspace/missions/<ID>/assets/audio/ |
| Texte → audio long | POST /v1/t2a_async_v2 + GET query | workspace/missions/<ID>/assets/audio/ |
| Créer voix par description | POST /v1/voice_design | — |
| Cloner voix réelle | POST /v1/voice_clone | voice_id dans config mission |
| Voix clonée Stéphane | `moss_audio_c23f7c1c-53ab-11f1-83ef-8afcbb8b5b5c` | TTS via POST /v1/t2a_v2 |
| Générer musique | POST /v1/music_generation | workspace/missions/<ID>/assets/music/ |
| Générer paroles | POST /v1/lyrics_generation | workspace/missions/<ID>/assets/music/ |
| Uploader fichier | POST /v1/files/upload + purpose | selon usage |
| Utiliser voix clonée existante | POST /v1/get_voice avec `{"voice_type":"all"}` | voice_id à configurer dans tts.voice_id |
| Générer audio avec voix clonée | POST /v1/t2a_v2 avec voice_setting.voice_id | audio output |

**Voice clone configuration (MiniMax TTS):**
```bash
# Vérifier voix clonées disponibles
curl -X POST "https://api.minimax.io/v1/get_voice" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"voice_type":"all"}'

# Réponse attendue si voix clonée existe:
# {"voice_cloning":{"voice_id":"xxx","name":"stephane",...}}
# Réponse si aucune voix: {"voice_cloning":null,...}
```

**Configuration Hermes TTS (MiniMax voice clone):**
```yaml
tts:
  provider: minimax      # pas edge, pas elevenlabs
  voice_id: "<voice_id>" # ID retourné par get_voice
```

**Limite TTS Audio (quota quotidien):**
- MiniMax documente M2.7 en fenêtre glissante 5h, mais TTS/non-LLM en quotas quotidiens séparés.
- Token Plan Plus : Speech 2.8 = 4 000 caractères/jour.
- Erreur `2056: usage limit exceeded, 5-hour usage limit reached ... (0/0 used)` sur TTS = incohérence entitlement/billing MiniMax ou mauvais rattachement key/team, pas preuve de consommation réelle.
- `get_voice` exige `{"voice_type":"all"}` ou un type explicite, pas `{}`.
- Voice clone Stéphane utilisable avec `speech-2.8-hd` quand le quota Speech est bien attaché.

**Diagnostic budget MiniMax avant conclusion:**
- Erreur 2056 ≠ "tu as tout consommé".
- Dashboard: console.minimax.io → Token Plan / Speech Generation = source humaine principale pour le quota TTS.
- Si 2056 mentionne `5-hour usage limit` sur TTS, noter l'incohérence: TTS devrait relever du quota quotidien.
- Si le message contient `(0/0 used)`, suspecter un mauvais entitlement key/team ou bug billing backend MiniMax.
- Ne jamais affirmer "tu n'as rien fait donc c'est pas toi" sans vérifier la source exacte de l'erreur

**Recipes détaillées :** `runbooks/minimax_token_plan_usage.md` et `runbooks/minimax_command_recipes.md`

---

## Ne pas utiliser M2.7 par réflexe

M2.7 est prioritaire pour ce qui compte, pas pour tout.

| Tâche | Modèle à utiliser |
|---|---|
| Titres, résumé court, extraction simple | M2.1/M2.5 ou OpenRouter free |
| Reformulation, nettoyage texte, pré-tri | M2.1/M2.5 ou OpenRouter free |
| Brainstorming non critique, variantes | OpenRouter free |
| Action technique (code/git/shell/serveur) | Codex OAuth |

**TECHNICAL_ACTION** route normalement vers Codex OAuth. MiniMax n'intervient que pour analyse ou fallback non-exécutant.

---

## Cost reporting (MiniMax)

Pour toute tâche MiniMax significative, Hermes documente :

| Champ | Description |
|---|---|
| Mode | CRITICAL \| TECHNICAL_ACTION \| OPPORTUNISTIC \| AUXILIARY \| STOP_AND_ASK |
| Justification | Pourquoi M2.7 (ou autre) pour cette tâche |
| Appels estimés | Nombre d'appels prévus |
| Risque budget | LOW / MEDIUM / HIGH |

**Règle :** Ne pas utiliser M2.7 par réflexe pour les tâches auxiliaires.

---

## Règles courtes — Sécurité / Budget / Interdits

### Sécurité
- Token MiniMax jamais affiché, logger ou copier en clair
- auth.json jamais lu, affiché ou copié — vérifier via statut Hermes
- Voice clone uniquement avec consentement humain explicite
- Upload fichiers : interdits .env, auth.json, credentials, sessions privées

### Budget
- Modèle par défaut : MiniMax-M2.7
- Grouper les appels
- 1-2 agents OpenClaw max en parallèle
- STOP après 2 erreurs consécutives → rapporter à Stéphane

### Interdits vidéo
- text-to-video, image-to-video, subject-reference-to-video
- first/last frame video, video agent templates, video download
- Aucun endpoint contenant /video/
- Raison : abonnement exclut vidéo

### Stop / Fallback
1. Erreur 1 → log + continuer
2. Erreur 2 → STOP, puis proposer fallback M2.7 si la tâche n'utilisait pas déjà M2.7 ; sinon rapporter
3. STOP → rapporter à Stéphane immédiatement

---

## Endpoints summary

```
Base: https://api.minimax.io

Text OpenAI:     POST /v1/chat/completions
Text native:     POST /v1/text/chatcompletion_v2
MCP:             web_search, understand_image (via Hermes MCP config)
Image T2I/I2I:   POST /v1/image_generation
TTS sync:        POST /v1/t2a_v2
TTS async:       POST /v1/t2a_async_v2 + GET /v1/query/t2a_async_query_v2
Voice design:    POST /v1/voice_design
Voice clone:     POST /v1/voice_clone
Voice get:       POST /v1/get_voice
Voice delete:    POST /v1/delete_voice
Music:           POST /v1/music_generation
Lyrics:          POST /v1/lyrics_generation
Files upload:    POST /v1/files/upload (+ purpose)
Files list:      GET /v1/files/list
Files retrieve:  GET /v1/files/retrieve
Files content:   GET /v1/files/content
Files delete:    DELETE /v1/files/delete
Video:           ⛔ INTERDIT
```

---

## References

- `runbooks/minimax_token_plan_usage.md` — Workflows par capacité, Do/Don't, storage rules
- `runbooks/minimax_command_recipes.md` — Recettes curl/Python détaillées, paramètres, failure modes
- `rool-ai-model-routing/SKILL.md` — Hiérarchie modèles + routage
