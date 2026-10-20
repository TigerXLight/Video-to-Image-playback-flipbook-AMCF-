# AMCF Tests File Review: Test 13M and Software Virtual Reader Emulator

## Scope

This review covers two high-priority groups from the local workspace:

- `Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC` and its `13M_FIX_13Q_13R_12K_GATE_CLOSEOUT` addendum;
- `Test AMCF_SOFTWARE_VIRTUAL_PHYSICAL_READER_EMULATOR`.

The review compares source files and acceptance records with the current public source tree. Generated archives, videos, frame dumps, reports, caches, and local setup packages are evidence only and are not copied into the public repository.

## Test 13M evidence

The 13M groups contain benchmark/specification consolidation, imported 07G/08B/10A/11B/13B/13D/13I/13J2/13P tools, regression runners, native archive experiments, and a closeout package. The primary source runners are historical experiment orchestrators, not a stable public module boundary.

The acceptance records explicitly distinguish bounded research-prototype readiness from production completion:

- `RESEARCH_PROTOTYPE_VALIDATION_READY`;
- `CLOSEOUT_ALL_TRACKS_READY`;
- `V1_RESEARCH_PROTOTYPE_PACKAGE_READY`;
- `V2_PLANNING_PACKAGE_READY`;
- native bounded proof ready: true;
- full native playback solved: false;
- final playback engine solved: false;
- semantic/object AMCF solved: false;
- stage-4 temporal scheduling solved: false;
- general native payload compression solved: false.

This makes 13M important accepted evidence and roadmap consolidation, but not evidence that every experiment in the folder should become public runtime code. The public repository already carries the selected bounded behavior through `src/amcf_v2/`, the V2 sidecar metadata layer, playback-index planning, archive writer/reader contracts, semantic diagnostics, quality metrics, and public demos/tests. No additional 13M bulk port is justified by this review.

## Software virtual-reader emulator evidence

The emulator contains 36 files, including nine Python files. Its maintained source concepts are:

| Local source concept | Public correspondence | Result |
|---|---|---|
| virtual cartridge and indexed sections | `src/amcf_virtual_hardware.py` (`VirtualCartridge`, `VirtualCartridgeSection`, `make_virtual_section`) | public superset |
| virtual reader navigation and lane reads | `src/amcf_virtual_hardware.py` (`VirtualReader`) | public superset |
| timing/registration/metadata/hash/colour lane validation | `src/amcf_virtual_hardware.py` (`VirtualScanGate`) and `src/amcf_virtual_carrier_reader.py` | public equivalent/superset |
| accepted/degraded/rescan/fail-closed outcomes | public virtual hardware and physical-player fail-closed tests | public tested |
| player handoff counters and validation log | `PlayerHandoffState` plus public virtual-hardware demo/tests | public equivalent |
| software-only adapter boundary | `ReaderAdapter`, `VirtualReaderAdapter`, `FuturePhysicalReaderAdapter` | public equivalent |
| future physical adapter placeholder | `FuturePhysicalReaderAdapter` | intentionally unimplemented |
| emulator CLI/demo | `demo/run_virtual_hardware_demo.py` and virtual reader recovery demos | public tested |

The local emulator's separate files are not byte-identical to the public module because the public implementation consolidated and expanded the behavior. The public module contains the local concepts plus scan-gate, playback-device, appliance, and fail-closed integration. That is consolidation, not a missing feature.

## Port decision

**No runtime port in this review.** Copying the 13M experiment runners would add historical/research duplication and local-data coupling. Copying the emulator files would duplicate behavior already present in the public consolidated module. The correct action is to keep the public tests and demos as the executable parity evidence.

## Tests and claims

- `unsafe_acceptance_count`: remains `0` in the public virtual-reader/release review paths;
- hardware validation claimed: `false`;
- physical Level 5 claimed: `false`;
- manufactured player claimed: `false`;
- real scanner, reader, printer, motor, sensor, cartridge, USB, and firmware communication claimed: `false`.

## Remaining parity boundary

This review closes these two priority groups as `PUBLIC_EQUIVALENT_OR_CONSOLIDATED`. It does not claim byte-for-byte parity with every generated 13M artifact, nor does it convert the 13M limitation flags into product claims. The remaining work is a final reconciliation of the full workspace inventory and then a deliberate CLI/app closeout based on the already-tested public modules.
