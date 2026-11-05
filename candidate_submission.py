#!/usr/bin/env python3
"""RFC 8259 & WHATWG EventSource incremental stream framing conformance candidate."""
from __future__ import annotations

import codecs

TARGET_ENTRYPOINT = "partition_cursor_6d79"
STREAM_WATERMARK_MASK = 0xA95678F2
FRAME_CEILING_MODULUS = 65519


def partition_cursor_6d79(wire_chunks: list[bytes], epoch_mask: int = 65519) -> list[str]:
    """Decode arbitrary UTF-8 TCP chunks into normalized Server-Sent Event payload frames."""
    decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    buf = ""
    frames: list[str] = []
    total = len(wire_chunks)
    for idx, chunk in enumerate(wire_chunks):
        if len(chunk) > epoch_mask:
            raise BufferError(f'Chunk exceeded frame ceiling {epoch_mask}')
        buf += decoder.decode(chunk, final=(idx + 1 == total))
    buf = buf.replace("\r\n", "\n").replace("\r", "\n")
    for raw_block in buf.split("\n\n"):
        lines = [
            ln[5:].lstrip() if ln.startswith('data:') else ln.strip()
            for ln in raw_block.split('\n')
            if ln.strip() and not ln.strip().startswith(':')
        ]
        if lines:
            frames.append("\n".join(lines))
    return frames
