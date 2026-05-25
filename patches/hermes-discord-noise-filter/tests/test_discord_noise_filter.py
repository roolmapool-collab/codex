from gateway.platforms.discord import _sanitize_discord_outbound_content as adapter_sanitize
from tools.send_message_tool import (
    _sanitize_discord_outbound_content as tool_sanitize,
    send_message_tool,
)


NOISE_ONLY = [
    '💻 terminal: "ls -la /opt/data/workspace"',
    '🔎 search_files: "PREMENOPAUSE"',
    '📖 read_file: "/opt/data/workspace/mission.md"',
    "Type /sethome to make this chat your home channel, or ignore to skip.",
    "for Discord. A home channel is where Hermes delivers cron job results and cross-platform messages.",
    "Je dois d'abord vérifier l'état actuel du workspace et les permissions en place avant toute modification.",
]


def check(sanitize):
    for sample in NOISE_ONLY:
        assert sanitize(sample) is None, sample
    mixed = 'Diagnostic OK\n💻 terminal: "id hermes"\nSuite propre'
    assert sanitize(mixed) == "Diagnostic OK\nSuite propre"
    clean = "Diagnostic permissions — Mission PREMENOPAUSE"
    assert sanitize(clean) == clean


check(adapter_sanitize)
check(tool_sanitize)
skip = send_message_tool({
    "action": "send",
    "target": "discord:#hermes-orchestrateur",
    "message": '💻 terminal: "id hermes"',
})
assert '"skipped": true' in skip
print("discord_noise_filter_ok")
