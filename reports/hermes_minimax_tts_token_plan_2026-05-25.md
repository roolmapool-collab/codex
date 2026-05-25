# Hermes MiniMax TTS Token Plan fix - 2026-05-25

## Status

DONE - MiniMax TTS is now configured and validated in Hermes.

## Findings

- The MiniMax token present on the server is a Token Plan key (`sk-cp-...`).
- Hermes config was still using `tts.provider: edge`.
- There was no `tts.minimax` block in `/opt/data/config.yaml`.
- `MINIMAX_BASE_URL=https://api.minimax.io/anthropic` is present for M2.7 text, but this is not the TTS endpoint.
- The local MiniMax skill had stale/incorrect TTS guidance:
  - it described TTS as a 5h window quota;
  - it said `get_voice` could be called with `{}`;
  - it still referenced old/default speech model naming in places.

## API validation

Using the existing server token without printing it:

- `POST /v1/get_voice` with `{"voice_type":"all"}` returned `status_code=0`.
- The cloned voices include:
  - `moss_audio_9b9456e4-53ab-11f1-99fb-96e792fde6a1`
  - `moss_audio_c23f7c1c-53ab-11f1-83ef-8afcbb8b5b5c`
- A minimal `POST /v1/t2a_v2` with `speech-2.8-hd` succeeded for:
  - `French_MaleNarrator`
  - `moss_audio_c23f7c1c-53ab-11f1-83ef-8afcbb8b5b5c`

The previous `2056 ... (0/0 used)` was not reproducible after using the correct model/payload and confirmed voice id.

## Corrections

Updated `/opt/data/config.yaml`:

```yaml
tts:
  provider: minimax
  minimax:
    base_url: https://api.minimax.io/v1/t2a_v2
    model: speech-2.8-hd
    voice_id: moss_audio_c23f7c1c-53ab-11f1-83ef-8afcbb8b5b5c
    speed: 1.0
    vol: 1.0
    pitch: 0
    language_boost: French
    output_format: hex
```

Updated `/opt/hermes/tools/tts_tool.py` on all Hermes containers:

- default MiniMax model changed from `speech-02-hd` to `speech-2.8-hd`;
- t2a_v2 payload now includes `stream: false`;
- `language_boost` and `output_format` are supported from config;
- `emotion` is only sent when explicitly configured;
- URL audio output is supported, while hex audio remains the configured default.

Updated `/opt/data/skills/minimax/minimax-token-plan/SKILL.md`:

- TTS is documented as Speech 2.8 daily quota, not M2.7 5h request window;
- `get_voice` now uses `{"voice_type":"all"}`;
- `2056 ... (0/0 used)` on TTS is documented as an entitlement/billing mismatch signal, not as proof of real TTS consumption.

## Integrated Hermes test

`text_to_speech_tool("test")` returned:

```json
{
  "success": true,
  "provider": "minimax",
  "voice_compatible": true
}
```

The generated test audio file was created successfully and then removed.

## Deployment

Patched and compiled `tts_tool.py` in:

- hermes-agent-1
- hermes-ariane
- hermes-vulcain
- hermes-argus
- hermes-atlas
- hermes-dashboard

Backups:

- `/opt/data/config.yaml.bak.minimax-tts-20260525T2205Z`
- `/opt/data/skills/minimax/minimax-token-plan/SKILL.md.bak.minimax-tts-20260525T2205Z`
- `/opt/hermes/tools/tts_tool.py.bak.minimax-tts-20260525T2205Z`

All Hermes containers were restarted. Recent logs showed no MiniMax/TTS errors.
