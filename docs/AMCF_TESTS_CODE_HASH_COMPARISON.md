# AMCF Tests Code Hash Comparison

This is the first content comparison after the complete path inventory. Run `python demo/run_amcf_tests_code_hash_comparison.py` to hash every `.py`, `.js`, `.ts`, `.cmd`, `.bat`, `.ps1`, `.sh`, `.html`, and `.css` file in the local `Tests` tree and compare it with local `Main` and tracked public code. Generated JSONL and summary output stay under ignored `output/amcf_tests_code_hash_comparison/`.

## Initial Result

| Hash status | Files |
| --- | ---: |
| Exact public hash | 318 |
| Public repo itself inside the `Tests` tree | 217 |
| Exact `Main` hash without exact public hash | 2 |
| Same public filename, different content | 143 |
| No exact public or `Main` hash and no same public filename | 1,642 |
| **Code/runnable files hashed** | **2,322** |

There are 991 distinct content hashes. The two `Main`-only exact matches are copies of its machine-specific `RUN_AMCF_VNEXT.cmd`; public has a portable replacement. They are not evidence of a missing runtime feature. A filename or hash mismatch by itself does not establish a missing feature, and an exact hash does not prove the source was accepted. Semantic reviews completed by this hash pass: **0**. Full parity proven: **false**.

Large unmatched groups contain imported copies of earlier runs. For example, 152 of Test 14H's 160 unmatched code/runnable files sit under its imported 14E2/14E3 folders. Those files need provenance and acceptance review, not 152 automatic ports.

## Newest `Test 02` Viewer Disposition

The initial filename heuristic matched eight local `viewer/index.html` files to the unrelated public Pages `site/index.html`. All eight local files are byte-identical (SHA-256 `417858afa386e8916bf99a8ca9d4140513fbddaaed17f6d6fdc91d6c7f12bda6`) generated viewer pages. They occur in runs `20261003_165701`, `20261013_023117`, `20261013_023556`, `20261013_054829`, `20261013_055937`, `20261013_060131`, `20261013_061205`, and `20261013_071127`. Their play, frame-step, speed, loop, contours, metrics, difference, track-focus, seek, and frame-export controls are represented by `src/amcf_test02_diagnostic_viewer.py` and its focused test. Disposition: `PUBLIC_EQUIVALENT_TESTED` for the viewer contract; the eight local HTML files remain `GENERATED_EVIDENCE_NOT_SOURCE`. This is not a claim of byte-identical generated HTML or media.

The only other `Test 02` code/runnable mismatch is `20261003_165701/viewer/START_VIEWER.cmd`. It starts `http.server` and a browser with a hardcoded machine-local Python path. Disposition: `LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY`; the public demo writes the viewer under ignored `output/`, and a user can serve that directory with their own Python runtime. These nine decisions reduce unexplained Test 02 source gaps but do not complete its data, document, media, and archive review.

## First Concrete Candidate

`Test 14H_LARGER_BOUNDED_V2_SAMPLE_GENERALISATION` records `LARGER_BOUNDED_V2_SAMPLE_GENERALISATION_READY` for two bounded samples and says component metadata is useful, **not** a general compression win. The initial scan found no public 14H schema or `motion_xor_zlib` handler. The subsequent bounded decoder port is documented in `AMCF_V2_14H_BOUNDED_ARCHIVE_DECODER.md`: all 16 available local variant archives decoded with matching recorded RGB checksums. This closes the bounded archive-read gap, not the full 14H runner, codec sweep, or broader workspace parity.

## `Main` Boundary

Local `Main` has 14 non-cache files. The existing static parity map has public counterparts for 13, with six exact hashes; the local README is superseded by public documentation. `Main` has five Python files and does not contain the Test 14F V2 package (39 Python files) or Test 14H's larger-sample decoder. Public already has the 39-file 14F V2 package, with 38 exact hashes and one documented optional-dependency hardening change. Therefore, comparing GitHub only with `Main` would miss useful work retained in `Tests`.

## Next Checks

1. Work through the 143 same-name-different and 1,642 unmatched file records by unique hash, provenance, run verdict, and accepted behavior. The 14H reader closes one behavior gap but does not change the original hash counts.
2. Continue with documents, metadata, archives, and media from the complete file inventory; do not treat the code hash pass as total coverage.
3. Only after the `Tests` dispositions are complete, compare the remaining workspace folders and resolve any useful AMCF-owned behavior not present in `Main` or public.

No hardware validation, physical Level 5, or manufactured player is claimed. Generated output is not committed.
