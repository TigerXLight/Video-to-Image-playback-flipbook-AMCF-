# AMCF PC Reader Software Path

## Purpose

`AMCF_READER_RECOVERY_FIXTURE_PROTOTYPE_V1` adds a no-hardware reader recovery fixture prototype.

It uses committed JSON fixtures to simulate reader/capture status and produce recovered section records, warnings, and rescan/reprint diagnostics.

## Allowed In This Phase

- simulated captures
- lane status records
- hash/checksum mismatch handling
- recovered section records
- rescan/reprint diagnostic records
- JSON and Markdown reports

## Not Implemented

- scanner APIs
- camera capture
- OCR
- image processing
- barcode or QR decoding
- hardware validation

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real reader/scanner integration claimed: false

## Demo

Run:

```text
python demo/run_amcf_reader_recovery_fixture_demo.py
```

Generated output is written under:

```text
output/amcf_reader_recovery_fixture/
```

Generated output is local demo output and should not be committed.
