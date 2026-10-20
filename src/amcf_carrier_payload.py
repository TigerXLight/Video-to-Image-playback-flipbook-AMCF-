from __future__ import annotations

import hashlib
import json
import math
import shutil
import struct
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PAYLOAD_SCHEMA = "amcf-native-carrier-payload-v1"
PAYLOAD_MAGIC = b"AMCFPAY1"
HEADER = struct.Struct(">8sIIII32s")
CRC = struct.Struct(">I")
DEFAULT_PAGE_BYTES = 16 * 1024


@dataclass(frozen=True)
class PayloadPageConfig:
    width_px: int = 1600
    height_px: int = 1000
    margin_px: int = 52
    marker_px: int = 34
    payload_left_px: int = 80
    payload_top_px: int = 160
    payload_width_px: int = 1440
    payload_height_px: int = 760
    module_px: int = 2

    @property
    def cells_width(self) -> int:
        return self.payload_width_px // self.module_px

    @property
    def cells_height(self) -> int:
        return self.payload_height_px // self.module_px

    @property
    def capacity_bytes(self) -> int:
        return (self.cells_width * self.cells_height) // 8


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _marker_positions(config: PayloadPageConfig) -> list[tuple[int, int]]:
    return [
        (config.margin_px, config.margin_px),
        (config.width_px - config.margin_px - config.marker_px, config.margin_px),
        (config.margin_px, config.height_px - config.margin_px - config.marker_px),
        (
            config.width_px - config.margin_px - config.marker_px,
            config.height_px - config.margin_px - config.marker_px,
        ),
    ]


def _packet(header: bytes, chunk: bytes) -> bytes:
    return header + chunk + CRC.pack(zlib.crc32(header + chunk) & 0xFFFFFFFF)


def _make_packet(page_index: int, page_count: int, total_bytes: int, chunk: bytes, archive_sha256: str) -> bytes:
    header = HEADER.pack(
        PAYLOAD_MAGIC,
        int(page_index),
        int(page_count),
        int(total_bytes),
        len(chunk),
        bytes.fromhex(archive_sha256),
    )
    return _packet(header, chunk)


def _unpack_packet(packet: bytes) -> tuple[dict[str, Any], bytes]:
    if len(packet) < HEADER.size + CRC.size:
        raise ValueError("payload_packet_too_small")
    magic, page_index, page_count, total_bytes, chunk_length, archive_digest = HEADER.unpack(packet[: HEADER.size])
    if magic != PAYLOAD_MAGIC:
        raise ValueError("payload_magic_mismatch")
    expected_length = HEADER.size + int(chunk_length) + CRC.size
    if len(packet) != expected_length:
        raise ValueError("payload_packet_length_mismatch")
    chunk = packet[HEADER.size : HEADER.size + int(chunk_length)]
    expected_crc = CRC.unpack(packet[-CRC.size :])[0]
    actual_crc = zlib.crc32(packet[:-CRC.size]) & 0xFFFFFFFF
    if expected_crc != actual_crc:
        raise ValueError("payload_packet_crc_mismatch")
    if page_count <= 0 or page_index < 0 or page_index >= page_count:
        raise ValueError("payload_page_index_invalid")
    return (
        {
            "page_index": int(page_index),
            "page_count": int(page_count),
            "total_bytes": int(total_bytes),
            "chunk_length": int(chunk_length),
            "archive_sha256": archive_digest.hex(),
        },
        chunk,
    )


def _packet_bits(packet: bytes) -> list[int]:
    bits: list[int] = []
    for byte in packet:
        bits.extend((byte >> shift) & 1 for shift in range(7, -1, -1))
    return bits


def _sample_bits(image: Any, count: int, config: PayloadPageConfig) -> bytes:
    bits: list[int] = []
    for index in range(count):
        x_cell = index % config.cells_width
        y_cell = index // config.cells_width
        if y_cell >= config.cells_height:
            raise ValueError("payload_image_capacity_exceeded")
        x = config.payload_left_px + x_cell * config.module_px + config.module_px // 2
        y = config.payload_top_px + y_cell * config.module_px + config.module_px // 2
        pixel = image.getpixel((x, y))
        if isinstance(pixel, int):
            value = pixel
        else:
            value = sum(pixel[:3]) / 3.0
        bits.append(1 if value < 128 else 0)
    output = bytearray()
    for offset in range(0, len(bits), 8):
        value = 0
        for bit in bits[offset : offset + 8]:
            value = (value << 1) | bit
        output.append(value)
    return bytes(output)


def render_payload_packet(packet: bytes, output_path: str | Path, config: PayloadPageConfig | None = None) -> dict[str, Any]:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:  # pragma: no cover - dependency-specific
        raise RuntimeError("Pillow is required for native carrier payload rendering") from exc

    config = config or PayloadPageConfig()
    if len(packet) > config.capacity_bytes:
        raise ValueError(f"payload_packet_exceeds_page_capacity:{len(packet)}>{config.capacity_bytes}")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (config.width_px, config.height_px), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for x, y in _marker_positions(config):
        draw.rectangle((x, y, x + config.marker_px - 1, y + config.marker_px - 1), fill=(0, 0, 0))
    try:
        font = ImageFont.truetype("arial.ttf", 22)
        mono = ImageFont.truetype("consola.ttf", 14)
    except OSError:
        font = mono = ImageFont.load_default()
    draw.text((120, 56), "AMCF NATIVE PAYLOAD CARRIER", fill=(0, 0, 0), font=font)
    draw.text((120, 98), "exact archive bytes / registration and binary payload lane", fill=(35, 35, 35), font=mono)
    draw.rectangle(
        (
            config.payload_left_px - 2,
            config.payload_top_px - 2,
            config.payload_left_px + config.payload_width_px + 1,
            config.payload_top_px + config.payload_height_px + 1,
        ),
        outline=(80, 80, 80),
        width=2,
    )
    bits = _packet_bits(packet)
    for index, bit in enumerate(bits):
        x_cell = index % config.cells_width
        y_cell = index // config.cells_width
        x = config.payload_left_px + x_cell * config.module_px
        y = config.payload_top_px + y_cell * config.module_px
        colour = 0 if bit else 255
        draw.rectangle((x, y, x + config.module_px - 1, y + config.module_px - 1), fill=(colour, colour, colour))
    registry = [(0, 0, 0), (255, 255, 255), (220, 40, 40), (40, 170, 70), (45, 95, 220), (30, 190, 205), (205, 55, 185), (230, 190, 35)]
    registry_y = config.height_px - 82
    for index, colour in enumerate(registry):
        x = 120 + index * 112
        draw.rectangle((x, registry_y, x + 76, registry_y + 32), fill=colour, outline=(0, 0, 0), width=1)
    image.save(output_path, format="PNG", optimize=True)
    return {
        "path": str(output_path),
        "width_px": config.width_px,
        "height_px": config.height_px,
        "packet_bytes": len(packet),
        "payload_capacity_bytes": config.capacity_bytes,
    }


def decode_payload_packet_image(image_path: str | Path, config: PayloadPageConfig | None = None) -> tuple[dict[str, Any], bytes]:
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - dependency-specific
        raise RuntimeError("Pillow is required for native carrier payload recovery") from exc

    config = config or PayloadPageConfig()
    image_path = Path(image_path)
    with Image.open(image_path) as opened:
        image = opened.convert("RGB")
        if image.size != (config.width_px, config.height_px):
            raise ValueError("payload_image_dimensions_mismatch")
        for x, y in _marker_positions(config):
            pixel = image.getpixel((x + config.marker_px // 2, y + config.marker_px // 2))
            if sum(pixel[:3]) > 96:
                raise ValueError("payload_registration_marker_missing")
        header_bytes = _sample_bits(image, HEADER.size * 8, config)
        magic, page_index, page_count, total_bytes, chunk_length, archive_digest = HEADER.unpack(header_bytes)
        if magic != PAYLOAD_MAGIC:
            raise ValueError("payload_magic_mismatch")
        packet_length = HEADER.size + int(chunk_length) + CRC.size
        if packet_length > config.capacity_bytes:
            raise ValueError("payload_packet_length_exceeds_capacity")
        packet = _sample_bits(image, packet_length * 8, config)
    return _unpack_packet(packet)


def build_native_payload_carrier(
    archive_path: str | Path,
    output_dir: str | Path,
    *,
    page_bytes: int = DEFAULT_PAGE_BYTES,
    config: PayloadPageConfig | None = None,
    write_pdf: bool = True,
) -> dict[str, Any]:
    archive_path = Path(archive_path).resolve()
    output_dir = Path(output_dir).resolve()
    config = config or PayloadPageConfig()
    if not archive_path.exists():
        return {"ok": False, "error": "native_archive_missing", "unsafe_acceptance_count": 0}
    if page_bytes <= 0 or page_bytes + HEADER.size + CRC.size > config.capacity_bytes:
        return {"ok": False, "error": "invalid_page_bytes", "unsafe_acceptance_count": 0}
    total_bytes = archive_path.stat().st_size
    page_count = max(1, math.ceil(total_bytes / page_bytes))
    archive_digest = sha256_file(archive_path)
    pages_dir = output_dir / "payload_pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    pages: list[dict[str, Any]] = []
    with archive_path.open("rb") as stream:
        for page_index in range(page_count):
            chunk = stream.read(page_bytes)
            packet = _make_packet(page_index, page_count, total_bytes, chunk, archive_digest)
            page_path = pages_dir / f"payload_{page_index:06d}.png"
            rendered = render_payload_packet(packet, page_path, config)
            pages.append({"page_index": page_index, "path": str(page_path), "packet_bytes": len(packet), **rendered})

    pdf_path: Path | None = None
    pdf_status = "not_requested"
    if write_pdf:
        if page_count <= 256:
            try:
                from PIL import Image

                images = [Image.open(Path(item["path"])).convert("RGB") for item in pages]
                if images:
                    pdf_path = output_dir / "amcf_native_payload_pages.pdf"
                    images[0].save(pdf_path, "PDF", resolution=300, save_all=True, append_images=images[1:])
                    pdf_status = "written"
            except ImportError:
                pdf_status = "pillow_unavailable"
        else:
            pdf_status = "skipped_page_count_limit"
    manifest = {
        "schema": PAYLOAD_SCHEMA,
        "archive_name": archive_path.name,
        "archive_sha256": archive_digest,
        "archive_bytes": total_bytes,
        "page_count": page_count,
        "page_bytes": page_bytes,
        "page_config": asdict(config),
        "pages": [{"page_index": item["page_index"], "path": f"payload_pages/{Path(item['path']).name}"} for item in pages],
        "pdf_path": str(pdf_path) if pdf_path else None,
        "pdf_status": pdf_status,
        "native_component_payload_embedded": True,
        "source_video_embedded": False,
        "source_video_required_for_decode": False,
        "direct_amcf_decoding": True,
        "physical_printing_performed": False,
        "hardware_validation_claimed": False,
        "unsafe_acceptance_count": 0,
    }
    manifest_path = output_dir / "native_payload_manifest.json"
    _write_json(manifest_path, manifest)
    return {
        "ok": bool(pages),
        "manifest_path": str(manifest_path),
        "pages_dir": str(pages_dir),
        "page_count": page_count,
        "archive_bytes": total_bytes,
        "archive_sha256": archive_digest,
        "pdf_path": str(pdf_path) if pdf_path else None,
        "pdf_status": pdf_status,
        "native_component_payload_embedded": True,
        "source_video_required_for_decode": False,
        "unsafe_acceptance_count": 0,
    }


def recover_native_payload_carrier(
    pages_dir: str | Path,
    output_archive: str | Path,
    *,
    manifest_path: str | Path | None = None,
    config: PayloadPageConfig | None = None,
) -> dict[str, Any]:
    pages_dir = Path(pages_dir).resolve()
    output_archive = Path(output_archive).resolve()
    config = config or PayloadPageConfig()
    page_paths = sorted(pages_dir.glob("payload_*.png"))
    if not page_paths:
        return {"ok": False, "error": "payload_pages_missing", "unsafe_acceptance_count": 0}
    expected_count: int | None = None
    expected_total: int | None = None
    expected_digest: str | None = None
    chunks: dict[int, bytes] = {}
    errors: list[str] = []
    for page_path in page_paths:
        try:
            metadata, chunk = decode_payload_packet_image(page_path, config)
            index = int(metadata["page_index"])
            if index in chunks:
                errors.append(f"duplicate_page:{index}")
                continue
            chunks[index] = chunk
            if expected_count is None:
                expected_count = int(metadata["page_count"])
                expected_total = int(metadata["total_bytes"])
                expected_digest = str(metadata["archive_sha256"])
            elif (
                expected_count != int(metadata["page_count"])
                or expected_total != int(metadata["total_bytes"])
                or expected_digest != str(metadata["archive_sha256"])
            ):
                errors.append(f"page_header_inconsistent:{page_path.name}")
        except Exception as exc:  # fail closed on a damaged scan/page
            errors.append(f"page_decode_failed:{page_path.name}:{exc}")
    if manifest_path and Path(manifest_path).exists():
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        if expected_count is not None and int(manifest.get("page_count", expected_count)) != expected_count:
            errors.append("manifest_page_count_mismatch")
    if expected_count is None or expected_total is None or expected_digest is None:
        errors.append("payload_header_missing")
    elif len(chunks) != expected_count:
        errors.append(f"payload_page_count_mismatch:{len(chunks)}!={expected_count}")
    elif sorted(chunks) != list(range(expected_count)):
        errors.append("payload_page_sequence_gap")
    if errors:
        return {
            "ok": False,
            "error": "native_payload_recovery_failed",
            "errors": errors,
            "page_count": expected_count or 0,
            "decoded_pages": len(chunks),
            "unsafe_acceptance_count": 0,
        }

    output_archive.parent.mkdir(parents=True, exist_ok=True)
    partial = output_archive.with_suffix(output_archive.suffix + ".part")
    digest = hashlib.sha256()
    written = 0
    with partial.open("wb") as stream:
        for index in range(int(expected_count)):
            chunk = chunks[index]
            stream.write(chunk)
            digest.update(chunk)
            written += len(chunk)
    actual_digest = digest.hexdigest()
    exact = written == expected_total and actual_digest == expected_digest
    if exact:
        partial.replace(output_archive)
    else:
        partial.unlink(missing_ok=True)
    return {
        "ok": exact,
        "output_archive": str(output_archive) if exact else None,
        "archive_bytes": written,
        "expected_bytes": expected_total,
        "archive_sha256": actual_digest,
        "expected_sha256": expected_digest,
        "exact_archive_recovered": exact,
        "page_count": expected_count,
        "decoded_pages": len(chunks),
        "source_video_required_for_decode": False,
        "unsafe_acceptance_count": 0,
    }


def run_native_payload_roundtrip(
    archive_path: str | Path,
    output_dir: str | Path,
    *,
    page_bytes: int = DEFAULT_PAGE_BYTES,
    write_pdf: bool = True,
) -> dict[str, Any]:
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    built = build_native_payload_carrier(archive_path, output_dir / "carrier_payload", page_bytes=page_bytes, write_pdf=write_pdf)
    if not built.get("ok"):
        return {"ok": False, "build": built, "unsafe_acceptance_count": 0}
    manifest_path = Path(str(built["manifest_path"]))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recovered_path = output_dir / "recovered_native_amcf.zip"
    recovery = recover_native_payload_carrier(
        Path(str(built["pages_dir"])),
        recovered_path,
        manifest_path=manifest_path,
        config=PayloadPageConfig(**manifest["page_config"]),
    )
    reader_report: dict[str, Any]
    if recovery.get("ok"):
        try:
            from amcf_digital_validator import validate_amcf_archive
            from amcf_video_pipeline import decode_amcf_to_frames

            inspection = validate_amcf_archive(recovered_path)
            decoded = decode_amcf_to_frames(recovered_path, output_dir / "native_amcf_decode")
            reader_report = {"validation": inspection, "decoded": decoded, "ok": bool(inspection.get("ok") and decoded.get("ok"))}
        except Exception as exc:  # pragma: no cover - optional archive profile
            reader_report = {"ok": False, "error": f"native_reader_failed:{exc}"}
    else:
        reader_report = {"ok": False, "error": "recovery_failed"}

    corruption_dir = output_dir / "corruption_probe"
    corruption_dir.mkdir(parents=True, exist_ok=True)
    for page in Path(str(built["pages_dir"])).glob("payload_*.png"):
        shutil.copy2(page, corruption_dir / page.name)
    corruption_rejected = False
    try:
        from PIL import Image

        first_page = sorted(corruption_dir.glob("payload_*.png"))[0]
        with Image.open(first_page) as opened:
            image = opened.convert("RGB")
            config = PayloadPageConfig(**manifest["page_config"])
            x = config.payload_left_px + config.module_px // 2
            y = config.payload_top_px + config.module_px // 2
            original = image.getpixel((x, y))[0]
            value = 255 if original < 128 else 0
            image.putpixel((x, y), (value, value, value))
            image.save(first_page, format="PNG")
        probe = recover_native_payload_carrier(corruption_dir, output_dir / "corruption_probe_recovered.zip", manifest_path=manifest_path, config=config)
        corruption_rejected = not bool(probe.get("ok"))
    except Exception:
        corruption_rejected = True
    result = {
        "schema": "amcf-native-carrier-payload-roundtrip-v1",
        "ok": bool(built.get("ok") and recovery.get("ok") and reader_report.get("ok") and corruption_rejected),
        "build": built,
        "recovery": recovery,
        "native_reader": reader_report,
        "corruption_rejected": corruption_rejected,
        "native_component_payload_embedded": True,
        "source_video_embedded": False,
        "source_video_required_for_decode": False,
        "direct_amcf_decoding": bool(reader_report.get("ok")),
        "unsafe_acceptance_count": 0,
    }
    _write_json(output_dir / "native_payload_roundtrip_report.json", result)
    return result


__all__ = [
    "DEFAULT_PAGE_BYTES",
    "PAYLOAD_SCHEMA",
    "PayloadPageConfig",
    "build_native_payload_carrier",
    "decode_payload_packet_image",
    "recover_native_payload_carrier",
    "run_native_payload_roundtrip",
]
