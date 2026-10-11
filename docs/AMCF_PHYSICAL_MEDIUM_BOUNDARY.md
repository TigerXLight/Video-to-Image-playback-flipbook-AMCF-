# Physical AMCF Boundary And Design Direction

The physical medium is not the proof that AMCF works. The proof path is the software-first AMCF process: video can be converted into AMCF and played back through image/component reconstruction with the same intended playback result.

The physical branch asks a different question:

```text
Can the AMCF sequence be carried by a physical image medium and then scanned/recovered or physically viewed through a controlled gate?
```

## Corrected physical framing

The earlier phrase "flipbook" is useful as inspiration, but a normal left-to-right book flip is not the default AMCF physical mechanism. It can introduce visible transition lines, page-turn delays, and lateral motion artifacts.

The better open design space is:

- vertical-stack / indexed-section transport
- indexed thin-page or thin-section AMCF media
- fixed scan gate for reader/recovery mode
- fixed view gate for physical playback mode
- illumination, front light, backlight, optical window, or projection path
- timing/index and registration markers
- colour registry
- metadata and checksum/hash lanes
- optional reader lane for diagnostics/recovery/export

Continuous ribbon or film-like transport may remain comparison/reference only. It is not the default primary assumption.

## Reader/recovery mode

Reader/recovery mode scans AMCF physical media through a controlled reader/scanner path and reconstructs AMCF digital state if needed.

## Physical view/playback mode

Physical view/playback mode presents AMCF physical media directly through controlled motion, a fixed view gate, and illumination/optical presentation so the sequence can be viewed without relying on a digital display system.

## Current status

The clean package provides software, virtual hardware, and documentation support only. It does not prove real paper, ink, optics, page curvature, transport slippage, scanner noise, physical viewing quality, hardware security, or prototype reliability.

No physical proof, physical Level 5, hardware validation, manufacturing readiness, final UI, or built prototype is claimed.
