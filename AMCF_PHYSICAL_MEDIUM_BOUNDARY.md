# Physical AMCF Boundary And Design Direction

The physical medium is not the proof that AMCF works. The proof is that video can be converted into AMCF and played back through image/component reconstruction with the same intended playback result.

The physical branch asks a different question:

```text
Can the AMCF sequence be carried by a physical image medium and scanned/reconstituted back into the same AMCF playback?
```

## Corrected Physical Framing

The earlier phrase "flipbook" is useful as inspiration, but a normal left-to-right book flip is probably not the best mechanism. It can introduce visible transition lines, page-turn delays, and lateral motion artifacts.

The better open design space is:

- vertical stack transport: pages move into and out of the viewing/scanning plane vertically or along depth
- continuous film-track ribbon: frames are carried like a loop or strip past an aperture
- sprocket or timing-marker control: frame boundaries are determined mechanically/optically
- USB scanner/CIS reader: a controlled optical reader replaces unstable phone-camera capture
- color registry: a header palette and per-frame metadata support color correction
- checksums/hashes: printed or scanned metadata validates each physical frame

## What The Current Simulations Proved

The ideal vertical-stack simulation showed that aligned physical-page capture can preserve AMCF playback exactly at proxy-frame level.

That does not yet prove real paper, ink, optics, page curvature, scanner noise, slippage, or human cranking. Those are future robustness tests.

## Next Physical Test

The next meaningful run should test non-ideal vertical-stack capture:

- feed jitter
- slight vertical offset
- perspective/skew
- motion blur
- scanner/camera noise
- compression noise
- registration-marker detection
- automatic crop recovery
- tolerance thresholds

The goal is to see how much real-world physical imperfection the AMCF physical carrier can tolerate before playback diverges from the digital AMCF reference.
