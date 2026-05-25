# SPEC — hermes_discord_payload_lint.py

## CLI attendue

```bash
hermes_discord_payload_lint.py --mode outbound_mission --file payload.json
hermes_discord_payload_lint.py --mode agent_reply --file payload.json
hermes_discord_payload_lint.py --mode outbound_mission '{...json...}'
```

## Sorties

- exit `0` si OK ;
- exit `1` si rejet ;
- stdout/stderr doit contenir une raison lisible.

## Règles outbound_mission

- JSON valide.
- `channel_id` obligatoire.
- `content` obligatoire.
- mention numérique `<@\d+>` obligatoire.
- `allowed_mentions.users` obligatoire.
- le bot user ID mentionné doit être dans `allowed_mentions.users`.
- `MISSION-ID` obligatoire.
- `TASK-ID` obligatoire.
- trace outil interdite.
- mention textuelle interdite.
- `thread_id` interdit sauf `metadata.thread_validated=true`.
- ACK seul interdit.

## Règles agent_reply

- trace outil interdite.
- ACK inutile interdit.
- `DONE`, `BLOCKED`, `NEEDS_VALIDATION`, `RISK_DETECTED` autorisés si réponse structurée.

## Mots interdits

```text
send_message
skill_view
search_files
read_file
terminal
tool_call
exit_code
Traceback
DEBUG
Result:
Output:
```
