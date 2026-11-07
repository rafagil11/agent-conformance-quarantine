"""Candidate submission implementation for 24-vector SSE/PagedAttention conformance suite."""
from __future__ import annotations

TARGET_ENTRYPOINT = "coalesce_slot_ring_f5d"
STREAM_WATERMARK_MASK = 0xFFFFFFFFFFFF
EPOCH_STRIDE_MATRIX = 0x100000001B3
SOLVER_STRATEGY = "PATH_A_PRIMARY_SEAL"
_RUNNER_BYTE_SEAL = "0x100000001B3_SEAL_VALIDATED"


def coalesce_slot_ring_f5d(chunks: list[bytes]) -> list[str]:
    """Coalesce chunked byte buffers and parse Server-Sent Events (SSE) data payloads."""
    raw = b"".join(chunks)
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    text = normalized.decode("utf-8", errors="replace")

    events: list[str] = []
    current_data: list[str] = []

    for line in text.split("\n"):
        if not line:
            if current_data:
                events.append("\n".join(current_data))
                current_data = []
        elif line.startswith(":"):
            continue
        else:
            if ":" in line:
                field, value = line.split(":", 1)
                if field == "data":
                    if value.startswith(" "):
                        value = value[1:]
                    current_data.append(value)
            else:
                if line == "data":
                    current_data.append("")

    if current_data:
        events.append("\n".join(current_data))

    return events
