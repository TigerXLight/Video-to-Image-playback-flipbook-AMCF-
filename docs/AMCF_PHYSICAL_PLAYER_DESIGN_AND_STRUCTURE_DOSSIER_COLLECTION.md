# AMCF Physical Player Design and Structure Dossier Collection

This is the AMCF Physical Player Design and Structure Dossier Collection. It defines the future physical AMCF player object/concept. It is not the same as the software I/O dossier.

This collection does not claim real hardware validation, physical Level 5 completion, manufactured-player completion, or that real motors, sensors, cartridges, or optics have been physically validated. The visible AMCF image path is modelled as physical/optical, not normal LCD/OLED video playback. Current work is software models, simulator logic, reports, docs, tests, demos, release review, and claim-boundary enforcement.

## Collection Metadata

- Collection name: AMCF Physical Player Design and Structure Dossier Collection
- Intended repo path: `docs/AMCF_PHYSICAL_PLAYER_DESIGN_AND_STRUCTURE_DOSSIER_COLLECTION.md`
- Branch: `dev/amcf-physical-player-design-structure`
- Source record: `AMCF Physical Player Design and Structure Dossier.txt`
- Hardware validation claimed: false
- Physical Level 5 claimed: false
- Manufactured player claimed: false
- Real sensors validated: false
- Real motors validated: false
- Real cartridges validated: false
- Built prototype claimed: false

## Source Anchors

The collection preserves these source anchors from the physical-player dossier:

- The physical player is a compact physical/optical playback device.
- It executes the digital AMCF schedule using material AMCF carrier sections.
- The correct chain is:

```text
Digital AMCF
→ AMCF schedule / update events
→ physical AMCF carrier
→ physical player transport
→ physical/optical viewing window
```

- The preferred physical-player direction is tablet-like, not scanner-board.
- The player follows AMCF update events, not fixed-FPS page flipping.
- The preferred transport abstraction is dynamic folded-path A/B staged indexed-section transport.
- The player uses visible view gate / hidden staging gate abstraction.
- Section verification must happen before display.
- Fail-closed behaviour must preserve `unsafe_acceptance_count == 0`.
- Reverse/seek remains limited and safe.
- Arbitrary physical seek remains future/high-end.
- Level 5 physical hardware is not achieved.

## Source-Note Cleanup

Chat-transfer markers, local-only workspace paths, and ChatGPT-only citation placeholders from the source record have been converted into normal repo-readable source notes. The technical content, run names, claim boundaries, and phase sequence are preserved.

---

# AMCF Physical Player Design and Structure Dossier  
## Part 1 — Boundary, Product Form, Visual Language, and Core Architecture

## 1. Purpose of this dossier

The purpose of this dossier is to define the **physical AMCF player** as a future product/mechanism concept.

This is not the same as:

```text
AMCF digital playback
AMCF reader/recovery
AMCF printer output
AMCF PC control software
```

Those are related, but the physical player has its own design problem:

```text
How can a physical object display AMCF playback through material media,
while still following the same dynamic AMCF schedule proven digitally?
```

The current intended design has already moved away from a scanner-board style object. The stronger description is a compact tablet-like physical AMCF player with a folded internal indexed-media path and physical/optical image playback through a front viewing window. (Source note: prior physical-player design/source record.)

So this dossier should define:

```text
- physical player boundary
- visual/product form
- internal media path
- view gate
- optical system
- A/B staged transport
- electronics/control layer
- audio sync
- cartridge/media relationship
- what is not yet claimed
```

---

## 2. Core boundary: what the player is

The physical AMCF player should be defined as:

```text
A compact physical/optical playback device that executes the digital AMCF schedule using material AMCF carrier sections, folded internal transport, staged view gates, illumination, optics, sensors, and embedded control electronics.
```

That means the physical player is not a separate AMCF system. It is the **physical executor** of the AMCF model.

Correct chain:

```text
Digital AMCF
→ AMCF schedule / update events
→ physical AMCF carrier
→ physical player transport
→ physical/optical viewing window
```

The important rule is:

```text
The digital AMCF defines what should happen and when.
The physical player determines whether it can physically execute that schedule.
```

So the player is not just a viewer. It is a mechanical/optical execution system.

---

## 3. What the physical player is not

The physical player should not be described as:

```text
- a normal tablet playing a video file
- an LCD/OLED screen showing decoded video
- a scanner that reads pages and then displays a digital reconstruction
- a long exposed roller transport
- a fixed-FPS page flipper
- a hand-cranked left-to-right flipbook
- a camcorder/scanner-board object
```

A screen can exist for menus or diagnostics, but the **main visible AMCF image** should be physical/optical.

The earlier structure already made this distinction: digital electronics are allowed for microcontroller/OS control, motor control, index feedback, audio sync, calibration, error correction, and power management, while the visible image playback remains physical/optical. (Source note: prior physical-player design/source record.)

So the boundary should be:

```text
Allowed:
digital control, timing, audio, sensors, diagnostics, calibration

Not the main physical-player claim:
normal digital screen generates the AMCF image
```

---

## 4. Product form: tablet-like physical/optical player

The physical player should look more like:

```text
iPad Mini / e-reader / compact tablet
but thicker internally
with a physical optical viewing window instead of a normal digital display
```

That matches the earlier design correction, where the target visual language was explicitly described as iPad Mini/tablet/e-reader proportions with a physical optical viewing window instead of a digital display. (Source note: prior physical-player design/source record.)

The exterior should be:

```text
Front:
- large square/rectangular optical viewing window
- minimal bezel
- side controls or small control strip
- optional small status display, but not the main image source

Side:
- cartridge slot
- eject/release control
- USB/data/power port if needed
- audio output or speaker vents

Back:
- service panel
- battery/control layer access
- optional stand/folio hinge

Internal:
- folded carrier path
- A/B staging gates
- view gate
- illumination/shutter
- folded optics
- sensor/control board
```

The design should not look like a rugged DVD player or scanner. It should look like a modern media device whose display area happens to be **optical/physical**, not electronic.

---

## 5. Visual design language

The target design language should be:

```text
clean
flat
tablet-like
controlled
protected-media
minimal exposed mechanism
modern consumer device
physical optics visible only where useful
```

Avoid:

```text
bulky scanner board
camcorder handle
industrial lab rig
long exposed strip
retro flipbook styling
early-2000s DVD player look
```

The earlier design notes already said the current look felt too early-2000s / rugged DVD-player / scanner-like and should move toward a squarer tablet body, large front optical viewing window, side cartridge slot, folded internal media path, compact optics, hidden electronics, and optional folio/stand case. (Source note: prior physical-player design/source record.)

So the public concept should be described as:

```text
AMCF Physical Player — Tablet Form Factor
```

not:

```text
AMCF Scanner Player
AMCF Roller Viewer
AMCF Mechanical Flipbook
```

---

## 6. Internal architecture overview

The physical player should be internally arranged around a folded path.

Baseline structure:

```text
side/top cartridge slot
→ cartridge recognition / index read
→ input alignment stage
→ folded U/S/three-pass media path
→ hidden staging gate
→ visible view gate
→ illumination / shutter layer
→ folded optical path
→ front physical viewing window
→ return / park / reverse path
```

This matches the earlier recommended cutaway structure: cartridge slot, alignment/index stage, folded U-turn transport, fixed view gate, illumination/shutter, compact folded optics, front viewing window, and return/park/take-up path. (Source note: prior physical-player design/source record.)

The internal device can be thought of as seven layers:

```text
Layer 1 — Physical shell / tablet body
Layer 2 — Cartridge/media loading bay
Layer 3 — Folded indexed-section transport
Layer 4 — A/B staged view-gate mechanism
Layer 5 — Illumination / shutter / exposure layer
Layer 6 — Compact optical viewing path
Layer 7 — Control electronics / audio / power / diagnostics
```

---

## 7. Why folded optics matter

The player needs a large front viewing window without requiring a long straight optical/mechanical path. Folded optics are therefore a useful design reference.

Modern periscope/folded camera modules use prisms or mirrors to bend the optical path and fit longer optics into compact smartphone bodies; Samsung Electro-Mechanics describes the folded method as bending light like a periscope to create high-magnification zoom without protruding from the phone body. [Samsung Semiconductor](https://samsungsem.com/global/product/module/camera-module/main-core-technology.do) A recent compact periscope-lens paper similarly describes integrating a right-angle prism to fold the optical path and reduce system length in a smartphone imaging module. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12844183/)

For AMCF, the design implication is:

```text
Do not place the physical media, illumination, lens path, and viewing window in one long straight line.

Fold the media path and fold the optical path so the player can stay tablet-like.
```

AMCF does not need to copy a phone camera. It uses the same broad engineering idea:

```text
folded path = compact device depth
```

Possible optical arrangement:

```text
physical AMCF section at view gate
→ controlled illumination
→ short lens/magnifier stage
→ prism/mirror fold
→ front viewing window
```

This lets the image plane sit inside the device rather than directly under the front surface.

---

## 8. Core mechanism: dynamic A/B staged transport

The physical player should use the same dynamic logic as digital AMCF.

It should not do:

```text
one physical section per fixed video frame
```

It should do:

```text
advance physical media according to AMCF update events
hold visible state until the next update is required
preload the next section before it is needed
switch optically/mechanically at the update timestamp
```

The earlier discussion already formalized this as a **dynamic folded-path A/B staged physical player**, where the current visible section is held at View Gate A, the next required section is preloaded at hidden Gate B, and at update time a shutter/illumination transition hides the switch. (Source note: prior physical-player design/source record.)

The core sequence:

```text
1. Current section is visible at Gate A.
2. Next required section is preloaded at hidden Gate B.
3. Scheduler waits for the AMCF update timestamp.
4. Illumination/shutter creates a tiny controlled blank/persistence interval.
5. Gate B becomes the visible gate.
6. Gate A section moves to return/park/reverse path.
7. Next section is preloaded again.
```

This is physical double-buffering.

Digital equivalent:

```text
front buffer / back buffer
```

Physical equivalent:

```text
visible gate / hidden staging gate
```

---

## 9. “Instant speed” is not actual infinite paper speed

The player should not try to solve speed by moving paper infinitely fast.

The better principle is:

```text
Do not move during the visible moment.
Move before the visible moment.
```

So apparent instant switching comes from:

```text
- prepositioned next section
- very short gate transition
- optical blanking
- illumination control
- mechanical latch/release
- sensor-confirmed alignment
- fail-closed if the next section is not ready
```

The viewer should perceive:

```text
visible state A
→ tiny optical blank / persistence interval
→ visible state B
```

not:

```text
paper moving across the visible window
```

This is the central design decision.

---

## 10. The player should use a dynamic physical schedule

The player needs a physical playback schedule derived from the digital AMCF schedule.

Digital AMCF has:

```text
source timing
component update events
reconstruction timing
```

Physical AMCF player needs:

```text
source timing
physical section update events
view-gate dwell duration
preload deadline
transition blank duration
optical presentation timing
```

Example event:

```json
{
  "timestamp_ms": 1200,
  "visible_section": "section_00041",
  "next_section": "section_00042",
  "dwell_ms": 80,
  "preload_required_by_ms": 1180,
  "transition_blank_ms": 8,
  "requires_verified_next_section": true
}
```

This lets the player decide:

```text
Can I execute this update safely?
Is the next section ready?
Is it verified?
Is the A/B gate ready?
Is the audio sync still acceptable?
Should I continue, pause, or fail closed?
```

---

## 11. Player subsystem breakdown

The player should be designed as a set of subsystems.

```text
A. Shell / enclosure
B. Cartridge bay
C. Carrier transport
D. A/B staging gates
E. View gate
F. Illumination/shutter
G. Optical path
H. Reader/prefetch sensor
I. Control electronics
J. Audio system
K. Power system
L. Safety/fail-closed system
```

Each subsystem has a role.

## A. Shell / enclosure

```text
- tablet-like shape
- protects carrier
- prevents dust/light leakage
- gives stable hand-held viewing
- allows cartridge insertion/removal
```

## B. Cartridge bay

```text
- accepts AMCF physical carrier
- protects thin sections
- provides carrier ID/header read zone
- aligns media before transport
```

## C. Carrier transport

```text
- moves indexed thin sections
- supports forward playback
- supports pause/hold
- supports reverse/seek if possible
- minimizes carrier damage
```

## D. A/B staging gates

```text
- hold current and next sections
- allow preloading
- allow fast visible switching
- support double-buffered physical playback
```

## E. View gate

```text
- holds section flat/aligned
- defines visible image plane
- maintains registration
- works with illumination and optics
```

## F. Illumination/shutter

```text
- controls exposure/dwell
- hides transitions
- stabilizes visible output
- may use LED light guide / micro-shutter / mechanical shutter
```

## G. Optical path

```text
- magnifies/transfers physical section image to front window
- may use folded mirrors/prisms
- keeps device compact
```

## H. Reader/prefetch sensor

```text
- reads index/timing/hash lanes before display
- verifies upcoming sections
- supports fail-closed playback
```

## I. Control electronics

```text
- runs schedule
- controls actuators
- reads sensors
- handles timing
- logs diagnostics
```

## J. Audio system

```text
- plays or syncs audio
- tracks drift
- can pause/fail if visual schedule falls behind
```

## K. Power system

```text
- USB power, battery, or hybrid
- local buffering/supercapacitor later
- energy recovery as support layer only
```

## L. Safety/fail-closed

```text
- refuses unsafe playback
- stops on jam/misfeed
- refuses unverified next section
- prevents wrong section display
```

---

## 12. Candidate actuator families for the player

Part 1 should not choose the final actuator, but it should identify serious candidates.

The strongest early candidates remain:

```text
1. Motor + encoder feed
2. Piezo ultrasonic feed
3. Piezo/electrostatic inchworm indexed feed
4. Constant-force spring + governor/brake/latch
5. Hybrid motor/spring/electronic regulation
```

Piezoelectric ultrasonic motors are serious candidates because reviews describe them as compact actuators that convert high-frequency vibration into rotary or linear motion and offer precision/control, fast response, compact size, quiet operation, and EMI-free behavior. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11433840/) Miniature ultrasonic motors are also described in recent literature as having millisecond-scale response, high-speed operation, and sub-micrometer-level resolution, which makes them relevant as a compact precision-motion candidate, not a proven AMCF solution. [The Advanced Portfolio](https://advanced.onlinelibrary.wiley.com/doi/pdf/10.1002/admt.202500711)

Constant-force springs are relevant for self-contained mechanical support because they are flat coiled springs designed to deliver near-uniform load over their working range. [lesjofors.com](https://www.lesjofors.com/en/technology/insights/what-are-constant-force-springs/) They should not be treated as the whole answer, because AMCF still needs regulation, latch/brake, index sensing, and dynamic scheduling.

So the first player design should not say:

```text
we use X final motor
```

It should say:

```text
the architecture supports several transport candidates, with motor/encoder and piezo/inchworm as controlled baselines, and constant-force spring mechanisms as self-contained comparison candidates
```

---

## 13. Physical carrier relationship

The player should accept an AMCF physical carrier, not loose random pages.

Possible carrier forms:

```text
A. side-loaded cartridge with indexed thin sections
B. folded flexible carrier inside cartridge
C. linked/chain-mounted page sections
D. micro-stack of thin cards/pages
E. hybrid laminated thin-section carrier
```

The strongest current product direction is:

```text
side-loaded cartridge
+ protected indexed thin-section media
+ folded internal player path
```

Reason:

```text
- keeps media protected
- makes the product feel modern
- avoids exposed strip
- allows carrier ID/manifest reading
- supports replacement/swap
- supports reader recovery later
```

The player should not require the user to handle the raw thin sections directly.

---

## 14. First public design description

The clean description should be:

```text
AMCF Physical Player V1 is a future compact tablet-like physical/optical playback concept. It uses a side-loaded AMCF carrier, a folded internal indexed-section path, A/B staged view gates, controlled illumination, and compact folded optics to physically present AMCF visual states through a front viewing window. Digital electronics may control timing, motor/index movement, audio sync, diagnostics, and safety, but the visible AMCF image path is modeled as physical/optical rather than ordinary LCD/OLED video playback.
```

That is the wording I would standardize.

---

## 15. What this Part 1 decides

Part 1 decides:

```text
- physical player is tablet-like, not scanner-board
- physical image output is optical/material, not normal screen video
- internal path is folded, not long straight transport
- player follows dynamic AMCF update schedule
- A/B staged view-gate transport is the primary mechanism concept
- cartridge-based indexed thin-section media is the primary product direction
- electronics are allowed for control/audio/safety
- actuator choice remains open
- real hardware is not claimed
```

---

## 16. What remains open

Still unresolved:

```text
- exact carrier form: linked sections, stack, folded carrier, or cartridge reel
- exact A/B gate geometry
- whether there is one view gate with optical switching or two physical gates
- exact illumination/shutter method
- exact lens/prism/mirror arrangement
- exact actuator family
- exact reverse/seek mechanism
- exact material thickness and stack capacity
- exact maximum update rate
- exact audio sync method
- whether player has an integrated reader or separate prefetch sensor
```

These should be covered in later parts.

---

## 17. Part 2 should cover next

Part 2 should cover:

```text
Internal Transport Architecture
```

Specifically:

```text
- folded U/S/three-pass path
- A/B gate layouts
- chain/indexed carrier option
- individual page/card shuttle option
- cartridge stack option
- linked thin-section option
- return/park/reverse path
- no-gap transition logic
- mechanical timing limits
- sensor and latch placement
- likely failure modes
```

Part 1 stops here because the **physical player boundary, form factor, visual language, and core architecture** are now defined.
----

# AMCF Physical Player Design and Structure Dossier  
## Part 2 — Internal Transport Architecture

## 1. Purpose of Part 2

Part 1 defined the physical AMCF player as a future compact physical/optical playback object.

Part 2 defines the internal transport architecture:

```text
How does the physical AMCF carrier move inside the player?
How does the player avoid visible gaps?
How do A/B staging gates work?
How does the reader/prefetch side change?
How does reverse/seek/pause fit?
Which transport models are preferred, secondary, or only research candidates?
```

This part must keep the important boundary:

```text
The physical player is not the same as the reader/scanner path.
The reader/scanner path recovers or validates AMCF media.
The physical player path physically/optically presents AMCF media for direct viewing.
```

However, the two paths can share hardware in a later hybrid reader-player appliance.

The older design context described a compact cartridge-based indexed scan reader: thin-page cartridge, alignment/feed stage, scan/view gate, CIS/line-scan sensor, LED, controller/cache, and PC/software playback. That remains useful for the reader/recovery and bench-device branch.

The newer corrected player branch is different:

```text
compact tablet-like optical player
+ folded internal indexed media path
+ side-loaded cartridge/card/section stack
+ visible view gate
+ hidden preload/staging gate
+ shutter/illumination blanking
+ reader/prefetch lanes
+ dynamic AMCF schedule
+ physical/optical viewing window
```

So Part 2 should not erase the older reader concept. It should classify it properly:

```text
older cartridge scanner/reader = reader/recovery / bench prototype / virtual-reader lineage
new tablet-like A/B player = future physical/optical player lineage
```

---

## 2. Core transport rule

The physical player must not be designed as:

```text
one physical page moved for every fixed 24/30/60 FPS frame
```

The physical transport rule is:

```text
Move physical media according to AMCF update events.
Hold the current visible state at the view gate.
Preload the next required state before it is needed.
Switch optically/mechanically at the update timestamp.
Fail closed if the next state is not verified.
```

This follows the AMCF logic:

```text
Digital AMCF:
source timing
→ component/update events
→ reconstruction timing

Physical AMCF player:
source timing
→ physical section update events
→ view-gate dwell duration
→ optical presentation timing
```

So the physical transport does not chase constant FPS movement. It follows the same dynamic schedule that digital AMCF already uses.

---

## 3. The “instant speed” problem

The user’s question was:

```text
How would we achieve instant speed?
```

The answer is:

```text
Do not move the visible paper instantly.
Prepare the next physical state before it is visible.
Hide the switch.
```

The apparent instant transition comes from:

```text
preloading
alignment
A/B staging
short transport distance
shutter/illumination blanking
index lock
sensor confirmation
fail-closed validation
```

The viewer should perceive:

```text
visible state A
→ tiny optical blank / persistence interval
→ visible state B
```

The viewer should not perceive:

```text
paper travelling across the viewing window
```

This is the central transport principle.

---

## 4. Preferred architecture: dynamic A/B staged folded path

The preferred internal transport should be named:

```text
Dynamic folded-path A/B staged indexed-section transport
```

The basic sequence is:

```text
1. Current section is locked at visible Gate A.
2. Next required section is loaded/aligned at hidden Gate B.
3. Reader/prefetch lane verifies timing/index/hash/registration.
4. AMCF scheduler waits for the update timestamp.
5. Illumination/shutter blanks the visible path briefly.
6. Gate B becomes visible or its section is transferred into the visible gate.
7. Old Gate A section moves to return/park/reverse path.
8. The next section is preloaded again.
```

This is physical double-buffering.

Digital equivalent:

```text
front buffer
back buffer
```

Physical AMCF equivalent:

```text
visible gate
hidden staging gate
```

The physical player does not have to move a page from the cartridge to the window at the exact visible update instant. It only has to complete the visible switch at that instant.

---

## 5. Three-pass folded transport model

The user’s “3 pass” idea should be formalised as:

```text
Pass 1 — input / preload / prefetch path
Pass 2 — active view-gate / optical presentation path
Pass 3 — return / park / reverse path
```

### Pass 1 — Input / preload / prefetch path

This path receives the next required physical section from the cartridge or carrier.

It should handle:

```text
- section selection
- coarse alignment
- timing/index read
- registration read
- hash/checksum read
- prefetch validation
- preparation for staging gate
```

This path does not need to be visible to the user.

### Pass 2 — Active view-gate path

This path holds the section that is currently visible.

It should handle:

```text
- flatness at the view plane
- precise registration
- illumination
- optical presentation
- dwell duration
- no movement during visible hold
```

This is the critical optical path.

### Pass 3 — Return / park / reverse path

This path receives the previous section after it leaves the visible gate.

It should support:

```text
- safe park
- short reverse buffer
- previous-section retrieval
- section re-use
- misfeed recovery
- no wrong-action movement
```

This is where the user’s “push back to the back or hold” idea belongs.

The depth of this return/park path should be limited. It should not become a large internal storage maze. For practical player design, it should hold only enough sections for:

```text
pause
step-back
short reverse
seek recovery
jam-safe clearing
```

not the whole cartridge.

---

## 6. Two possible A/B gate geometries

There are two major ways to implement A/B staging.

## Option A — Two physical gates

```text
Gate A = visible gate
Gate B = hidden staging gate
```

Then they alternate.

Concept:

```text
A visible, B hidden
→ blank
→ B visible, A hidden/returning
→ next section staged at A
→ blank
→ A visible, B hidden/returning
```

Advantages:

```text
- clean double-buffering logic
- next section can be fully aligned before display
- visible transition can be very short
- easier to model in software
```

Problems:

```text
- optical path is harder
- two gates may need equal registration precision
- physical body may become thicker
- illumination must be consistent across both gates
```

## Option B — One visible gate plus hidden staging slot

```text
Hidden staging slot prepares the next section.
At update time, section transfers into the single visible gate.
```

Advantages:

```text
- one true optical view plane
- simpler optics
- easier colour/brightness consistency
```

Problems:

```text
- transfer into the visible gate must be very fast and precise
- more dependence on shutter/blanking
- misalignment risk during transfer
```

### Recommendation

For the first simulator and design documentation, use the more abstract model:

```text
visible_gate
hidden_staging_gate
```

Do not overcommit yet to whether they are two physically separate optical gates or one optical gate with a hidden staging slot.

The repo simulator already models this at the right abstraction level:

```text
view_gate_id
hidden_gate_id
current_gate_section
next_staging_section
preload_queue
transition_blank_ms
reader_prefetch_ahead_ms
section_verified_before_display
reverse_buffer_depth
fail_closed_on_unverified_next_section
```

This is the correct software model before committing to a mechanical layout.

---

## 7. Carrier movement options

Part 2 should distinguish candidate media movement systems.

## Option 1 — Folded indexed strip / linked section carrier

```text
cartridge
→ folded indexed carrier path
→ hidden staging
→ visible gate
→ return/take-up/park
```

This is probably the best near-term conceptual transport for a tablet-like player.

Advantages:

```text
- media remains connected
- section order is easier to preserve
- less loose-page handling
- easier to prefetch upcoming sections
- good fit for folded U/S path
```

Problems:

```text
- may drift under tension
- repeated bending may damage sections
- material must tolerate folding/radius
- reverse/seek requires careful take-up logic
```

Best use:

```text
preferred baseline for compact folded-path player
```

## Option 2 — Individual page/card shuttle

```text
cartridge stack
→ select card/page
→ shuttle into staging gate
→ shuttle into view gate
→ push back / park / return
```

Advantages:

```text
- closest to the user’s “individual paper” idea
- supports discrete sections cleanly
- damaged sections can theoretically be isolated
- physical “page” identity is clear
```

Problems:

```text
- harder at speed
- loose pages/cards can jam
- reverse/seek is harder
- selecting arbitrary cards requires more mechanism
- high-motion AMCF segments may require many rapid shuttles
```

Best use:

```text
lower-speed prototype
bench validation
archive/reader mode
not primary fluid playback unless heavily staged
```

## Option 3 — Chain-mounted individual sections

```text
individual pages/cards mounted on a chain or linked carrier
```

Advantages:

```text
- preserves individual-section identity
- prevents loose page scatter
- indexing can be mechanically regular
- could support folded path
```

Problems:

```text
- chain adds bulk
- hinge/connection wear
- spacing between sections creates dead travel unless carefully overlapped
- noise and mechanical complexity
- difficult to keep perfectly flat at view gate
```

Best use:

```text
research candidate
possibly useful for demonstration model
not yet the preferred final product path
```

## Option 4 — Two-track shuttle

```text
Track A = visible / ready-to-visible
Track B = hidden preload / staging
```

Advantages:

```text
- maps directly to physical double-buffering
- one track can prepare while the other displays
- good for no-gap logic
```

Problems:

```text
- track switching mechanism is complex
- both tracks need accurate registration
- more width/thickness
- transport must prevent cross-track interference
```

Best use:

```text
strong candidate for A/B staging abstraction
possible internal implementation for advanced player
```

## Option 5 — Magnetic/electrostatic/mechanical guide tracks

These should be treated as section-control aids, not the whole transport.

They can help with:

```text
- holding
- anti-slip alignment
- stop-gate control
- wrong-motion prevention
- reverse indexing
- latch/brake support
- precise gate registration
```

Risks:

```text
- friction
- dust sensitivity
- sticking
- material constraints
- possible interference with printed marks or conductive layers
```

Best use:

```text
registration and stop-gate support layer
not the primary transport by itself
```

---

## 8. Gate-level state machine

The physical transport should be modeled as a state machine.

Recommended states:

```text
EMPTY
CARTRIDGE_INSERTED
SECTION_PREFETCH
SECTION_STAGED
SECTION_VERIFIED
VISIBLE_LOCKED
TRANSITION_BLANK
SECTION_SWITCH
OLD_SECTION_PARK
NEXT_PREFETCH
PAUSED
REVERSE_READY
SEEKING
FAIL_CLOSED
```

A normal forward playback cycle:

```text
CARTRIDGE_INSERTED
→ SECTION_PREFETCH
→ SECTION_STAGED
→ SECTION_VERIFIED
→ VISIBLE_LOCKED
→ TRANSITION_BLANK
→ SECTION_SWITCH
→ OLD_SECTION_PARK
→ NEXT_PREFETCH
→ SECTION_STAGED
```

A failure cycle:

```text
SECTION_PREFETCH
→ section missing / hash mismatch / marker unreadable
→ FAIL_CLOSED
→ optical path blanked
→ playback stopped or rescan requested
```

A reverse cycle:

```text
VISIBLE_LOCKED
→ request reverse
→ check reverse buffer
→ preload previous verified section
→ TRANSITION_BLANK
→ previous section visible
→ old section parked
```

This state model is more important than choosing a final motor. The simulator and docs should prove the logic first.

---

## 9. Prefetch reader lane

The transport cannot rely only on the visible view gate.

It needs a prefetch reader lane before display.

The prefetch reader lane should read:

```text
- section index
- timing marks
- registration marks
- colour registry or colour reference
- metadata/transform lane
- hash/checksum lane
- damage/missing marker status
```

The prefetch lane should answer:

```text
Is this the correct next section?
Is it in the expected order?
Is it aligned enough to stage?
Is the hash/checksum valid?
Is colour degraded but usable?
Is the section safe to display?
Should playback continue, rescan, skip, pause, or fail closed?
```

This is why the reader changes. The older reader path was mainly:

```text
scan/recover physical carrier
→ reconstruct digital AMCF
→ output to PC/software
```

The player-prefetch reader is:

```text
read ahead
→ verify upcoming section
→ feed scheduler
→ allow or block visible display
```

So the player may contain a small reader function even if it is not primarily a scanner.

---

## 10. Timing windows

The transport needs timing windows.

Recommended timing variables:

```text
update_timestamp_ms
view_gate_dwell_ms
preload_start_ms
preload_deadline_ms
reader_prefetch_ahead_ms
transition_blank_ms
gate_lock_timeout_ms
verification_timeout_ms
reverse_buffer_depth
```

Example:

```text
AMCF update timestamp:       1200 ms
reader prefetch ahead:       120 ms
preload must begin by:       1080 ms
section verified by:         1170 ms
transition blank begins:     1196 ms
visible switch completes:    1200 ms
new section dwell begins:    1200 ms
```

This lets the player determine:

```text
Can the mechanism keep up?
Is the next section ready early enough?
Is the section verified before display?
Should it continue or fail closed?
```

The important point:

```text
The player must know about the next section before it is needed.
```

That is why A/B staging and prefetch are linked.

---

## 11. Pause, seek, and reverse

The internal path must support more than forward movement.

## Pause

Pause should mean:

```text
hold current visible section at view gate
keep illumination stable or dim safely
keep next section staged if already verified
do not allow drift
```

Pause does not require moving media.

## Step forward

Step forward should mean:

```text
verify next section
blank optical path
switch to next section
park old section
```

## Step backward / reverse

Reverse is harder.

Possible reverse strategies:

```text
1. Short reverse buffer
   Keep last N sections in a park/reverse path.

2. Cartridge rewind
   Reverse the connected carrier path.

3. Re-select previous card
   For individual card stack systems.

4. Software-assisted reverse
   Use digital display/diagnostic only for review, not physical playback claim.
```

For the physical player concept, the best first claim is:

```text
limited reverse / short step-back via reverse buffer
```

Not:

```text
instant arbitrary seek across the whole cartridge
```

Arbitrary seek should remain future/high-end.

---

## 12. Transport failure modes

The internal transport docs should explicitly list failure modes.

```text
- next section missing
- wrong section staged
- index mismatch
- hash/checksum mismatch
- colour registry degraded
- registration mark unreadable
- section skewed
- section curled
- section jammed
- double-feed
- track slip
- gate not locked
- illumination failure
- shutter stuck
- reader prefetch timeout
- reverse buffer miss
- cartridge metadata mismatch
```

The fail-closed rule:

```text
If a critical lane fails, do not display the section.
Blank/pause/fail closed instead.
```

Critical failures:

```text
wrong section index
missing required marker
hash/checksum mismatch where no recovery is allowed
gate not locked
unsafe misalignment
unverified next section at transition time
```

Non-critical/degraded conditions:

```text
minor colour degradation
non-essential metadata warning
recoverable registration warning
rescan-needed status before display
```

The simulator should preserve the rule:

```text
unsafe_acceptance_count must remain zero
```

---

## 13. Physical hierarchy after Part 2

The correct hierarchy is:

```text
Level 1 — Digital AMCF
canonical representation, scheduler, validation

Level 2 — Physical carrier package
indexed sections, lanes, metadata, timing, hashes

Level 3 — Virtual reader/recovery
software emulation of reader/scanner lane logic

Level 4 — Mechanical/optical player simulator
software model of dynamic folded-path A/B staged playback

Level 5 — Future physical hardware concept
tablet-like physical/optical player with folded internal path, A/B staging, optical view gate, prefetch, sensors, and fail-closed logic
```

Important:

```text
Level 5 is not achieved yet.
```

---

## 14. How Part 2 should update the design direction

The physical-player design should now say:

```text
Preferred internal transport:
dynamic folded-path A/B staged indexed-section transport.
```

Expanded description:

```text
The AMCF physical player uses a protected side/top cartridge or card-section carrier. It prefetches and verifies upcoming indexed sections, stages the next required physical state at a hidden gate, holds the current physical state at the visible view gate, and uses shutter/illumination blanking to hide the transition. The mechanism follows AMCF update events rather than fixed video FPS page flipping. Reverse and seek are handled through limited buffer/park paths at first, with arbitrary seek left for later research.
```

Avoid saying:

```text
the paper moves instantly
the mechanism is proven
full physical playback exists
the device is a normal tablet
the scanner path and player path are identical
fixed-FPS physical pages are the target
```

---

## 15. What Codex should eventually model from this part

The simulator/docs should eventually include:

```text
TransportArchitecture
TransportPass
ViewGate
HiddenStagingGate
PrefetchReaderLane
SectionVerificationState
TransitionBlankingState
ReverseParkBuffer
FailClosedTransportDecision
```

Suggested fields:

```text
transport_mode
carrier_mode
current_gate_section
next_staging_section
preload_queue
view_gate_state
hidden_gate_state
prefetch_lane_state
section_verified_before_display
transition_blank_ms
reader_prefetch_ahead_ms
reverse_buffer_depth
gate_lock_status
fail_closed_reason
unsafe_acceptance_count
```

This matches the current repo direction and should not be treated as a new unrelated system.

---

## 16. Part 2 conclusion

Part 2 decides:

```text
- the preferred internal transport is folded, not long-straight
- the player uses A/B physical double-buffering
- apparent instant switching comes from preloading and optical blanking
- the reader/prefetch lane must verify upcoming sections before display
- individual pages/cards, chains, folded carriers, two-track shuttles, and magnetic guides are options, but not all equal
- the strongest baseline is folded indexed carrier + A/B staging + fail-closed validation
- reverse/seek should start limited, not arbitrary
- physical proof is still not claimed
```

Part 3 should cover:

```text
A/B Gate, View Gate, Shutter, Illumination, and Optics
```

Specifically:

```text
- visible gate geometry
- hidden gate geometry
- one-gate vs two-gate optical design
- shutter/illumination blanking
- LED light guide
- physical section flatness
- optical window
- folded optics/prism/mirror path
- colour/brightness consistency
- human-visible transition quality
- what the simulator should model visually
```
-----

# AMCF Physical Player Design and Structure Dossier  
## Part 3 — A/B Gate, View Gate, Shutter, Illumination, and Optics

## 1. Purpose of Part 3

Part 1 defined the physical AMCF player object.

Part 2 defined the internal transport architecture:

```text id="x1oa9p"
dynamic folded-path A/B staged indexed-section transport
```

Part 3 now defines the **presentation core** of the physical player:

```text id="ijddbo"
A/B gates
visible view gate
hidden staging gate
shutter / illumination blanking
physical section flatness
optical path
front viewing window
```

This is the part of the player where the physical AMCF carrier stops being merely “transported” and becomes **visible physical/optical playback**.

The earlier files already establish that the corrected player direction is not a long roller, not a normal LCD/OLED screen, and not a scanner-board object. It should be a compact tablet-like physical/optical player with folded internal media path, side cartridge, dynamic indexed feed, fixed optical view gate, compact folded optics, digital electronics for control/audio/sync, and physical/optical visual playback.

So Part 3 focuses on the central question:

```text id="exmr2z"
How does a prepared physical AMCF section become the visible image,
and how does the device switch to the next section without showing ugly mechanical movement?
```

---

## 2. Core presentation principle

The physical player should not show the viewer the transport process.

The viewer should not see:

```text id="7ywvk5"
paper sliding
paper jumping
misalignment
gate travel
carrier gaps
mechanical handoff
```

The viewer should see:

```text id="sbca8y"
stable physical image A
→ tiny controlled blank / optical transition
→ stable physical image B
```

This follows the already-established A/B staging logic:

```text id="bdfvbk"
Current visible section = held at View Gate A
Next required section = preloaded/aligned at hidden Gate B
At update time = shutter/illumination hides transition
Gate B becomes visible
Old section moves to return/park path
Next section is preloaded again
```



The physical player therefore needs two things at once:

```text id="3rzhha"
1. mechanical precision
2. optical concealment
```

Mechanical precision gets the next section ready.

Optical concealment hides the switch.

---

## 3. Difference between scan gate, view gate, and staging gate

Earlier physical-reader work used language like:

```text id="ylwpck"
scan gate
CIS line sensor
LED bar
timing/index/colour/hash lanes
```

That belongs mainly to the reader/recovery branch. `Physical design.txt` describes this older reader device as an indexed cartridge/stack moving through an alignment/feed stage, near-contact scan/view gate, CIS/line-scan sensor, LED, controller/cache, and PC/software playback.

For the physical-player branch, we should separate the gates more clearly:

```text id="4rx13h"
Scan gate:
reads or verifies physical AMCF lanes.

Hidden staging gate:
pre-aligns the next physical section before display.

Visible view gate:
holds the physical section at the exact optical presentation plane.
```

They may be physically near each other, and a future hybrid appliance may combine them, but conceptually they are different.

### Scan gate

```text id="tulbc6"
Purpose:
read lanes, verify identity, validate section safety.

Main concern:
data recovery / validation.
```

### Hidden staging gate

```text id="g2km7n"
Purpose:
prepare the next section before it becomes visible.

Main concern:
pre-alignment / readiness / timing.
```

### Visible view gate

```text id="d07cv2"
Purpose:
present the physical image to the viewer.

Main concern:
flatness, registration, illumination, optical quality, dwell stability.
```

The player must not treat the visible view gate as just another scanner position. It is the **physical image plane**.

---

## 4. Visible view gate

The visible view gate is the most important physical presentation component.

It is where the current AMCF physical section is held while it is visible.

The view gate must provide:

```text id="n4a86g"
- exact section position
- flatness
- registration lock
- no visible drift
- controlled illumination
- optical focus plane
- stable dwell duration
- safe release after transition
```

The section should not move while it is being visibly presented.

A correct view-gate state is:

```text id="huf7cy"
section inserted
→ section registered
→ section flattened or tensioned
→ section locked
→ section illuminated
→ section optically visible
→ section held until next AMCF update event
```

An incorrect view-gate state is:

```text id="d84cug"
section still moving
section partly aligned
section curled
section slipping
section not verified
section displayed before lock
```

The fail-closed rule should be:

```text id="j0k8au"
If the section is not locked, aligned, and verified,
do not display it.
```

---

## 5. View gate physical requirements

The view gate should be treated like a precise presentation frame, not a loose transport gap.

It needs:

```text id="f9sh0g"
1. edge guides
2. registration stops
3. pressure or tension control
4. anti-curl support
5. optical aperture
6. illumination window
7. section release path
8. sensor feedback
```

## 5.1 Edge guides

Edge guides keep the section laterally aligned.

They should prevent:

```text id="nlg9d9"
- left/right drift
- rotation
- skew
- section walking out of frame
```

## 5.2 Registration stops

Registration stops define the final position.

They should support:

```text id="o55zvo"
- repeatable alignment
- known optical position
- known coordinate origin
- predictable view window crop
```

## 5.3 Pressure or tension control

The section must be held flat enough for viewing.

Possible methods:

```text id="5nokmn"
- light pressure frame
- edge clamp
- tensioned carrier
- vacuum-like conceptual hold-down
- electrostatic/magnetic holding as a research branch
```

Do not claim one final method yet.

## 5.4 Anti-curl support

Ultra-thin paper or film can curl, bow, wrinkle, or shift. The view gate must reduce this.

Possible support:

```text id="r1t4ed"
- backing plate
- transparent pressure layer
- edge tension
- shallow curved guide before gate
- humidity/material control in later real hardware
```

## 5.5 Optical aperture

The aperture defines what the viewer sees.

It should hide:

```text id="gc32lm"
- timing lanes if not meant to be visible
- edge marks
- carrier margins
- transport holes or guides
- mechanical supports
```

But the design may optionally expose some technical lanes in a service mode.

## 5.6 Illumination window

The illumination system should light the physical image area evenly.

It should avoid:

```text id="p708m9"
- visible hot spots
- flicker
- uneven colour
- edge darkening
- showing transport movement during switching
```

---

## 6. Hidden staging gate

The hidden staging gate prepares the next physical section while the current one is still visible.

It should provide:

```text id="eaekel"
- pre-positioning
- rough alignment
- fine alignment
- verification confirmation
- readiness status
- fast handoff or optical switch path
```

The hidden staging gate is not necessarily visible to the user. It exists so the device does not need impossible instant media travel.

A typical hidden-gate cycle:

```text id="ac411w"
1. Receive next section from preload path.
2. Read/confirm section index.
3. Confirm timing match.
4. Confirm hash/checksum or safe degraded state.
5. Align section to staging marks.
6. Hold section ready.
7. Signal scheduler: next section ready.
```

If the hidden gate cannot verify the section in time, the player must not display it.

Fail state:

```text id="rsn270"
next section not verified by preload deadline
→ do not transition
→ hold current section if safe
→ blank/pause/fail closed
```

---

## 7. A/B gate design models

There are several ways to interpret A/B staging physically.

Part 3 should keep them open, because the repo/simulator should not overclaim a final mechanical layout.

## Model 1 — True dual visible-capable gates

```text id="gpjtt6"
Gate A and Gate B are both capable of becoming optically visible.
```

Sequence:

```text id="422qp8"
A visible / B hidden
→ blank
→ B visible / A hidden
→ preload A
→ blank
→ A visible / B hidden
```

Advantages:

```text id="phkv1s"
- clean physical double-buffering
- next section can be fully ready
- very short visible switch
```

Problems:

```text id="d7efc1"
- harder optics
- both gates need equal image quality
- more thickness/complexity
- illumination must match both gates
```

Use case:

```text id="plly3z"
best high-end conceptual model
```

## Model 2 — One true view gate plus hidden staging gate

```text id="fkycjb"
Only one gate is optically visible.
Hidden staging prepares the next section near the view gate.
At transition, the new section is transferred into the single view gate.
```

Advantages:

```text id="pgarqi"
- simpler optical path
- one calibrated image plane
- consistent brightness/focus
```

Problems:

```text id="2xmpx0"
- physical transfer must be fast
- requires stronger blanking
- alignment must complete quickly
```

Use case:

```text id="6q2n7t"
strongest practical baseline for early hardware thinking
```

## Model 3 — Sliding optical selector

```text id="5uq0pq"
Both A and B are physically staged,
but an optical selector / shutter / mirror path determines which one is visible.
```

Advantages:

```text id="tu075m"
- media movement can happen away from visible path
- optical switching may be faster than media switching
```

Problems:

```text id="mwjza9"
- optical complexity
- possible brightness/focus differences
- more calibration
```

Use case:

```text id="rf9jh2"
future advanced concept
```

## Model 4 — Layered optical overlay

```text id="1xbhkt"
Background or static layer stays fixed.
Dynamic component layers update independently in smaller staging gates.
```

This is the more AMCF-native version.

Advantages:

```text id="0is58o"
- closer to component-based AMCF
- static content does not need to move
- dynamic regions can update separately
```

Problems:

```text id="q5ebit"
- much more complex
- alignment between layers is difficult
- optical overlay quality is hard
- physical colour/alpha handling is unresolved
```

Use case:

```text id="74dd8j"
future research branch,
not the first physical-player simulator baseline
```

The uploaded notes already distinguish the simpler model, where each physical section is a precomposited AMCF visible state, from the harder AMCF-native version, where separate physical tracks/layers represent different components.

---

## 8. Recommended gate baseline

For the dossier and simulator, the correct baseline is:

```text id="qe7zxs"
one visible view gate
+ one hidden staging gate
+ abstract A/B state switching
```

This gives the best balance:

```text id="znwcbe"
- preserves the A/B staging logic
- avoids overclaiming final dual-gate optics
- keeps simulation clean
- supports later high-end dual-gate or optical-selector designs
```

So the documentation should say:

```text id="t4j9qx"
The current simulator models A/B staging abstractly.
It does not prove which physical gate geometry is final.
```

This is important because the repo already contains simulator fields for A/B staging and fail-closed decisions, but those are software/hardware-support abstractions, not real hardware validation. The public claim boundaries also explicitly forbid claiming physical proof, manufacturing readiness, or physical Level 5 validation.

---

## 9. Shutter / illumination blanking

The shutter/illumination system is how the player hides the mechanical transition.

The transition should not be described as magic instant paper movement.

It should be described as:

```text id="qv8f3z"
a tiny controlled optical blanking interval
```

Possible blanking methods:

```text id="5fv1m7"
1. turn off / dim illumination briefly
2. mechanical micro-shutter
3. optical shutter layer
4. moving mask
5. LED strobe timing
6. combined dimming + shutter
```

The notes already identify shutter/illumination blanking as a requirement for no-gap transition, along with pre-aligned next section, dwell/view gate, index lock, sensor feedback, short transport distance, and buffering queue.

The simplest simulator model is:

```text id="pa4ufv"
transition_blank_ms
```

Example:

```text id="zkb2x5"
visible A
→ transition_blank_ms = 8
→ visible B
```

The simulator should not claim that `8 ms` is physically proven. It should treat it as a configurable design parameter.

---

## 10. Illumination design

The illumination system should support stable physical viewing.

It should be treated as a presentation subsystem, not just a scanner LED.

Possible illumination approaches:

```text id="9wcx7p"
- LED light guide
- backlight-style illumination
- edge-lit panel
- controlled front illumination
- short strobe during dwell
- dim/blank during transition
```

Requirements:

```text id="gztwbi"
- even brightness
- stable colour temperature
- no visible flicker
- low heat near carrier
- no paper/film damage
- fast blanking response
- repeatable exposure between sections
```

The previous design notes already included modern compact-device ideas such as high-CRI micro-LED light guide, MEMS or micro-shutter for exposure/dwell control, encoder-controlled micro motor, piezo/electrostatic inchworm feed, and embedded controller for audio sync and transport timing.

For AMCF, illumination has two roles:

```text id="0e00nz"
1. make the current physical section visible
2. hide or soften transitions
```

So it is not just a lamp. It is part of the timing system.

---

## 11. Optical path

The optical path transfers the physical section at the view gate to the front viewing window.

The earlier design correction said the side cutaway should show:

```text id="f5g6sn"
cartridge slot
→ alignment/index stage
→ folded U-turn transport
→ fixed view gate
→ illumination/shutter
→ compact folded optics
→ front viewing window
→ return/park path or take-up/stack
```



The optical path should therefore be compact and folded.

Possible optical structures:

```text id="rra0r3"
1. direct viewing window over the physical section
2. magnifier lens over the view gate
3. folded mirror/prism path
4. light-guide + viewing aperture
5. service-window mode for debug
```

## 11.1 Direct viewing

```text id="6srsdx"
physical section sits directly behind front window
```

Advantages:

```text id="5kn787"
- simplest
- least optical complexity
- easiest to understand
```

Problems:

```text id="t4xrjw"
- transport must sit directly under viewing window
- device may become thicker/wider
- gate movement may be harder to hide
```

## 11.2 Magnified view gate

```text id="11ua9b"
physical section is smaller than the front image,
and optics enlarge it.
```

Advantages:

```text id="kpmavl"
- smaller physical sections
- smaller carrier
- larger apparent viewing area
```

Problems:

```text id="et8g45"
- focus/aberration issues
- brightness loss
- alignment becomes more sensitive
```

## 11.3 Folded optical path

```text id="1fsie9"
physical section is inside the device,
and mirrors/prisms fold the image path to the front viewing window.
```

Advantages:

```text id="htmmbm"
- supports tablet-like shape
- separates transport plane from viewing plane
- hides more mechanism internally
```

Problems:

```text id="py2921"
- more optical complexity
- more calibration
- brightness/colour consistency harder
```

Recommended baseline:

```text id="9s8yn7"
compact folded optics as design direction,
without committing to final lens/prism geometry.
```

---

## 12. Front viewing window

The front viewing window is the user-facing “display,” but it is not a normal digital screen.

It should be described as:

```text id="k3c4kq"
physical/optical viewing window
```

Not:

```text id="4iuafq"
LCD screen
OLED screen
normal video display
```

The window’s role:

```text id="7rpp8v"
- frames the physical AMCF image
- hides transport edges
- protects internal media path
- gives the player a tablet-like front surface
- provides stable viewing geometry
```

The viewing window may include:

```text id="b4k1tq"
- transparent cover
- aperture mask
- lens or magnifier
- anti-reflection layer
- service/debug markings in prototype only
```

It should not expose:

```text id="gcedrt"
- raw carrier path
- misaligned section edges
- feed rollers
- gate clamps
- timing lanes unless intentionally shown
```

---

## 13. Handling AMCF lanes at the view gate

AMCF sections may include lanes such as:

```text id="sg82k1"
timing/index
registration
image/component payload
colour registry
metadata
hash/checksum
```

The physical plan and `Physical design.txt` both preserve this machine-readable section concept: AMCF sections are not normal picture pages; they include timing/index/marker lanes, image or component payload area, colour registry, metadata, and hash/checksum.

At the visible view gate, the design must decide:

```text id="glbv2l"
Are technical lanes visible to the user,
or are they masked away?
```

Recommended rule:

```text id="l1jhgz"
Normal playback:
show only image/presentation area.

Service/diagnostic mode:
optionally expose lanes or overlays.
```

So the optical aperture should normally crop to:

```text id="81nh8c"
AMCF visible image area
```

while the reader/prefetch path reads:

```text id="ee2cpx"
timing/index lane
registration lane
colour registry lane
metadata lane
hash/checksum lane
```

This prevents the device from looking like a raw scanner during normal playback.

---

## 14. Colour and brightness consistency

The physical player must avoid visible brightness/colour jumps between sections.

Potential causes:

```text id="e7lwam"
- different ink density
- section material differences
- illumination angle changes
- gate A/Gate B mismatch
- dust/surface wear
- optical path variation
- colour registry degradation
```

The player should handle this through:

```text id="lwmcp2"
- colour registry/header data
- per-section calibration metadata
- consistent illumination
- view-gate alignment
- optional warning/degraded-colour state
```

The virtual reader/emulator branch already includes degraded colour, hash mismatch, missing marker, rescan-needed, accepted-with-degraded-colour, rescan-required, and rejected-fail-closed decision states in the planning context.

For physical playback, degraded colour might be allowed only if:

```text id="f8j8op"
the section identity is valid
the image is safe to display
the degradation is marked
the scheduler/player records the degraded state
```

But critical identity/registration/hash failure must fail closed.

---

## 15. Human-visible transition quality

The goal is not just mechanical correctness. The visible output should feel continuous enough.

Transition quality depends on:

```text id="1h7rsc"
- how long the blank interval is
- whether brightness returns consistently
- whether the next image is aligned
- whether the section is flat
- whether the optical focus changes
- whether the viewer notices gate switching
- whether audio remains synced
```

A transition should be judged by:

```text id="el7dcq"
1. no visible paper travel
2. no wrong frame/section flash
3. no partial section display
4. no visible skew jump
5. no severe brightness flicker
6. no unsafe unverified display
7. audio does not drift beyond allowed tolerance
```

This can be simulated first.

The simulator can model:

```text id="r5p2jj"
transition_blank_ms
section_verified_before_display
gate_alignment_status
illumination_state
view_gate_state
audio_sync_state
fail_closed_reason
```

It should not claim real human perceptual success until physical testing exists.

---

## 16. Gate and optics failure modes

Part 3 should record failure modes specific to the gate/optics area.

```text id="jmm748"
- visible gate not locked
- hidden gate not ready
- section curled at view gate
- section skewed
- wrong section in staging gate
- transition blank too short
- shutter stuck open
- shutter stuck closed
- illumination flicker
- illumination mismatch between gates
- optical path misaligned
- focus plane mismatch
- dust/scratch visible
- section edge visible in aperture
- metadata lane accidentally visible
- gate switch produces partial image
```

Fail-closed examples:

```text id="7w5fca"
wrong section in hidden gate
→ do not transition

hidden gate not verified by deadline
→ hold or blank

view gate not locked
→ do not illuminate

shutter cannot blank
→ do not perform visible switch

hash/checksum critical failure
→ reject section / fail closed
```

The public repo language already requires avoiding claims of real physical proof, and this section should preserve that caution.

---

## 17. Recommended simulator abstraction for Part 3

The simulator should not try to become CAD.

It should model states and decisions.

Recommended classes or structures:

```text id="iptrsg"
ViewGateState
HiddenGateState
OpticalPresentationState
IlluminationState
TransitionBlankingState
GateSwitchDecision
PhysicalDisplayReadiness
OpticalFailureState
```

Recommended fields:

```text id="4ncbii"
visible_gate_section_id
hidden_gate_section_id
visible_gate_locked
hidden_gate_ready
section_flatness_status
registration_status
illumination_state
shutter_state
transition_blank_ms
optical_path_mode
front_window_mode
technical_lanes_visible
section_verified_before_display
display_allowed
fail_closed_reason
```

Decision rule:

```text id="v20qgv"
display_allowed = true only if:
- section identity is verified
- required lanes are valid
- view gate is locked
- section is aligned
- shutter/illumination state is safe
- no critical fail-closed condition exists
```

---

## 18. Recommended wording for the dossier

The final description for this part should be:

```text id="3ne2lq"
The AMCF physical player presents material AMCF sections through a controlled physical/optical view gate. The current section is held flat, aligned, illuminated, and optically presented through the front viewing window. The next section is preloaded and verified at a hidden staging gate. At the AMCF update timestamp, the player uses a brief shutter or illumination blanking interval to hide the transition, then presents the next verified section. This gives near-instant visible switching without requiring physically impossible instant paper movement. The exact gate geometry remains future hardware research; the current software model should represent A/B staging, gate readiness, blanking, optical state, and fail-closed behaviour.
```

This preserves the core logic.

---

## 19. What Part 3 decides

Part 3 decides:

```text id="g0h8z1"
- the view gate is the physical image plane
- the hidden gate is the preloaded next-state staging point
- A/B staging should remain abstract until hardware geometry is chosen
- the shutter/illumination system hides mechanical transition
- the front window is physical/optical, not normal digital display
- normal playback should hide technical lanes
- reader/prefetch may read lanes before visible display
- gate/optics failures must fail closed
- simulator should model states, not CAD
```

---

## 20. What remains open

Still unresolved:

```text id="54j9kq"
- exact gate geometry
- one-gate vs two-gate physical implementation
- exact shutter type
- exact illumination type
- exact optical magnification
- exact folded optics geometry
- exact physical section size
- exact visible window size
- exact blanking duration that feels acceptable
- whether component-layer optical overlay is practical
- how real materials behave under repeated gate locking
```

These belong to future hardware research or a later simulator refinement, not current proof claims.

---

## 21. Part 4 should cover next

Part 4 should cover:

```text id="bfi0tz"
Cartridge, Carrier, and Section Anatomy
```

Specifically:

```text id="yf3c18"
- cartridge form
- indexed thin-section carrier
- connected carrier vs individual sections
- AMCF section layout
- timing/index lane
- registration lane
- image/component payload area
- alpha/mask handling
- colour registry lane
- metadata/transform lane
- hash/checksum lane
- physical dimensions as abstract parameters
- how the section supports prefetch, display, and recovery
```

Part 3 stops here because the A/B gate, view gate, shutter/illumination, and optical presentation model are now defined.
-----
_+ Part 4_+

# AMCF Physical Player Design and Structure Dossier  
## Part 4 — Cartridge, Carrier, and Section Anatomy

## 1. Purpose of Part 4

Parts 1–3 defined:

```text id="p4a9f1"
Part 1 — physical player boundary, product form, visual language, and core architecture
Part 2 — internal transport architecture
Part 3 — A/B gate, view gate, shutter, illumination, and optics
```

Part 4 now defines the **physical media object** that the player handles:

```text id="r5kd2v"
cartridge
→ carrier
→ indexed sections
→ lanes
→ payload
→ metadata
→ validation marks
```

This is important because the physical player is not moving ordinary photographs, normal paper pages, or a normal film strip.

The uploaded physical-design baseline already says the carrier should look like a thin stack or cartridge of AMCF “sections,” and that each section should have machine-readable lanes: timing/index/marker lane, image/frame area, colour strip, metadata, and hash/checksum. Physical design

So Part 4 answers:

```text id="ncmcpb"
What exactly is inside the cartridge?
What is a physical AMCF section?
What lanes does it carry?
How does this support reader recovery, player prefetch, and physical/optical display?
How does it avoid becoming a normal film strip or fixed-FPS page flipbook?
```

---

## 2. Core media boundary

The correct media boundary is:

```text id="z9ziyx"
AMCF physical media is an indexed physical carrier
containing machine-readable AMCF sections,
not a normal picture page sequence.
```

It is not:

```text id="ue61pd"
- normal film strip
- normal video frames
- normal printed screenshots
- one long ribbon-first design
- loose unmarked pages
- a hand-flipped book
```

`Physical design.txt` explicitly says the target is an **indexed AMCF section carrier**, not normal film strip, not normal video frames, and not a one-long-ribbon-first design. Physical design

The carrier must preserve AMCF’s logic:

```text id="yx3o0w"
source video
→ digital AMCF component/update schedule
→ physical manifest
→ indexed physical sections
→ reader recovery and/or player execution
```

So the physical media must serve three roles:

```text id="u6s6o6"
1. printer/output role
   It can be generated from digital AMCF.

2. reader/recovery role
   It can be scanned/validated/recovered.

3. player/execution role
   It can be physically/optically presented according to AMCF timing.
```

---

## 3. Cartridge vs carrier vs section

The vocabulary should be strict.

```text id="dxrfpq"
Cartridge:
The protective container or loading object inserted into the player/reader.

Carrier:
The ordered physical media inside the cartridge.

Section:
One indexed AMCF physical unit on the carrier.

Lane:
A machine-readable or presentation sub-area inside a section.

Payload:
The image/component/visible-state information carried by a section.
```

This prevents confusion.

Do not use:

```text id="w0qr6s"
page
frame
photo
film cell
slide
```

as the primary terms unless you are making an analogy.

Use:

```text id="d8sd7c"
section
indexed section
carrier section
physical AMCF section
```

because AMCF sections may contain component payloads, masks, transforms, metadata, timing, colour registry, and validation data — not just a picture.

---

## 4. Cartridge role

The cartridge is the user-handled object.

It should provide:

```text id="axoeu6"
- protection for thin sections
- correct orientation
- carrier ID
- insertion/removal handling
- dust/light protection
- alignment reference
- manifest/header access
- safe feed into the internal transport
```

The cartridge should make the system feel like a modern protected media format, not loose paper handling.

Recommended cartridge concept:

```text id="y8awaa"
side/top-loaded AMCF cartridge
containing an indexed thin-section carrier
with manifest/header region
and physical alignment features
```

The earlier design baseline described a replaceable thin-page cartridge, motor/encoder indexed feed, near-contact scan gate, CIS/line-scan sensor, LED illumination, visible/service window, USB connection, and software reconstruction. Physical design

For the newer physical-player branch, the cartridge should be reused but redirected:

```text id="4s7y43"
reader branch:
cartridge → scan/recover → PC/software playback

player branch:
cartridge → prefetch/verify → staged view gate → physical/optical playback
```

So the cartridge is shared, but the appliance behaviour differs.

---

## 5. Cartridge header / manifest zone

The cartridge should have a header/manifest region.

This may be:

```text id="ts026e"
- first physical section
- separate header strip
- printed machine-readable header
- embedded marker area
- digital sidecar manifest in software
- combined physical + digital manifest
```

The header should identify:

```text id="fkjy3q"
- carrier ID
- source AMCF archive ID
- section count
- section order
- carrier format version
- lane schema version
- material profile
- colour registry profile
- physical playback requirements
- recovery/fail-closed policy
```

The software manifest should be the stronger canonical object. The physical cartridge header helps the reader/player identify and verify the inserted media.

Recommended rule:

```text id="96qbdc"
The physical header helps recognition.
The digital AMCFPhysicalManifest defines the full contract.
```

---

## 6. Carrier forms

There are several possible carrier forms.

## 6.1 Folded indexed carrier

```text id="o3yosr"
A connected, folded, indexed carrier stored inside the cartridge.
```

This is the strongest match for the compact tablet-like A/B folded-path player.

Advantages:

```text id="esmytu"
- keeps section order
- easier prefetch
- easier return/take-up path
- less loose-page handling
- works with folded U/S/three-pass path
```

Problems:

```text id="81ou83"
- bending fatigue
- tension control
- possible curl
- material must tolerate repeated folded movement
```

Best classification:

```text id="2fz932"
Preferred physical-player carrier candidate.
```

## 6.2 Indexed thin-section stack

```text id="2soiw7"
A stack of discrete thin sections/cards/pages in a cartridge.
```

Advantages:

```text id="y2hfzx"
- close to original page idea
- each section is separable
- easier conceptual replacement of damaged sections
```

Problems:

```text id="9xnzbc"
- page selection is harder
- double-feed risk
- reverse/seek more complex
- high-speed smooth playback harder
```

Best classification:

```text id="ud5iuu"
Useful for reader/recovery, bench prototype, or lower-speed player concepts.
```

## 6.3 Linked chain carrier

```text id="vaczsv"
Individual sections mounted on a chain or linked transport.
```

Advantages:

```text id="f8lyza"
- preserves page-like sections
- keeps ordering
- gives mechanical indexing points
```

Problems:

```text id="xx9wmg"
- adds bulk
- hinges/links wear
- spacing creates dead travel
- harder to keep section flat at view gate
```

Best classification:

```text id="4d4ugv"
Research candidate, not the default.
```

## 6.4 Ribbon / strip comparison

A continuous ribbon may be studied only as a comparison transport.

It should not become the primary framing.

```text id="2y7haz"
continuous ribbon = comparison/reference candidate
indexed thin sections = primary AMCF physical model
```

The earlier physical plan already established that the continuous ribbon model can remain a comparison transport, but the primary physical AMCF model should remain indexed thin sections/pages. physical plan(4)

---

## 7. Physical section anatomy

A physical AMCF section should have a predictable layout.

Baseline layout:

```text id="mva674"
┌──────────────────────────────────────────────┐
│ TIMING / INDEX / REGISTRATION LANE           │
├──────────────────────────────────────────────┤
│                                              │
│       AMCF IMAGE / COMPONENT PAYLOAD AREA    │
│                                              │
├──────────────────────────────────────────────┤
│ COLOUR REGISTRY | METADATA | HASH / CHECKSUM │
└──────────────────────────────────────────────┘
```

This matches `Physical design.txt`, which describes a timing/index/marker lane, AMCF image/frame area, colour strip, metadata, and hash/checksum. Physical design

A stricter section anatomy:

```text id="qph72h"
1. timing/index lane
2. registration lane
3. image/component payload area
4. alpha/object mask lane or encoded mask reference
5. colour registry lane
6. metadata/transform lane
7. checksum/hash lane
8. optional service/debug marks
```

This matches the virtual-cartridge model already planned in the uploaded physical-design file: cartridge ID, section count, section index, section payload, timing/index lane, registration lane, component payload lane, alpha/object mask lane, colour registry lane, metadata/transform lane, and hash/checksum lane. Physical design

---

## 8. Timing / index lane

The timing/index lane identifies where the section belongs in the AMCF physical schedule.

It should contain or encode:

```text id="k5o9vw"
- section index
- section ID
- carrier ID reference
- timestamp start
- timestamp end or dwell duration
- sequence order
- update-event marker
- optional previous/next section reference
```

Reader use:

```text id="m88hcs"
recognize section order
detect missing sections
detect wrong section
recover schedule
```

Player use:

```text id="6tm0ee"
confirm this is the next expected section
preload it before the update timestamp
block display if section index is wrong
```

Printer/output use:

```text id="cfhe8a"
print correct lane marks
place marks inside layout tolerance
include schedule information from manifest
```

Fail-closed rule:

```text id="t58gst"
If the required section identity or order cannot be verified,
do not display the section.
```

---

## 9. Registration lane

The registration lane helps the reader/player know whether the section is positioned correctly.

It should support:

```text id="mapglr"
- skew detection
- lateral alignment
- vertical alignment
- crop/origin reference
- view-gate lock confirmation
- scan correction
```

Possible marks:

```text id="s6qh4w"
- corner marks
- edge bars
- fiducials
- timing bars
- alignment ticks
- gate lock marks
```

Reader use:

```text id="znzu82"
deskew
crop
map payload coordinates
detect deformation
```

Player use:

```text id="wmsskr"
verify section is flat/aligned before illumination
confirm view-gate readiness
prevent partial/misaligned display
```

The view gate should not illuminate a section until registration is good enough.

---

## 10. Image / component payload area

This is the central payload region.

Important correction:

```text id="l2de3n"
The physical section should remain rectangular,
even if the object/component inside it has an alpha mask.
```

The uploaded file explicitly says the preferred model is a rectangular AMCF section containing tight tree bounding box, tree image/texture, alpha mask/cut-out mask, transform/position data, timing/index metadata, and hash/checksum — not a whole page with blank deadspace and not a physical tree-shaped cut-out. Physical design

So the rule is:

```text id="9j5c76"
Digitally cut out the object with mask/alpha.
Physically keep the section rectangular for scanning, registration, and transport.
```

This is crucial.

Bad design:

```text id="1a903x"
whole page containing tiny object and lots of blank deadspace
```

Also bad as primary design:

```text id="tsr2mz"
physical object-shaped cut-out
```

Preferred:

```text id="73szod"
rectangular indexed section
containing tight component payload
plus mask/alpha and transform metadata
```

---

## 11. Component payload types

The payload area may contain different kinds of AMCF physical content.

## 11.1 Precomposited visible-state payload

```text id="6xk57p"
One physical section = one visible state to display.
```

This is the simplest physical-player model.

Best for:

```text id="f7t8ao"
- first simulator
- physical-player concept docs
- A/B staged switching
- visible-state playback
```

## 11.2 Component payload

```text id="r4hb4w"
One physical section = one component/object/region payload.
```

Example:

```text id="m1s042"
tree component
water ripple component
leaf cluster component
background patch
```

This is more AMCF-native, because digital AMCF is based on independently updating visual components.

But physical display becomes harder, because the player must optically composite multiple physical components.

Best for:

```text id="hju7a2"
future high-end AMCF-native physical branch
```

## 11.3 Residual / tile payload

```text id="t6uzfz"
section carries a small residual/tile update
rather than a whole object or visible state
```

Useful for:

```text id="uc363p"
- compression research
- reader recovery
- digital reconstruction
```

Harder for:

```text id="04j2zj"
direct physical/optical playback
```

Recommendation:

```text id="rcbbk8"
First physical-player simulator:
precomposited visible-state sections.

Physical carrier/recovery model:
support component payload sections.

Future high-end physical AMCF:
research layered component optical composition.
```

---

## 12. Alpha / mask handling

A section may include alpha/mask data.

But the mask should not require the physical sheet to be cut into object shape.

Correct model:

```text id="wznvcj"
rectangular physical section
+ printed/encoded component texture
+ alpha/object mask data
+ transform/position metadata
```

Uses:

```text id="x28iuk"
- digital reconstruction
- component compositing
- reader validation
- possible future optical overlay
```

For physical/optical direct playback, alpha handling is hard. The first player model should avoid needing physical transparency compositing unless the section is already precomposited.

So:

```text id="b73uvq"
alpha/mask lane = important for AMCF data
physical transparent overlay playback = future research
```

---

## 13. Colour registry lane

The colour registry lane gives the reader/player a colour reference.

It should support:

```text id="id7mkn"
- colour baseline
- ink/material variation detection
- degraded colour classification
- reconstruction correction
- section-to-section consistency
```

Possible content:

```text id="kcoy1x"
- colour patches
- grayscale patches
- calibration bars
- material/ink reference code
- carrier-level colour profile reference
```

Reader use:

```text id="fy4r5v"
recover colour mapping
flag degraded colour
avoid false payload interpretation
```

Player use:

```text id="qdx52r"
avoid displaying severely degraded or untrusted sections
record degraded colour state
optionally adjust illumination if supported
```

The virtual reader plan already includes colour registry valid/degraded and `accepted_with_degraded_colour` as a state, while preserving fail-closed behaviour for critical failures. Physical design

So degraded colour can be a warning state, not automatically a fatal state.

---

## 14. Metadata / transform lane

The metadata/transform lane should describe how the payload is used.

Possible fields:

```text id="mzpbic"
- component ID
- object/region ID
- original coordinates
- bounding box
- scale/rotation/transform
- layer order
- opacity/compositing mode
- timestamp reference
- source AMCF reference
- playback flags
```

For precomposited visible-state sections, metadata may be simple:

```text id="uiwfbb"
section_id
visible_state_id
timestamp
dwell_ms
```

For component sections, metadata is more important:

```text id="0z02ps"
component_id
position
mask reference
layer order
transform
```

The metadata lane allows the same physical section concept to support both:

```text id="t8t205"
simple physical visible-state playback
and
future component-native physical AMCF research
```

---

## 15. Hash / checksum lane

The hash/checksum lane protects integrity.

It should support:

```text id="3q7jms"
- section identity verification
- payload integrity
- metadata integrity
- lane corruption detection
- fail-closed safety
```

Reader use:

```text id="by1gba"
detect damaged/misread sections
request rescan
reject corrupted critical payload
```

Player use:

```text id="f9fyv7"
do not show wrong or corrupted section
block transition if the next section is unverified
```

Critical rule:

```text id="c6u9z8"
Hash/checksum mismatch must not be silently accepted for required playback sections.
```

Possible decision states:

```text id="anvy7a"
accepted
accepted_with_degraded_colour
rescan_required
rejected_fail_closed
```

These states are already part of the virtual scan-gate/lane-reader plan in `Physical design.txt`. Physical design

---

## 16. Section layout profiles

Not every section needs the exact same visible payload size, but every section should obey a known profile.

Possible profiles:

```text id="ecsd2j"
PROFILE_A — visible-state section
PROFILE_B — component payload section
PROFILE_C — calibration/header section
PROFILE_D — metadata/control section
PROFILE_E — recovery/redundancy section
```

## PROFILE_A — visible-state section

```text id="rjytlt"
Used for physical/optical playback.
Contains one precomposited visible state.
```

## PROFILE_B — component payload section

```text id="vj48te"
Used for AMCF component storage/recovery.
Contains object/region payload, mask, transform metadata.
```

## PROFILE_C — calibration/header section

```text id="5kbhfq"
Used to initialize cartridge/reader/player recognition.
Contains colour and layout reference data.
```

## PROFILE_D — metadata/control section

```text id="3gg8wo"
Used for manifest extension, schedule data, or carrier metadata.
```

## PROFILE_E — recovery/redundancy section

```text id="rexpy3"
Used for error recovery, duplicate critical metadata, or fallback.
```

This lets the system support playback and recovery without forcing every physical section to do everything.

---

## 17. Section order and dynamic AMCF timing

Because AMCF is dynamic, section order does not mean fixed video FPS.

The physical carrier should support:

```text id="xvqzqq"
- variable dwell duration
- update-event timing
- repeated hold states
- high-motion bursts with more sections
- static/slow periods with fewer sections
```

The dynamic physical rule remains:

```text id="7s2l2i"
Do not move one physical page per video frame.
Move physical media according to AMCF update events.
Hold current physical view state until a new AMCF update is needed.
```

This exact rule is preserved in `Physical design.txt`. Physical design

So a carrier sequence may look like:

```text id="pm4za4"
section_001 dwell 500 ms
section_002 dwell 80 ms
section_003 dwell 80 ms
section_004 dwell 1200 ms
section_005 dwell 40 ms
```

The player must read the schedule, not assume a fixed physical frame rate.

---

## 18. Reader-prefetch requirements

Each section must support prefetch.

That means the player/reader should be able to verify a section before it becomes visible.

Prefetch-readable data:

```text id="vpj4jk"
- section index
- timestamp/dwell data
- required/optional status
- registration marks
- hash/checksum
- metadata flags
- degraded colour status
```

The internal transport Part 2 already established that the player may need the reader to run faster than playback for metadata/index lanes, because upcoming sections must be known before visible switching.

So section design should put critical prefetch lanes where they can be read before the visible image area reaches the view gate.

Possible arrangement:

```text id="hp0gka"
leading edge:
section ID / timing / index / quick hash

main body:
payload / image / component data

trailing or lower lane:
colour registry / metadata / full checksum
```

The exact layout remains future design, but the principle is settled:

```text id="uwfept"
critical identity and readiness data should be readable early.
```

---

## 19. Display masking

At the visible view gate, not all physical section content should be visible.

Normal playback should show:

```text id="4x0pdl"
visible image / presentation area
```

Normal playback should hide:

```text id="2q4v6n"
timing/index lane
registration marks
metadata lane
hash/checksum lane
transport edges
guide holes or marks
```

Service/diagnostic mode may show them.

So the section anatomy supports two views:

```text id="hx61lb"
Machine view:
all lanes readable.

Human view:
only presentation area visible.
```

This prevents the player from looking like a scanner or raw technical sheet during normal playback.

---

## 20. Manifest relationship

Every physical section should be described by the physical manifest.

Minimum manifest data per section:

```text id="syh1jb"
section_id
section_index
section_type
timestamp_start_ms
timestamp_end_ms or dwell_ms
payload_type
payload_ref
payload_hash
lane_schema
required_lanes
display_area
prefetch_area
recovery_policy
fail_closed_policy
```

The manifest should define what each lane means.

The section should contain enough physical data to be identified and validated, but the full logical contract should live in:

```text id="177twc"
AMCFPhysicalManifest
```

This matches the unified physical I/O direction: the manifest is the shared contract between printer, reader, and player.

---

## 21. Damage and recovery policy

Sections should have recovery policies.

Possible policies:

```text id="8kdpzv"
required_fail_closed
required_rescan_once
optional_skip
optional_degraded_allowed
redundant_recoverable
calibration_required
```

Examples:

```text id="xj7mzy"
Timing/index lane missing:
required_fail_closed

Colour registry degraded:
accepted_with_degraded_colour or rescan_required

Hash mismatch:
rescan_required or rejected_fail_closed

Optional subtitle/metadata lane missing:
warning, depending on section type

Visible payload damaged:
rescan_required or rejected_fail_closed
```

The current software/virtual-reader plan already treats invalid critical lanes as unsafe and requires fail-closed decisions rather than unsafe acceptance. Physical design

The rule remains:

```text id="jhj4el"
Unsafe acceptance must remain false.
```

---

## 22. Physical material considerations

Part 4 is not the full materials dossier, but section anatomy must account for material behaviour.

Important material risks:

```text id="83q1n9"
- thickness
- curl
- humidity sensitivity
- marker contrast
- colour stability
- friction
- stiffness
- scanner reflectance
- repeated gate pressure
- bending fatigue
```

The physical-plan materials branch already judged materials by thinness, printability, colour stability, marker readability, scan contact behaviour, curvature risk, tear risk, humidity sensitivity, energy/electronics compatibility, and suitability for simulation/prototype. physical plan(4)

So each section should not be thought of as abstract paper only. It should be parameterized by material profile.

Use:

```text id="xuahyk"
MaterialProfile
```

with fields like:

```text id="dt5drt"
material_family
thickness_um
stiffness_proxy
friction_proxy
curl_risk
humidity_sensitivity
marker_contrast_proxy
colour_stability_proxy
scanner_reflectance_proxy
profile_confidence
```

This avoids pretending the physical material is solved.

---

## 23. Recommended first section model for simulator

The first simulator should use a simple section model.

```text id="glvi6f"
section_id
section_index
section_type
timestamp_start_ms
dwell_ms
payload_type
payload_label
component_id
bounding_box
has_alpha_mask
colour_status
timing_index_valid
registration_valid
metadata_valid
hash_status
display_required
recovery_policy
```

Example:

```json id="r8lpso"
{
  "section_id": "section_0008",
  "section_index": 8,
  "section_type": "visible_state",
  "timestamp_start_ms": 1200,
  "dwell_ms": 80,
  "payload_type": "precomposited_visible_state",
  "payload_label": "waterfall_visible_state_008",
  "component_id": null,
  "bounding_box": [0, 0, 1920, 1080],
  "has_alpha_mask": false,
  "colour_status": "valid",
  "timing_index_valid": true,
  "registration_valid": true,
  "metadata_valid": true,
  "hash_status": "valid",
  "display_required": true,
  "recovery_policy": "required_fail_closed"
}
```

For a component payload:

```json id="v41n4y"
{
  "section_id": "section_0041",
  "section_index": 41,
  "section_type": "component_payload",
  "timestamp_start_ms": 2400,
  "dwell_ms": null,
  "payload_type": "component_texture_mask_transform",
  "payload_label": "tree_branch_cluster",
  "component_id": "tree_cluster_03",
  "bounding_box": [412, 210, 380, 290],
  "has_alpha_mask": true,
  "colour_status": "valid",
  "timing_index_valid": true,
  "registration_valid": true,
  "metadata_valid": true,
  "hash_status": "valid",
  "display_required": false,
  "recovery_policy": "required_rescan_once"
}
```

This model is enough for software simulation without claiming physical manufacture.

---

## 24. Recommended wording for Part 4

The clean description should be:

```text id="hm39nz"
An AMCF physical cartridge contains an indexed carrier made of rectangular AMCF sections. Each section may represent a precomposited visible state, component payload, calibration/header data, metadata/control data, or recovery data. Sections are not normal video frames or ordinary printed pages. They include machine-readable timing/index, registration, colour registry, metadata/transform, and hash/checksum lanes, plus a payload area for visible-state or component data. The physical section remains rectangular for scanning, transport, registration, and player handling, even when the AMCF object inside it is digitally cut out by alpha/mask data.
```

This wording should be used in docs.

---

## 25. What Part 4 decides

Part 4 decides:

```text id="9zk8yv"
- the cartridge is the user-handled protected media object
- the carrier is indexed physical AMCF media inside the cartridge
- the section is the basic physical AMCF unit
- sections are rectangular, not object-shaped cut-outs
- sections are not normal frames/pages/film cells
- AMCF lanes are required for timing, registration, payload, colour, metadata, and integrity
- precomposited visible-state sections are best for the first physical-player simulator
- component payload sections remain important for AMCF-native recovery/future physical research
- the physical manifest defines the full contract
- fail-closed validation remains mandatory
```

---

## 26. What remains open

Still unresolved:

```text id="ntkt63"
- exact section dimensions
- exact cartridge dimensions
- exact material
- exact lane encoding
- exact colour registry pattern
- exact hash/checksum encoding
- exact physical marker shapes
- whether visible-state and component sections should share one carrier
- whether component-native physical optical overlay is practical
- how many reverse/park sections the cartridge/player should support
- how much redundancy is needed
```

These should remain open until simulator evidence and later hardware research exist.

---

## 27. Part 5 should cover next

Part 5 should cover:

```text id="vqe06v"
Reader-Prefetch, Sensors, Reverse/Seek, and Fail-Closed Logic
```

Specifically:

```text id="xjg7ha"
- reader-prefetch lane placement
- sensor roles
- section verification timeline
- wrong-section detection
- rescan/request-retry decisions
- reverse buffer logic
- seek limitations
- jam/misfeed states
- fail-closed safety model
- simulator state machine
```

Part 4 stops here because the cartridge, carrier, and section anatomy are now defined.
```
-----

# AMCF Physical Player Design and Structure Dossier  
## Part 5 — Reader-Prefetch, Sensors, Reverse/Seek, and Fail-Closed Logic

## 1. Purpose of Part 5

Parts 1–4 defined:

```text id="u1yh2g"
Part 1 — Boundary, product form, visual language, and core architecture
Part 2 — Internal transport architecture
Part 3 — A/B gate, view gate, shutter, illumination, and optics
Part 4 — Cartridge, carrier, and section anatomy
```

Part 5 now defines the **control and safety layer** that makes the physical-player concept coherent:

```text id="evliib"
reader-prefetch
sensor feedback
section verification
reverse/seek behaviour
rescan/retry decisions
jam/misfeed handling
fail-closed safety
```

This is necessary because the AMCF physical player should not merely move sections through a gate. It must know:

```text id="brbf9z"
What section is next?
Is it the correct section?
Is it verified?
Is it aligned?
Is it safe to display?
Can playback continue?
Should it pause, rescan, reverse, or fail closed?
```

The uploaded physical-design file already states that the reader changes because live reader-player mode must read ahead of the active playback gate, maintain a buffer of upcoming section metadata, timing, hash, index, and audio sync, and may need to run faster than playback for metadata/index lanes. Physical design

So Part 5 defines the safety and verification layer that sits between:

```text id="d8k11u"
physical carrier movement
and
visible physical/optical display
```

---

## 2. Core rule: verified before visible

The core rule is:

```text id="qr88gg"
A physical AMCF section must be verified before it becomes visible.
```

The player must not display a section merely because it reached the view gate.

It should display only if:

```text id="h75ok4"
- the section index is expected
- the timing/index lane is valid
- required registration is valid
- the payload is safe to show
- the hash/checksum state is acceptable
- the view gate is locked
- the section is aligned
- the shutter/illumination state is safe
- the scheduler confirms the update time
```

If any critical requirement fails, the player should not “try its best” and show the section anyway.

It should:

```text id="c7cx7v"
pause
blank
rescan
retry
hold previous safe state
or fail closed
```

The existing virtual-reader plan already uses decision states such as:

```text id="mnvnsg"
accepted
accepted_with_degraded_colour
rescan_required
rejected_fail_closed
```

and requires unsafe acceptance to remain false for invalid critical lanes. Physical design

---

## 3. Reader-prefetch role

The reader-prefetch system is not the same as the older full reader/scanner path.

The older reader path is:

```text id="b9sqxm"
physical carrier
→ scan/recover
→ reconstruct digital AMCF
→ PC/software playback
```

The player-prefetch path is:

```text id="spo0xd"
physical carrier
→ read ahead
→ verify next section
→ stage section
→ allow or block physical display
```

So the player can contain a limited reader function without becoming merely a scanner.

The prefetch reader should read enough information to answer:

```text id="zojoke"
Is this the correct next section?
Is it safe to stage?
Is it safe to display?
Is playback still synchronized?
```

It does not necessarily need to scan the entire visual payload before display, depending on the carrier model. But it must read enough critical lanes to prevent wrong or unsafe display.

---

## 4. What prefetch must read

The prefetch system should read:

```text id="o3b2ak"
- cartridge ID
- carrier ID
- section index
- timing/update marker
- dwell duration or timestamp range
- registration marks
- colour registry status
- metadata/transform flags
- hash/checksum lane
- required/optional section flag
- recovery policy
```

This matches the physical section anatomy from Part 4:

```text id="ol56wh"
timing/index lane
registration lane
image/component payload area
alpha/object mask lane
colour registry lane
metadata/transform lane
hash/checksum lane
```

The uploaded planning file already defined the virtual cartridge model with these lane categories: timing/index lane, registration lane, component payload lane, alpha/object mask lane, colour registry lane, metadata/transform lane, and hash/checksum lane. Physical design

---

## 5. Prefetch timeline

The player should not wait until the update timestamp to discover the next section.

The timeline should be:

```text id="fl0492"
1. Current section is visible.
2. Reader-prefetch identifies upcoming section.
3. Upcoming section is read enough to verify identity and safety.
4. Hidden staging gate receives and aligns the section.
5. Scheduler confirms the update timestamp.
6. Transition blanking begins.
7. Verified next section becomes visible.
8. Old section moves to park/reverse path.
```

Example timing:

```text id="a6t0sh"
AMCF update timestamp:        1200 ms
reader prefetch ahead:        120 ms
next section identified by:   1080 ms
next section staged by:       1140 ms
next section verified by:     1170 ms
transition blank starts:      1196 ms
visible switch completes:     1200 ms
```

The important rule:

```text id="nwhrst"
The player should know whether the next section is safe before the visible switch begins.
```

If the section is not verified in time:

```text id="uqxc30"
do not switch
```

---

## 6. Prefetch buffer

The player should maintain a small buffer of upcoming section states.

Recommended buffer fields:

```text id="hhu887"
section_id
section_index
expected_timestamp_ms
dwell_ms
prefetch_status
verification_status
staging_status
gate_target
hash_status
registration_status
colour_status
metadata_status
display_allowed
fail_closed_reason
```

A simple prefetch queue:

```json id="lpviym"
[
  {
    "section_id": "section_0041",
    "section_index": 41,
    "expected_timestamp_ms": 1200,
    "dwell_ms": 80,
    "prefetch_status": "read",
    "verification_status": "verified",
    "staging_status": "hidden_gate_ready",
    "display_allowed": true,
    "fail_closed_reason": null
  },
  {
    "section_id": "section_0042",
    "section_index": 42,
    "expected_timestamp_ms": 1280,
    "dwell_ms": 120,
    "prefetch_status": "pending",
    "verification_status": "not_yet_verified",
    "staging_status": "not_staged",
    "display_allowed": false,
    "fail_closed_reason": "not_verified_yet"
  }
]
```

The existing repo/design direction already called for simulator fields such as:

```text id="k6fwl9"
current_gate_section
next_gate_section
preload_queue
view_gate_state
hidden_gate_state
transition_blank_ms
section_verified_before_display
reader_prefetch_ahead_ms
reverse_buffer_depth
```

Physical design

Part 5 expands those into the reader/safety state model.

---

## 7. Sensor roles

The physical player needs sensor feedback because open-loop movement is unsafe.

It should not simply assume:

```text id="mkl0z9"
motor moved X steps
therefore correct section is visible
```

It should verify:

```text id="z7hqpu"
section identity
section position
gate lock
alignment
movement completion
staging readiness
jam/misfeed status
```

Possible sensor categories:

```text id="h4t77r"
1. cartridge presence sensor
2. section/index reader
3. registration/fiducial reader
4. gate lock sensor
5. encoder / movement sensor
6. end-stop sensor
7. tension/pressure sensor
8. jam/misfeed sensor
9. illumination/shutter status sensor
10. optional audio sync/timing monitor
```

This does not mean the current project has real sensors.

It means the simulator/docs should model the required feedback states.

---

## 8. Cartridge presence and identity sensing

Before playback, the player should know:

```text id="q304u2"
Is a cartridge inserted?
Is it seated correctly?
Is its orientation correct?
Does its carrier ID match the manifest?
Is its format supported?
```

Possible states:

```text id="k6nu0e"
NO_CARTRIDGE
CARTRIDGE_INSERTED
CARTRIDGE_UNREADABLE
CARTRIDGE_UNSUPPORTED
CARTRIDGE_RECOGNIZED
MANIFEST_MATCHED
MANIFEST_MISMATCH
```

Fail-closed rule:

```text id="vyvfgq"
If the cartridge cannot be identified or matched to a manifest,
physical playback must not begin.
```

Reader/recovery mode may still attempt diagnostic recovery, but visible player mode should remain stricter.

---

## 9. Section index sensing

The section index reader verifies that the expected section is being staged.

It checks:

```text id="kltx1t"
- section index
- section ID
- previous/next relationship
- carrier ID reference
- schedule timestamp
```

Wrong section examples:

```text id="sg3xqt"
expected section_0041 but read section_0042
expected carrier A but read carrier B
expected visible-state section but read metadata/control section
expected playback-required section but read damaged/unreadable section
```

Fail-closed rule:

```text id="zl5k6r"
Wrong section must never be displayed as if it were correct.
```

Possible decision:

```text id="8nkgs1"
wrong section staged
→ stop transition
→ hold current section if safe
→ request resync/reseek
→ fail closed if unresolved
```

---

## 10. Registration / fiducial sensing

The registration sensor verifies physical alignment.

It should check:

```text id="a7ir3b"
- skew
- lateral offset
- vertical offset
- crop origin
- view-gate placement
- section flatness proxy
```

Possible states:

```text id="f2rilb"
REGISTRATION_OK
REGISTRATION_DEGRADED
REGISTRATION_RESCAN_REQUIRED
REGISTRATION_FAIL_CLOSED
```

Display decision:

```text id="gzv0pr"
REGISTRATION_OK:
display allowed if other checks pass

REGISTRATION_DEGRADED:
possibly allowed only if within tolerance and non-critical

REGISTRATION_RESCAN_REQUIRED:
do not display yet

REGISTRATION_FAIL_CLOSED:
do not display
```

For physical/optical playback, registration matters more than in a purely digital file because misalignment can produce visible jumping, wrong cropping, or partial section display.

---

## 11. Gate lock sensing

The view gate must report whether the section is physically locked.

Possible states:

```text id="b2muw6"
GATE_EMPTY
GATE_LOADING
GATE_ROUGH_ALIGNED
GATE_FINE_ALIGNED
GATE_LOCKED
GATE_VISIBLE
GATE_RELEASED
GATE_FAULT
```

Display rule:

```text id="cm92un"
Only GATE_LOCKED or GATE_VISIBLE may allow illumination for normal playback.
```

Unsafe states:

```text id="fwn994"
GATE_LOADING
GATE_ROUGH_ALIGNED
GATE_RELEASED
GATE_FAULT
```

If the gate is not locked at the transition time:

```text id="gqfhnv"
do not illuminate
do not switch visible state
fail closed or hold previous section
```

---

## 12. Movement and encoder sensing

The transport should know whether motion completed as expected.

Movement sensing should track:

```text id="p5x9vv"
- motor/actuator command issued
- movement started
- movement completed
- expected distance reached
- section stopped
- no overtravel
- no undertravel
- no unexpected reverse movement
```

Possible states:

```text id="o1i4uo"
MOVE_IDLE
MOVE_COMMAND_SENT
MOVE_IN_PROGRESS
MOVE_COMPLETE
MOVE_TIMEOUT
MOVE_OVERRUN
MOVE_UNDERRUN
MOVE_DIRECTION_ERROR
```

Movement completion alone is not enough.

The player also needs section identity and registration verification.

So:

```text id="ggxfj1"
movement_complete = necessary
but not sufficient
```

---

## 13. Jam and misfeed sensing

The transport should detect:

```text id="v4ad0n"
- no section advanced
- double-feed
- section stuck
- section skewed
- section torn
- section arrived late
- section arrived too far
- return path blocked
- reverse buffer blocked
- cartridge feed blocked
```

Possible states:

```text id="vh1tjo"
NO_JAM
POSSIBLE_JAM
CONFIRMED_JAM
DOUBLE_FEED
MISFEED
RETURN_PATH_BLOCKED
REVERSE_PATH_BLOCKED
```

Fail response:

```text id="c1r5gz"
stop motion
blank optical path
release motor force if safe
hold current section if safe
write diagnostic event
request user intervention if needed
```

The player should not continue trying to force movement if a jam is detected.

---

## 14. Shutter / illumination feedback

The shutter and illumination system must also be part of fail-closed logic.

Possible states:

```text id="ykhx89"
ILLUMINATION_OFF
ILLUMINATION_STABLE
ILLUMINATION_DIMMED
ILLUMINATION_BLANKING
ILLUMINATION_FAULT

SHUTTER_OPEN
SHUTTER_CLOSED
SHUTTER_TRANSITION
SHUTTER_STUCK_OPEN
SHUTTER_STUCK_CLOSED
```

Fail-closed examples:

```text id="xfr0i9"
shutter stuck open during mechanical transition
→ do not move visible section

illumination cannot blank
→ do not perform visible switch

illumination unstable
→ pause or display degraded-state warning

shutter stuck closed
→ playback cannot visibly continue
```

The key point:

```text id="ayrwnt"
The optical concealment system is part of safety, not just presentation.
```

---

## 15. Reverse behaviour

Reverse must be limited and explicitly modeled.

The physical player should not claim instant arbitrary reverse across the whole carrier unless the mechanism proves it.

The first safe model is:

```text id="z2o39b"
short reverse buffer
```

The reverse buffer should hold or allow retrieval of the last N verified sections.

Possible fields:

```text id="qr2v51"
reverse_buffer_depth
reverse_buffer_sections
current_section
previous_section
reverse_available
reverse_reason_unavailable
```

Example:

```json id="f8x05q"
{
  "reverse_buffer_depth": 3,
  "reverse_buffer_sections": [
    "section_0038",
    "section_0039",
    "section_0040"
  ],
  "current_section": "section_0041",
  "reverse_available": true
}
```

If the user presses reverse:

```text id="gztopj"
1. Check previous section exists in reverse buffer.
2. Verify previous section identity.
3. Stage previous section.
4. Blank transition.
5. Display previous verified section.
6. Move current section to appropriate park/staging state.
```

If previous section is not available:

```text id="4p18xm"
do not attempt unsafe reverse
pause or require seek/reload/resync
```

---

## 16. Reverse with different carrier types

Reverse behaviour differs by carrier form.

## 16.1 Folded connected carrier

```text id="kvbmga"
Reverse may be possible by moving the carrier backward,
but tension, take-up, and alignment must remain controlled.
```

Strength:

```text id="ki7ccd"
better ordered reverse
```

Risk:

```text id="l5srcq"
tension error, curl, misalignment, rewind complexity
```

## 16.2 Individual card/section stack

```text id="kuyejx"
Reverse requires retrieving a previous section from park/return buffer
or reselecting it from the stack.
```

Strength:

```text id="ttmbsh"
clear section identity
```

Risk:

```text id="iecbdf"
harder retrieval, stack handling, misfeed
```

## 16.3 Chain/linked carrier

```text id="x7sebk"
Reverse may be mechanically regular,
but chain backlash and gate flatness remain concerns.
```

Strength:

```text id="yh9bu8"
ordered reverse path
```

Risk:

```text id="4ss1rj"
bulk, backlash, hinge wear
```

Recommendation:

```text id="ys3ile"
Claim only limited reverse/step-back in the near-term physical-player concept.
Leave arbitrary reverse/seek as future research.
```

---

## 17. Seek behaviour

Seek is harder than reverse.

Possible seek levels:

```text id="cr7q3v"
Level 0 — no seek
Level 1 — pause / resume only
Level 2 — step forward / short step back
Level 3 — seek within local buffer
Level 4 — seek by scanning/reindexing carrier
Level 5 — arbitrary physical seek
```

The first physical-player simulator should model:

```text id="k1ev5j"
pause
resume
step forward
short reverse
local-buffer seek
```

It should not claim:

```text id="prcgil"
fast arbitrary physical random access
```

unless the carrier architecture supports it.

Seek request example:

```json id="f7nmsd"
{
  "requested_timestamp_ms": 2400,
  "requested_section_id": "section_0084",
  "seek_mode": "local_buffer",
  "available": false,
  "reason": "section_not_in_reverse_or_prefetch_buffer"
}
```

---

## 18. Rescan / retry decisions

Not every failed read should immediately end playback.

The player should distinguish:

```text id="s6w8zd"
recoverable read issue
critical safety failure
mechanical fault
```

Possible outcomes:

```text id="l3yxvm"
ACCEPTED
ACCEPTED_WITH_WARNING
RESCAN_REQUIRED
RETRY_STAGING
PAUSE_AND_RETRY
REJECTED_FAIL_CLOSED
MECHANICAL_FAULT_STOP
```

Examples:

```text id="ydhh1n"
minor colour registry degradation:
ACCEPTED_WITH_WARNING

registration unclear before staging:
RESCAN_REQUIRED

hash mismatch:
RESCAN_REQUIRED or REJECTED_FAIL_CLOSED

wrong section index:
REJECTED_FAIL_CLOSED

gate not locked:
PAUSE_AND_RETRY or MECHANICAL_FAULT_STOP

jam detected:
MECHANICAL_FAULT_STOP
```

The uploaded context already uses `accepted_with_degraded_colour`, `rescan_required`, and `rejected_fail_closed` as planned decision states. Physical design

---

## 19. Fail-closed categories

Fail-closed should not be a vague phrase.

It should have categories.

```text id="v4vn12"
FAIL_CLOSED_UNVERIFIED_SECTION
FAIL_CLOSED_WRONG_SECTION
FAIL_CLOSED_HASH_MISMATCH
FAIL_CLOSED_REGISTRATION_FAILURE
FAIL_CLOSED_GATE_UNLOCKED
FAIL_CLOSED_PREFETCH_TIMEOUT
FAIL_CLOSED_SHUTTER_FAILURE
FAIL_CLOSED_ILLUMINATION_FAILURE
FAIL_CLOSED_JAM
FAIL_CLOSED_MANIFEST_MISMATCH
FAIL_CLOSED_UNSUPPORTED_CARRIER
FAIL_CLOSED_AUDIO_SYNC_LIMIT
```

Each fail-closed event should record:

```text id="f2revi"
timestamp_ms
current_section_id
next_section_id
carrier_id
reason
sensor_state
reader_state
gate_state
illumination_state
recommended_action
```

Example:

```json id="jp6q3g"
{
  "timestamp_ms": 1200,
  "current_section_id": "section_0040",
  "next_section_id": "section_0041",
  "carrier_id": "carrier_demo_001",
  "reason": "FAIL_CLOSED_UNVERIFIED_SECTION",
  "reader_state": "prefetch_timeout",
  "gate_state": "hidden_gate_not_ready",
  "illumination_state": "blanked",
  "recommended_action": "pause_and_rescan"
}
```

---

## 20. Audio sync safety

Because the player follows AMCF timing, visual playback and audio must remain synchronized.

Audio sync states:

```text id="egfwqi"
AUDIO_SYNC_OK
AUDIO_SYNC_MINOR_DRIFT
AUDIO_SYNC_RESYNC_REQUIRED
AUDIO_SYNC_FAIL_CLOSED
```

If the visual mechanism falls behind:

```text id="y181ub"
pause audio
hold visual state
resync
or fail closed
```

Do not allow:

```text id="b217me"
audio continues normally while physical visuals fall into unsafe or wrong-section display
```

The uploaded physical-design context includes audio sync in the live reader-player buffer requirements and player state model. Physical design

---

## 21. Main player safety state

The physical player should maintain a single high-level safety state.

Recommended values:

```text id="c4n1mi"
SAFE_IDLE
SAFE_READY
PLAYBACK_ALLOWED
PLAYBACK_DEGRADED
PAUSED_SAFE
RESCAN_REQUIRED
RETRY_ALLOWED
FAIL_CLOSED
MECHANICAL_STOP
UNSUPPORTED
```

Playback is allowed only if:

```text id="yp30lm"
cartridge recognized
manifest matched
current section verified
next section prefetchable or staged
view gate locked
hidden gate state known
critical lanes valid
no active jam
illumination/shutter safe
audio sync acceptable
```

This safety state should be included in every player report.

---

## 22. Simulator state machine

The Part 5 simulator should model decisions, not real hardware.

Recommended abstract state machine:

```text id="n28yoe"
NO_CARTRIDGE
→ CARTRIDGE_INSERTED
→ MANIFEST_RECOGNIZED
→ PREFETCH_CURRENT
→ VERIFY_CURRENT
→ LOAD_VIEW_GATE
→ VIEW_GATE_LOCKED
→ PLAYBACK_READY
→ PREFETCH_NEXT
→ VERIFY_NEXT
→ STAGE_NEXT
→ WAIT_UPDATE_TIMESTAMP
→ TRANSITION_BLANK
→ SWITCH_VISIBLE_SECTION
→ PARK_OLD_SECTION
→ PREFETCH_NEXT
```

Failure branch:

```text id="nqrtq3"
PREFETCH_NEXT
→ verification failure
→ RESCAN_REQUIRED
→ retry if allowed
→ FAIL_CLOSED if unresolved
```

Mechanical failure branch:

```text id="mmk2w6"
MOVE_IN_PROGRESS
→ jam/misfeed/timeout
→ MECHANICAL_STOP
→ optical blank
→ fail closed
```

Reverse branch:

```text id="oafyai"
PLAYBACK_READY
→ reverse requested
→ check reverse buffer
→ verify previous section
→ stage previous section
→ transition blank
→ switch visible section
```

---

## 23. Recommended simulator data structures

Suggested structures:

```text id="fwiu1z"
ReaderPrefetchState
SectionVerificationState
SensorFeedbackState
ViewGateSafetyState
HiddenGateSafetyState
ReverseBufferState
SeekRequestState
TransportFaultState
FailClosedDecision
PlayerSafetyState
```

Suggested fields:

```text id="sdrv5q"
cartridge_present
cartridge_id
manifest_matched
current_section_id
next_section_id
prefetch_ahead_ms
prefetch_status
section_verified_before_display
timing_index_valid
registration_valid
colour_status
metadata_valid
hash_status
view_gate_locked
hidden_gate_ready
movement_status
jam_status
shutter_state
illumination_state
reverse_buffer_depth
reverse_available
seek_available
audio_sync_state
display_allowed
fail_closed_reason
unsafe_acceptance_count
```

This directly extends the existing planned simulator fields from the uploaded context. Physical design

---

## 24. Unsafe acceptance count

The simulator and future docs should include:

```text id="o5bw47"
unsafe_acceptance_count
```

This must remain:

```text id="d469cs"
0
```

Unsafe acceptance means:

```text id="gicn59"
a section was displayed even though critical validation failed
```

Any simulator/demo that allows unsafe acceptance should fail.

Acceptance criteria:

```text id="xn6e01"
valid section accepted
degraded colour accepted only with warning
rescan-needed section not displayed until resolved
hash mismatch not silently accepted
missing marker not silently accepted
wrong section never displayed
unsafe_acceptance_count remains zero
```

This matches the virtual-reader test direction from the uploaded physical-design file. Physical design

---

## 25. Recommended wording for Part 5

The clean description should be:

```text id="td2cg3"
The AMCF physical player should use a reader-prefetch and sensor-feedback layer before physical display. The prefetch system reads upcoming section identity, timing, registration, metadata, colour, and checksum/hash information before the section reaches the visible gate. The player displays a section only after it is verified, staged, aligned, and gate-locked. Reverse and seek are limited at first to local buffer behaviour, not arbitrary physical random access. Any wrong section, unverified section, critical hash failure, gate unlock, jam, or unsafe timing condition must cause pause, rescan, blanking, mechanical stop, or fail-closed behaviour rather than unsafe display.
```

This wording should be used in docs.

---

## 26. What Part 5 decides

Part 5 decides:

```text id="r7tkh1"
- reader-prefetch is required for live physical playback
- verification must happen before visible display
- sensors are modeled as safety feedback, not proof of real hardware
- movement completion alone is not enough
- section identity, registration, gate lock, and hash/checksum matter
- reverse should start as limited local-buffer reverse
- arbitrary physical seek remains future research
- degraded colour may be warning-level
- wrong section / hash failure / unverified critical lane must fail closed
- unsafe_acceptance_count must remain zero
```

---

## 27. What remains open

Still unresolved:

```text id="s83eec"
- exact physical sensors
- exact fiducial shapes
- exact sensor placement
- exact prefetch lane geometry
- exact timing tolerances
- exact reverse buffer capacity
- exact retry/rescan count
- exact audio drift threshold
- exact hardware jam detection method
- exact recovery method after mechanical stop
```

These remain future hardware or simulator-refinement questions.

---

## 28. Part 6 should cover next

Part 6 should cover:

```text id="s0pakj"
Mechanism Family Ranking and Physical Layout Variants
```

Specifically:

```text id="b58x7h"
- folded indexed carrier
- individual card shuttle
- chain/linked carrier
- two-track A/B shuttle
- magnetic/guided tracks
- motor/encoder feed
- piezo/inchworm feed
- constant-force spring/governor/brake support
- which mechanism best fits dynamic AMCF
- which mechanism is best for simulation first
- what should remain future hardware research
```

Part 5 stops here because the reader-prefetch, sensor, reverse/seek, and fail-closed safety model are now defined.
-----

# AMCF Physical Player Design and Structure Dossier  
## Part 6 — Mechanism Family Ranking and Physical Layout Variants

## 1. Purpose of Part 6

Parts 1–5 defined:

```text id="46a0xp"
Part 1 — Boundary, product form, visual language, and core architecture
Part 2 — Internal transport architecture
Part 3 — A/B gate, view gate, shutter, illumination, and optics
Part 4 — Cartridge, carrier, and section anatomy
Part 5 — Reader-prefetch, sensors, reverse/seek, and fail-closed logic
```

Part 6 now ranks the candidate **mechanism families** and **physical layout variants**.

The goal is not to pick a final manufactured mechanism.

The goal is to decide:

```text id="u4tqvc"
Which physical mechanism family best matches AMCF logic?
Which layout should be the preferred future-player concept?
Which mechanisms are secondary?
Which mechanisms belong only in research comparison?
Which mechanism should the simulator model first?
```

The uploaded physical plan already gives an early mechanism-family ranking: motor/encoder or piezo ultrasonic feed is most controllable, piezo/electrostatic inchworm is most AMCF-index-like, spring/governor/brake is most self-contained, energy recovery is a support layer, soft actuators are experimental, and nanocellulose/cellulose carriers are material-aligned. physical plan(4)

So Part 6 should preserve that ranking, but connect it to the newer physical-player architecture:

```text id="yu0wvn"
compact tablet-like player
+ folded internal path
+ A/B staging
+ optical view gate
+ reader prefetch
+ fail-closed logic
```

---

## 2. Core decision principle

The mechanism should be chosen by AMCF needs, not by ordinary media-player habits.

AMCF physical playback needs:

```text id="842ua8"
- dynamic update timing
- indexed section movement
- preloaded next section
- stable view-gate dwell
- short visible transition
- reader-prefetch verification
- reverse/seek support if possible
- fail-closed safety
```

So the mechanism should not be judged only by:

```text id="qbso8d"
Can it move paper?
```

It should be judged by:

```text id="had2tv"
Can it move, stage, verify, hold, switch, reverse, and fail safely according to AMCF update events?
```

The uploaded physical-design file already states that for speed the best layout is probably **A/B dual-gate + folded internal path**, because it gives time to move the next section while the current one is being viewed. Physical design

---

## 3. Mechanism families to rank

The candidate families are:

```text id="d9sf7h"
1. Folded indexed carrier path
2. A/B dual-gate staged transport
3. Two-track shuttle
4. Cartridge stack + shuttle
5. Chain / indexed carrier
6. Magnetic or guided clamp tracks
7. Motor + encoder feed
8. Piezo / ultrasonic / inchworm feed
9. Constant-force spring + governor + brake
10. Energy-recovery support layer
11. Experimental soft-actuator families
12. Material-aligned carrier branch
```

Some are **layout families**.

Some are **actuator families**.

Some are **support layers**.

They should not all be treated as equal replacements.

---

## 4. Ranking criteria

The mechanism should be ranked using these criteria:

```text id="7m3g8e"
A. AMCF schedule fit
Does it support dynamic update-event playback?

B. A/B staging compatibility
Can it preload the next section while the current section is visible?

C. View-gate stability
Can it hold the section flat/aligned during dwell?

D. Prefetch compatibility
Can reader-prefetch verify upcoming sections before display?

E. Transition quality
Can it hide or reduce visible gaps?

F. Reverse/seek potential
Can it support pause, step-back, local reverse, or seek?

G. Fail-closed safety
Can it stop safely if verification fails?

H. Mechanical simplicity
Can it be simulated and documented without pretending hardware is solved?

I. Tablet-like product fit
Can it fit a compact folded internal player?

J. Future hardware plausibility
Does it remain plausible without becoming fantasy hardware?
```

The highest-ranked mechanism is not necessarily the fastest paper mover.

The highest-ranked mechanism is the one that best supports:

```text id="4497tx"
AMCF dynamic timing
+ verified staging
+ stable optical presentation
+ safe failure behaviour
```

---

## 5. Preferred overall layout

The preferred overall layout is:

```text id="gxqdm2"
Dynamic folded-path A/B staged indexed-section player
```

Expanded:

```text id="742i2t"
side/top cartridge
→ input/preload path
→ reader-prefetch lane
→ hidden staging gate
→ visible view gate
→ shutter/illumination blanking
→ folded optical path
→ front physical/optical viewing window
→ return/park/reverse path
```

This is the strongest current physical-player architecture.

Reason:

```text id="qki4bm"
- it matches AMCF dynamic update logic
- it avoids fixed-FPS page flipping
- it avoids visible transport movement
- it allows section verification before display
- it supports no-gap or near-no-gap transitions
- it can fit a tablet-like body
- it can be simulated before hardware exists
```

The uploaded physical-design file lists the same layout family: folded loop path, A/B dual-gate staging, two-track shuttle, cartridge stack + shuttle, chain/indexed carrier, and magnetic/guided clamp tracks. Physical design

---

## 6. Layout Variant 1 — Folded loop path

```text id="spkw3q"
cartridge
→ folded loop
→ prefetch
→ staging
→ view gate
→ return / take-up / park
```

Description:

```text id="e13nfg"
The carrier remains connected and moves through a folded internal path. The media enters from the cartridge, passes through the prefetch and staging area, reaches the view gate, then returns or takes up internally.
```

Strengths:

```text id="rk61bl"
- strong fit for tablet-like body
- keeps section order controlled
- reduces loose-page handling
- supports reader-prefetch
- supports folded U/S/three-pass internal path
- can support A/B staging
```

Weaknesses:

```text id="7hm590"
- carrier tension must be controlled
- repeated bending may damage material
- reverse requires controlled rewind/take-up
- curl and friction become important
```

Ranking:

```text id="0gh9e9"
Primary layout candidate.
```

Use in simulator:

```text id="odtuil"
Yes — model first as the default physical layout.
```

Why:

```text id="7up5n2"
It best connects cartridge, prefetch, staging, visible gate, return path, and compact product form.
```

---

## 7. Layout Variant 2 — A/B dual-gate staging

```text id="e03f5z"
Gate A = current visible or ready-visible section
Gate B = hidden next/preloaded section
```

Description:

```text id="j19lpt"
The device uses two gate positions or two logical gate states. One section is visible while the next is pre-aligned in a hidden staging position. At update time, shutter/illumination blanking hides the switch.
```

Strengths:

```text id="h4w1jb"
- strongest answer to the “instant speed” problem
- supports preloading
- supports verified-before-visible playback
- maps cleanly to digital double-buffering
- reduces visible travel gap
- matches AMCF dynamic update events
```

Weaknesses:

```text id="5nwjvh"
- exact geometry is unresolved
- two physical gates may complicate optics
- one-gate-plus-staging may require fast transfer
- illumination consistency must be controlled
```

Ranking:

```text id="d0nhu6"
Primary presentation/transition mechanism.
```

Use in simulator:

```text id="odotib"
Yes — model as abstract A/B gate states.
```

Important boundary:

```text id="epvxyl"
The simulator should model A/B staging logic,
not claim a final physical dual-gate geometry.
```

The physical-design file states that a real no-gap system needs pre-aligned next section, shutter/illumination blanking, dwell/view gate, index lock, sensor feedback, short transport distance, and buffering queue. Physical design

---

## 8. Layout Variant 3 — Two-track shuttle

```text id="17zm6r"
Track A = visible / ready-to-visible
Track B = preload / hidden staging
```

Description:

```text id="ej5yhd"
Two parallel or layered tracks alternate. One track presents the active section while the other prepares the next section.
```

Strengths:

```text id="pwvk9r"
- strong A/B logic
- one path can prepare while another displays
- can reduce transition delay
- maps clearly to physical double-buffering
```

Weaknesses:

```text id="awy2g2"
- wider or thicker device
- both tracks need accurate registration
- track switching is complex
- cross-track jams or misalignment become possible
```

Ranking:

```text id="3xqvj3"
Secondary high-value layout candidate.
```

Use in simulator:

```text id="hw4id1"
Yes, but as a variant of A/B staging,
not the default physical layout.
```

Best role:

```text id="7k7gqn"
Alternative A/B implementation model.
```

---

## 9. Layout Variant 4 — Cartridge stack + shuttle

```text id="7w2y6l"
section stack
→ select section
→ shuttle into staging
→ view gate
→ push back / park / recycle
```

Description:

```text id="lctjtw"
Individual sections/cards are stored in a stack or cartridge. A shuttle selects or feeds one section at a time into the staging/view path, then returns or parks it.
```

Strengths:

```text id="c6gobz"
- close to the user’s individual paper/card idea
- discrete sections are easy to conceptualize
- damaged sections may be isolated
- good for bench prototype thinking
```

Weaknesses:

```text id="apec2m"
- high risk of double-feed
- harder at speed
- harder reverse/seek
- more complex section selection
- not as smooth as connected carrier path
```

Ranking:

```text id="447gav"
Useful secondary / prototype candidate.
```

Use in simulator:

```text id="dbark4"
Yes, later as a layout variant.
Not the first default.
```

Best role:

```text id="yh4alr"
Reader/recovery prototype,
slow player demo,
or alternate cartridge model.
```

---

## 10. Layout Variant 5 — Chain / indexed carrier

```text id="2zfyyv"
individual sections mounted on chain or linked carrier
```

Description:

```text id="p3ezsu"
Physical sections are attached to a chain or linked carrier with indexing points. The chain carries them through the internal gate path.
```

Strengths:

```text id="cy5tng"
- preserves individual section identity
- maintains order
- gives regular mechanical indexing points
- could support folded internal movement
```

Weaknesses:

```text id="h2l7ga"
- bulky
- hinge/link wear
- spacing creates dead travel
- harder to keep section flat at view gate
- may look more mechanical/retro than tablet-like
```

Ranking:

```text id="wn8kt6"
Research/demo candidate.
```

Use in simulator:

```text id="f8qoxf"
Only as optional comparison.
```

Best role:

```text id="5fvgxp"
Concept exploration for linked-page transport,
not the default player path.
```

---

## 11. Layout Variant 6 — Magnetic or guided clamp tracks

```text id="bm1j2j"
guided tracks + stop gates + clamp/hold points
```

Description:

```text id="q64is7"
Magnetic, electrostatic, or mechanical guides help hold and align thin sections. Stop gates prevent wrong movement or overtravel.
```

Strengths:

```text id="oe54we"
- useful for anti-slip alignment
- useful for stop-gate control
- useful for wrong-motion prevention
- useful for reverse indexing
- useful for view-gate registration
```

Weaknesses:

```text id="u63klt"
- can increase friction
- may attract dust or debris
- may create sticking
- may constrain material choice
- should not be treated as the whole transport
```

Ranking:

```text id="cfdvtq"
Support mechanism, not primary transport.
```

Use in simulator:

```text id="yb3h4j"
Yes, as abstract states:
guide_locked
stop_gate_active
clamp_engaged
wrong_motion_blocked
```

Best role:

```text id="bykol8"
Registration and safety layer.
```

---

## 12. Actuator Family 1 — Motor + encoder feed

```text id="rw9d9z"
micro motor
+ encoder
+ closed-loop section indexing
```

Description:

```text id="4ed9wc"
A small motor moves the carrier or shuttle. Encoder feedback confirms movement distance, speed, and stop position.
```

Strengths:

```text id="w37ihv"
- most controllable baseline
- easiest to understand
- easiest to simulate
- supports closed-loop feedback
- works with folded carrier path
- works with cartridge feed
```

Weaknesses:

```text id="17x5qp"
- motor noise
- power usage
- gear/backlash issues
- mechanical wear
- may need brake/latch for stable dwell
```

Ranking:

```text id="6mybvf"
Best first actuator baseline.
```

Use in simulator:

```text id="516fmm"
Yes — model first.
```

Reason:

```text id="3685nq"
It provides the clearest controllable baseline for movement commands, encoder feedback, timeout, overrun, underrun, and fail-closed logic.
```

This agrees with the physical plan’s early ranking, which lists encoder-controlled micro motor or piezo ultrasonic motor as the most controllable category. physical plan(4)

---

## 13. Actuator Family 2 — Piezo ultrasonic feed

```text id="61w9v3"
piezo ultrasonic motor
or compact piezo feed actuator
```

Description:

```text id="2s0ufm"
Piezo actuation moves or indexes the carrier through small controlled motions.
```

Strengths:

```text id="juu05n"
- compact
- precise
- potentially quiet
- suitable for small internal mechanisms
- can fit modern tablet-like product language
```

Weaknesses:

```text id="f25wzv"
- more specialised
- harder to prototype casually
- needs careful material/contact design
- not yet proven for AMCF carrier handling
```

Ranking:

```text id="oqjowl"
High-value actuator candidate.
```

Use in simulator:

```text id="j6nqxc"
Yes, as a profile option.
```

Recommended simulator representation:

```text id="mlc1vr"
actuator_type = "piezo_ultrasonic"
movement_profile = "precision_indexed"
claim_status = "candidate_not_validated"
```

---

## 14. Actuator Family 3 — Piezo/electrostatic inchworm feed

```text id="w5mfj2"
clamp
→ step
→ release
→ clamp
→ step
```

Description:

```text id="e943k7"
The carrier advances through repeated small clamp-step-release movements.
```

Strengths:

```text id="776ayk"
- very AMCF-index-like
- naturally discrete
- good conceptual match for indexed sections
- can support precise staging
- maps well to section-by-section movement
```

Weaknesses:

```text id="kgutd1"
- mechanical complexity
- contact wear
- friction/sticking issues
- requires careful clamp timing
- real hardware proof absent
```

Ranking:

```text id="97dxs5"
Best AMCF-index-like actuator concept.
```

Use in simulator:

```text id="ty2o5z"
Yes, as a second actuator profile after motor/encoder.
```

The physical plan specifically identifies piezo or electrostatic inchworm feed with clamp-step-release behaviour as the most AMCF-index-like mechanism family. physical plan(4)

---

## 15. Actuator Family 4 — Constant-force spring + governor + brake

```text id="hl8a8i"
stored tension
+ latch
+ governor
+ brake
+ electronic or mechanical release
```

Description:

```text id="ss9w7m"
A stored-energy mechanism supplies motion. A governor, latch, and brake regulate section movement.
```

Strengths:

```text id="8e6v3x"
- self-contained mechanical branch
- could reduce continuous motor demand
- useful comparison to classic mechanical media
- may support emergency/backup movement
```

Weaknesses:

```text id="y3nv9n"
- dynamic AMCF scheduling is harder
- precise stop/start is harder
- A/B staging still needs sensors
- brake/latch complexity
- not ideal as first controlled simulator baseline
```

Ranking:

```text id="4wwy6f"
Self-contained mechanical comparison candidate.
```

Use in simulator:

```text id="iw5tl3"
Yes, later as a comparison profile.
Not the default.
```

The physical plan ranks stored tension / constant-force strip / spiral spring plus latch/governor/brake as the most self-contained mechanical branch, but not as the main controlled baseline. physical plan(4)

---

## 16. Support Layer — Energy recovery

```text id="r5slhz"
electret
triboelectric
piezo charge recovery
regenerative stop-start recovery
```

Description:

```text id="bk5s2h"
Energy recovery may reclaim small amounts of energy from motion, braking, charge cycling, or contact events.
```

Correct role:

```text id="ygb69s"
support layer
```

Incorrect role:

```text id="oycu8q"
main power source
infinite energy claim
proof that hardware is solved
```

Strengths:

```text id="noxlq4"
- useful for later efficiency research
- fits physical/mechanical branch
- may support sensors or small buffers
```

Weaknesses:

```text id="rs31kg"
- not a primary transport mechanism
- does not solve timing
- does not solve view-gate staging
- does not remove need for power/control
```

Ranking:

```text id="qw01er"
Interesting support layer only.
```

Use in simulator:

```text id="7a89hp"
Not necessary for first player simulator.
Optional later energy-state field.
```

The physical plan places electret, triboelectric, piezo charge recovery, and regenerative stop-start recovery under “most interesting energy-recovery layer,” separate from the main transport ranking. physical plan(4)

---

## 17. Experimental branch — Soft actuators and electro-active media

```text id="ztqyir"
dielectric elastomer
HASEL/electrohydraulic
electro-active paper
```

Description:

```text id="mys0z7"
These are experimental actuator/material concepts that may be relevant to long-term AMCF physical research.
```

Strengths:

```text id="ru713z"
- interesting for future compact motion
- interesting for material-integrated actuation
- may connect to future physical AMCF research
```

Weaknesses:

```text id="hjzo9h"
- too experimental for first simulator
- high complexity
- may require special materials
- may involve difficult voltage/control issues
- not a near-term default player architecture
```

Ranking:

```text id="d7e3iu"
Research comparison only.
```

Use in simulator:

```text id="x15flu"
No for first simulator.
Mention in documentation only.
```

The physical plan lists dielectric elastomer, HASEL/electrohydraulic, and electro-active paper as the “most experimental” mechanism family. physical plan(4)

---

## 18. Material-aligned carrier branch

```text id="xe14nz"
nanocellulose
bacterial cellulose
cellulose-nanocrystal carrier
printed marker lanes
colour-registry lanes
```

Description:

```text id="dv2qlk"
This is not primarily an actuator. It is the material branch for future carrier media.
```

Strengths:

```text id="fh3b9w"
- aligns with thin carrier research
- may support printed markers and colour lanes
- relevant to section durability and scan/read quality
```

Weaknesses:

```text id="9qniqb"
- not the first transport mechanism
- material performance remains unproven for AMCF
- requires separate material testing
```

Ranking:

```text id="9m8jz2"
Longer-term material research branch.
```

Use in simulator:

```text id="j7gah9"
Yes, as parameterized MaterialProfile fields only.
```

The physical plan names nanocellulose, bacterial cellulose, and cellulose-nanocrystal carrier with printed marker and colour-registry lanes as the most material-aligned branch. physical plan(4)

---

## 19. Recommended mechanism ranking

The recommended overall ranking is:

```text id="h3jfv0"
Rank 1:
Folded indexed carrier path
+ A/B staged view-gate logic
+ motor/encoder baseline

Rank 2:
Folded indexed carrier path
+ A/B staging
+ piezo/inchworm actuator profile

Rank 3:
Two-track A/B shuttle

Rank 4:
Cartridge stack + shuttle

Rank 5:
Chain / indexed linked carrier

Rank 6:
Constant-force spring + governor + brake

Rank 7:
Magnetic/guided clamp tracks as support layer

Rank 8:
Energy-recovery support layer

Rank 9:
Experimental soft-actuator branches

Rank 10:
Advanced material-integrated carrier branch
```

This ranking does not mean Rank 10 is unimportant.

It means:

```text id="gs0b7g"
Rank 1 is best for current simulator and documentation.
Lower ranks are comparison, support, or future research branches.
```

---

## 20. Preferred first simulator mechanism

The first simulator should model:

```text id="8wq7h1"
carrier_layout = "folded_indexed_carrier"
staging_model = "abstract_ab_staging"
actuator_profile = "motor_encoder_baseline"
view_gate_model = "single_visible_gate_plus_hidden_staging"
prefetch_model = "reader_prefetch_ahead"
reverse_model = "limited_reverse_buffer"
failure_model = "fail_closed"
```

Reason:

```text id="u9mc1y"
This gives the cleanest deterministic model without pretending final hardware exists.
```

It supports:

```text id="vf0jv6"
- dynamic AMCF update events
- section dwell duration
- preload deadline
- verified-before-visible display
- transition blanking
- local reverse
- safety/fault states
```

It avoids:

```text id="anvu67"
- final motor selection claim
- final gate geometry claim
- final material claim
- physical playback proof claim
```

---

## 21. Simulator mechanism profiles

The simulator should allow profiles, not hardcode one final hardware answer.

Suggested mechanism profile object:

```python id="vtblql"
@dataclass
class AMCFMechanismProfile:
    profile_id: str
    carrier_layout: str
    staging_model: str
    actuator_family: str
    gate_model: str
    prefetch_model: str
    reverse_model: str
    guide_model: str
    energy_support_model: str | None
    material_profile_id: str | None
    claim_status: str
```

Example default:

```json id="ytw3h9"
{
  "profile_id": "folded_ab_motor_encoder_baseline",
  "carrier_layout": "folded_indexed_carrier",
  "staging_model": "abstract_ab_staging",
  "actuator_family": "motor_encoder",
  "gate_model": "single_visible_gate_plus_hidden_staging",
  "prefetch_model": "reader_prefetch_ahead",
  "reverse_model": "limited_reverse_buffer",
  "guide_model": "edge_guides_and_stop_gates",
  "energy_support_model": null,
  "material_profile_id": "parameterized_thin_section_carrier",
  "claim_status": "simulated_concept_not_physical_validation"
}
```

Example research profile:

```json id="bfbxb5"
{
  "profile_id": "folded_ab_inchworm_research",
  "carrier_layout": "folded_indexed_carrier",
  "staging_model": "abstract_ab_staging",
  "actuator_family": "piezo_electrostatic_inchworm",
  "gate_model": "dual_gate_candidate",
  "prefetch_model": "reader_prefetch_ahead",
  "reverse_model": "limited_reverse_buffer",
  "guide_model": "clamp_step_release_guides",
  "energy_support_model": "piezo_charge_recovery_optional",
  "material_profile_id": "parameterized_thin_section_carrier",
  "claim_status": "research_candidate_not_physical_validation"
}
```

---

## 22. Mechanism comparison table

```text id="c6onpv"
Mechanism / layout                AMCF fit     Simulator first?   Status
────────────────────────────────────────────────────────────────────────────
Folded indexed carrier path        Very high    Yes                Primary
A/B staged gate logic              Very high    Yes                Primary
Motor + encoder feed               High         Yes                Baseline actuator
Piezo / inchworm feed              High         Later/profile      Research actuator
Two-track shuttle                  High         Later/profile      Secondary layout
Cartridge stack + shuttle          Medium       Later/profile      Prototype candidate
Chain / indexed carrier            Medium       Optional           Demo/research candidate
Magnetic/guided clamp tracks       Support      Abstract only      Support layer
Constant-force spring/governor     Medium       Optional           Mechanical comparison
Energy recovery                    Support      No / later         Support layer
Soft actuators                     Low now      No                 Experimental
Nanocellulose/cellulose carriers   Material     Profile only       Material branch
```

---

## 23. What should be documented as settled

Settled:

```text id="igx36k"
- physical playback is dynamic, not fixed FPS page flipping
- preferred concept is folded-path A/B staged player
- preloading is required for apparent instant switching
- reader-prefetch is required for safe live playback
- sections must be verified before display
- first simulator should model mechanism logic, not CAD
- no physical Level 5 validation is claimed
```

The uploaded hierarchy classifies Level 5 as a future hardware concept: tablet-like player with folded internal path, A/B staging, optical view gate, and reader prefetch. It also says the mechanical/optical simulator exists but should be refined around dynamic A/B folded-path staging. Physical design

---

## 24. What should remain open

Open:

```text id="lxh39o"
- final carrier form
- final gate geometry
- one-gate vs two-gate physical implementation
- exact motor type
- exact piezo/inchworm viability
- exact spring/brake/latch design
- exact guide/clamp material
- exact sensor placement
- exact material substrate
- exact maximum update rate
- exact transition blank duration
- exact reverse buffer depth
- exact manufactured device thickness
```

These remain open because there is no real physical hardware validation yet.

---

## 25. What Codex should model from Part 6

Codex should not build real hardware drivers.

It should model mechanism profiles.

Suggested files later:

```text id="nbs25h"
src/amcf_physical_mechanism_profiles.py
tests/test_physical_mechanism_profiles.py
docs/AMCF_PHYSICAL_MECHANISM_RANKING.md
demo/run_physical_mechanism_profile_demo.py
```

Suggested model structures:

```text id="26m7xr"
AMCFMechanismProfile
CarrierLayoutProfile
StagingMechanismProfile
ActuatorFamilyProfile
GuideClampProfile
ReverseCapabilityProfile
MechanismRankingReport
MechanismClaimBoundary
```

Suggested tests:

```text id="o11li7"
- default profile is folded indexed carrier + A/B staging
- motor/encoder baseline is marked simulated only
- piezo/inchworm is marked research candidate
- chain carrier is not ranked as default
- energy recovery is support layer only
- experimental soft actuators are not selected as default
- claim_status never says physical validation
```

---

## 26. Recommended wording for Part 6

Use this wording:

```text id="pp6o8a"
The preferred AMCF physical-player mechanism is a dynamic folded-path A/B staged indexed-section transport. The first simulator should model a folded indexed carrier with abstract A/B staging, reader-prefetch, motor/encoder baseline movement, transition blanking, limited reverse buffer, and fail-closed safety. Piezo/inchworm actuation is the strongest AMCF-index-like research candidate. Two-track shuttles, cartridge-stack shuttles, chain carriers, magnetic/guided tracks, constant-force spring systems, energy recovery, and experimental soft-actuator families should remain comparison/support/research branches until physical evidence exists.
```

---

## 27. What Part 6 decides

Part 6 decides:

```text id="zxpgiy"
- the preferred mechanism family is folded indexed carrier + A/B staging
- the first actuator baseline should be motor/encoder
- piezo/inchworm is the strongest AMCF-index-like research branch
- two-track shuttle is a high-value secondary layout
- cartridge stack + shuttle is useful but not default for fluid playback
- chain/indexed carrier is a research/demo candidate
- magnetic/guided tracks are support layers
- spring/governor/brake is a self-contained comparison branch
- energy recovery is not a main transport solution
- soft actuators are experimental only
- material-aligned carriers stay parameterized until tested
```

---

## 28. Part 7 should cover next

Part 7 should cover:

```text id="d3v4eu"
Physical Player Simulator Data Model and Development Sequence
```

Specifically:

```text id="vnsi4l"
- simulator object hierarchy
- player state machine
- mechanism profile model
- cartridge/section model
- gate and staging states
- prefetch verification states
- reverse/seek states
- fail-closed reports
- demo outputs
- tests
- Codex-ready implementation sequence
```

Part 6 stops here because the mechanism-family ranking and physical layout variants are now defined.
-----

# AMCF Physical Player Design and Structure Dossier  
## Part 7 — Physical Player Simulator Data Model and Development Sequence

## 1. Purpose of Part 7

Parts 1–6 defined:

```text id="zt5qre"
Part 1 — Boundary, product form, visual language, and core architecture
Part 2 — Internal transport architecture
Part 3 — A/B gate, view gate, shutter, illumination, and optics
Part 4 — Cartridge, carrier, and section anatomy
Part 5 — Reader-prefetch, sensors, reverse/seek, and fail-closed logic
Part 6 — Mechanism family ranking and physical layout variants
```

Part 7 now turns the physical-player design into a **software simulator data model and development sequence**.

The goal is not to build real hardware.

The goal is to define:

```text id="g7k1kh"
- what the simulator should model
- what objects/classes it should contain
- what state machines it should use
- what reports it should output
- what tests should prove
- how Codex should implement it safely
```

The uploaded context already classifies the current physical branch as:

```text id="r01uav"
Level 4 — Mechanical/optical player simulator
Level 5 — Future hardware concept
```

with Level 5 being the tablet-like player with folded internal path, A/B staging, optical view gate, and reader prefetch. Physical design

So Part 7 should build the **Level 4 simulator**, not claim Level 5 hardware.

---

## 2. Simulator boundary

The simulator should model:

```text id="lbjgvq"
dynamic folded-path A/B staged physical-player behaviour
```

It should not claim:

```text id="sbwm5z"
- manufactured physical hardware
- real sensor validation
- real motor validation
- real cartridge validation
- real physical optical playback
- real no-gap playback proof
- Level 5 physical proof
```

The simulator is a software model for:

```text id="cd4d7q"
- cartridge insertion
- physical section scheduling
- reader-prefetch
- section verification
- A/B staging
- view-gate state
- transition blanking
- reverse/seek limits
- fail-closed decisions
- mechanism profile comparison
```

This matches the already established direction that the mechanical/optical simulator exists but should be refined around dynamic A/B folded-path staging, while the real hardware player remains a future concept. Physical design

---

## 3. What the simulator is not

The simulator should not become:

```text id="euzt6b"
- CAD
- motor firmware
- USB driver
- real scanner driver
- real printer driver
- optical ray-tracing engine
- physical material laboratory
- real-time hardware controller
```

It should also not over-specify:

```text id="r452h3"
- exact motor part
- exact sensor part
- exact material thickness
- exact prism/lens geometry
- exact cartridge dimensions
- exact gate tolerances
```

Instead, it should use:

```text id="ohf1bh"
parameterized profiles
state machines
deterministic demo data
validation reports
claim boundaries
```

---

## 4. Core simulator chain

The simulator should model the full physical-player logic chain:

```text id="cdyy46"
AMCF physical manifest
→ cartridge profile
→ carrier sections
→ mechanism profile
→ reader-prefetch
→ section verification
→ hidden staging gate
→ visible view gate
→ transition blanking
→ physical/optical display state
→ reverse/park buffer
→ fail-closed report
```

The mechanism branch should preserve the preferred physical layout from Part 6:

```text id="qhrymx"
folded indexed carrier path
+ A/B staged gate logic
+ motor/encoder baseline
+ reader-prefetch
+ limited reverse buffer
+ fail-closed safety
```

The uploaded physical-design file already gives the required layout options: folded loop path, A/B dual-gate staging, two-track shuttle, cartridge stack + shuttle, chain/indexed carrier, and magnetic/guided clamp tracks. Physical design

The first simulator should choose the preferred default, while keeping the other options as mechanism profiles.

---

## 5. Recommended simulator files

The physical-player simulator should be separated from the general physical I/O system.

Suggested repo files:

```text id="lodogs"
docs/
├── AMCF_PHYSICAL_PLAYER_SIMULATOR.md
├── AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
├── AMCF_PHYSICAL_MECHANISM_RANKING.md
├── AMCF_PHYSICAL_PLAYER_CLAIM_BOUNDARIES.md
└── AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

src/
├── amcf_physical_player_simulator.py
├── amcf_physical_player_models.py
├── amcf_physical_mechanism_profiles.py
└── amcf_physical_player_reports.py

demo/
└── run_physical_player_simulator_demo.py

tests/
├── test_physical_player_simulator.py
├── test_physical_mechanism_profiles.py
├── test_physical_player_state_machine.py
└── test_physical_player_fail_closed.py
```

If the repo already has some of these concepts under different filenames, Codex should extend the existing files instead of duplicating them.

---

## 6. Main simulator object hierarchy

The simulator should use an object hierarchy like this:

```text id="p16ao3"
AMCFPhysicalPlayerSimulator
│
├── AMCFPhysicalPlayerProfile
├── AMCFMechanismProfile
├── AMCFPhysicalCartridge
├── AMCFPhysicalCarrier
├── AMCFPhysicalSection
├── AMCFPhysicalLaneStatus
├── ReaderPrefetchState
├── SectionVerificationState
├── ABGateState
├── ViewGateState
├── HiddenStagingGateState
├── TransitionBlankingState
├── ReverseParkBufferState
├── SeekRequestState
├── AudioSyncState
├── PlayerSafetyState
├── FailClosedDecision
└── PhysicalPlayerSimulationReport
```

This hierarchy keeps the simulator focused.

It does not require hardware.

It represents the logic of:

```text id="fon36t"
verify
stage
display
transition
park
reverse
fail closed
```

---

## 7. AMCFPhysicalPlayerSimulator

Main controller object:

```python id="rp20ei"
@dataclass
class AMCFPhysicalPlayerSimulator:
    player_profile: "AMCFPhysicalPlayerProfile"
    mechanism_profile: "AMCFMechanismProfile"
    cartridge: "AMCFPhysicalCartridge | None"

    current_time_ms: int
    current_section_id: str | None
    next_section_id: str | None

    reader_prefetch_state: "ReaderPrefetchState"
    view_gate_state: "ViewGateState"
    hidden_gate_state: "HiddenStagingGateState"
    transition_state: "TransitionBlankingState"
    reverse_buffer_state: "ReverseParkBufferState"
    audio_sync_state: "AudioSyncState"
    safety_state: "PlayerSafetyState"

    event_log: list[dict]
    fail_closed_events: list["FailClosedDecision"]
```

Required methods:

```python id="mon89i"
def insert_cartridge(self, cartridge): ...
def eject_cartridge(self): ...
def load_manifest(self, manifest): ...
def prefetch_next(self): ...
def verify_section(self, section_id): ...
def stage_next(self): ...
def tick(self, delta_ms: int): ...
def transition_if_ready(self): ...
def pause(self): ...
def step_forward(self): ...
def step_reverse(self): ...
def seek(self, timestamp_ms: int): ...
def fail_closed(self, reason: str): ...
def build_report(self): ...
```

The simulator should be deterministic.

Given the same cartridge, mechanism profile, and schedule, it should produce the same timeline and reports.

---

## 8. AMCFPhysicalPlayerProfile

The player profile describes the simulated player’s capabilities.

```python id="lwve07"
@dataclass
class AMCFPhysicalPlayerProfile:
    player_id: str
    player_name: str

    supports_ab_staging: bool
    supports_reader_prefetch: bool
    supports_reverse_buffer: bool
    supports_seek: bool
    supports_audio_sync: bool

    max_prefetch_ahead_ms: int
    transition_blank_ms: int
    reverse_buffer_depth: int

    claim_status: str
```

Example:

```json id="mwb3u9"
{
  "player_id": "amcf_physical_player_sim_v1",
  "player_name": "AMCF Physical Player Simulator V1",
  "supports_ab_staging": true,
  "supports_reader_prefetch": true,
  "supports_reverse_buffer": true,
  "supports_seek": false,
  "supports_audio_sync": true,
  "max_prefetch_ahead_ms": 120,
  "transition_blank_ms": 8,
  "reverse_buffer_depth": 3,
  "claim_status": "software_simulator_not_physical_hardware"
}
```

---

## 9. AMCFMechanismProfile

The mechanism profile should represent the mechanism-family choice from Part 6.

```python id="gaxwmo"
@dataclass
class AMCFMechanismProfile:
    profile_id: str

    carrier_layout: str
    staging_model: str
    actuator_family: str
    gate_model: str
    prefetch_model: str
    reverse_model: str
    guide_model: str

    energy_support_model: str | None
    material_profile_id: str | None

    ranking_tier: str
    claim_status: str
```

Default profile:

```json id="gh8iuy"
{
  "profile_id": "folded_ab_motor_encoder_baseline",
  "carrier_layout": "folded_indexed_carrier",
  "staging_model": "abstract_ab_staging",
  "actuator_family": "motor_encoder",
  "gate_model": "single_visible_gate_plus_hidden_staging",
  "prefetch_model": "reader_prefetch_ahead",
  "reverse_model": "limited_reverse_buffer",
  "guide_model": "edge_guides_and_stop_gates",
  "energy_support_model": null,
  "material_profile_id": "parameterized_thin_section_carrier",
  "ranking_tier": "primary_simulator_baseline",
  "claim_status": "simulated_concept_not_physical_validation"
}
```

Research profile:

```json id="v38o3h"
{
  "profile_id": "folded_ab_inchworm_research",
  "carrier_layout": "folded_indexed_carrier",
  "staging_model": "abstract_ab_staging",
  "actuator_family": "piezo_electrostatic_inchworm",
  "gate_model": "dual_gate_candidate",
  "prefetch_model": "reader_prefetch_ahead",
  "reverse_model": "limited_reverse_buffer",
  "guide_model": "clamp_step_release_guides",
  "energy_support_model": "piezo_charge_recovery_optional",
  "material_profile_id": "parameterized_thin_section_carrier",
  "ranking_tier": "research_candidate",
  "claim_status": "research_candidate_not_physical_validation"
}
```

The physical plan already ranked motor/encoder or piezo ultrasonic as the most controllable, piezo/electrostatic inchworm as most AMCF-index-like, spring/governor/brake as the self-contained mechanical branch, and energy recovery as only a support layer. physical plan(4)

---

## 10. Cartridge and section model

The simulator should use a simplified cartridge and section model.

```python id="faj0ag"
@dataclass
class AMCFPhysicalCartridge:
    cartridge_id: str
    carrier_id: str
    manifest_id: str
    section_count: int
    sections: list["AMCFPhysicalSection"]
    inserted: bool
    recognized: bool
    manifest_matched: bool
```

```python id="vuccnp"
@dataclass
class AMCFPhysicalSection:
    section_id: str
    section_index: int
    section_type: str

    timestamp_start_ms: int
    dwell_ms: int | None

    payload_type: str
    payload_label: str | None
    component_id: str | None

    timing_index_valid: bool
    registration_valid: bool
    colour_status: str
    metadata_valid: bool
    hash_status: str

    required_for_playback: bool
    recovery_policy: str
```

The section model should preserve the Part 4 anatomy:

```text id="jz3lvh"
timing/index lane
registration lane
image/component payload area
alpha/object mask lane
colour registry lane
metadata/transform lane
hash/checksum lane
```

The uploaded physical-design file already defines the virtual-cartridge model with these same lane categories. Physical design

---

## 11. ReaderPrefetchState

The prefetch state tracks whether the next section is known before display.

```python id="s6wggk"
@dataclass
class ReaderPrefetchState:
    enabled: bool
    prefetch_ahead_ms: int

    expected_next_section_id: str | None
    prefetched_section_id: str | None

    timing_index_read: bool
    registration_read: bool
    colour_registry_read: bool
    metadata_read: bool
    hash_read: bool

    prefetch_status: str
    prefetch_deadline_ms: int | None
    prefetch_completed_ms: int | None
```

Possible statuses:

```text id="r8b69z"
NOT_STARTED
PREFETCHING
PREFETCHED
VERIFIED
RESCAN_REQUIRED
FAILED
TIMEOUT
```

The player-prefetch system must read ahead of the active playback gate and maintain upcoming metadata/timing/hash/index information before visible switching. Physical design

---

## 12. SectionVerificationState

The verification state decides whether a section may be displayed.

```python id="xwqvf3"
@dataclass
class SectionVerificationState:
    section_id: str

    timing_index_valid: bool
    registration_valid: bool
    payload_present: bool
    alpha_mask_valid: bool | None
    colour_status: str
    metadata_valid: bool
    hash_status: str

    decision: str
    display_allowed: bool
    unsafe_acceptance: bool
    fail_closed_reason: str | None
```

Allowed decisions:

```text id="cd8gs7"
ACCEPTED
ACCEPTED_WITH_DEGRADED_COLOUR
RESCAN_REQUIRED
REJECTED_FAIL_CLOSED
```

These match the virtual scan-gate/lane-reader decision states already planned in the uploaded file. Physical design

Critical rule:

```text id="fh1n4h"
unsafe_acceptance must always remain false.
```

---

## 13. A/B gate state

The simulator should model A/B gate logic abstractly.

```python id="pz2y7g"
@dataclass
class ABGateState:
    visible_gate_id: str
    hidden_gate_id: str

    visible_section_id: str | None
    hidden_section_id: str | None

    visible_gate_locked: bool
    hidden_gate_ready: bool

    current_gate_role: str
    next_gate_role: str

    last_switch_ms: int | None
```

Gate roles:

```text id="kygpx4"
VISIBLE
HIDDEN_STAGING
PARKING
EMPTY
FAULT
```

The simulator should not claim whether the real hardware uses:

```text id="mgkblt"
two true optical gates
one gate plus hidden staging slot
sliding optical selector
two-track shuttle
```

It should model the abstract A/B staging state.

This matches the earlier conclusion that A/B dual-gate plus folded internal path is the best speed direction, because the next section can be prepared while the current section is viewed. Physical design

---

## 14. ViewGateState

The view gate represents the visible physical image plane.

```python id="kv1lfb"
@dataclass
class ViewGateState:
    section_id: str | None

    state: str
    locked: bool
    aligned: bool
    flatness_status: str
    illumination_allowed: bool
    visible: bool

    fault_reason: str | None
```

Possible states:

```text id="uslh17"
EMPTY
LOADING
ROUGH_ALIGNED
FINE_ALIGNED
LOCKED
VISIBLE
RELEASING
FAULT
```

Display rule:

```text id="dmfjcr"
A section may become visible only if:
- state is LOCKED or VISIBLE
- locked is true
- aligned is true
- verification display_allowed is true
- no critical fault exists
```

---

## 15. HiddenStagingGateState

The hidden staging gate prepares the next section.

```python id="sqaz7y"
@dataclass
class HiddenStagingGateState:
    section_id: str | None

    state: str
    rough_aligned: bool
    fine_aligned: bool
    verified: bool
    ready_for_switch: bool

    preload_started_ms: int | None
    preload_completed_ms: int | None
    fault_reason: str | None
```

Possible states:

```text id="fcnwb3"
EMPTY
PRELOADING
ROUGH_ALIGNED
FINE_ALIGNED
VERIFIED
READY
FAULT
```

Fail rule:

```text id="ar1juo"
If hidden staging is not READY by the update timestamp,
do not switch visible state.
```

---

## 16. TransitionBlankingState

The transition system hides mechanical switching.

```python id="a4w494"
@dataclass
class TransitionBlankingState:
    transition_blank_ms: int
    blanking_active: bool
    blanking_started_ms: int | None
    blanking_completed_ms: int | None

    shutter_state: str
    illumination_state: str

    transition_safe: bool
    fault_reason: str | None
```

Possible shutter states:

```text id="xffroe"
OPEN
CLOSED
TRANSITION
STUCK_OPEN
STUCK_CLOSED
```

Possible illumination states:

```text id="yozj3m"
OFF
STABLE
DIMMED
BLANKING
FAULT
```

The uploaded file already states that a no-gap system needs pre-aligned next section, shutter/illumination blanking, dwell/view gate, index lock, sensor feedback, short transport distance, and buffering queue. Physical design

---

## 17. ReverseParkBufferState

Reverse should be limited at first.

```python id="tzfpnf"
@dataclass
class ReverseParkBufferState:
    enabled: bool
    depth: int
    section_ids: list[str]

    reverse_available: bool
    requested_reverse_section_id: str | None
    reverse_denial_reason: str | None
```

Rules:

```text id="ubfw68"
- previous verified sections may enter the reverse buffer
- buffer depth is limited
- reverse is allowed only for sections still in the buffer
- arbitrary physical seek is not claimed
```

Example:

```json id="d5s7uc"
{
  "enabled": true,
  "depth": 3,
  "section_ids": ["section_0038", "section_0039", "section_0040"],
  "reverse_available": true,
  "requested_reverse_section_id": "section_0040",
  "reverse_denial_reason": null
}
```

---

## 18. SeekRequestState

Seek should be explicit and limited.

```python id="jty7fy"
@dataclass
class SeekRequestState:
    requested_timestamp_ms: int | None
    requested_section_id: str | None

    seek_mode: str
    seek_available: bool
    seek_status: str
    denial_reason: str | None
```

Seek levels:

```text id="yiypg9"
NO_SEEK
LOCAL_BUFFER_SEEK
PREFETCH_QUEUE_SEEK
REINDEX_REQUIRED
UNSUPPORTED
```

First simulator default:

```text id="qfmrca"
LOCAL_BUFFER_SEEK only
```

Do not claim arbitrary physical seek.

---

## 19. AudioSyncState

Audio must not drift away from the physical visual schedule.

```python id="u69o7s"
@dataclass
class AudioSyncState:
    enabled: bool
    audio_position_ms: int
    visual_position_ms: int

    drift_ms: int
    drift_status: str
    resync_required: bool
```

Possible statuses:

```text id="ep7k14"
SYNC_OK
MINOR_DRIFT
RESYNC_REQUIRED
FAIL_CLOSED
```

Rule:

```text id="pb33kd"
If physical visual playback cannot safely transition,
audio should pause/resync rather than continuing over unsafe visual state.
```

---

## 20. PlayerSafetyState

The simulator should maintain one high-level safety state.

```python id="iwmc3d"
@dataclass
class PlayerSafetyState:
    state: str
    display_allowed: bool
    motion_allowed: bool
    transition_allowed: bool

    unsafe_acceptance_count: int
    active_faults: list[str]
    last_fail_closed_reason: str | None
```

Possible states:

```text id="qfb3mc"
SAFE_IDLE
SAFE_READY
PLAYBACK_ALLOWED
PLAYBACK_DEGRADED
PAUSED_SAFE
RESCAN_REQUIRED
RETRY_ALLOWED
FAIL_CLOSED
MECHANICAL_STOP
UNSUPPORTED
```

The simulator should fail tests if:

```text id="ou6a2t"
unsafe_acceptance_count > 0
```

---

## 21. FailClosedDecision

Fail-closed decisions must be structured.

```python id="jv7ou2"
@dataclass
class FailClosedDecision:
    timestamp_ms: int

    reason: str
    current_section_id: str | None
    next_section_id: str | None
    carrier_id: str | None

    reader_state: str
    view_gate_state: str
    hidden_gate_state: str
    transition_state: str
    motion_state: str
    audio_sync_state: str

    recommended_action: str
```

Fail-closed reasons:

```text id="mxq5wp"
FAIL_CLOSED_UNVERIFIED_SECTION
FAIL_CLOSED_WRONG_SECTION
FAIL_CLOSED_HASH_MISMATCH
FAIL_CLOSED_REGISTRATION_FAILURE
FAIL_CLOSED_GATE_UNLOCKED
FAIL_CLOSED_PREFETCH_TIMEOUT
FAIL_CLOSED_SHUTTER_FAILURE
FAIL_CLOSED_ILLUMINATION_FAILURE
FAIL_CLOSED_JAM
FAIL_CLOSED_MANIFEST_MISMATCH
FAIL_CLOSED_UNSUPPORTED_CARRIER
FAIL_CLOSED_AUDIO_SYNC_LIMIT
```

Recommended actions:

```text id="qv0u09"
pause_and_rescan
blank_and_stop
hold_previous_safe_state
mechanical_stop
eject_required
manifest_recovery_required
unsupported_carrier
```

---

## 22. Main simulator state machine

The simulator should use a clear state machine.

```text id="n6p5g4"
NO_CARTRIDGE
→ CARTRIDGE_INSERTED
→ MANIFEST_RECOGNIZED
→ PREFETCH_CURRENT
→ VERIFY_CURRENT
→ LOAD_VIEW_GATE
→ VIEW_GATE_LOCKED
→ PLAYBACK_READY
→ PREFETCH_NEXT
→ VERIFY_NEXT
→ STAGE_NEXT
→ WAIT_UPDATE_TIMESTAMP
→ TRANSITION_BLANK
→ SWITCH_VISIBLE_SECTION
→ PARK_OLD_SECTION
→ PREFETCH_NEXT
```

Failure branch:

```text id="gny638"
PREFETCH_NEXT
→ verification failure
→ RESCAN_REQUIRED
→ retry if allowed
→ FAIL_CLOSED if unresolved
```

Mechanical failure branch:

```text id="izfeji"
MOVE_IN_PROGRESS
→ jam / misfeed / timeout
→ MECHANICAL_STOP
→ optical blank
→ FAIL_CLOSED
```

Reverse branch:

```text id="jcpwrn"
PLAYBACK_READY
→ reverse requested
→ check reverse buffer
→ verify previous section
→ stage previous section
→ transition blank
→ switch visible section
```

Seek branch:

```text id="zhl4zx"
PLAYBACK_READY
→ seek requested
→ check local buffer / prefetch queue
→ if unavailable, deny seek safely
→ if available, stage verified target
→ transition blank
→ switch visible section
```

---

## 23. Demo output folder

The simulator demo should output a complete report package.

```text id="tpbe8g"
output/physical_player_simulator_demo/
│
├── input/
│   ├── sample_physical_manifest.json
│   ├── sample_cartridge.json
│   ├── sample_sections.json
│   └── mechanism_profile.json
│
├── timeline/
│   ├── playback_timeline.json
│   ├── prefetch_timeline.json
│   ├── ab_gate_timeline.json
│   ├── transition_blanking_timeline.json
│   └── reverse_buffer_timeline.json
│
├── validation/
│   ├── section_verification_report.json
│   ├── fail_closed_events.json
│   ├── unsafe_acceptance_report.json
│   └── safety_state_report.json
│
├── reports/
│   ├── PHYSICAL_PLAYER_SIMULATION_REPORT.md
│   ├── MECHANISM_PROFILE_REPORT.md
│   ├── CLAIM_BOUNDARY_REPORT.md
│   └── NEXT_STEPS.md
│
└── README.md
```

This demo should prove the software model is coherent.

It should not claim real playback.

---

## 24. Required demo scenario

The demo should include at least:

```text id="c4irt1"
1. cartridge insertion
2. manifest recognition
3. valid current section
4. valid next section
5. successful A/B staged transition
6. degraded colour section accepted with warning
7. hash mismatch rejected or rescan-required
8. wrong section fail-closed
9. missing marker fail-closed or rescan-required
10. reverse buffer step-back
11. denied arbitrary seek
12. unsafe_acceptance_count remains zero
```

This mirrors the existing virtual-reader test direction in the uploaded planning file, where cartridge insert/eject, section seek, advance/reverse, valid section acceptance, degraded colour warning, hash mismatch, missing marker, correct summary counts, and unsafe acceptance staying zero were specified. Physical design

---

## 25. Required tests

The test suite should include:

```text id="xaptjw"
test_default_mechanism_profile_is_folded_ab_motor_encoder
test_cartridge_insert_manifest_match
test_valid_section_can_be_displayed
test_next_section_must_be_verified_before_display
test_ab_transition_requires_hidden_gate_ready
test_transition_blanking_required_for_switch
test_degraded_colour_is_warning_not_unsafe
test_hash_mismatch_does_not_display
test_wrong_section_fails_closed
test_missing_marker_rescan_or_fail_closed
test_view_gate_must_be_locked_before_illumination
test_reverse_buffer_limited_depth
test_arbitrary_seek_denied_when_not_supported
test_audio_sync_failure_pauses_or_fails_closed
test_unsafe_acceptance_count_stays_zero
test_report_contains_claim_boundary
```

Acceptance criteria:

```text id="st21ue"
- tests pass
- no physical hardware claimed
- no real sensors claimed
- no real motor claimed
- no real no-gap proof claimed
- unsafe_acceptance_count equals 0
- fail-closed events are structured
- simulator output is deterministic
```

---

## 26. Development sequence

Do not build everything at once.

Use staged development.

## Stage 1 — Data models

```text id="thcpo4"
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
```

Create:

```text id="b29kg6"
AMCFPhysicalPlayerProfile
AMCFMechanismProfile
AMCFPhysicalCartridge
AMCFPhysicalSection
ReaderPrefetchState
SectionVerificationState
ABGateState
ViewGateState
HiddenStagingGateState
TransitionBlankingState
ReverseParkBufferState
PlayerSafetyState
FailClosedDecision
```

Goal:

```text id="goemss"
Create the shared simulator vocabulary.
```

## Stage 2 — State machine

```text id="fn2eqs"
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
```

Implement:

```text id="ndkwos"
insert cartridge
recognize manifest
prefetch current
verify current
load view gate
prefetch next
stage next
transition
park old section
fail closed
```

Goal:

```text id="ek51v8"
Make the simulator run a safe forward playback cycle.
```

## Stage 3 — Failure handling

```text id="llrlso"
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
```

Implement:

```text id="fv1f7i"
wrong section
hash mismatch
missing marker
registration failure
prefetch timeout
gate unlocked
illumination/shutter failure
jam/misfeed placeholder
unsafe acceptance count
```

Goal:

```text id="c2v5fe"
Prove unsafe sections are not displayed.
```

## Stage 4 — Reverse / seek

```text id="nolx33"
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
```

Implement:

```text id="v335ji"
limited reverse buffer
step back
local-buffer seek
safe denial of unsupported arbitrary seek
```

Goal:

```text id="ud458t"
Model realistic reverse/seek limits without overclaiming.
```

## Stage 5 — Mechanism profiles

```text id="nnzysq"
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
```

Implement profiles:

```text id="ynj7ao"
folded_ab_motor_encoder_baseline
folded_ab_inchworm_research
two_track_ab_shuttle_candidate
cartridge_stack_shuttle_candidate
chain_indexed_carrier_research
spring_governor_brake_comparison
```

Goal:

```text id="tkc7ba"
Allow comparison without changing the core simulator.
```

## Stage 6 — Demo and reports

```text id="v2za01"
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
```

Create:

```text id="onuvuk"
sample cartridge
sample section schedule
playback timeline
prefetch timeline
A/B gate timeline
fail-closed events
reverse buffer timeline
final report
```

Goal:

```text id="kcwaaw"
Produce a readable demonstration package.
```

---

## 27. What Codex should build first

The immediate first Codex target should be:

```text id="efsgzf"
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
```

Reason:

```text id="mw2ppc"
The simulator needs stable data structures before adding state-machine complexity.
```

Stage 1 should create:

```text id="ysc5wd"
- player profile model
- mechanism profile model
- cartridge model
- section model
- gate state models
- prefetch state model
- verification state model
- reverse buffer model
- fail-closed decision model
- basic tests
- claim-boundary documentation
```

Stage 1 should not create:

```text id="ms6x65"
- real hardware drivers
- real USB interfaces
- real motor control
- real scanner acquisition
- real optical calculations
- package installs
- image generation
```

---

## 28. Stage 1 acceptance criteria

Stage 1 passes only if:

```text id="af6daz"
1. All core simulator dataclasses exist.
2. The default mechanism profile is folded indexed carrier + A/B staging + motor/encoder baseline.
3. Piezo/inchworm is marked as research candidate, not default proof.
4. Energy recovery is marked as support layer only.
5. The cartridge/section model includes timing/index, registration, colour, metadata, and hash/checksum status.
6. Section verification can produce accepted, accepted_with_degraded_colour, rescan_required, and rejected_fail_closed.
7. unsafe_acceptance_count exists and defaults to 0.
8. Claim boundary says software simulator only.
9. Tests pass.
10. No real hardware claim is made.
```

---

## 29. Recommended wording for Part 7

Use this wording:

```text id="szo78m"
The AMCF physical-player simulator should model the future mechanical/optical player as a deterministic software state machine. It should use a folded indexed-carrier and A/B staged transport profile by default, with motor/encoder as the baseline actuator profile and piezo/inchworm as a research candidate. The simulator should represent cartridge insertion, section prefetch, verification, hidden staging, view-gate locking, transition blanking, reverse buffer behaviour, audio sync, and fail-closed decisions. It must not claim physical hardware validation. A section may be displayed only if it is verified, staged, gate-locked, and safe; otherwise playback must pause, rescan, blank, or fail closed.
```

---

## 30. What Part 7 decides

Part 7 decides:

```text id="d0plrg"
- the physical-player simulator is Level 4, not Level 5
- the simulator models state and safety, not CAD/hardware
- the default mechanism profile is folded indexed carrier + A/B staging + motor/encoder baseline
- mechanism variants should be profiles, not separate systems
- section verification must happen before display
- view-gate and hidden-gate states must be explicit
- transition blanking must be explicit
- reverse/seek must be limited and safe
- fail-closed events must be structured
- unsafe_acceptance_count must remain zero
- first Codex target should be simulator data models
```

---

## 31. What remains open

Still unresolved:

```text id="vckqvz"
- exact real hardware design
- exact motor/actuator choice
- exact gate geometry
- exact optical geometry
- exact sensor placement
- exact timing tolerances
- exact material behaviour
- exact manufactured cartridge dimensions
- exact real no-gap transition timing
- exact audio drift threshold
```

These remain future research.

---

## 32. Part 8 should cover next

Part 8 should be:

```text id="wksov6"
Codex-Ready Implementation Prompt
```

for:

```text id="kqu385"
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
```

It should include:

```text id="pk5vpz"
- workspace path
- exact files to inspect
- exact files to add/edit
- dataclasses to create
- tests to write
- demo output requirements
- claim-boundary requirements
- validation commands
- git diff/stat instructions
- commit instruction
- no-push instruction
```

Part 7 stops here because the simulator data model and development sequence are now defined.
----

The current repo framing still says AMCF is software-first, no real hardware is required, and future physical work connects through abstractions/adapters rather than sensors, motors, cartridges, real scans, or prototypes now. [GitHub](https://raw.githubusercontent.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-/main/README.md) The repo also already lists the mechanical/optical physical-player simulator as a software simulation of dynamic folded-path A/B staged transport, fixed view gate, hidden staging gate, preload queue, transition blanking, illumination, alignment, and controls, while explicitly saying it is not real physical playback or hardware validation. [GitHub](https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-)

# AMCF Physical Player Design and Structure Dossier  
## Part 8 — Codex-Ready Implementation Prompt for Physical Player Simulator Models V1

## 1. Purpose of Part 8

Parts 1–7 defined the physical-player design and simulator direction.

Part 8 is the actual **Codex-ready implementation prompt** for the first implementation run:

```text id="mxnl7j"
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
```

The purpose of this run is not to build a full simulator yet.

The purpose is to create the stable **data model foundation** for the future physical-player simulator:

```text id="xpqltt"
player profile
mechanism profile
cartridge model
section model
lane/status model
reader-prefetch state
section verification state
A/B gate state
view gate state
hidden staging gate state
transition blanking state
reverse/seek state
audio sync state
player safety state
fail-closed decision
claim-boundary reports
tests
```

This gives the repo a clean base for later state-machine and demo runs.

---

## 2. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_simulator_models_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1

Public repo context:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If the actual Codex workspace is already inside the GitHub clean package/repo root, use that current repo root instead of guessing another path.

Current repo framing to preserve:
- AMCF is software-first.
- Digital AMCF is canonical.
- Physical AMCF is a future material / mechanical / optical embodiment of the same AMCF timing and update schedule.
- Current repo supports software abstractions, virtual hardware, docs, demos, and tests.
- Do not claim real physical hardware, physical Level 5, real sensor validation, real motors, real cartridges, real scans, manufacturing readiness, or a built prototype.
- The physical player is not a normal LCD/OLED screen player.
- The physical player is not just the software UI viewer.
- The physical player is not merely the reader/scanner path.
- Future physical player = mechanical/optical execution of AMCF media through indexed carrier sections, dynamic folded-path transport, A/B staging, view gate, hidden staging, reader-prefetch, transition blanking, and fail-closed safety.

Important design context:
- Preferred physical-player concept:
  compact tablet-like mechanical/optical player
  + folded indexed carrier path
  + side/top cartridge
  + reader-prefetch lane
  + hidden staging gate
  + visible view gate
  + shutter/illumination blanking
  + folded optical viewing path
  + reverse/park buffer where practical
  + fail-closed safety.

- Preferred simulator baseline:
  folded indexed carrier
  + abstract A/B staging
  + motor/encoder baseline actuator profile
  + reader-prefetch ahead
  + single visible gate plus hidden staging gate
  + limited reverse buffer
  + fail-closed model.

- Piezo/inchworm should be treated as a research candidate profile, not proven hardware.
- Energy recovery should be treated as a support layer only, not a power solution or proof.
- Chain carrier, cartridge stack shuttle, two-track shuttle, spring/governor/brake, magnetic/guided tracks, and soft actuators should be comparison/research/support profiles, not the default.

Relevant existing repo files to inspect first:
- README.md
- CLAIM_BOUNDARIES.md
- docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
- docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
- docs/AMCF_PHYSICAL_IO_ARCHITECTURE.md if present
- docs/AMCF_PHYSICAL_MANIFEST_SCHEMA.md if present
- src/amcf_mechanical_optical_player.py
- src/amcf_physical_io.py if present
- src/amcf_virtual_hardware.py
- tests/ existing physical/mechanical/virtual hardware tests
- demo/ existing mechanical/physical/virtual hardware demos

Do not duplicate an existing model if one already exists.
If existing files already contain matching classes or structures, extend them carefully instead of creating parallel incompatible names.

Do not install packages.
Use Python standard library only.
Do not download anything.
Do not run deep tools.
Do not generate images.
Do not create a large ZIP.
Do not push.
Do not modify unrelated files.
Do not weaken claim boundaries.

================================================================================
00 — INPUT AUDIT
================================================================================

First inspect the repo and create a short audit note in:

docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_AUDIT.md

Include:
- which existing physical-player simulator files exist
- whether src/amcf_mechanical_optical_player.py exists
- whether src/amcf_physical_io.py exists
- whether relevant docs already exist
- which files you will edit
- which files you will create
- whether any class names already exist that should be reused
- confirmation that no real hardware work is being attempted

================================================================================
01 — DATA MODEL MODULE
================================================================================

Create or update:

src/amcf_physical_player_models.py

If equivalent structures already exist in src/amcf_mechanical_optical_player.py, you may either:
1. extend that file directly, or
2. create src/amcf_physical_player_models.py and import/use it from the simulator file.

Prefer the cleanest structure with the least duplication.

Implement standard-library dataclasses and enums/string constants for:

1. AMCFPhysicalPlayerProfile
2. AMCFMechanismProfile
3. AMCFPhysicalCartridge
4. AMCFPhysicalCarrier
5. AMCFPhysicalSection
6. AMCFPhysicalLaneStatus
7. ReaderPrefetchState
8. SectionVerificationState
9. ABGateState
10. ViewGateState
11. HiddenStagingGateState
12. TransitionBlankingState
13. ReverseParkBufferState
14. SeekRequestState
15. AudioSyncState
16. PlayerSafetyState
17. FailClosedDecision
18. PhysicalPlayerSimulationClaimBoundary
19. PhysicalPlayerModelBundle

Use dataclasses.
Use type hints.
Use JSON-serializable fields where practical.
Use simple string status values rather than external dependencies.

================================================================================
02 — REQUIRED MODEL DETAILS
================================================================================

AMCFPhysicalPlayerProfile should include at least:

- player_id
- player_name
- supports_ab_staging
- supports_reader_prefetch
- supports_reverse_buffer
- supports_seek
- supports_audio_sync
- max_prefetch_ahead_ms
- transition_blank_ms
- reverse_buffer_depth
- claim_status

Default claim_status:
software_simulator_not_physical_hardware

AMCFMechanismProfile should include at least:

- profile_id
- carrier_layout
- staging_model
- actuator_family
- gate_model
- prefetch_model
- reverse_model
- guide_model
- energy_support_model
- material_profile_id
- ranking_tier
- claim_status

Default baseline profile:

profile_id:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

guide_model:
edge_guides_and_stop_gates

energy_support_model:
none

material_profile_id:
parameterized_thin_section_carrier

ranking_tier:
primary_simulator_baseline

claim_status:
simulated_concept_not_physical_validation

Research profile:

profile_id:
folded_ab_inchworm_research

actuator_family:
piezo_electrostatic_inchworm

ranking_tier:
research_candidate

claim_status:
research_candidate_not_physical_validation

Energy recovery must be a support model only, never default proof.

================================================================================
03 — CARTRIDGE / CARRIER / SECTION MODELS
================================================================================

AMCFPhysicalCartridge should include:

- cartridge_id
- carrier_id
- manifest_id
- section_count
- inserted
- recognized
- manifest_matched
- sections

AMCFPhysicalCarrier should include:

- carrier_id
- carrier_type
- section_count
- carrier_format_version
- material_profile_id
- lane_schema_id
- claim_status

AMCFPhysicalSection should include:

- section_id
- section_index
- section_type
- timestamp_start_ms
- dwell_ms
- payload_type
- payload_label
- component_id
- timing_index_valid
- registration_valid
- colour_status
- metadata_valid
- hash_status
- required_for_playback
- recovery_policy

AMCFPhysicalLaneStatus should include:

- timing_index_valid
- registration_valid
- payload_present
- alpha_mask_valid
- colour_status
- metadata_valid
- hash_status
- missing_marker
- degraded_colour
- critical_failure

Allowed colour statuses:
valid
degraded
failed
unknown

Allowed hash statuses:
valid
mismatch
missing
unknown

================================================================================
04 — PREFETCH / VERIFICATION / GATE MODELS
================================================================================

ReaderPrefetchState should include:

- enabled
- prefetch_ahead_ms
- expected_next_section_id
- prefetched_section_id
- timing_index_read
- registration_read
- colour_registry_read
- metadata_read
- hash_read
- prefetch_status
- prefetch_deadline_ms
- prefetch_completed_ms

Allowed prefetch statuses:
not_started
prefetching
prefetched
verified
rescan_required
failed
timeout

SectionVerificationState should include:

- section_id
- timing_index_valid
- registration_valid
- payload_present
- alpha_mask_valid
- colour_status
- metadata_valid
- hash_status
- decision
- display_allowed
- unsafe_acceptance
- fail_closed_reason

Allowed decisions:
accepted
accepted_with_degraded_colour
rescan_required
rejected_fail_closed

Critical rule:
unsafe_acceptance must never be true for invalid critical lanes.

ABGateState should include:

- visible_gate_id
- hidden_gate_id
- visible_section_id
- hidden_section_id
- visible_gate_locked
- hidden_gate_ready
- current_gate_role
- next_gate_role
- last_switch_ms

ViewGateState should include:

- section_id
- state
- locked
- aligned
- flatness_status
- illumination_allowed
- visible
- fault_reason

HiddenStagingGateState should include:

- section_id
- state
- rough_aligned
- fine_aligned
- verified
- ready_for_switch
- preload_started_ms
- preload_completed_ms
- fault_reason

TransitionBlankingState should include:

- transition_blank_ms
- blanking_active
- blanking_started_ms
- blanking_completed_ms
- shutter_state
- illumination_state
- transition_safe
- fault_reason

================================================================================
05 — REVERSE / SEEK / AUDIO / SAFETY MODELS
================================================================================

ReverseParkBufferState should include:

- enabled
- depth
- section_ids
- reverse_available
- requested_reverse_section_id
- reverse_denial_reason

SeekRequestState should include:

- requested_timestamp_ms
- requested_section_id
- seek_mode
- seek_available
- seek_status
- denial_reason

Allowed seek modes:
no_seek
local_buffer_seek
prefetch_queue_seek
reindex_required
unsupported

AudioSyncState should include:

- enabled
- audio_position_ms
- visual_position_ms
- drift_ms
- drift_status
- resync_required

Allowed drift statuses:
sync_ok
minor_drift
resync_required
fail_closed

PlayerSafetyState should include:

- state
- display_allowed
- motion_allowed
- transition_allowed
- unsafe_acceptance_count
- active_faults
- last_fail_closed_reason

Allowed safety states:
safe_idle
safe_ready
playback_allowed
playback_degraded
paused_safe
rescan_required
retry_allowed
fail_closed
mechanical_stop
unsupported

FailClosedDecision should include:

- timestamp_ms
- reason
- current_section_id
- next_section_id
- carrier_id
- reader_state
- view_gate_state
- hidden_gate_state
- transition_state
- motion_state
- audio_sync_state
- recommended_action

Allowed fail-closed reasons should include:

- fail_closed_unverified_section
- fail_closed_wrong_section
- fail_closed_hash_mismatch
- fail_closed_registration_failure
- fail_closed_gate_unlocked
- fail_closed_prefetch_timeout
- fail_closed_shutter_failure
- fail_closed_illumination_failure
- fail_closed_jam
- fail_closed_manifest_mismatch
- fail_closed_unsupported_carrier
- fail_closed_audio_sync_limit

================================================================================
06 — FACTORY HELPERS
================================================================================

Create helper functions to build:

- default_physical_player_profile()
- default_mechanism_profile()
- inchworm_research_mechanism_profile()
- two_track_ab_shuttle_candidate_profile()
- cartridge_stack_shuttle_candidate_profile()
- chain_indexed_carrier_research_profile()
- spring_governor_brake_comparison_profile()
- default_claim_boundary()
- sample_physical_section_set()
- sample_physical_cartridge()
- sample_model_bundle()

These should return deterministic data.

sample_physical_section_set() should include at least:

1. valid section
2. degraded colour section
3. hash mismatch section
4. missing marker / registration failure section
5. wrong-section candidate or unsupported section type

================================================================================
07 — VERIFICATION HELPER
================================================================================

Implement a simple function:

verify_physical_section(section: AMCFPhysicalSection) -> SectionVerificationState

Rules:

- valid timing/index + valid registration + hash_status valid + metadata valid + colour valid:
  decision = accepted
  display_allowed = true
  unsafe_acceptance = false

- colour_status degraded but critical lanes valid:
  decision = accepted_with_degraded_colour
  display_allowed = true
  unsafe_acceptance = false

- hash_status mismatch:
  decision = rejected_fail_closed
  display_allowed = false
  unsafe_acceptance = false
  fail_closed_reason = fail_closed_hash_mismatch

- registration invalid:
  decision = rejected_fail_closed or rescan_required
  display_allowed = false
  unsafe_acceptance = false

- timing/index invalid:
  decision = rejected_fail_closed
  display_allowed = false
  unsafe_acceptance = false

- missing/unknown critical data:
  display_allowed = false
  unsafe_acceptance = false

================================================================================
08 — CLAIM BOUNDARY MODEL
================================================================================

PhysicalPlayerSimulationClaimBoundary should include booleans:

- software_simulator_only
- physical_hardware_claimed
- hardware_validation_claimed
- real_sensors_required
- real_motors_required
- real_cartridge_required
- real_scans_required
- manufacturing_readiness_claimed
- physical_level_5_claimed
- built_prototype_claimed

Defaults:

software_simulator_only = true
all claim booleans above = false

Include a method or helper that exports this as dict/json.

================================================================================
09 — REPORT HELPERS
================================================================================

Create or update:

src/amcf_physical_player_reports.py

If better to keep reports in the model file for this first run, that is acceptable, but avoid unnecessary complexity.

Implement helpers:

- model_bundle_to_dict(bundle)
- write_model_bundle_json(bundle, path)
- write_claim_boundary_json(boundary, path)
- build_model_summary_markdown(bundle) -> str

The summary markdown must state:

- software simulator only
- no physical hardware proof
- no real sensors/motors/cartridges/scans required
- default profile is folded indexed carrier + A/B staging + motor/encoder baseline
- piezo/inchworm is research candidate only
- unsafe acceptance must remain zero

================================================================================
10 — DOCS
================================================================================

Create or update:

docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS.md

Include:

- purpose
- model hierarchy
- default mechanism profile
- research mechanism profiles
- section verification decisions
- fail-closed reasons
- claim boundary
- what is not claimed
- next stage

Create or update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add this staged sequence if not already present:

Stage 1:
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
data models only

Stage 2:
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
safe forward playback cycle

Stage 3:
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
failure handling and unsafe acceptance tests

Stage 4:
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
limited reverse and local seek

Stage 5:
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
mechanism profile comparisons

Stage 6:
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
deterministic demo and reports

Do not claim any physical validation.

================================================================================
11 — DEMO
================================================================================

Create:

demo/run_physical_player_models_demo.py

The demo should:

1. build default player profile
2. build default mechanism profile
3. build research mechanism profiles
4. build sample cartridge with sample sections
5. verify each sample section
6. build claim boundary
7. write output files

Output folder:

output/physical_player_models_demo/

Output files:

- player_profile.json
- mechanism_profile_default.json
- mechanism_profiles_all.json
- sample_cartridge.json
- section_verification_results.json
- claim_boundary.json
- MODEL_SUMMARY.md

The demo must be deterministic.

================================================================================
12 — TESTS
================================================================================

Create or update:

tests/test_physical_player_models.py

Tests must verify:

1. default player profile claim_status is software_simulator_not_physical_hardware
2. default mechanism profile is folded indexed carrier + A/B staging + motor/encoder baseline
3. inchworm profile is research candidate, not physical validation
4. energy recovery is not default transport
5. sample cartridge has expected section count
6. valid section is accepted and display_allowed true
7. degraded colour section is accepted_with_degraded_colour
8. hash mismatch section is rejected_fail_closed and display_allowed false
9. invalid timing/index section is not display_allowed
10. unsafe_acceptance is false for every verification result
11. claim boundary has software_simulator_only true
12. claim boundary has physical_hardware_claimed false
13. claim boundary has hardware_validation_claimed false
14. claim boundary has physical_level_5_claimed false
15. generated model summary contains no physical proof claim

Use unittest or pytest only if the repo already uses pytest.
Prefer unittest and standard library.

================================================================================
13 — VALIDATION COMMANDS
================================================================================

Run validation from repo root.

Use commands equivalent to:

python -m py_compile src/amcf_physical_player_models.py
python -m py_compile src/amcf_physical_player_reports.py
python -m py_compile demo/run_physical_player_models_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_models_demo.py

If filenames differ because you extended existing modules instead of creating new ones, adjust commands accordingly and document the exact commands used.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
14 — COMMIT
================================================================================

If all tests pass and the repo is clean except intended changes, commit with:

git add docs src demo tests
git commit -m "Add physical player simulator model foundation"

If commit is not appropriate because this is a local test run only, explain why and still provide:

- changed files
- test results
- demo outputs
- git status
- git diff --stat

Do not push.

================================================================================
15 — FINAL REPORT
================================================================================

In your final response, report:

- run name
- files created
- files modified
- demo output folder
- test commands run
- test results
- unsafe_acceptance_count result
- claim boundary status
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not say hardware is proven.
Do not say no-gap is physically proven.
Do not say a real physical player exists.
```

---

## 3. What Part 8 decides

```text id="qswl7s"
Part 8 decides that the next Codex run should be:
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1

It should build the model foundation only:
- dataclasses
- profiles
- verification states
- fail-closed decision structures
- claim boundaries
- docs
- deterministic demo
- tests

It should not yet build the full state machine, full playback simulator, hardware adapter, motor control, sensor driver, CAD model, or physical proof claim.
```

## 4. What Part 9 should cover next

```text id="sfutqq"
Part 9 should be:
Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
```

That next prompt should build the safe forward playback cycle:

```text id="moi1n0"
insert cartridge
→ recognize manifest
→ prefetch current
→ verify current
→ load view gate
→ prefetch next
→ stage next
→ wait update timestamp
→ transition blank
→ switch visible section
→ park old section
→ write playback timeline
```
----

Yes — the wording should be corrected.

The right framing is not:

```text id="uhdkt4"
This is not real, so it is only theoretical.
```

The right framing is:

```text id="xuqm7d"
This is the software/control/simulation foundation for a future working physical structure.

The hardware is not present yet, but the software can still define, test, and validate the logic that the later hardware must obey:
- carrier model
- mechanism profiles
- reader-prefetch
- A/B staging
- section verification
- gate state machine
- fail-closed decisions
- reverse/seek limits
- playback timing
- reports and claim boundaries
```

So the correct claim boundary is:

```text id="i3d1ap"
Software implementation of the physical-player control structure is valid work now.
Physical hardware proof comes later when real mechanisms, sensors, cartridges, materials, and optical playback are built and tested.
```

The uploaded context already frames the physical hierarchy this way: Level 4 is the mechanical/optical player simulator, while Level 5 is the later physical hardware concept with folded path, A/B staging, optical view gate, and reader prefetch. Physical design

# AMCF Physical Player Design and Structure Dossier  
## Part 9 — Codex-Ready Implementation Prompt for Physical Player State Machine V1

## 1. Purpose of Part 9

Part 8 created the prompt for:

```text id="b1hhkn"
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
```

That run builds the **data model foundation**.

Part 9 now defines the next Codex run:

```text id="h58chu"
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
```

The purpose is to make the simulator do something useful:

```text id="fj0o67"
insert cartridge
→ recognize manifest
→ prefetch current section
→ verify current section
→ load view gate
→ prefetch next section
→ stage next section
→ wait for update timestamp
→ blank transition
→ switch visible section
→ park old section
→ continue safely
```

This is not hardware-driver work.

It is the **software execution model** for the future physical-player structure.

The point is:

```text id="mtfxnn"
Even before hardware exists, the AMCF project can implement the control logic that future hardware must follow.
```

That includes:

```text id="l50eq7"
- state transitions
- safety decisions
- section verification
- A/B staging rules
- timing windows
- fail-closed behaviour
- timeline reporting
- deterministic tests
```

---

## 2. Corrected framing

Do not describe this as:

```text id="xpshvk"
not real physical playback, therefore only theoretical
```

Describe it as:

```text id="uu7d72"
software-first physical-player control architecture
```

Correct wording:

```text id="hzs4t5"
The current work implements the software structure that a later physical AMCF player would need: section scheduling, cartridge recognition, prefetch, verification, A/B staging, view-gate control, transition blanking, reverse buffer logic, audio sync state, and fail-closed safety. This does not claim that the physical hardware has already been manufactured or validated, but it does create the working software/control foundation required before hardware can be arranged, built, and tested.
```

So the boundary is:

```text id="y69vhf"
Software/control structure: can be implemented now.
Physical mechanism proof: requires later hardware.
```

The uploaded design notes already say the physical player should use dynamic AMCF event/update scheduling, indexed section changes, hold at view gate, illumination/optical presentation, and advance only when the next physical update is needed. Physical design

---

## 3. What can be done without hardware

Without hardware, the repo can still implement:

```text id="ac6n6t"
1. AMCF physical-player state machine
2. deterministic virtual cartridge playback
3. virtual section verification
4. reader-prefetch timing
5. A/B staging simulation
6. gate lock and hidden-gate readiness logic
7. transition blanking timing
8. reverse/park buffer
9. seek denial / safe seek limits
10. fail-closed decision engine
11. audio sync state tracking
12. playback timeline reports
13. safety reports
14. demo outputs
15. tests proving unsafe sections are never accepted
```

This is meaningful because later hardware should not be designed blind.

The software can define:

```text id="emjt9f"
what the hardware must do
when it must do it
what feedback it must provide
what failures must stop playback
what counts as safe display
```

So the software-first path is not a side project. It is the specification and control layer for the future physical structure.

---

## 4. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_state_machine_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1

Public repo context:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If the Codex workspace is already inside the repo root, use that current repo root.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run is not “fake hardware” and not a throwaway theory run.

This run implements the software/control structure that a later physical AMCF player would need.

Correct framing:

- The hardware is not present yet.
- The software state machine can still be implemented now.
- The state machine defines how a future physical player should behave.
- Later hardware should conform to this software/control logic.
- The simulator can test cartridge recognition, section verification, A/B staging, view-gate state, hidden-gate readiness, transition blanking, reverse buffer, timing, audio sync state, and fail-closed safety before physical hardware exists.

Do not claim:
- manufactured hardware
- real sensors
- real motors
- real physical cartridge validation
- real optical playback proof
- real no-gap proof
- physical Level 5 completion
- hardware validation

Do claim:
- software model
- control-state foundation
- deterministic simulator behaviour
- future hardware-support architecture
- safe fail-closed decision logic
- working state-machine implementation for later hardware alignment

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator mechanism baseline:

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

claim_status:
software_control_simulator_not_physical_validation

The physical player should not advance one page for every fixed video frame.
It should advance according to AMCF update events.

The key state-machine principle:

current section visible
→ next section prefetched
→ next section verified
→ next section staged hidden
→ update timestamp reached
→ transition blanking
→ staged section becomes visible
→ old section parks
→ repeat.

================================================================================
PREREQUISITE
================================================================================

This run should build on:

AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1

If the model-foundation run has already been completed, inspect and reuse those files.

Likely files from the previous run:

src/amcf_physical_player_models.py
src/amcf_physical_player_reports.py
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS.md
demo/run_physical_player_models_demo.py
tests/test_physical_player_models.py

If those exact files do not exist, inspect the repo for equivalent physical-player model files and reuse them.

Do not duplicate incompatible structures.

================================================================================
EXISTING FILES TO INSPECT
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md

docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS.md if present
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md if present

src/amcf_mechanical_optical_player.py
src/amcf_physical_player_models.py if present
src/amcf_physical_player_reports.py if present
src/amcf_physical_io.py if present
src/amcf_virtual_hardware.py if present

tests/test_physical_player_models.py if present
tests/ existing physical/mechanical/virtual hardware tests

demo/ existing physical/mechanical/virtual hardware demos

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP.
Do not push.
Do not modify unrelated files.
Do not weaken existing claim boundaries.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE_AUDIT.md

Include:

- which physical-player model files exist
- which simulator/state-machine files already exist
- whether AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1 appears already implemented
- which files you will edit
- which files you will create
- whether existing classes are reused
- confirmation that this is software/control-state implementation
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — STATE MACHINE MODULE
================================================================================

Create or update:

src/amcf_physical_player_state_machine.py

This module should implement the deterministic state machine for the physical-player simulator.

Import/reuse model classes from:

src/amcf_physical_player_models.py

If model classes exist elsewhere, import from the existing correct module.

Create:

AMCFPhysicalPlayerStateMachine

This class should contain:

- player_profile
- mechanism_profile
- cartridge
- current_time_ms
- current_section_id
- next_section_id
- playback_state
- reader_prefetch_state
- current_verification_state
- next_verification_state
- ab_gate_state
- view_gate_state
- hidden_gate_state
- transition_state
- reverse_buffer_state
- seek_request_state
- audio_sync_state
- safety_state
- event_log
- fail_closed_events

================================================================================
02 — PLAYBACK STATES
================================================================================

Use string states or enum constants.

Required states:

no_cartridge
cartridge_inserted
manifest_recognized
prefetch_current
verify_current
load_view_gate
view_gate_locked
playback_ready
prefetch_next
verify_next
stage_next
wait_update_timestamp
transition_blank
switch_visible_section
park_old_section
paused_safe
rescan_required
retry_allowed
fail_closed
mechanical_stop
playback_complete

The normal forward chain should be:

no_cartridge
→ cartridge_inserted
→ manifest_recognized
→ prefetch_current
→ verify_current
→ load_view_gate
→ view_gate_locked
→ playback_ready
→ prefetch_next
→ verify_next
→ stage_next
→ wait_update_timestamp
→ transition_blank
→ switch_visible_section
→ park_old_section
→ prefetch_next

================================================================================
03 — REQUIRED METHODS
================================================================================

AMCFPhysicalPlayerStateMachine should implement:

__init__(...)
insert_cartridge(cartridge)
recognize_manifest()
prefetch_current()
verify_current()
load_view_gate()
lock_view_gate()
enter_playback_ready()
prefetch_next()
verify_next()
stage_next()
wait_until_update_timestamp(target_timestamp_ms)
begin_transition_blank()
switch_visible_section()
park_old_section()
tick(delta_ms)
pause()
resume()
step_forward()
step_reverse()
request_seek(timestamp_ms=None, section_id=None)
fail_closed(reason, recommended_action)
build_timeline()
build_summary()
to_dict()

Methods may be simple and deterministic.
Do not make this overcomplicated.
The point is to create the safe control structure.

================================================================================
04 — INSERT / MANIFEST RECOGNITION
================================================================================

insert_cartridge(cartridge) should:

- set cartridge inserted
- record event
- move state to cartridge_inserted
- not allow playback yet

recognize_manifest() should:

- check cartridge exists
- check cartridge.recognized or set recognized if sample data is valid
- check manifest_matched
- move state to manifest_recognized if valid
- fail_closed with fail_closed_manifest_mismatch if invalid

No real manifest parser is required in this run if the sample model already has manifest_id / manifest_matched.

================================================================================
05 — PREFETCH CURRENT / VERIFY CURRENT
================================================================================

prefetch_current() should:

- choose first playback-required section
- set expected/prefetched section fields
- mark timing/index, registration, metadata, hash as read from the section model
- move state to prefetch_current
- record event

verify_current() should:

- call verify_physical_section(section)
- store current_verification_state
- if display_allowed true:
  move to verify_current
- if decision is rescan_required:
  move to rescan_required
- if rejected_fail_closed:
  fail_closed with the verification fail reason

================================================================================
06 — LOAD AND LOCK VIEW GATE
================================================================================

load_view_gate() should:

- require current section display_allowed
- set view_gate_state.section_id
- set view gate state to loading or fine_aligned
- record event
- move to load_view_gate

lock_view_gate() should:

- set view gate locked true
- set aligned true
- set illumination_allowed true only if verification display_allowed is true
- move to view_gate_locked
- record event

enter_playback_ready() should:

- require view gate locked
- require display_allowed true
- set current section visible
- set safety state playback_allowed
- move to playback_ready
- record event

================================================================================
07 — PREFETCH / VERIFY / STAGE NEXT
================================================================================

prefetch_next() should:

- find the next playback-required section after current_section_id
- update ReaderPrefetchState
- move to prefetch_next
- record event

If no next section exists:
- move to playback_complete
- record event

verify_next() should:

- call verify_physical_section(next section)
- store next_verification_state
- if display_allowed true:
  move to verify_next
- if rescan_required:
  move to rescan_required
- if rejected_fail_closed:
  fail_closed with the verification reason

stage_next() should:

- require next_verification_state.display_allowed true
- set hidden_gate_state.section_id
- set hidden gate verified true
- set hidden gate ready_for_switch true
- set ABGateState.hidden_section_id
- move to stage_next
- record event

================================================================================
08 — TIMING AND TRANSITION
================================================================================

wait_until_update_timestamp(target_timestamp_ms) should:

- advance current_time_ms to target_timestamp_ms if needed
- require hidden gate ready
- require next section verified
- move to wait_update_timestamp
- record event

begin_transition_blank() should:

- require hidden gate ready
- require transition system safe
- set blanking_active true
- set shutter/illumination to blanking/closed or equivalent
- move to transition_blank
- record event

switch_visible_section() should:

- require blanking active
- require hidden_gate_state.ready_for_switch true
- require next_verification_state.display_allowed true
- move current view gate section into old/current for parking
- move hidden section into visible gate / current_section_id
- update AB gate visible/hidden section fields
- set current section visible
- clear next section
- move to switch_visible_section
- record event

park_old_section() should:

- add old section to reverse buffer if enabled
- respect reverse_buffer_depth
- clear old/parked state
- stop blanking
- set illumination stable
- move to park_old_section
- record event
- then allow prefetch_next again

================================================================================
09 — TICK METHOD
================================================================================

tick(delta_ms) should:

- increment current_time_ms
- record a tick event if useful
- not automatically make unsafe transitions
- not display unverified sections

Do not create hidden asynchronous/background work.
This is a deterministic simulator method only.

================================================================================
10 — PAUSE / RESUME
================================================================================

pause() should:

- set state paused_safe
- keep current section visible only if it was already verified and gate-locked
- motion_allowed false
- record event

resume() should:

- if safe state and current section verified:
  return to playback_ready
- otherwise fail_closed or rescan_required
- record event

================================================================================
11 — STEP FORWARD
================================================================================

step_forward() should run one safe transition cycle:

prefetch_next()
verify_next()
stage_next()
wait_until_update_timestamp(...)
begin_transition_blank()
switch_visible_section()
park_old_section()

It should stop early if any method fails closed.

================================================================================
12 — REVERSE
================================================================================

step_reverse() should:

- check reverse_buffer_state.enabled
- check reverse buffer has previous section
- if not available:
  deny safely and record event
- if available:
  set requested_reverse_section_id
  verify previous section if available in cartridge
  stage previous section
  blank transition
  switch visible section
  record event

Do not claim arbitrary physical reverse.
This is limited local-buffer reverse only.

================================================================================
13 — SEEK
================================================================================

request_seek(timestamp_ms=None, section_id=None) should:

- support local buffer seek only for now
- if requested section is in reverse buffer or prefetch queue:
  allow safe seek path
- otherwise:
  deny safely
  set seek_available false
  denial_reason = unsupported_or_not_in_local_buffer
  record event

Do not claim arbitrary physical seek.

================================================================================
14 — FAIL-CLOSED
================================================================================

fail_closed(reason, recommended_action) should:

- create FailClosedDecision
- append to fail_closed_events
- set playback_state fail_closed
- set safety_state fail_closed
- set display_allowed false unless holding a previously verified safe state
- set transition_allowed false
- set motion_allowed false
- record event
- never increment unsafe acceptance as a success path

Allowed reasons should include:

fail_closed_unverified_section
fail_closed_wrong_section
fail_closed_hash_mismatch
fail_closed_registration_failure
fail_closed_gate_unlocked
fail_closed_prefetch_timeout
fail_closed_shutter_failure
fail_closed_illumination_failure
fail_closed_jam
fail_closed_manifest_mismatch
fail_closed_unsupported_carrier
fail_closed_audio_sync_limit

================================================================================
15 — EVENT LOG
================================================================================

Every state transition should add an event dict:

- timestamp_ms
- event_type
- from_state
- to_state
- current_section_id
- next_section_id
- detail
- safety_state
- display_allowed

The event log should be JSON serializable.

================================================================================
16 — REPORTS
================================================================================

Create or update:

src/amcf_physical_player_state_machine_reports.py

Implement:

- state_machine_to_dict(machine)
- write_state_machine_timeline(machine, path)
- write_fail_closed_events(machine, path)
- build_state_machine_summary_markdown(machine) -> str

The markdown summary must include:

- software/control simulator only
- what can be done without hardware
- no physical hardware validation claimed
- default folded A/B motor/encoder profile
- number of events
- number of fail-closed events
- unsafe_acceptance_count
- final playback state
- final safety state

================================================================================
17 — DOCS
================================================================================

Create or update:

docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md

Include:

- purpose
- corrected framing:
  software/control structure can be built now;
  hardware validation comes later
- state list
- normal forward state chain
- failure branch
- reverse branch
- seek branch
- fail-closed rules
- what can be tested without hardware
- what is not claimed

Create or update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Mark Stage 2:

AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1

as implementing:

- safe forward playback cycle
- state transitions
- event logs
- fail-closed integration
- local reverse/seek denial basics

Do not mark physical hardware as complete.

================================================================================
18 — DEMO
================================================================================

Create:

demo/run_physical_player_state_machine_demo.py

The demo should:

1. build sample model bundle or sample cartridge from AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
2. create AMCFPhysicalPlayerStateMachine
3. insert cartridge
4. recognize manifest
5. prefetch current
6. verify current
7. load and lock view gate
8. enter playback ready
9. run at least two safe step_forward() transitions
10. attempt a degraded colour section if sample data supports it
11. attempt a hash mismatch or invalid section path and show fail-closed
12. attempt unsupported arbitrary seek and show safe denial
13. write output files

Output folder:

output/physical_player_state_machine_demo/

Output files:

- state_machine_timeline.json
- fail_closed_events.json
- final_state.json
- STATE_MACHINE_SUMMARY.md

The demo must be deterministic.

================================================================================
19 — TESTS
================================================================================

Create or update:

tests/test_physical_player_state_machine.py

Tests must verify:

1. state machine starts at no_cartridge
2. insert_cartridge moves to cartridge_inserted
3. recognize_manifest moves to manifest_recognized for valid sample
4. invalid manifest fails closed
5. prefetch_current chooses a section
6. verify_current accepts valid section
7. load_view_gate requires verification
8. lock_view_gate sets locked/aligned/illumination_allowed
9. playback_ready requires locked verified section
10. prefetch_next finds next section
11. verify_next rejects hash mismatch
12. stage_next requires next section display_allowed
13. transition requires hidden gate ready
14. switch_visible_section requires blanking active
15. park_old_section adds previous section to reverse buffer
16. step_forward performs a safe transition for valid next section
17. step_forward fails closed on invalid next section
18. step_reverse works only when reverse buffer has section
19. arbitrary seek outside local buffer is safely denied
20. fail_closed creates FailClosedDecision
21. unsafe_acceptance_count remains zero
22. summary says software/control simulator only and no hardware validation claimed

Use unittest and standard library unless the repo already uses pytest.

================================================================================
20 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile src/amcf_physical_player_state_machine.py
python -m py_compile src/amcf_physical_player_state_machine_reports.py
python -m py_compile demo/run_physical_player_state_machine_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_state_machine_demo.py

If file names differ because you extended existing files, adjust commands and report exact commands used.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
21 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add docs src demo tests
git commit -m "Add physical player state machine foundation"

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- demo output folder
- test results
- git status
- git diff --stat

================================================================================
22 — FINAL REPORT
================================================================================

In final response, report:

- run name
- corrected framing preserved yes/no
- files created
- files modified
- demo output folder
- validation commands run
- test results
- final playback state
- fail-closed event count
- unsafe_acceptance_count
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim a manufactured physical player exists.
```

---

## 5. What Part 9 decides

```text id="huuz7f"
Part 9 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
```

This run builds:

```text id="eviefb"
- deterministic physical-player software state machine
- cartridge insertion flow
- manifest recognition flow
- prefetch current / verify current
- load and lock view gate
- playback-ready state
- prefetch next / verify next / stage next
- transition blanking
- visible section switch
- old section parking
- limited reverse buffer
- safe seek denial
- fail-closed event creation
- event timeline
- demo outputs
- tests
```

It does **not** build hardware yet.

But it does build the software/control structure needed before hardware can be arranged and made.

---

## 6. What Part 10 should cover next

```text id="g21zrp"
Part 10 should be:

Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
```

That next run should harden failure cases:

```text id="9j4gqz"
wrong section
hash mismatch
missing marker
registration failure
prefetch timeout
gate unlocked
shutter failure
illumination failure
jam/misfeed placeholder
audio drift limit
unsafe acceptance audit
structured safety report
```

Part 9 stops here because the state-machine implementation prompt is now defined.
----

Pushed result understood.

Current state from your pasted run:

```text id="vnf3we"
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
Commit: f8b6e91e1dfd9b57345ee38ac262635d446f47c8
Pushed: yes
Branch: main
Result: state-machine foundation added
Tests: 98 passed
Demo: passed
unsafe_acceptance_count: 0
```

So Part 10 should now continue exactly as planned:

```text id="eoprn3"
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
```

This should harden the safety/failure layer on top of the state-machine commit, not restart the simulator.

# AMCF Physical Player Design and Structure Dossier  
## Part 10 — Codex-Ready Implementation Prompt for Physical Player Fail-Closed V1

## 1. Purpose of Part 10

Part 9 produced the implementation prompt for:

```text id="yzksr2"
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
```

That run is now completed and pushed as:

```text id="cz723h"
f8b6e91e1dfd9b57345ee38ac262635d446f47c8
```

It added:

```text id="hqdv4k"
src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
demo/run_physical_player_state_machine_demo.py
tests/test_physical_player_state_machine.py
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE_AUDIT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
```

Part 10 now defines the next Codex run:

```text id="fe23my"
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
```

The purpose is to harden the safety model.

The current state machine already has fail-closed events and one intentionally bad-section fail-closed path. This next run should expand that into a more complete failure/safety layer:

```text id="j9zkxk"
wrong section
hash mismatch
missing marker
registration failure
prefetch timeout
gate unlocked
shutter failure
illumination failure
jam/misfeed placeholder
audio drift limit
unsafe acceptance audit
structured safety report
```

This run should not build hardware.

It should implement the software/control safety behaviour that future hardware must obey.

---

## 2. Correct framing

Do not frame this as:

```text id="vo1dqx"
This is only theoretical because hardware does not exist.
```

Frame it as:

```text id="lig93f"
This is the fail-closed software/control layer required before hardware can safely be arranged, built, and tested.
```

The hardware is not present yet, but the software can already define:

```text id="ayfdku"
- what conditions are unsafe
- what must stop playback
- what can be retried
- what can be degraded but allowed
- what must never be displayed
- what the future hardware must report
- what timeline/report evidence must exist
```

So this run is meaningful because it creates the safety contract for later physical mechanisms.

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_fail_closed_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

f8b6e91e1dfd9b57345ee38ac262635d446f47c8

That commit added the physical-player software/control state-machine foundation:

- src/amcf_physical_player_state_machine.py
- src/amcf_physical_player_state_machine_reports.py
- demo/run_physical_player_state_machine_demo.py
- tests/test_physical_player_state_machine.py
- docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE_AUDIT.md
- docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
- docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 98 tests
- state-machine demo: PASS
- final playback state: park_old_section
- fail-closed event count: 1
- unsafe_acceptance_count: 0
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no

This run should extend that foundation.

Do not restart it.
Do not replace it with a separate incompatible simulator.
Do not duplicate state-machine classes unless a small helper class is clearly needed.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run implements the fail-closed software/control safety layer that a future physical AMCF player must obey.

Correct framing:

- The hardware is not present yet.
- The software can still define unsafe conditions and safe responses now.
- Later hardware should conform to this fail-closed logic.
- The repo can test wrong sections, marker failures, hash failures, gate failures, prefetch failures, shutter/illumination failures, jam placeholders, and audio drift limits before real hardware exists.

Do not claim:

- manufactured hardware
- real sensors
- real motors
- real cartridge validation
- real optical playback proof
- real no-gap proof
- physical Level 5 completion
- hardware validation

Do claim:

- software/control safety model
- deterministic fail-closed simulator behaviour
- structured fail-closed decisions
- unsafe-acceptance prevention
- future hardware-support safety contract

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator baseline:

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

The physical player should not advance one page for every fixed video frame.
It should advance according to AMCF update events.

The safety rule:

A section may be displayed only if it is verified, staged, gate-locked, and safe.

If a critical lane, section identity, gate state, transition state, or sync state fails:
pause, rescan, blank, stop, or fail closed.
Never display an unsafe section.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md

docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE_AUDIT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_mechanical_optical_player.py if present
src/amcf_virtual_hardware.py if present

demo/run_physical_player_state_machine_demo.py

tests/test_physical_player_state_machine.py
other existing tests

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP.
Do not push.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim hardware validation.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_AUDIT.md

Include:

- current git HEAD
- whether f8b6e91 or later is present
- which state-machine files exist
- what fail-closed support already exists
- which fail-closed scenarios are already tested
- which fail-closed scenarios this run will add
- which files will be edited
- which files will be created
- confirmation that this is software/control safety implementation
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — FAIL-CLOSED REASON MODEL
================================================================================

Update or extend:

src/amcf_physical_player_state_machine.py

Add a clear fail-closed reason catalogue if not already present.

Required reasons:

fail_closed_unverified_section
fail_closed_wrong_section
fail_closed_hash_mismatch
fail_closed_missing_marker
fail_closed_registration_failure
fail_closed_gate_unlocked
fail_closed_prefetch_timeout
fail_closed_shutter_failure
fail_closed_illumination_failure
fail_closed_jam
fail_closed_double_feed
fail_closed_misfeed
fail_closed_manifest_mismatch
fail_closed_unsupported_carrier
fail_closed_audio_sync_limit
fail_closed_unsafe_transition
fail_closed_hidden_gate_not_ready
fail_closed_view_gate_not_locked
fail_closed_unknown_critical_lane

Do not use vague failure strings where structured reasons are possible.

================================================================================
02 — SAFETY DECISION MODEL
================================================================================

Add or extend a lightweight safety decision helper.

Suggested name:

PhysicalPlayerSafetyDecision

If you prefer not to add a dataclass, a JSON-serializable dict is acceptable, but keep it structured.

Fields:

- decision_id
- timestamp_ms
- decision
- reason
- severity
- current_section_id
- next_section_id
- display_allowed
- motion_allowed
- transition_allowed
- rescan_allowed
- retry_allowed
- hold_previous_safe_state_allowed
- recommended_action
- unsafe_acceptance
- notes

Allowed decisions:

accepted
accepted_with_warning
rescan_required
retry_allowed
hold_previous_safe_state
rejected_fail_closed
mechanical_stop

Allowed severity:

info
warning
recoverable
critical
mechanical_stop

Rules:

- critical failures must set display_allowed false
- critical failures must set unsafe_acceptance false
- wrong section must reject/fail closed
- hash mismatch must reject/fail closed unless explicitly modeled as rescan before display
- missing critical marker must rescan or fail closed
- gate unlocked must fail closed before illumination/display
- hidden gate not ready must prevent transition
- shutter/illumination failure must prevent visible switching
- jam/misfeed must mechanical_stop or fail closed
- audio sync limit must pause/resync or fail closed
- unsafe_acceptance must never be true in successful code paths

================================================================================
03 — SECTION FAILURE SCENARIOS
================================================================================

Extend sample data or add helpers to create failure sections.

Required sample scenarios:

1. valid section
2. degraded colour section
3. hash mismatch section
4. missing marker section
5. wrong section index
6. invalid timing/index section
7. invalid registration section
8. unsupported section type
9. missing metadata critical section
10. unknown hash status section

If the existing sample cartridge already has some of these, extend it rather than replacing it.

Each sample should be deterministic.

================================================================================
04 — VERIFY SECTION HARDENING
================================================================================

Find the existing section verification logic.

Harden it so these decisions are explicit:

Valid section:
decision accepted
display_allowed true
unsafe_acceptance false

Degraded colour only:
decision accepted_with_degraded_colour or accepted_with_warning
display_allowed true
unsafe_acceptance false

Hash mismatch:
decision rejected_fail_closed or rescan_required before display
display_allowed false
unsafe_acceptance false
reason fail_closed_hash_mismatch

Missing marker:
decision rescan_required or rejected_fail_closed
display_allowed false
unsafe_acceptance false
reason fail_closed_missing_marker

Wrong section:
decision rejected_fail_closed
display_allowed false
unsafe_acceptance false
reason fail_closed_wrong_section

Invalid timing/index:
decision rejected_fail_closed
display_allowed false
unsafe_acceptance false
reason fail_closed_unverified_section or fail_closed_unknown_critical_lane

Invalid registration:
decision rejected_fail_closed or rescan_required
display_allowed false
unsafe_acceptance false
reason fail_closed_registration_failure

Unsupported section type:
decision rejected_fail_closed
display_allowed false
unsafe_acceptance false
reason fail_closed_unsupported_carrier or unsupported_section_type

Unknown critical lane:
decision rejected_fail_closed
display_allowed false
unsafe_acceptance false
reason fail_closed_unknown_critical_lane

================================================================================
05 — PREFETCH TIMEOUT
================================================================================

Add or extend a deterministic prefetch timeout path.

Implement a method or helper such as:

simulate_prefetch_timeout()
or
prefetch_next(timeout=True)
or a test helper that forces ReaderPrefetchState to timeout.

Expected behaviour:

- playback_state becomes fail_closed or rescan_required depending on existing style
- fail_closed event reason:
  fail_closed_prefetch_timeout
- display_allowed false for the unverified next section
- transition_allowed false
- unsafe_acceptance_count remains zero

Do not allow transition if prefetch did not verify the next section.

================================================================================
06 — GATE SAFETY FAILURES
================================================================================

Add or extend gate safety checks.

Scenarios:

1. view gate not locked
2. hidden gate not ready
3. transition requested without blanking active
4. visible switch requested with unverified next section

Expected behaviours:

View gate not locked:
reason fail_closed_view_gate_not_locked or fail_closed_gate_unlocked
display_allowed false
illumination_allowed false

Hidden gate not ready:
reason fail_closed_hidden_gate_not_ready
transition_allowed false

No blanking active:
reason fail_closed_unsafe_transition
switch denied

Unverified next section:
reason fail_closed_unverified_section
switch denied

Tests must prove these paths.

================================================================================
07 — SHUTTER / ILLUMINATION FAILURES
================================================================================

Add simple software-control placeholders for shutter/illumination failure.

No hardware drivers.

Scenarios:

- shutter stuck open
- shutter stuck closed
- illumination fault
- illumination cannot blank

Expected behaviours:

shutter stuck open during transition:
reason fail_closed_shutter_failure
transition denied

shutter stuck closed:
playback cannot visibly continue
reason fail_closed_shutter_failure

illumination fault:
reason fail_closed_illumination_failure
display_allowed false

illumination cannot blank:
reason fail_closed_illumination_failure or fail_closed_unsafe_transition
switch denied

These can be modeled as state fields and test helpers.
No real shutter code.

================================================================================
08 — JAM / MISFEED PLACEHOLDERS
================================================================================

Add deterministic placeholder handling for:

- jam
- double feed
- misfeed

No real sensors.

Methods may be:

simulate_jam()
simulate_double_feed()
simulate_misfeed()

Expected behaviours:

jam:
playback_state mechanical_stop or fail_closed
reason fail_closed_jam
motion_allowed false
transition_allowed false

double feed:
reason fail_closed_double_feed
display_allowed false

misfeed:
reason fail_closed_misfeed
display_allowed false

These are software safety states for future hardware to report later.

================================================================================
09 — AUDIO SYNC LIMIT
================================================================================

Add or extend audio sync safety.

Scenario:

visual playback falls behind audio beyond allowed threshold.

Implement:

check_audio_sync(max_drift_ms=...)

or equivalent.

Expected behaviours:

minor drift:
warning / resync_required allowed

major drift:
fail_closed_audio_sync_limit or paused_safe/resync_required
transition/display of unsafe state denied
unsafe_acceptance_count remains zero

No real audio playback required.

================================================================================
10 — UNSAFE ACCEPTANCE AUDIT
================================================================================

Add a helper:

audit_unsafe_acceptance()

It should inspect:

- verification decisions
- event log
- fail-closed events
- safety state
- any display_allowed events for invalid sections

It should return a JSON-serializable report:

- unsafe_acceptance_count
- unsafe_events
- checked_event_count
- checked_section_count
- passed

Expected:

passed true
unsafe_acceptance_count 0

Add this to reports and demo output.

================================================================================
11 — REPORT HELPERS
================================================================================

Update:

src/amcf_physical_player_state_machine_reports.py

Add helpers:

- build_fail_closed_safety_report(machine)
- write_fail_closed_safety_report(machine, path)
- build_unsafe_acceptance_audit(machine)
- write_unsafe_acceptance_audit(machine, path)

The safety report should include:

- run type
- software/control safety model
- hardware validation claimed: false
- physical Level 5 claimed: false
- real sensors required: false
- fail-closed event count
- fail-closed reasons encountered
- unsafe_acceptance_count
- passed
- recommended next stage

================================================================================
12 — DOCS
================================================================================

Create or update:

docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md

Include:

- purpose
- why fail-closed software can be built before hardware
- structured fail-closed reasons
- safety decision model
- section failure scenarios
- prefetch timeout
- gate failure
- shutter/illumination failure placeholders
- jam/misfeed placeholders
- audio sync limit
- unsafe acceptance audit
- what is not claimed

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Mark Stage 3:

AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1

as implementing:

- failure hardening
- structured safety decisions
- expanded fail-closed reasons
- unsafe acceptance audit
- deterministic failure demo
- tests

Do not mark hardware complete.

================================================================================
13 — DEMO
================================================================================

Create:

demo/run_physical_player_fail_closed_demo.py

The demo should:

1. build or load sample cartridge/state-machine
2. run one valid section path
3. run degraded colour warning path
4. trigger hash mismatch failure
5. trigger missing marker failure
6. trigger wrong section failure
7. trigger invalid registration failure
8. trigger prefetch timeout
9. trigger hidden gate not ready
10. trigger view gate unlocked
11. trigger shutter/illumination failure placeholder
12. trigger jam/double-feed/misfeed placeholders
13. trigger audio sync limit
14. run unsafe acceptance audit
15. write output files

Output folder:

output/physical_player_fail_closed_demo/

Output files:

- fail_closed_scenarios.json
- fail_closed_events.json
- unsafe_acceptance_audit.json
- safety_report.json
- FAIL_CLOSED_SUMMARY.md

The demo must be deterministic.

================================================================================
14 — TESTS
================================================================================

Create or update:

tests/test_physical_player_fail_closed.py

Tests must verify:

1. valid section path accepted
2. degraded colour accepted with warning and unsafe_acceptance false
3. hash mismatch rejected/fail-closed
4. missing marker rescan or fail-closed
5. wrong section rejected/fail-closed
6. invalid timing/index rejected/fail-closed
7. invalid registration rejected/fail-closed or rescan before display
8. unsupported section type rejected/fail-closed
9. unknown critical lane rejected/fail-closed
10. prefetch timeout prevents transition
11. view gate unlocked prevents display
12. hidden gate not ready prevents transition
13. switch without blanking is denied
14. unverified next section cannot switch visible
15. shutter failure denies transition
16. illumination failure denies display/switch
17. jam creates mechanical stop or fail-closed
18. double feed fails closed
19. misfeed fails closed
20. audio sync limit pauses/resyncs/fails closed safely
21. unsafe acceptance audit reports zero
22. safety report says hardware validation claimed false
23. safety report says physical Level 5 claimed false
24. full unittest suite passes

Use unittest and standard library unless the repo already uses pytest.

================================================================================
15 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile src/amcf_physical_player_state_machine.py
python -m py_compile src/amcf_physical_player_state_machine_reports.py
python -m py_compile demo/run_physical_player_state_machine_demo.py
python -m py_compile demo/run_physical_player_fail_closed_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_fail_closed_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in the previous successful run, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
16 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add docs src demo tests
git commit -m "Harden physical player fail-closed safety model"

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_physical_player_fail_closed.py

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- demo output folder
- test results
- git status
- git diff --stat

================================================================================
17 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- demo output folder
- validation commands run
- test results
- fail-closed scenario count
- fail-closed event count
- unsafe_acceptance_count
- safety report passed yes/no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 10 decides

```text id="zdgxao"
Part 10 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
```

This run should harden the fail-closed layer by adding:

```text id="j12i8r"
- structured fail-closed reason catalogue
- safety decision model
- expanded section failure scenarios
- prefetch timeout handling
- gate safety failures
- shutter/illumination failure placeholders
- jam/double-feed/misfeed placeholders
- audio sync limit handling
- unsafe acceptance audit
- safety report
- deterministic failure demo
- tests
```

It should build on the already pushed state-machine foundation.

It should not restart the simulator, replace the state machine, or claim hardware proof.

---

## 5. What Part 11 should cover next

```text id="b9z6g0"
Part 11 should be:

Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
```

That next run should refine:

```text id="xk2qn4"
- limited reverse buffer
- step-back behaviour
- local-buffer seek
- safe arbitrary-seek denial
- reverse timeline reports
- reverse safety checks
- interaction between reverse, A/B gates, and fail-closed logic
```

Part 10 stops here because the fail-closed implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="zdo1lt"
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
Base commit: f8b6e91e1dfd9b57345ee38ac262635d446f47c8
New commit: 4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e
Pushed: yes
Tests: 121 passed
Fail-closed scenario count: 21
Fail-closed event count: 10
unsafe_acceptance_count: 0
Safety report passed: yes
```

So Part 11 should build directly on `4716c3b`, not restart the simulator.

# AMCF Physical Player Design and Structure Dossier  
## Part 11 — Codex-Ready Implementation Prompt for Physical Player Reverse / Seek V1

## 1. Purpose of Part 11

Part 10 completed and pushed:

```text id="n0kyr2"
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
```

Commit:

```text id="yu3m8k"
4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e
```

That run hardened the fail-closed software/control safety layer:

```text id="wd8jd4"
- structured fail-closed reasons
- safety decisions
- failure-section samples
- prefetch timeout handling
- gate safety failures
- shutter/illumination placeholders
- jam/double-feed/misfeed placeholders
- audio sync limit
- unsafe acceptance audit
- fail-closed demo
- 121 passing tests
```

Part 11 now defines the next Codex run:

```text id="vkiufw"
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
```

This run should refine:

```text id="qxxu0d"
- limited reverse buffer
- step-back behaviour
- local-buffer seek
- safe arbitrary-seek denial
- reverse timeline reports
- seek timeline reports
- reverse safety checks
- interaction between reverse, A/B gates, hidden staging, view gate, transition blanking, and fail-closed logic
```

This is still software/control architecture for future hardware alignment.

It does not claim real hardware reverse, real motor reverse, physical random access, or actual manufactured seek mechanics.

---

## 2. Correct framing

Do not frame this as:

```text id="ih3myf"
We cannot do reverse/seek until hardware exists.
```

Correct framing:

```text id="cg5imw"
The hardware is not present yet, but the software/control model can define how reverse and seek must behave safely when hardware is later arranged.

The simulator can model:
- what sections are locally available
- what sections are no longer available
- when reverse is safe
- when reverse must be denied
- when a local seek is possible
- when arbitrary seek must be denied
- how A/B staging interacts with reverse
- how fail-closed prevents unsafe reverse display
```

So the boundary is:

```text id="yz4c2r"
Software/control reverse and seek logic: can be implemented now.
Physical reverse/seek hardware proof: later hardware/testing.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_reverse_seek_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e

That commit completed:

AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 121 tests
- fail-closed demo: PASS
- fail-closed scenario count: 21
- fail-closed event count: 10
- unsafe_acceptance_count: 0
- safety report passed: yes
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no

This run should extend the existing state-machine and fail-closed work.

Do not restart the simulator.
Do not create a parallel incompatible player model.
Do not weaken the existing fail-closed behaviour.
Do not claim hardware validation.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run implements the reverse/seek software-control layer that future physical AMCF player hardware should obey.

Correct framing:

- The hardware is not present yet.
- The software can define safe reverse and seek rules now.
- Later hardware should conform to these reverse/seek limits and safety decisions.
- The simulator can test local reverse, local seek, arbitrary seek denial, reverse buffer limits, A/B staging during reverse, and fail-closed interaction before real hardware exists.

Do not claim:

- manufactured hardware
- real motor reverse
- real random-access hardware
- real physical cartridge reverse validation
- real optical playback proof
- real no-gap reverse proof
- physical Level 5 completion
- hardware validation

Do claim:

- software/control reverse model
- deterministic reverse/seek simulator behaviour
- bounded reverse buffer
- safe arbitrary-seek denial
- future hardware-support control contract
- interaction with existing fail-closed safety logic

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator baseline:

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

Reverse/seek rule:

- Reverse starts as limited local-buffer step-back.
- Local seek may be allowed only if the target section is in a verified local buffer.
- Arbitrary physical seek across the whole cartridge is not claimed.
- Unsafe reverse/seek must be denied safely.
- A/B staging and transition blanking still apply during reverse/seek.
- Fail-closed logic must block unverified, wrong, corrupted, or unstaged sections.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md

docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
other existing tests

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP.
Do not push.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical reverse hardware.
Do not claim arbitrary physical seek hardware.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_AUDIT.md

Include:

- current git HEAD
- whether 4716c3b or later is present
- which state-machine files exist
- which fail-closed files exist
- current reverse/seek support found
- current reverse/seek tests found
- gaps this run will fill
- files to edit
- files to create
- confirmation that this is software/control reverse-seek implementation
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — REVERSE / SEEK MODEL HARDENING
================================================================================

Update:

src/amcf_physical_player_state_machine.py

Extend the existing reverse/seek model without replacing the whole state machine.

Add or harden structures/fields for:

Reverse buffer:
- enabled
- depth
- section_ids
- section_records if helpful
- current_index
- reverse_available
- requested_reverse_section_id
- reverse_denial_reason
- last_reverse_timestamp_ms

Seek state:
- requested_timestamp_ms
- requested_section_id
- seek_mode
- seek_available
- seek_status
- denial_reason
- resolved_section_id
- resolved_from_buffer

Reverse / seek safety:
- reverse_transition_allowed
- seek_transition_allowed
- reverse_fail_closed_reason
- seek_fail_closed_reason

Do not overcomplicate this with real hardware movement.
Keep it deterministic.

================================================================================
02 — REVERSE / SEEK CONSTANTS
================================================================================

Add clear constants or string values for reverse and seek states.

Reverse statuses:

reverse_not_requested
reverse_available
reverse_buffer_empty
reverse_target_not_found
reverse_target_unverified
reverse_staged
reverse_transition_blank
reverse_switched
reverse_denied
reverse_fail_closed

Seek modes:

no_seek
local_buffer_seek
prefetch_queue_seek
arbitrary_seek_requested
reindex_required
unsupported

Seek statuses:

seek_not_requested
seek_available
seek_resolved_local_buffer
seek_resolved_prefetch_queue
seek_denied_not_in_local_buffer
seek_denied_arbitrary_not_supported
seek_denied_unverified_target
seek_fail_closed

Keep arbitrary physical seek denied by default.

================================================================================
03 — REVERSE BUFFER RECORDS
================================================================================

The reverse buffer should not store only raw IDs if that makes safety checks weak.

Either keep existing section_ids and add lookup against cartridge sections, or add a simple record structure.

Suggested reverse buffer record:

- section_id
- section_index
- timestamp_start_ms
- dwell_ms
- verification_decision
- display_allowed
- gate_locked_when_displayed
- parked_at_ms
- safe_for_reverse

Only sections that were actually verified and displayed safely should become safe reverse targets.

Rules:

- Valid displayed section can enter reverse buffer.
- Invalid section must never enter reverse buffer as safe target.
- Hash mismatch section must never enter safe reverse buffer.
- Wrong section must never enter safe reverse buffer.
- Reverse buffer must respect depth.
- Oldest entries drop first when depth exceeded.

================================================================================
04 — STEP-BACK / REVERSE METHOD
================================================================================

Update or add:

step_reverse()

Required behaviour:

1. Check reverse buffer enabled.
2. Check reverse buffer has at least one previous safe target.
3. Resolve previous target section.
4. Verify the target section still passes safety checks.
5. Stage target in hidden gate.
6. Require hidden gate ready.
7. Require transition blanking.
8. Switch visible section to previous target.
9. Park the old current section safely.
10. Update current_section_id.
11. Record reverse timeline events.
12. Preserve unsafe_acceptance_count = 0.

If reverse buffer is empty:

- deny safely
- set reverse_denial_reason = reverse_buffer_empty
- do not fail hardware
- do not display anything unsafe

If target section fails verification:

- fail closed or deny safely
- reason fail_closed_unverified_section or fail_closed_hash_mismatch
- display_allowed false

If hidden gate is not ready:

- fail closed with fail_closed_hidden_gate_not_ready
- switch denied

If transition blanking cannot occur:

- fail closed with fail_closed_unsafe_transition or fail_closed_shutter_failure
- switch denied

================================================================================
05 — LOCAL SEEK METHOD
================================================================================

Update or add:

request_seek(timestamp_ms=None, section_id=None)

Required behaviour:

- If no target is provided:
  deny safely with denial_reason = missing_seek_target

- If target section is in reverse buffer:
  allow local_buffer_seek path if verified and safe.

- If target section is in current/prefetch buffer:
  allow prefetch_queue_seek path if verified and safe.

- If target section is not in local buffer:
  deny safely with seek_denied_not_in_local_buffer.

- If target is arbitrary future/past section outside local buffer:
  deny safely with seek_denied_arbitrary_not_supported.

- Do not claim physical random access.

Add helper if useful:

resolve_seek_target(timestamp_ms=None, section_id=None)

This should return:

- resolved_section_id
- seek_mode
- seek_available
- denial_reason

================================================================================
06 — SEEK EXECUTION METHOD
================================================================================

Add or update:

execute_seek()

or implement within request_seek if simpler.

If seek is available:

1. Verify target section.
2. Stage target in hidden gate.
3. Begin transition blanking.
4. Switch visible section.
5. Park previous section.
6. Record seek timeline events.
7. Update current_section_id.

If seek is denied:

- record event
- do not transition
- do not fail closed unless the request attempted unsafe display
- safety state remains paused_safe or playback_ready as appropriate
- unsafe_acceptance_count remains 0

================================================================================
07 — REVERSE / SEEK EVENT LOGGING
================================================================================

Every reverse/seek event must add an event dict to event_log.

Event fields should include:

- timestamp_ms
- event_type
- from_state
- to_state
- current_section_id
- next_section_id
- requested_section_id
- requested_timestamp_ms
- resolved_section_id
- seek_mode
- reverse_status
- seek_status
- detail
- safety_state
- display_allowed

Add event types:

reverse_requested
reverse_denied
reverse_target_resolved
reverse_staged
reverse_transition_blank
reverse_switched
reverse_complete
seek_requested
seek_denied
seek_target_resolved
seek_staged
seek_transition_blank
seek_switched
seek_complete

================================================================================
08 — REVERSE / SEEK REPORT HELPERS
================================================================================

Update:

src/amcf_physical_player_state_machine_reports.py

Add helpers:

- build_reverse_seek_report(machine)
- write_reverse_seek_report(machine, path)
- build_reverse_buffer_report(machine)
- write_reverse_buffer_report(machine, path)
- build_seek_denial_report(machine)
- write_seek_denial_report(machine, path)

Reports should include:

- software/control reverse-seek model
- hardware validation claimed: false
- physical Level 5 claimed: false
- real motors required: false
- reverse buffer depth
- reverse buffer entries
- reverse attempts
- reverse successes
- reverse denials
- seek attempts
- seek successes
- seek denials
- arbitrary seek denied count
- fail-closed count during reverse/seek
- unsafe_acceptance_count
- passed

================================================================================
09 — DOCS
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md

Include:

- purpose
- why reverse/seek software can be built before hardware
- limited reverse buffer model
- safe step-back model
- local-buffer seek model
- arbitrary seek denial
- interaction with A/B staging
- interaction with hidden gate
- interaction with view gate
- transition blanking during reverse/seek
- fail-closed integration
- unsafe acceptance rule
- what is not claimed

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Mark Stage 4:

AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1

as implementing:

- limited reverse buffer
- step-back behaviour
- local-buffer seek
- arbitrary seek denial
- reverse/seek timeline reporting
- fail-closed integration
- tests

Do not mark physical reverse hardware complete.

================================================================================
10 — DEMO
================================================================================

Create:

demo/run_physical_player_reverse_seek_demo.py

The demo should:

1. build sample cartridge/state-machine
2. run valid forward setup
3. run at least three forward transitions to populate reverse buffer
4. perform one successful step_reverse()
5. attempt reverse beyond buffer and deny safely
6. perform one successful local-buffer seek if available
7. attempt arbitrary seek outside local buffer and deny safely
8. attempt seek to hash-mismatch/invalid section and deny/fail closed safely
9. run unsafe acceptance audit
10. write output files

Output folder:

output/physical_player_reverse_seek_demo/

Output files:

- reverse_seek_timeline.json
- reverse_buffer_report.json
- seek_denial_report.json
- fail_closed_events.json
- unsafe_acceptance_audit.json
- reverse_seek_report.json
- REVERSE_SEEK_SUMMARY.md

The demo must be deterministic.

================================================================================
11 — TESTS
================================================================================

Create or update:

tests/test_physical_player_reverse_seek.py

Tests must verify:

1. reverse buffer starts empty
2. verified displayed sections enter reverse buffer
3. invalid sections do not enter safe reverse buffer
4. reverse buffer respects configured depth
5. step_reverse denied when buffer empty
6. step_reverse resolves previous safe section
7. step_reverse stages previous section in hidden gate
8. step_reverse uses transition blanking
9. step_reverse updates current_section_id
10. step_reverse records timeline events
11. reverse target hash mismatch fails closed or denies safely
12. reverse hidden gate not ready fails closed
13. reverse without blanking denied
14. local-buffer seek resolves available section
15. local-buffer seek switches only verified target
16. arbitrary seek outside local buffer is denied
17. seek to invalid section fails closed or denies safely
18. seek denial does not increment unsafe_acceptance_count
19. reverse/seek report says hardware validation claimed false
20. reverse/seek report says physical Level 5 claimed false
21. unsafe acceptance audit remains zero
22. full unittest suite passes

Use unittest and standard library unless the repo already uses pytest.

================================================================================
12 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile src/amcf_physical_player_state_machine.py
python -m py_compile src/amcf_physical_player_state_machine_reports.py
python -m py_compile demo/run_physical_player_state_machine_demo.py
python -m py_compile demo/run_physical_player_fail_closed_demo.py
python -m py_compile demo/run_physical_player_reverse_seek_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_reverse_seek_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in the previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
13 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add docs src demo tests
git commit -m "Add physical player reverse seek controls"

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_physical_player_reverse_seek.py

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- demo output folder
- test results
- git status
- git diff --stat

================================================================================
14 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- demo output folder
- validation commands run
- test results
- reverse attempts
- reverse successes
- reverse denials
- seek attempts
- seek successes
- seek denials
- arbitrary seek denied count
- fail-closed event count during reverse/seek
- unsafe_acceptance_count
- reverse/seek report passed yes/no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 11 decides

```text id="z8pt5i"
Part 11 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
```

This run should add:

```text id="dt131u"
- limited reverse buffer hardening
- safe step-back behaviour
- local-buffer seek
- arbitrary seek denial
- reverse/seek event logging
- reverse/seek reports
- reverse/seek tests
- fail-closed interaction
- unsafe acceptance audit preservation
```

It should build on:

```text id="aue28y"
4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e
```

It should not restart the simulator or claim hardware reverse/seek proof.

---

## 5. What Part 12 should cover next

```text id="wt9snt"
Part 12 should be:

Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
```

That next run should refine:

```text id="lcu91s"
- folded indexed carrier baseline
- motor/encoder baseline profile
- piezo/inchworm research profile
- two-track A/B shuttle candidate
- cartridge stack shuttle candidate
- chain/indexed carrier candidate
- spring/governor/brake comparison profile
- magnetic/guided clamp support profile
- energy recovery as support layer only
- mechanism comparison reports
- tests proving no research profile is presented as validated hardware
```

Part 11 stops here because the reverse/seek implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part12"
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
Base commit: 4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e
New commit: 802042b5395ac860c437188e0d79031d7dd5f591
Pushed: yes
Tests: 142 passed
Reverse successes: 1
Reverse denials: 1
Seek successes: 1
Seek denials: 1
Arbitrary seek denied count: 1
unsafe_acceptance_count: 0
```

So Part 12 should now build directly on `802042b`.

# AMCF Physical Player Design and Structure Dossier  
## Part 12 — Codex-Ready Implementation Prompt for Physical Player Mechanism Profiles V1

## 1. Purpose of Part 12

Part 11 completed and pushed:

```text id="part11_done"
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
```

Commit:

```text id="part11_commit"
802042b5395ac860c437188e0d79031d7dd5f591
```

That run refined:

```text id="part11_features"
- limited reverse buffer
- safe step-back behaviour
- local-buffer seek
- arbitrary seek denial
- reverse/seek event logging
- reverse/seek reports
- fail-closed interaction
- unsafe acceptance preservation
- 142 passing tests
```

Part 12 now defines the next Codex run:

```text id="part12_run"
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
```

The purpose is to formalize and compare the physical-player mechanism families as **software/control profiles**.

This is not CAD.

This is not hardware proof.

This is the profile layer that tells the simulator:

```text id="profile_layer"
Which physical-player mechanism family is being simulated?
What is the default baseline?
Which profiles are research candidates?
Which are support layers only?
Which ones are not allowed to be claimed as validated hardware?
```

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame"
We need real hardware before we can define mechanisms.
```

Correct framing:

```text id="correct_frame"
The hardware is not present yet, but the software can define mechanism profiles now.

These profiles become the control/specification layer for later hardware work. They define what kind of transport, staging, actuator, guide, reverse, seek, and safety assumptions each future mechanism would require.
```

So the boundary is:

```text id="boundary"
Mechanism profile software/control model: can be implemented now.
Physical mechanism validation: requires later hardware/testing.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_mechanism_profiles_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

802042b5395ac860c437188e0d79031d7dd5f591

That commit completed:

AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 142 tests
- reverse/seek demo: PASS
- reverse attempts: 2
- reverse successes: 1
- reverse denials: 1
- seek attempts: 2
- seek successes: 1
- seek denials: 1
- arbitrary seek denied count: 1
- unsafe_acceptance_count: 0
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no

This run should extend the existing physical-player software/control model.

Do not restart the simulator.
Do not replace the state machine.
Do not create an incompatible parallel system.
Do not weaken fail-closed, reverse, seek, or claim-boundary behaviour.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run implements mechanism profiles for the future physical-player control architecture.

Correct framing:

- The hardware is not present yet.
- The software can define mechanism profiles now.
- Later hardware should be compared against these profile contracts.
- The simulator can use profiles to model assumptions about transport, staging, actuator family, guide/clamp support, reverse capability, seek capability, energy support, and claim status.
- Mechanism profiles are not physical validation.

Do not claim:

- manufactured hardware
- real motor validation
- real piezo validation
- real chain carrier validation
- real cartridge shuttle validation
- real folded-path mechanism validation
- real physical random access
- real no-gap optical switching proof
- physical Level 5 completion
- hardware validation

Do claim:

- software/control mechanism profile model
- simulator profile contracts
- default mechanism profile
- research mechanism profiles
- support-layer profiles
- mechanism comparison reports
- future hardware-support decision layer

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

claim_status:
software_control_profile_not_physical_validation

Mechanism ranking to preserve:

1. Folded indexed carrier + A/B staging + motor/encoder baseline
2. Folded indexed carrier + A/B staging + piezo/inchworm research profile
3. Two-track A/B shuttle candidate
4. Cartridge stack + shuttle candidate
5. Chain/indexed carrier research candidate
6. Constant-force spring + governor + brake comparison profile
7. Magnetic/guided clamp tracks as support layer
8. Energy recovery as support layer only
9. Experimental soft-actuator branch as research comparison only
10. Material-aligned carrier branch as material profile only

The first simulator default must remain:
folded indexed carrier + abstract A/B staging + motor/encoder baseline.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md

docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
other existing tests

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP.
Do not push.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim any mechanism is physically validated.
Do not claim physical Level 5 is complete.
Do not claim the folded path is manufactured.
Do not claim piezo/inchworm is proven.
Do not claim energy recovery powers the system.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_AUDIT.md

Include:

- current git HEAD
- whether 802042b or later is present
- existing state-machine files found
- existing fail-closed files found
- existing reverse/seek files found
- current mechanism/profile support found
- gaps this run will fill
- files to edit
- files to create
- confirmation that this is software/control mechanism-profile implementation
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — MECHANISM PROFILE MODULE
================================================================================

Create:

src/amcf_physical_player_mechanism_profiles.py

This module should define the mechanism-profile layer used by the simulator.

Use standard library only.

Use dataclasses.

Create:

AMCFMechanismProfile
AMCFMechanismProfileCapability
AMCFMechanismProfileRanking
AMCFMechanismProfileClaimBoundary
AMCFMechanismProfileComparisonReport

If similar classes already exist in the state-machine module, do not duplicate incompatible structures. Either:
1. import and reuse them, or
2. create this module as the canonical profile module and keep compatibility helpers for existing code.

The profile model should be JSON serializable.

================================================================================
02 — AMCFMechanismProfile FIELDS
================================================================================

AMCFMechanismProfile should include at least:

- profile_id
- display_name
- profile_family
- carrier_layout
- staging_model
- actuator_family
- gate_model
- prefetch_model
- reverse_model
- seek_model
- guide_model
- energy_support_model
- material_profile_model
- safety_model
- primary_use
- ranking_tier
- simulator_default
- research_candidate
- support_layer_only
- hardware_validated
- physical_level_5_claimed
- claim_status
- notes

Required boolean defaults:

hardware_validated = false
physical_level_5_claimed = false

Only the default profile should have:

simulator_default = true

Research profiles should have:

research_candidate = true
hardware_validated = false
physical_level_5_claimed = false

Support layers should have:

support_layer_only = true
simulator_default = false
hardware_validated = false
physical_level_5_claimed = false

================================================================================
03 — REQUIRED PROFILE IDS
================================================================================

Implement deterministic factory helpers for at least these profiles:

1. folded_ab_motor_encoder_baseline

2. folded_ab_inchworm_research

3. two_track_ab_shuttle_candidate

4. cartridge_stack_shuttle_candidate

5. chain_indexed_carrier_research

6. spring_governor_brake_comparison

7. magnetic_guided_clamp_support

8. energy_recovery_support_layer

9. soft_actuator_experimental_branch

10. material_aligned_carrier_branch

Also implement:

all_mechanism_profiles()
default_mechanism_profile()
profile_by_id(profile_id)
rank_mechanism_profiles(profiles)

================================================================================
04 — PROFILE DETAILS
================================================================================

Profile 1:

profile_id:
folded_ab_motor_encoder_baseline

display_name:
Folded A/B Motor Encoder Baseline

profile_family:
primary_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

guide_model:
edge_guides_and_stop_gates

energy_support_model:
none

material_profile_model:
parameterized_thin_section_carrier

safety_model:
fail_closed_required

primary_use:
default_simulator_control_profile

ranking_tier:
rank_1_primary

simulator_default:
true

research_candidate:
false

support_layer_only:
false

hardware_validated:
false

physical_level_5_claimed:
false

claim_status:
software_control_profile_not_physical_validation

Profile 2:

profile_id:
folded_ab_inchworm_research

display_name:
Folded A/B Inchworm Research Candidate

profile_family:
research_actuator_candidate

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
piezo_electrostatic_inchworm

gate_model:
single_visible_gate_plus_hidden_staging_or_dual_gate_candidate

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

guide_model:
clamp_step_release_guides

energy_support_model:
piezo_charge_recovery_optional_support_only

material_profile_model:
parameterized_thin_section_carrier

safety_model:
fail_closed_required

primary_use:
amcf_index_like_research_profile

ranking_tier:
rank_2_research

simulator_default:
false

research_candidate:
true

support_layer_only:
false

hardware_validated:
false

physical_level_5_claimed:
false

claim_status:
research_candidate_not_physical_validation

Profile 3:

profile_id:
two_track_ab_shuttle_candidate

profile_family:
layout_candidate

carrier_layout:
two_track_shuttle

staging_model:
ab_double_buffered_tracks

actuator_family:
motor_encoder_or_piezo_candidate

gate_model:
dual_track_visible_hidden_candidate

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

guide_model:
track_guides_and_stop_gates

energy_support_model:
none

ranking_tier:
rank_3_secondary

simulator_default:
false

research_candidate:
true

hardware_validated:
false

claim_status:
layout_candidate_not_physical_validation

Profile 4:

profile_id:
cartridge_stack_shuttle_candidate

profile_family:
layout_candidate

carrier_layout:
indexed_section_stack

staging_model:
stack_to_hidden_staging_shuttle

actuator_family:
motor_encoder_shuttle

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_or_reselect_required

seek_model:
local_buffer_or_reselect_future

guide_model:
stack_guides_and_stop_gates

ranking_tier:
rank_4_secondary_prototype

simulator_default:
false

research_candidate:
true

hardware_validated:
false

claim_status:
prototype_candidate_not_physical_validation

Profile 5:

profile_id:
chain_indexed_carrier_research

profile_family:
research_layout_candidate

carrier_layout:
chain_indexed_carrier

staging_model:
chain_positioned_ab_staging

actuator_family:
motor_encoder_chain_drive

gate_model:
view_gate_with_chain_flattening_requirement

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_chain_reverse_candidate

seek_model:
local_buffer_seek_only

guide_model:
chain_guides_stop_gates_and_flattening

ranking_tier:
rank_5_research

simulator_default:
false

research_candidate:
true

hardware_validated:
false

claim_status:
research_candidate_not_physical_validation

Profile 6:

profile_id:
spring_governor_brake_comparison

profile_family:
mechanical_comparison

carrier_layout:
folded_indexed_carrier_or_cartridge_stack

staging_model:
latched_indexed_staging

actuator_family:
constant_force_spring_governor_brake

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_only

seek_model:
not_default

guide_model:
brake_latch_stop_gate_support

ranking_tier:
rank_6_comparison

simulator_default:
false

research_candidate:
true

hardware_validated:
false

claim_status:
mechanical_comparison_not_physical_validation

Profile 7:

profile_id:
magnetic_guided_clamp_support

profile_family:
support_layer

carrier_layout:
not_primary_transport

staging_model:
supports_ab_staging

actuator_family:
not_primary_actuator

gate_model:
guide_clamp_stop_gate_support

prefetch_model:
supports_reader_prefetch_alignment

reverse_model:
supports_limited_reverse_alignment

seek_model:
support_only

guide_model:
magnetic_electrostatic_or_mechanical_guides

energy_support_model:
none

ranking_tier:
support_layer

simulator_default:
false

research_candidate:
false

support_layer_only:
true

hardware_validated:
false

claim_status:
support_layer_not_physical_validation

Profile 8:

profile_id:
energy_recovery_support_layer

profile_family:
support_layer

carrier_layout:
not_primary_transport

staging_model:
not_primary_staging

actuator_family:
not_primary_actuator

gate_model:
not_primary_gate

prefetch_model:
none

reverse_model:
none

seek_model:
none

guide_model:
none

energy_support_model:
electret_triboelectric_piezo_or_regenerative_recovery_support_only

ranking_tier:
support_layer

simulator_default:
false

research_candidate:
false

support_layer_only:
true

hardware_validated:
false

claim_status:
energy_support_only_not_power_solution_not_validation

Profile 9:

profile_id:
soft_actuator_experimental_branch

profile_family:
experimental_research

carrier_layout:
future_material_integrated_candidate

staging_model:
experimental

actuator_family:
dielectric_elastomer_hasel_electroactive_paper

gate_model:
experimental

prefetch_model:
reader_prefetch_required_if_ever_used

reverse_model:
unresolved

seek_model:
unresolved

guide_model:
unresolved

ranking_tier:
rank_9_experimental

simulator_default:
false

research_candidate:
true

support_layer_only:
false

hardware_validated:
false

claim_status:
experimental_branch_not_physical_validation

Profile 10:

profile_id:
material_aligned_carrier_branch

profile_family:
material_profile_branch

carrier_layout:
thin_section_carrier_material_branch

staging_model:
supports_future_folded_carrier_if_validated

actuator_family:
not_actuator

gate_model:
material_support_for_view_gate

prefetch_model:
marker_colour_lane_support

reverse_model:
material_dependent

seek_model:
material_dependent

guide_model:
material_dependent

material_profile_model:
nanocellulose_bacterial_cellulose_cnc_or_hybrid_laminate_candidate

ranking_tier:
rank_10_material_branch

simulator_default:
false

research_candidate:
true

support_layer_only:
false

hardware_validated:
false

claim_status:
material_branch_not_physical_validation

================================================================================
05 — CAPABILITY SCORING
================================================================================

Add a deterministic capability scoring helper.

Suggested fields:

AMCFMechanismProfileCapability:

- profile_id
- amcf_schedule_fit
- ab_staging_fit
- view_gate_stability_fit
- reader_prefetch_fit
- reverse_fit
- seek_fit
- fail_closed_fit
- tablet_form_factor_fit
- simulator_readiness
- hardware_uncertainty
- overall_score
- recommendation

Scores can be simple integers from 0 to 5.

The purpose is comparison only.

Do not imply physical measurement.

For default profile, scores should be high for simulator readiness and AMCF fit.

For energy recovery support layer, overall_score should not outrank the transport mechanisms because it is not a transport.

For soft actuators, hardware_uncertainty should be high and recommendation should say experimental only.

================================================================================
06 — RANKING REPORT
================================================================================

Create:

AMCFMechanismProfileRanking

Fields:

- profiles_ranked
- default_profile_id
- recommended_first_simulator_profile
- research_profiles
- support_layer_profiles
- experimental_profiles
- hardware_validated_profiles
- physical_level_5_claimed_profiles
- warnings

Rules:

- default_profile_id must be folded_ab_motor_encoder_baseline
- hardware_validated_profiles must be empty
- physical_level_5_claimed_profiles must be empty
- support layers must not become simulator default
- energy recovery must not be treated as a main transport mechanism
- piezo/inchworm must remain research candidate
- folded_ab_motor_encoder_baseline must be recommended first simulator profile

================================================================================
07 — CLAIM BOUNDARY
================================================================================

AMCFMechanismProfileClaimBoundary should include:

- software_control_profiles_only
- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- real_motor_validation_claimed
- real_piezo_validation_claimed
- real_carrier_validation_claimed
- real_reverse_seek_hardware_claimed
- manufacturing_readiness_claimed
- energy_self_powering_claimed

Defaults:

software_control_profiles_only = true
all claim booleans = false

Add helper:

default_mechanism_profile_claim_boundary()

Add validation helper:

validate_mechanism_claim_boundaries(profiles)

It should fail if any profile claims:

hardware_validated = true
physical_level_5_claimed = true

unless future explicit test data exists.
For now, no profile should claim those.

================================================================================
08 — REPORT HELPERS
================================================================================

Create:

src/amcf_physical_player_mechanism_profile_reports.py

Implement:

- mechanism_profile_to_dict(profile)
- mechanism_profiles_to_dict(profiles)
- build_mechanism_profile_ranking(profiles)
- build_mechanism_comparison_report(profiles)
- build_mechanism_claim_boundary_report(profiles)
- write_mechanism_profiles_json(profiles, path)
- write_mechanism_ranking_report(ranking, path)
- write_mechanism_comparison_markdown(profiles, path)
- write_mechanism_claim_boundary_report(profiles, path)

Reports must state:

- software/control profiles only
- hardware validation claimed: false
- physical Level 5 claimed: false
- default profile: folded_ab_motor_encoder_baseline
- piezo/inchworm: research candidate only
- energy recovery: support layer only
- soft actuators: experimental only
- no profile is a manufactured hardware proof

================================================================================
09 — DOCS
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md

Include:

- purpose
- why mechanism profiles can be built before hardware
- default profile
- research profiles
- support layers
- experimental branches
- material branch
- ranking criteria
- capability scoring
- claim boundaries
- what is not claimed

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Mark Stage 5:

AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1

as implementing:

- mechanism profile model
- default folded A/B motor/encoder profile
- piezo/inchworm research profile
- candidate layout profiles
- support-layer profiles
- mechanism comparison report
- claim-boundary validation
- tests

Do not mark hardware complete.

================================================================================
10 — DEMO
================================================================================

Create:

demo/run_physical_player_mechanism_profiles_demo.py

The demo should:

1. build all mechanism profiles
2. select default profile
3. rank profiles
4. build capability scores
5. build claim-boundary report
6. write output files

Output folder:

output/physical_player_mechanism_profiles_demo/

Output files:

- mechanism_profiles.json
- mechanism_capability_scores.json
- mechanism_ranking_report.json
- mechanism_claim_boundary_report.json
- MECHANISM_PROFILE_COMPARISON.md
- MECHANISM_PROFILE_SUMMARY.md

The demo must be deterministic.

Expected demo facts:

- default profile: folded_ab_motor_encoder_baseline
- hardware_validated_profiles: []
- physical_level_5_claimed_profiles: []
- energy recovery support layer only: true
- piezo/inchworm research candidate only: true

================================================================================
11 — TESTS
================================================================================

Create:

tests/test_physical_player_mechanism_profiles.py

Tests must verify:

1. all required profile IDs exist
2. exactly one profile is simulator_default true
3. default profile is folded_ab_motor_encoder_baseline
4. default profile uses folded_indexed_carrier
5. default profile uses abstract_ab_staging
6. default profile uses motor_encoder
7. default profile has hardware_validated false
8. default profile has physical_level_5_claimed false
9. piezo/inchworm profile is research_candidate true
10. piezo/inchworm profile is simulator_default false
11. two-track shuttle profile is a candidate, not default
12. cartridge stack shuttle profile is a candidate, not default
13. chain indexed carrier profile is research candidate, not default
14. magnetic guided clamp profile is support_layer_only true
15. energy recovery profile is support_layer_only true
16. energy recovery profile is not a transport default
17. soft actuator branch is experimental/research and not default
18. material branch is not actuator/default
19. hardware_validated_profiles is empty
20. physical_level_5_claimed_profiles is empty
21. claim boundary says hardware validation claimed false
22. claim boundary says energy self-powering claimed false
23. ranking recommends folded_ab_motor_encoder_baseline first
24. support layers do not outrank primary transport profile
25. full unittest suite passes

Use unittest and standard library unless the repo already uses pytest.

================================================================================
12 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile src/amcf_physical_player_mechanism_profiles.py
python -m py_compile src/amcf_physical_player_mechanism_profile_reports.py
python -m py_compile demo/run_physical_player_mechanism_profiles_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_mechanism_profiles_demo.py

Also run the existing relevant demos if practical:

python demo/run_physical_player_state_machine_demo.py
python demo/run_physical_player_fail_closed_demo.py
python demo/run_physical_player_reverse_seek_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in the previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
13 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add docs src demo tests
git commit -m "Add physical player mechanism profiles"

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_physical_player_mechanism_profiles.py

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- demo output folder
- test results
- git status
- git diff --stat

================================================================================
14 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- demo output folder
- validation commands run
- test results
- profile count
- default profile ID
- research profile count
- support layer count
- experimental profile count
- hardware_validated_profiles count
- physical_level_5_claimed_profiles count
- energy recovery support only yes/no
- piezo/inchworm research only yes/no
- mechanism profile report passed yes/no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical mechanisms are proven.
Do not claim real motor/encoder hardware is validated.
Do not claim piezo/inchworm hardware is validated.
Do not claim energy recovery powers the system.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 12 decides

```text id="part12_decision"
Part 12 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
```

This run should add:

```text id="part12_adds"
- mechanism profile module
- default folded A/B motor/encoder profile
- piezo/inchworm research profile
- two-track shuttle candidate
- cartridge stack shuttle candidate
- chain/indexed carrier candidate
- spring/governor/brake comparison profile
- magnetic/guided clamp support profile
- energy recovery support-only profile
- soft-actuator experimental branch
- material-aligned carrier branch
- capability scoring
- ranking report
- claim-boundary validation
- deterministic demo
- tests
```

It should build on:

```text id="part12_base"
802042b5395ac860c437188e0d79031d7dd5f591
```

It should not restart the simulator or claim physical mechanism validation.

---

## 5. What Part 13 should cover next

```text id="part13_next"
Part 13 should be:

Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
```

That next run should unify the existing pieces into a full deterministic demo:

```text id="part13_scope"
- mechanism profile selection
- cartridge insertion
- manifest recognition
- forward playback
- fail-closed scenarios
- reverse/seek behaviour
- unsafe acceptance audit
- mechanism profile report
- final software/control physical-player simulation package
```

Part 12 stops here because the mechanism-profile implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part13"
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
Base commit: 802042b5395ac860c437188e0d79031d7dd5f591
New commit: 01093024f9bbd11d10615a0f526b4440e5f8f41b
Pushed: yes
Tests: 166 passed
Profile count: 10
Default profile: folded_ab_motor_encoder_baseline
hardware_validated_profiles: 0
physical_level_5_claimed_profiles: 0
unsafe hardware claims: no
```

So Part 13 should now build directly on `0109302`.

# AMCF Physical Player Design and Structure Dossier  
## Part 13 — Codex-Ready Implementation Prompt for Physical Player Integrated Simulator Demo V1

## 1. Purpose of Part 13

Part 12 completed and pushed:

```text id="part12_done"
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
```

Commit:

```text id="part12_commit"
01093024f9bbd11d10615a0f526b4440e5f8f41b
```

That run added:

```text id="part12_added"
- mechanism profile module
- mechanism profile reports
- mechanism profile demo
- mechanism profile docs
- mechanism profile tests
- 10 deterministic mechanism profiles
- default folded A/B motor/encoder profile
- piezo/inchworm research profile
- support-layer profiles
- claim-boundary validation
- 166 passing tests
```

Part 13 now defines the next Codex run:

```text id="part13_run"
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
```

This run should unify the already-created pieces into one deterministic **software/control physical-player simulation package**.

It should combine:

```text id="part13_unifies"
- mechanism profile selection
- cartridge insertion
- manifest recognition
- forward playback
- fail-closed scenarios
- reverse/seek behaviour
- unsafe acceptance audit
- mechanism profile report
- final summary report
```

This run should not create a new simulator from scratch.

It should orchestrate the existing modules and demos into one integrated demonstration.

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part13"
This proves a physical player exists.
```

Correct framing:

```text id="correct_frame_part13"
This is the integrated software/control simulation package for the future AMCF physical player.

It shows that the software side can already coordinate mechanism profiles, cartridge/state-machine flow, fail-closed safety, reverse/seek limits, unsafe-acceptance auditing, and reporting before hardware is built.
```

The boundary is:

```text id="part13_boundary"
Software/control simulator integration: can be implemented now.
Manufactured physical hardware proof: later hardware/testing.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_simulator_demo_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

01093024f9bbd11d10615a0f526b4440e5f8f41b

That commit completed:

AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 166 tests
- mechanism profiles demo: PASS
- existing state-machine demo: PASS
- existing fail-closed demo: PASS
- existing reverse/seek demo: PASS
- profile count: 10
- default profile ID: folded_ab_motor_encoder_baseline
- hardware_validated_profiles count: 0
- physical_level_5_claimed_profiles count: 0
- energy recovery support only: yes
- piezo/inchworm research only: yes
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no

This run should integrate existing modules into one deterministic physical-player simulator demo package.

Do not restart the simulator.
Do not replace the state machine.
Do not create a parallel incompatible player model.
Do not weaken fail-closed, reverse, seek, mechanism-profile, or claim-boundary behaviour.
Do not claim hardware validation.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run implements an integrated software/control simulator demo for the future AMCF physical player.

Correct framing:

- The hardware is not present yet.
- The software can still orchestrate the physical-player control logic now.
- The integrated demo should show how future hardware must behave.
- The demo should combine mechanism profiles, cartridge recognition, safe forward playback, fail-closed behaviour, reverse/seek limits, unsafe-acceptance audit, and reports.
- This is a working software/control package for later hardware alignment, not physical validation.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek
- physical Level 5 completion
- hardware validation

Do claim:

- integrated software/control simulation
- deterministic physical-player simulator demo
- future hardware-support control contract
- mechanism profile selection
- safe state-machine orchestration
- fail-closed safety demonstration
- bounded reverse/seek demonstration
- unsafe-acceptance audit
- claim-boundary report

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

The physical player should not advance one page for every fixed video frame.
It should advance according to AMCF update events.

The integrated demo should show:

current section visible
→ next section prefetched
→ next section verified
→ next section staged
→ transition blanking
→ visible switch
→ old section parked
→ reverse/seek limited to safe local buffers
→ fail-closed blocks unsafe states
→ unsafe_acceptance_count remains zero.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md

docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
other existing tests

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP.
Do not push.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the integrated demo is a manufactured player.
Do not claim real optical no-gap switching is proven.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_AUDIT.md

Include:

- current git HEAD
- whether 0109302 or later is present
- existing state-machine files found
- existing fail-closed files found
- existing reverse/seek files found
- existing mechanism-profile files found
- existing demos found
- existing tests found
- what this integrated demo will add
- files to edit
- files to create
- confirmation that this is software/control simulator integration
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — INTEGRATED DEMO SCRIPT
================================================================================

Create:

demo/run_physical_player_simulator_demo.py

This should be the top-level integrated demo.

It should import and use existing modules where possible:

- amcf_physical_player_state_machine
- amcf_physical_player_state_machine_reports
- amcf_physical_player_mechanism_profiles
- amcf_physical_player_mechanism_profile_reports

Do not duplicate all logic from the existing demos.
Call existing helpers where practical.

The demo should run these phases:

1. Mechanism profile phase
2. Nominal forward playback phase
3. Fail-closed safety phase
4. Reverse/seek phase
5. Unsafe-acceptance audit phase
6. Unified report phase

================================================================================
02 — PHASE 1: MECHANISM PROFILE SELECTION
================================================================================

The integrated demo should:

- build all mechanism profiles
- select default_mechanism_profile()
- assert default profile ID is folded_ab_motor_encoder_baseline
- build mechanism ranking report
- build mechanism claim-boundary report
- confirm hardware_validated_profiles is empty
- confirm physical_level_5_claimed_profiles is empty

Record phase status:

mechanism_profile_phase:
passed true/false
default_profile_id
profile_count
hardware_validated_profiles_count
physical_level_5_claimed_profiles_count

================================================================================
03 — PHASE 2: NOMINAL FORWARD PLAYBACK
================================================================================

The integrated demo should:

- create or reuse sample cartridge/state machine
- insert cartridge
- recognize manifest
- prefetch current
- verify current
- load view gate
- lock view gate
- enter playback ready
- run at least two safe forward transitions
- park old sections into reverse buffer
- produce a forward playback timeline

Expected nominal result:

- final state should be park_old_section or playback_ready depending on existing API
- unsafe_acceptance_count should remain 0
- at least one verified visible transition should occur
- no physical hardware should be required

Record phase status:

forward_playback_phase:
passed true/false
forward_transition_count
final_playback_state
unsafe_acceptance_count

================================================================================
04 — PHASE 3: FAIL-CLOSED SAFETY
================================================================================

The integrated demo should reuse the fail-closed safety logic already implemented.

Run deterministic safety scenarios, including at least:

- valid section path
- degraded colour warning path
- hash mismatch failure
- missing marker failure
- wrong section failure
- invalid registration failure
- prefetch timeout
- hidden gate not ready
- view gate unlocked
- shutter/illumination failure placeholder
- jam/double-feed/misfeed placeholders
- audio sync limit

It is acceptable to call helpers from the fail-closed demo if they exist.

Record:

fail_closed_phase:
passed true/false
scenario_count
fail_closed_event_count
unsafe_acceptance_count

================================================================================
05 — PHASE 4: REVERSE / SEEK
================================================================================

The integrated demo should reuse reverse/seek logic already implemented.

Run deterministic reverse/seek scenarios:

- populate reverse buffer through safe forward transitions
- perform one successful step_reverse()
- attempt reverse beyond buffer and deny safely
- perform one successful local-buffer seek if available
- attempt arbitrary seek outside local buffer and deny safely
- attempt invalid seek target and deny/fail closed safely

Record:

reverse_seek_phase:
passed true/false
reverse_attempts
reverse_successes
reverse_denials
seek_attempts
seek_successes
seek_denials
arbitrary_seek_denied_count
unsafe_acceptance_count

================================================================================
06 — PHASE 5: UNSAFE ACCEPTANCE AUDIT
================================================================================

Run or reuse unsafe acceptance audit helpers.

The integrated demo should check:

- no invalid section was displayed
- no hash-mismatch section was displayed
- no wrong section was displayed
- no unverified next section switched visible
- no denied seek/reverse produced visible unsafe state
- unsafe_acceptance_count remains 0

Record:

unsafe_acceptance_audit:
passed true/false
unsafe_acceptance_count
unsafe_events_count
checked_event_count
checked_section_count

================================================================================
07 — PHASE 6: UNIFIED REPORT
================================================================================

Create a unified report object/dict.

Required top-level fields:

- run_name
- base_commit_hint
- software_control_simulator_only
- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- real_sensors_required
- real_motors_required
- real_cartridges_required
- real_scans_required
- manufactured_player_claimed
- default_mechanism_profile_id
- mechanism_profile_phase
- forward_playback_phase
- fail_closed_phase
- reverse_seek_phase
- unsafe_acceptance_audit
- final_passed
- recommended_next_stage

Required claim values:

software_control_simulator_only = true
physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
real_sensors_required = false
real_motors_required = false
real_cartridges_required = false
real_scans_required = false
manufactured_player_claimed = false

final_passed should be true only if:

- mechanism profile phase passed
- forward playback phase passed
- fail-closed phase passed
- reverse/seek phase passed
- unsafe acceptance audit passed
- unsafe_acceptance_count == 0
- hardware claim values remain false

================================================================================
08 — OUTPUT FOLDER
================================================================================

Output folder:

output/physical_player_simulator_demo/

Output files:

- integrated_simulation_summary.json
- mechanism_profile_report.json
- forward_playback_timeline.json
- fail_closed_safety_report.json
- reverse_seek_report.json
- unsafe_acceptance_audit.json
- claim_boundary_report.json
- PHYSICAL_PLAYER_SIMULATOR_DEMO_SUMMARY.md
- NEXT_STEPS.md

Generated output should not be committed unless the repo already commits output files.
Prefer not to commit generated output.

================================================================================
09 — REPORT HELPERS
================================================================================

Create if useful:

src/amcf_physical_player_integrated_demo_reports.py

Only create this if it avoids making the demo script too large.

Possible helpers:

- build_integrated_simulation_summary(...)
- write_integrated_simulation_summary(...)
- build_integrated_summary_markdown(...)
- build_next_steps_markdown(...)

Keep simple.
Use standard library only.

The markdown summary must state:

- software/control simulator only
- hardware validation claimed: false
- physical Level 5 claimed: false
- default mechanism profile: folded_ab_motor_encoder_baseline
- forward playback exercised
- fail-closed exercised
- reverse/seek exercised
- unsafe_acceptance_count: 0
- generated outputs are demo artifacts, not hardware proof

================================================================================
10 — DOCS
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md

Include:

- purpose
- why an integrated simulator demo can be built before hardware
- modules integrated
- phase list
- mechanism profile phase
- forward playback phase
- fail-closed phase
- reverse/seek phase
- unsafe-acceptance audit
- claim boundary
- output files
- what is not claimed

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Mark Stage 6:

AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1

as implementing:

- integrated deterministic simulator demo
- mechanism profile selection
- forward playback orchestration
- fail-closed scenario orchestration
- reverse/seek orchestration
- unsafe acceptance audit
- unified report package
- tests

Do not mark hardware complete.

================================================================================
11 — TESTS
================================================================================

Create:

tests/test_physical_player_simulator_demo.py

Tests should verify:

1. integrated demo can build mechanism profile phase
2. default mechanism profile is folded_ab_motor_encoder_baseline
3. hardware_validated_profiles count is 0
4. physical_level_5_claimed_profiles count is 0
5. integrated demo can run forward playback phase
6. forward playback phase records at least one transition
7. integrated demo can run fail-closed phase
8. fail-closed phase records at least one fail-closed event
9. integrated demo can run reverse/seek phase
10. reverse/seek phase records at least one reverse success or safe denial
11. arbitrary seek denial is recorded
12. unsafe acceptance audit passes
13. unsafe_acceptance_count is 0
14. unified report has software_control_simulator_only true
15. unified report has hardware_validation_claimed false
16. unified report has physical_level_5_claimed false
17. unified report has manufactured_player_claimed false
18. final_passed true for deterministic nominal integrated run
19. summary markdown states no hardware validation claimed
20. full unittest suite passes

Use unittest and standard library unless the repo already uses pytest.

================================================================================
12 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile src/amcf_physical_player_integrated_demo_reports.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m py_compile demo/run_physical_player_state_machine_demo.py
python -m py_compile demo/run_physical_player_fail_closed_demo.py
python -m py_compile demo/run_physical_player_reverse_seek_demo.py
python -m py_compile demo/run_physical_player_mechanism_profiles_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py

If src/amcf_physical_player_integrated_demo_reports.py is not created, skip that py_compile command and report why.

Also run existing demos if practical:

python demo/run_physical_player_state_machine_demo.py
python demo/run_physical_player_fail_closed_demo.py
python demo/run_physical_player_reverse_seek_demo.py
python demo/run_physical_player_mechanism_profiles_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in the previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
13 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add docs src demo tests
git commit -m "Add integrated physical player simulator demo"

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_physical_player_simulator_demo.py

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- demo output folder
- test results
- git status
- git diff --stat

================================================================================
14 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- demo output folder
- validation commands run
- test results
- default mechanism profile ID
- profile count
- forward transition count
- fail-closed scenario count
- fail-closed event count
- reverse attempts
- reverse successes
- reverse denials
- seek attempts
- seek successes
- seek denials
- arbitrary seek denied count
- unsafe_acceptance_count
- integrated report passed yes/no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 13 decides

```text id="part13_decision"
Part 13 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
```

This run should add:

```text id="part13_adds"
- integrated simulator demo script
- integrated report helpers if useful
- integrated simulator docs
- integrated simulator audit
- integrated simulator tests
- unified output package
- mechanism profile phase
- forward playback phase
- fail-closed phase
- reverse/seek phase
- unsafe acceptance audit phase
- final claim-boundary report
```

It should build on:

```text id="part13_base"
01093024f9bbd11d10615a0f526b4440e5f8f41b
```

It should not restart the simulator or claim physical hardware validation.

---

## 5. What Part 14 should cover next

```text id="part14_next"
Part 14 should be:

Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
```

That next run should update public-facing docs/site navigation so the repo clearly exposes:

```text id="part14_scope"
- Physical Player Concept
- State Machine
- Fail-Closed Safety
- Reverse/Seek
- Mechanism Profiles
- Integrated Simulator Demo
- Claim Boundaries
- Development Sequence
```

Part 13 stops here because the integrated simulator demo implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part14"
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
Base commit: 01093024f9bbd11d10615a0f526b4440e5f8f41b
New commit: fea00409262dea39d5c9068daac0a206c02d07f5
Pushed: yes
Tests: 185 passed
Integrated demo: passed
Default profile: folded_ab_motor_encoder_baseline
Forward transitions: 2
Fail-closed scenarios: 15
Fail-closed events: 8
Reverse/seek: passed
unsafe_acceptance_count: 0
physical hardware claimed: no
hardware validation claimed: no
physical Level 5 claimed: no
```

So Part 14 should now build directly on `fea0040`.

# AMCF Physical Player Design and Structure Dossier  
## Part 14 — Codex-Ready Implementation Prompt for Physical Player Public Docs Sync V1

## 1. Purpose of Part 14

Part 13 completed and pushed:

```text id="part13_done"
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
```

Commit:

```text id="part13_commit"
fea00409262dea39d5c9068daac0a206c02d07f5
```

That run created the integrated physical-player software/control simulator demo:

```text id="part13_added"
- mechanism profile phase
- forward playback phase
- fail-closed phase
- reverse/seek phase
- unsafe-acceptance audit
- unified report
- integrated simulator docs
- 185 passing tests
```

Part 14 now defines the next Codex run:

```text id="part14_run"
AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
```

The purpose is to synchronize the public-facing docs and site/navigation so the repo clearly exposes the full physical-player software/control development sequence.

This run should not add new simulator logic.

It should make the existing work easier to discover.

It should connect these docs cleanly:

```text id="part14_docs"
- Physical Player Concept
- State Machine
- Fail-Closed Safety
- Reverse/Seek
- Mechanism Profiles
- Integrated Simulator Demo
- Claim Boundaries
- Hardware/Software Paths
- Development Sequence
```

This is a public documentation/navigation pass, not a code-feature run.

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part14"
The project now has a working physical player.
```

Correct framing:

```text id="correct_frame_part14"
The project now has a working software/control simulator package for a future physical AMCF player.

The public docs should clearly explain that the repo contains:
- software-control foundations
- deterministic simulator demos
- mechanism profiles
- fail-closed safety logic
- reverse/seek limits
- integrated reports
- claim boundaries

It should not claim manufactured hardware, physical validation, real motors, real sensors, real cartridges, or physical Level 5 completion.
```

The boundary is:

```text id="part14_boundary"
Public documentation sync: yes.
Hardware validation claim: no.
Manufactured physical player claim: no.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_public_docs_sync_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

fea00409262dea39d5c9068daac0a206c02d07f5

That commit completed:

AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 185 tests
- integrated simulator demo: PASS
- state-machine demo: PASS
- fail-closed demo: PASS
- reverse/seek demo: PASS
- mechanism profiles demo: PASS
- default mechanism profile: folded_ab_motor_encoder_baseline
- profile count: 10
- forward transitions: 2
- fail-closed scenarios: 15
- fail-closed events: 8
- reverse attempts/successes/denials: 2 / 1 / 1
- seek attempts/successes/denials: 2 / 1 / 1
- arbitrary seek denied count: 1
- unsafe_acceptance_count: 0
- integrated report passed: yes
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no

This run should update public-facing docs and navigation only.

Do not restart the simulator.
Do not replace the state machine.
Do not add new physical-player logic unless needed for documentation links.
Do not weaken fail-closed, reverse/seek, mechanism-profile, integrated-demo, or claim-boundary behaviour.
Do not claim hardware validation.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run synchronizes the public documentation around the physical-player software/control simulator sequence.

Correct framing:

- The hardware is not present yet.
- The software/control foundations are implemented and tested.
- The repo now has deterministic demos and reports for a future physical-player control architecture.
- The public docs should expose the sequence clearly.
- The docs should help readers understand what is software/control, what is simulated, what is future hardware, and what is not claimed.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim:

- software/control simulator sequence
- deterministic physical-player demos
- future hardware-support control contract
- mechanism profile selection
- safe state-machine orchestration
- fail-closed safety demonstration
- bounded reverse/seek demonstration
- unsafe-acceptance audit
- integrated simulator package
- claim-boundary preservation

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

Important public wording:

The physical-player branch is a software/control foundation for future hardware alignment. It can define and test the behaviour that later hardware must obey, but it does not prove manufactured hardware exists.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md
PUBLICATION_STATUS.md if present
docs/README.md if present
docs/INDEX.md if present
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_PHYSICAL_PLAYER_CLAIM_BOUNDARIES.md if present
docs/AMCF_PHYSICAL_IO_ARCHITECTURE.md if present

site/index.html if present
site/ any docs/navigation files if present

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_integrated_demo_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
other existing tests

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP.
Do not push.
Do not modify unrelated code.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the integrated demo is a manufactured player.
Do not claim real optical no-gap switching is proven.
Do not claim real reverse hardware is proven.
Do not claim arbitrary physical seek is proven.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_AUDIT.md

Include:

- current git HEAD
- whether fea0040 or later is present
- physical-player docs found
- physical-player demos found
- physical-player tests found
- existing site/docs navigation files found
- public docs gaps found
- files to edit
- files to create
- confirmation that this is a public documentation/navigation sync
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — PUBLIC DOCS MAP
================================================================================

Create or update:

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md

This file should act as the public-facing map for the physical-player branch.

Include sections:

1. Overview
2. Reading order
3. Physical-player docs
4. Demo scripts
5. Test files
6. Output/report folders
7. Claim boundaries
8. What is implemented now
9. What remains future hardware
10. Recommended next development step

Reading order should be:

1. docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
2. docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
3. docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
4. docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
5. docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
6. docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
7. docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
8. CLAIM_BOUNDARIES.md
9. docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

Demo scripts should include:

- demo/run_physical_player_state_machine_demo.py
- demo/run_physical_player_fail_closed_demo.py
- demo/run_physical_player_reverse_seek_demo.py
- demo/run_physical_player_mechanism_profiles_demo.py
- demo/run_physical_player_simulator_demo.py

Test files should include:

- tests/test_physical_player_state_machine.py
- tests/test_physical_player_fail_closed.py
- tests/test_physical_player_reverse_seek.py
- tests/test_physical_player_mechanism_profiles.py
- tests/test_physical_player_simulator_demo.py

Output folders should include:

- output/physical_player_state_machine_demo/
- output/physical_player_fail_closed_demo/
- output/physical_player_reverse_seek_demo/
- output/physical_player_mechanism_profiles_demo/
- output/physical_player_simulator_demo/

Mention generated output is demo output and normally not committed.

================================================================================
02 — README UPDATE
================================================================================

Update README.md.

Add or refine a section titled something like:

AMCF Physical Player Software-Control Simulator

The section should briefly explain:

- AMCF is software-first.
- The physical-player branch is the software/control foundation for future mechanical/optical hardware.
- It models folded indexed carrier, A/B staging, view gate, hidden staging, reader-prefetch, transition blanking, fail-closed safety, reverse/seek limits, and mechanism profiles.
- The integrated demo combines mechanism profiles, forward playback, fail-closed scenarios, reverse/seek, and unsafe-acceptance audit.
- It does not claim manufactured physical hardware.
- It does not claim physical Level 5 validation.
- It does not require real sensors, motors, cartridges, or scans.

Add links to:

- docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
- docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
- docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
- docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
- docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
- docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
- docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
- docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
- CLAIM_BOUNDARIES.md

Keep README wording concise.
Do not turn README into the full dossier.

================================================================================
03 — CLAIM BOUNDARY DOC SYNC
================================================================================

Update CLAIM_BOUNDARIES.md only if needed.

Add or refine a section for:

Physical Player Software-Control Simulator

It should say:

Claimed:

- software/control simulator modules
- deterministic demo scripts
- mechanism profile model
- state-machine control flow
- fail-closed safety model
- bounded reverse/seek model
- unsafe-acceptance audit
- integrated demo/report generation

Not claimed:

- manufactured physical player
- real physical/optical playback
- real motor validation
- real sensor validation
- real cartridge validation
- real scan validation
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do not weaken any existing claim boundary.

================================================================================
04 — HARDWARE / SOFTWARE PATHS DOC SYNC
================================================================================

Update:

docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

only if it exists.

Add or refine the physical-player path to mention the new completed software/control stages:

- state machine
- fail-closed safety
- reverse/seek controls
- mechanism profiles
- integrated simulator demo

Clarify:

- these are software/control stages
- future hardware should align to these control contracts
- hardware proof remains future work

Do not claim hardware exists.

================================================================================
05 — DEVELOPMENT SEQUENCE DOC SYNC
================================================================================

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Ensure stages are listed cleanly:

Stage 1:
AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1
or state that model structures were integrated into state-machine work if no separate model-foundation commit exists.

Stage 2:
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1

Stage 3:
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1

Stage 4:
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1

Stage 5:
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1

Stage 6:
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1

Stage 7:
AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1

For each completed stage, include:

- commit if known
- purpose
- validation summary if known
- claim boundary

Known commits:

Stage 2:
f8b6e91e1dfd9b57345ee38ac262635d446f47c8

Stage 3:
4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e

Stage 4:
802042b5395ac860c437188e0d79031d7dd5f591

Stage 5:
01093024f9bbd11d10615a0f526b4440e5f8f41b

Stage 6:
fea00409262dea39d5c9068daac0a206c02d07f5

Stage 7:
current run, not committed yet

Do not invent Stage 1 commit if it was not separate.
Explain if Stage 1 was effectively folded into Stage 2 due absent prior model module.

================================================================================
06 — SITE / PAGES NAVIGATION SYNC
================================================================================

If site/index.html exists, update it.

Add a public-facing section or link group:

Physical Player Software-Control Simulator

Include links to:

- Physical Player Concept
- State Machine
- Fail-Closed Safety
- Reverse/Seek
- Mechanism Profiles
- Integrated Simulator Demo
- Development Sequence
- Claim Boundaries

Keep it concise.

Do not make the site claim hardware.

Suggested wording:

The physical-player branch documents and simulates the software/control architecture for a future mechanical/optical AMCF player. It includes deterministic state-machine, fail-closed, reverse/seek, mechanism-profile, and integrated-demo layers. It does not claim manufactured hardware or physical validation.

If there is no site/index.html, skip this step and report that no site file was found.

================================================================================
07 — DOC LINK CHECK
================================================================================

Add a lightweight link/check helper if practical, or use existing tests.

Preferred simple approach:

Create:

tests/test_physical_player_public_docs_sync.py

Tests should verify:

1. README.md links to docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
2. README.md links to docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
3. README.md contains no manufactured hardware claim for physical player
4. CLAIM_BOUNDARIES.md contains physical-player software/control simulator boundary
5. docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md exists
6. docs map links to all physical-player docs
7. docs map links to all five demo scripts
8. development sequence mentions Stage 2 through Stage 7
9. development sequence mentions known commits for Stages 2 through 6
10. docs or README mention unsafe_acceptance_count remains 0
11. docs or README mention hardware validation claimed no / not claimed
12. if site/index.html exists, it links to at least docs map or simulator demo doc

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
08 — PUBLIC SUMMARY DOC
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md

This should be short and public-facing.

Include:

- What this branch is
- What is implemented in software/control
- What the integrated demo covers
- What the mechanism profiles represent
- What fail-closed means
- Why reverse/seek is bounded
- What unsafe_acceptance_count means
- What is not claimed
- Next development step

This doc should be easier to read than the detailed technical docs.

Do not include too much dossier text.
Do not claim hardware exists.

================================================================================
09 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile demo/run_physical_player_simulator_demo.py
python -m py_compile src/amcf_physical_player_integrated_demo_reports.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py

Also run existing docs/site/package tests if they exist under unittest discover.

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
10 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md CLAIM_BOUNDARIES.md docs site tests

If site does not exist or is unchanged, omit it from git add.

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_physical_player_public_docs_sync.py

Commit message:

git commit -m "Sync physical player public docs"

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- test results
- git status
- git diff --stat

================================================================================
11 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- site updated yes/no
- docs map created yes/no
- public summary created yes/no
- README updated yes/no
- claim boundaries updated yes/no
- development sequence updated yes/no
- validation commands run
- test results
- integrated simulator demo still passes yes/no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 14 decides

```text id="part14_decision"
Part 14 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
```

This run should add or update:

```text id="part14_adds"
- public docs map
- public summary
- README physical-player simulator section
- claim-boundary sync if needed
- hardware/software paths sync if needed
- development sequence sync
- site navigation if site/index.html exists
- public docs sync audit
- docs/link tests
```

It should build on:

```text id="part14_base"
fea00409262dea39d5c9068daac0a206c02d07f5
```

It should not restart the simulator or claim physical hardware validation.

---

## 5. What Part 15 should cover next

```text id="part15_next"
Part 15 should be:

Codex-Ready Implementation Prompt for AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
```

That next run should perform a release-style review:

```text id="part15_scope"
- run full tests
- run all physical-player demos
- verify docs links
- verify claim boundaries
- verify no generated output committed
- verify no local paths leaked into public docs
- verify README/site navigation
- verify package size tests
- produce release review report
```

Part 14 stops here because the public docs sync implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part15"
AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
Base commit: fea00409262dea39d5c9068daac0a206c02d07f5
New commit: c7c2658877f04d40b94b127c6e44fe30d3597a18
Pushed: yes
Tests: 197 passed
Integrated simulator demo: passed
Site updated: yes
Docs map created: yes
Public summary created: yes
README updated: yes
Claim boundaries updated: yes
unsafe_acceptance_count: 0
physical hardware claimed: no
hardware validation claimed: no
physical Level 5 claimed: no
```

So Part 15 should now build directly on `c7c2658`.

# AMCF Physical Player Design and Structure Dossier  
## Part 15 — Codex-Ready Implementation Prompt for Physical Player Release Review V1

## 1. Purpose of Part 15

Part 14 completed and pushed:

```text id="part14_done"
AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
```

Commit:

```text id="part14_commit"
c7c2658877f04d40b94b127c6e44fe30d3597a18
```

That run synchronized the public docs, README, claim boundaries, development sequence, and Pages site navigation.

Part 15 now defines the next Codex run:

```text id="part15_run"
AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
```

The purpose is to perform a release-style review of the physical-player software/control branch.

This is not a feature run.

It should verify:

```text id="part15_scope"
- full tests pass
- all physical-player demos pass
- docs links are present
- public site links are present
- claim boundaries are preserved
- no generated output is committed
- no unsafe hardware claim appears
- no local Windows paths leaked into public docs
- no real hardware validation is claimed
- package/release checks still pass
- release review report is generated
```

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part15"
This releases a finished physical hardware player.
```

Correct framing:

```text id="correct_frame_part15"
This is a release review for the physical-player software/control simulator and documentation sequence.

It verifies the repo’s public-facing software-control branch is coherent, tested, documented, and claim-bounded before further releases or packaging.
```

The boundary is:

```text id="part15_boundary"
Release review of software/control simulator branch: yes.
Manufactured physical hardware validation: no.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_physical_player_release_review_v1"
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

c7c2658877f04d40b94b127c6e44fe30d3597a18

That commit completed:

AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 197 tests
- integrated simulator demo: PASS
- default profile: folded_ab_motor_encoder_baseline
- profile count: 10
- forward transitions: 2
- fail-closed scenarios/events: 15 / 8
- reverse attempts/successes/denials: 2 / 1 / 1
- seek attempts/successes/denials: 2 / 1 / 1
- arbitrary seek denied count: 1
- unsafe_acceptance_count: 0
- site updated: yes
- docs map created: yes
- public summary created: yes
- README updated: yes
- claim boundaries updated: yes
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no

This run should review and report.

Do not add new simulator features.
Do not restart the simulator.
Do not replace the state machine.
Do not alter mechanism profiles unless a release-review issue requires a small documentation/test fix.
Do not weaken claim boundaries.
Do not claim hardware validation.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run performs a release review of the physical-player software/control simulator branch.

Correct framing:

- The hardware is not present yet.
- The repo has software-control simulator layers for future hardware alignment.
- The release review verifies that tests, demos, docs, site links, package checks, and claim boundaries are consistent.
- Any report generated by this run is a software/control release-review artifact, not hardware proof.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim if verified:

- tests pass
- demos pass
- docs links exist
- public docs map exists
- site navigation exists
- claim boundaries preserved
- unsafe_acceptance_count remains 0
- generated output is not committed
- physical-player release review passed

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

Public framing to preserve:

The physical-player branch is a software/control foundation for future hardware alignment. It can define and test the behaviour that later hardware must obey, but it does not prove manufactured hardware exists.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md
PUBLICATION_STATUS.md if present

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_AUDIT.md

site/index.html if present

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py
src/amcf_physical_player_integrated_demo_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
tests/test_physical_player_public_docs_sync.py
tests/test_release_package.py if present
other existing tests

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not create a large ZIP unless the repo already has a release-package test that creates one.
Do not push.
Do not modify simulator code unless a test failure requires a minimal fix.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the integrated demo is a manufactured player.
Do not claim real optical no-gap switching is proven.
Do not claim real reverse hardware is proven.
Do not claim arbitrary physical seek is proven.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_AUDIT.md

Include:

- current git HEAD
- whether c7c2658 or later is present
- repo status before review
- physical-player docs found
- physical-player demos found
- physical-player tests found
- site navigation found yes/no
- claim-boundary files found
- package/release tests found
- generated-output folders found
- files to edit
- files to create
- confirmation that this is release review only
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — RELEASE REVIEW SCRIPT
================================================================================

Create:

demo/run_physical_player_release_review.py

This script should run lightweight repo-local checks and write a deterministic release review report.

Use standard library only.

Do not shell out to run the full test suite inside this script unless simple and safe.
The main validation commands will run separately.

The script should inspect files and run/import existing helpers where practical.

It should check:

1. Required docs exist.
2. Required demos exist.
3. Required tests exist.
4. README links to docs map.
5. README links to simulator demo docs.
6. CLAIM_BOUNDARIES.md contains physical-player software/control boundary.
7. Docs map links to all physical-player docs.
8. Docs map links to all five demo scripts.
9. site/index.html links to physical-player docs if site exists.
10. Development sequence mentions Stages 2–7.
11. Known commits for Stages 2–6 are present in development sequence.
12. Integrated demo summary can be generated or existing demo helpers can build a summary.
13. unsafe_acceptance_count remains 0 in integrated demo helper/report if available.
14. No generated output appears staged/tracked under output/ if checkable through git or filesystem.
15. Public docs do not contain obvious local Windows workspace paths.
16. Public docs do not contain prohibited overclaim phrases.

Required output folder:

output/physical_player_release_review/

Required output files:

- release_review_report.json
- RELEASE_REVIEW_SUMMARY.md
- claim_boundary_scan.json
- docs_link_scan.json
- generated_output_scan.json
- local_path_scan.json
- next_steps.md

Generated output should not be committed.

================================================================================
02 — CLAIM BOUNDARY SCAN
================================================================================

Implement a scan over public docs and site files.

Files to scan:

- README.md
- CLAIM_BOUNDARIES.md
- docs/*.md
- site/index.html if present

Flag dangerous phrases if they appear in an unsafe context:

- manufactured physical player exists
- real physical player exists
- physical Level 5 complete
- hardware validated
- real motor validated
- real sensor validated
- real cartridge validated
- real optical playback proven
- no-gap physically proven
- arbitrary physical seek proven
- reverse hardware proven
- energy recovery powers the system

Important:

The docs may contain negative boundary wording like:

- hardware validation claimed: no
- not hardware validated
- does not claim manufactured hardware
- physical Level 5 is not claimed

Do not treat clear negative-boundary wording as a failure.

The scan can be simple:
- collect matches
- mark whether each line appears to be a negative boundary
- final pass only if no unsafe affirmative overclaims are found.

================================================================================
03 — LOCAL PATH SCAN
================================================================================

Scan public-facing docs and site files for local Windows paths.

Flag patterns like:

- <local-drive>\
- <local-user-home>\
- AppData\
- Tests\Test AMCF_PUBLIC
- AMCF_GITHUB_CLEAN_PACKAGE
- codex-runtimes

Allow these only in generated output folders that are not committed.
Public docs should not include local machine paths.

If any public doc contains local paths, fix the doc.

================================================================================
04 — GENERATED OUTPUT SCAN
================================================================================

Check whether generated output folders are tracked or staged.

Folders:

- output/physical_player_state_machine_demo/
- output/physical_player_fail_closed_demo/
- output/physical_player_reverse_seek_demo/
- output/physical_player_mechanism_profiles_demo/
- output/physical_player_simulator_demo/
- output/physical_player_release_review/

Expected:

- generated outputs may exist locally
- generated outputs should not be committed unless the repo policy says otherwise
- release review should report generated output committed: no

================================================================================
05 — DOC LINK CHECK
================================================================================

Create or update:

tests/test_physical_player_release_review.py

Tests should verify:

1. docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md exists
2. docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md exists
3. docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md exists
4. README.md links to docs map
5. README.md links to simulator demo doc
6. CLAIM_BOUNDARIES.md contains physical-player software/control simulator boundary
7. development sequence mentions Stage 2 through Stage 7
8. development sequence contains known commits for Stages 2 through 6
9. site/index.html exists and links to physical-player docs if site exists
10. public docs contain no local Windows workspace paths
11. public docs do not contain unsafe affirmative hardware validation claims
12. release review script can build a report dict
13. release review report says physical_hardware_claimed false
14. release review report says hardware_validation_claimed false
15. release review report says physical_level_5_claimed false
16. release review report says unsafe_acceptance_count 0
17. release review report final_passed true
18. full unittest suite passes

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
06 — RELEASE REVIEW DOC
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md

Include:

- purpose
- baseline commit
- what the review checks
- tests and demos included
- docs and site checks
- claim-boundary checks
- generated-output checks
- local-path checks
- what is not claimed
- how to run the release review script
- expected output folder
- next step

Do not claim hardware exists.

================================================================================
07 — DEVELOPMENT SEQUENCE UPDATE
================================================================================

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add Stage 8:

AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1

Purpose:

- release-style review of physical-player software/control branch
- verify tests, demos, docs, site navigation, claim boundaries, generated-output policy, local-path scan, and release review report

Status:

current run, not committed yet

Claim boundary:

- software/control release review only
- no physical hardware validation
- no physical Level 5 claim

================================================================================
08 — README OR DOCS MAP UPDATE
================================================================================

Update README.md or docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md only if needed.

Add a link to:

docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md

Add demo script link:

demo/run_physical_player_release_review.py

Keep concise.

================================================================================
09 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile demo/run_physical_player_release_review.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m py_compile src/amcf_physical_player_integrated_demo_reports.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py
python demo/run_physical_player_release_review.py

Also run all physical-player demos if practical:

python demo/run_physical_player_state_machine_demo.py
python demo/run_physical_player_fail_closed_demo.py
python demo/run_physical_player_reverse_seek_demo.py
python demo/run_physical_player_mechanism_profiles_demo.py
python demo/run_physical_player_simulator_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
10 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md docs demo tests

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_physical_player_release_review.py

Commit message:

git commit -m "Add physical player release review"

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- test results
- demo results
- release review output folder
- git status
- git diff --stat

================================================================================
11 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- release review script created yes/no
- release review doc created yes/no
- docs map updated yes/no
- development sequence updated yes/no
- validation commands run
- test results
- all physical-player demos pass yes/no
- release review final_passed yes/no
- unsafe_acceptance_count
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 15 decides

```text id="part15_decision"
Part 15 decides that the next Codex run should be:

AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
```

This run should add:

```text id="part15_adds"
- release review audit
- release review script
- release review docs
- release review tests
- claim-boundary scan
- docs-link scan
- local-path scan
- generated-output scan
- development-sequence Stage 8
- docs map / README link if needed
```

It should build on:

```text id="part15_base"
c7c2658877f04d40b94b127c6e44fe30d3597a18
```

It should not add new simulator logic or claim hardware validation.

---

## 5. What Part 16 should cover next

```text id="part16_next"
Part 16 should be:

Codex-Ready Implementation Prompt for AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
```

That next run should prepare a refreshed public package/release bundle after the physical-player docs/simulator sequence:

```text id="part16_scope"
- confirm repo clean
- run tests/demos
- refresh package manifest if needed
- ensure generated output excluded
- ensure docs/site included
- ensure claim boundaries included
- produce package review report
- no push unless explicitly instructed
```

Part 15 stops here because the release-review implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part16"
AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
Base commit: c7c2658877f04d40b94b127c6e44fe30d3597a18
New commit: 659bd3e74a9e4dd254600558aec6e76309ba596f
Pushed: yes
Tests: 214 passed
Integrated simulator demo: passed
Release review script: passed
All physical-player demos: passed
unsafe_acceptance_count: 0
generated output committed: no
local path leak found: no
unsafe hardware claim found: no
physical hardware claimed: no
hardware validation claimed: no
physical Level 5 claimed: no
```

So Part 16 should now build directly on `659bd3e`.

# AMCF Physical Player Design and Structure Dossier  
## Part 16 — Codex-Ready Implementation Prompt for Public Release Package Refresh V1

## 1. Purpose of Part 16

Part 15 completed and pushed:

```text id="part15_done"
AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
```

Commit:

```text id="part15_commit"
659bd3e74a9e4dd254600558aec6e76309ba596f
```

That run added the release-review layer:

```text id="part15_added"
- release review script
- release review docs
- release review audit
- release review tests
- docs link scan
- claim-boundary scan
- generated-output scan
- local-path scan
- Stage 8 development-sequence entry
- 214 passing tests
```

Part 16 now defines the next Codex run:

```text id="part16_run"
AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
```

The purpose is to refresh the public package/release bundle after the physical-player software/control sequence.

This is not a simulator feature run.

It should verify and refresh public package metadata, package manifest/review docs, and release-readiness checks.

It should ensure the public repo/package includes the new physical-player docs, site navigation, tests, scripts, and claim boundaries, while excluding generated demo outputs and local machine paths.

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part16"
This packages a completed physical hardware player.
```

Correct framing:

```text id="correct_frame_part16"
This refreshes the public software package after the physical-player software/control simulator sequence.

It verifies that the repo/package contains the correct source, demos, tests, docs, claim boundaries, and site files, while excluding generated output and local environment paths.
```

The boundary is:

```text id="part16_boundary"
Public release package refresh: yes.
Physical hardware validation: no.
Manufactured physical player claim: no.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_public_release_package_refresh_v1"
You are working on my AMCF project.

Run name:
AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

659bd3e74a9e4dd254600558aec6e76309ba596f

That commit completed:

AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 214 tests
- integrated simulator demo: PASS
- release review script: PASS
- all physical-player demos: PASS
- release review final_passed: yes
- unsafe_acceptance_count: 0
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no

This run should refresh the public release/package layer.

Do not add new simulator features.
Do not restart the simulator.
Do not replace the state machine.
Do not alter mechanism profiles unless a packaging/release check exposes a documentation or packaging reference problem.
Do not weaken claim boundaries.
Do not claim hardware validation.
Do not push.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run refreshes the public package/release state after the physical-player software/control simulator sequence.

Correct framing:

- The hardware is not present yet.
- The repo has software-control simulator layers for future hardware alignment.
- The public package should include source, docs, demos, tests, site files, release-review docs, claim boundaries, and metadata needed to understand the software-control work.
- Generated demo output should remain excluded from committed release source.
- Any release/package report generated by this run is a software release-review artifact, not hardware proof.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim if verified:

- tests pass
- demos pass
- release review passes
- package manifest includes physical-player docs/scripts/tests
- generated outputs are excluded
- local paths are absent from public docs/package metadata
- claim boundaries are included
- public package refresh passed

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

Public framing to preserve:

The physical-player branch is a software/control foundation for future hardware alignment. It can define and test the behaviour that later hardware must obey, but it does not prove manufactured hardware exists.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md
LICENSE
NOTICE if present
PUBLICATION_STATUS.md if present
RELEASE_NOTES.md if present
CHANGELOG.md if present
MANIFEST.md if present
PACKAGE_MANIFEST.md if present
docs/README.md if present
docs/INDEX.md if present

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_AUDIT.md

site/index.html if present

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py
src/amcf_physical_player_integrated_demo_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py
demo/run_physical_player_release_review.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
tests/test_physical_player_public_docs_sync.py
tests/test_physical_player_release_review.py
tests/test_release_package.py if present
other existing tests

.gitignore
any packaging/build scripts
any existing release/package scripts

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not push.
Do not modify simulator code unless a release/package check exposes a minimal bug.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the package contains a manufactured player.
Do not claim real optical no-gap switching is proven.
Do not claim real reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not commit generated output folders.
Do not commit generated ZIPs unless the repo already tracks release ZIPs by policy.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_AUDIT.md

Include:

- current git HEAD
- whether 659bd3e or later is present
- repo status before refresh
- existing release/package files found
- existing package/release tests found
- physical-player source files found
- physical-player docs found
- physical-player demo scripts found
- physical-player tests found
- site files found
- generated output folders found
- packaging gaps found
- files to edit
- files to create
- confirmation that this is public release/package refresh only
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — PACKAGE INVENTORY SCRIPT
================================================================================

Create:

demo/run_public_release_package_refresh.py

This script should inspect the repo and write a deterministic package-refresh report.

Use standard library only.

It should not create a committed package ZIP by default.
It may create JSON/Markdown reports under output/ if useful.

Required output folder:

output/public_release_package_refresh/

Required output files:

- package_refresh_report.json
- package_inventory.json
- package_claim_boundary_scan.json
- package_local_path_scan.json
- package_generated_output_scan.json
- PACKAGE_REFRESH_SUMMARY.md
- NEXT_STEPS.md

Generated output should not be committed.

The script should check:

1. Required source files exist.
2. Required demo scripts exist.
3. Required tests exist.
4. Required docs exist.
5. README links to physical-player docs map.
6. README links to release review doc or package refresh doc if added.
7. CLAIM_BOUNDARIES.md contains physical-player software/control simulator boundary.
8. Docs map includes release review and public summary.
9. Development sequence includes Stages 2–8.
10. Release review doc exists.
11. Release review script exists.
12. Site navigation exists and links to physical-player docs if site exists.
13. No generated output is tracked or staged.
14. No local Windows workspace paths appear in public docs/site/package metadata.
15. No unsafe affirmative hardware claims appear in public docs/site/package metadata.
16. Package manifest/release inventory includes all new physical-player docs/scripts/tests.
17. unsafe_acceptance_count remains 0 if integrated simulator summary helper is available.

The report should include:

- run_name
- base_commit_hint
- required_docs_present
- required_source_present
- required_demos_present
- required_tests_present
- site_present
- site_links_present
- generated_output_tracked
- local_path_leak_found
- unsafe_hardware_claim_found
- unsafe_acceptance_count
- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- real_sensors_required
- real_motors_required
- real_cartridges_required
- real_scans_required
- manufactured_player_claimed
- final_passed
- recommended_next_step

Required claim values:

physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
real_sensors_required = false
real_motors_required = false
real_cartridges_required = false
real_scans_required = false
manufactured_player_claimed = false

final_passed true only if all required checks pass and all claim booleans remain false.

================================================================================
02 — PACKAGE MANIFEST / INVENTORY DOC
================================================================================

Create or update:

docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md

Include:

- purpose
- baseline commit
- what the package refresh checks
- required source files
- required demo scripts
- required test files
- required docs
- site/navigation inclusion
- generated-output exclusion
- local-path scan
- claim-boundary scan
- what is not claimed
- how to run the package refresh script
- expected output folder
- next development step

Do not claim hardware exists.

Create or update:

docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md

This should be a human-readable package inventory.

Include sections:

1. Core repo files
2. Physical-player source modules
3. Physical-player demos
4. Physical-player tests
5. Physical-player docs
6. Site/public pages
7. Claim-boundary files
8. Generated-output policy
9. Excluded files/folders
10. Package-refresh command

Physical-player docs should include at least:

- docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
- docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
- docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
- docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
- docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
- docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
- docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
- docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
- docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md
- docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Physical-player demos should include:

- demo/run_physical_player_state_machine_demo.py
- demo/run_physical_player_fail_closed_demo.py
- demo/run_physical_player_reverse_seek_demo.py
- demo/run_physical_player_mechanism_profiles_demo.py
- demo/run_physical_player_simulator_demo.py
- demo/run_physical_player_release_review.py

Physical-player tests should include:

- tests/test_physical_player_state_machine.py
- tests/test_physical_player_fail_closed.py
- tests/test_physical_player_reverse_seek.py
- tests/test_physical_player_mechanism_profiles.py
- tests/test_physical_player_simulator_demo.py
- tests/test_physical_player_public_docs_sync.py
- tests/test_physical_player_release_review.py

================================================================================
03 — README / DOCS MAP UPDATE
================================================================================

Update README.md only if needed.

Add concise link to:

docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md

or package inventory doc.

Update:

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md

Add links to:

- docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md
- docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md

Keep it concise.

================================================================================
04 — DEVELOPMENT SEQUENCE UPDATE
================================================================================

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add Stage 9:

AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1

Purpose:

- public package/release inventory refresh
- verify source/docs/demos/tests/site inclusion
- verify generated-output exclusion
- verify claim-boundary scan
- verify local-path scan
- verify package refresh report

Status:

current run, not committed yet

Claim boundary:

- software/control release-package refresh only
- no physical hardware validation
- no physical Level 5 claim
- no manufactured physical player claim

Also update Stage 8 from current run to actual pushed commit if not already done:

659bd3e74a9e4dd254600558aec6e76309ba596f

================================================================================
05 — PACKAGE TESTS
================================================================================

Create:

tests/test_public_release_package_refresh.py

Tests should verify:

1. demo/run_public_release_package_refresh.py exists
2. docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md exists
3. docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md exists
4. README links to package refresh or package inventory doc
5. docs map links to package refresh or inventory doc
6. package refresh script can build a report dict
7. package refresh report final_passed true
8. package refresh report generated_output_tracked false
9. package refresh report local_path_leak_found false
10. package refresh report unsafe_hardware_claim_found false
11. package refresh report physical_hardware_claimed false
12. package refresh report hardware_validation_claimed false
13. package refresh report physical_level_5_claimed false
14. package refresh report manufactured_player_claimed false
15. package inventory lists all physical-player demos
16. package inventory lists all physical-player tests
17. package inventory lists all physical-player docs
18. development sequence mentions Stage 9
19. development sequence mentions Stage 8 commit 659bd3e
20. full unittest suite passes

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
06 — OPTIONAL PACKAGE ARCHIVE
================================================================================

Do not create a release ZIP unless an existing repo script/test already expects one or unless it is trivial and placed only under ignored output/.

If you do create an archive under output/public_release_package_refresh/, make it clear:

- generated archive is local output
- generated archive is not committed
- generated archive is not hardware proof

Do not add generated ZIPs to Git.

================================================================================
07 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile demo/run_public_release_package_refresh.py
python -m py_compile demo/run_physical_player_release_review.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py
python demo/run_physical_player_release_review.py
python demo/run_public_release_package_refresh.py

Also run package/release-related tests through unittest discovery.

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
08 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md docs demo tests

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_public_release_package_refresh.py

Commit message:

git commit -m "Refresh public release package inventory"

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- test results
- demo results
- package refresh output folder
- git status
- git diff --stat

================================================================================
09 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- package refresh script created yes/no
- package inventory created yes/no
- package refresh doc created yes/no
- docs map updated yes/no
- development sequence updated yes/no
- validation commands run
- test results
- integrated simulator demo still passes yes/no
- release review still passes yes/no
- package refresh final_passed yes/no
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 16 decides

```text id="part16_decision"
Part 16 decides that the next Codex run should be:

AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
```

This run should add:

```text id="part16_adds"
- package refresh audit
- package refresh script
- package refresh docs
- public release package inventory
- package refresh tests
- package inventory report
- generated-output scan
- local-path scan
- claim-boundary scan
- development-sequence Stage 9
- docs map / README package links
```

It should build on:

```text id="part16_base"
659bd3e74a9e4dd254600558aec6e76309ba596f
```

It should not add new simulator logic or claim hardware validation.

---

## 5. What Part 17 should cover next

```text id="part17_next"
Part 17 should be:

Codex-Ready Implementation Prompt for AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
```

That next run should perform a final GitHub Pages/public docs review:

```text id="part17_scope"
- verify site/index.html links
- verify docs links from site
- verify README public entry points
- verify docs map and public summary
- verify no local paths
- verify no unsafe hardware claims
- verify package inventory is linked
- run tests and public demos
- produce final Pages/public review report
```

Part 16 stops here because the public release package refresh implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part17"
AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
Base commit: 659bd3e74a9e4dd254600558aec6e76309ba596f
New commit: 8f76d7528e4f6399ef719a99f15e1b248ce8e2ff
Pushed: yes
Tests: 233 passed
Integrated simulator demo: passed
Release review script: passed
Package refresh script: passed
Package refresh final_passed: yes
generated output committed/tracked: no
local path leak found: no
unsafe hardware claim found: no
unsafe_acceptance_count: 0
physical hardware claimed: no
hardware validation claimed: no
physical Level 5 claimed: no
```

So Part 17 should now build directly on `8f76d75`.

# AMCF Physical Player Design and Structure Dossier  
## Part 17 — Codex-Ready Implementation Prompt for Public GitHub Pages Final Review V1

## 1. Purpose of Part 17

Part 16 completed and pushed:

```text id="part16_done"
AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
```

Commit:

```text id="part16_commit"
8f76d7528e4f6399ef719a99f15e1b248ce8e2ff
```

That run added the public package-refresh layer:

```text id="part16_added"
- package refresh script
- package refresh docs
- public release package inventory
- package refresh audit
- package refresh tests
- README/package links
- docs map/package links
- Stage 9 development-sequence entry
- 233 passing tests
```

Part 17 now defines the next Codex run:

```text id="part17_run"
AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
```

The purpose is to perform a final GitHub Pages / public documentation review.

This is not a simulator feature run.

This is not a package-build run.

It should verify the public-facing entry points are coherent:

```text id="part17_scope"
- site/index.html links
- README public entry points
- docs map
- public summary
- release review
- package inventory
- package refresh
- claim boundaries
- no local path leaks
- no unsafe hardware claims
- all public docs reachable from site/README/docs map
- tests and public demos still pass
```

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part17"
The GitHub Pages site proves a physical player exists.
```

Correct framing:

```text id="correct_frame_part17"
This is a final public documentation and GitHub Pages review for the AMCF physical-player software/control branch.

It verifies that public readers can navigate the docs, demos, claim boundaries, package inventory, and release review without encountering local paths, generated-output leaks, or unsafe hardware claims.
```

The boundary is:

```text id="part17_boundary"
GitHub Pages/public docs review: yes.
Physical hardware validation: no.
Manufactured physical player claim: no.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_public_github_pages_final_review_v1"
You are working on my AMCF project.

Run name:
AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

8f76d7528e4f6399ef719a99f15e1b248ce8e2ff

That commit completed:

AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 233 tests
- integrated simulator demo: PASS
- release review script: PASS
- package refresh script: PASS
- package refresh final_passed: yes
- required source/docs/demos/tests present: yes
- generated output committed/tracked: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count: 0
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no

This run should perform a final GitHub Pages / public documentation review.

Do not add new simulator features.
Do not restart the simulator.
Do not replace the state machine.
Do not alter mechanism profiles unless a public documentation check exposes a link/reference problem.
Do not weaken claim boundaries.
Do not claim hardware validation.
Do not push.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run performs a final public GitHub Pages and documentation review after the physical-player software/control simulator sequence.

Correct framing:

- The hardware is not present yet.
- The repo has software-control simulator layers for future hardware alignment.
- The public site and docs should clearly expose the physical-player docs, demos, release review, package inventory, and claim boundaries.
- The final review verifies public navigation and claim safety.
- Any report generated by this run is a public documentation/release-readiness artifact, not hardware proof.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim if verified:

- GitHub Pages/public docs navigation passes
- README public entry points pass
- docs map and public summary are linked
- release review and package inventory are linked
- claim boundaries are visible
- no local paths leak into public docs/site
- no unsafe hardware claims appear
- generated output remains excluded
- tests and public demos pass

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

Public framing to preserve:

The physical-player branch is a software/control foundation for future hardware alignment. It can define and test the behaviour that later hardware must obey, but it does not prove manufactured hardware exists.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md
LICENSE
NOTICE if present
PUBLICATION_STATUS.md if present
RELEASE_NOTES.md if present
CHANGELOG.md if present
MANIFEST.md if present
PACKAGE_MANIFEST.md if present
RELEASE_MANIFEST.json if present

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_AUDIT.md
docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

site/index.html if present
site/ any supporting files if present

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py
src/amcf_physical_player_integrated_demo_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py
demo/run_physical_player_release_review.py
demo/run_public_release_package_refresh.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
tests/test_physical_player_public_docs_sync.py
tests/test_physical_player_release_review.py
tests/test_public_release_package_refresh.py
tests/test_release_package.py if present
other existing tests

.gitignore
any packaging/build scripts
any existing release/package scripts

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not push.
Do not modify simulator code unless a public review check exposes a minimal documentation-reference bug.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the Pages site shows a manufactured player.
Do not claim real optical no-gap switching is proven.
Do not claim real reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not commit generated output folders.
Do not commit generated ZIPs.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_AUDIT.md

Include:

- current git HEAD
- whether 8f76d75 or later is present
- repo status before review
- site files found
- README/public entry points found
- docs map found
- public summary found
- release review docs found
- package refresh/inventory docs found
- claim-boundary docs found
- physical-player demos found
- physical-player tests found
- generated output folders found
- public navigation gaps found
- files to edit
- files to create
- confirmation that this is GitHub Pages/public docs final review only
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — FINAL PAGES REVIEW SCRIPT
================================================================================

Create:

demo/run_public_github_pages_final_review.py

This script should inspect the repo and write a deterministic GitHub Pages/public docs final-review report.

Use standard library only.

Required output folder:

output/public_github_pages_final_review/

Required output files:

- github_pages_final_review_report.json
- public_navigation_scan.json
- readme_entrypoint_scan.json
- docs_map_scan.json
- site_link_scan.json
- claim_boundary_scan.json
- local_path_scan.json
- generated_output_scan.json
- GITHUB_PAGES_FINAL_REVIEW_SUMMARY.md
- NEXT_STEPS.md

Generated output should not be committed.

The script should check:

1. README.md exists.
2. README links to docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md.
3. README links to docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md or simulator docs.
4. README links to package refresh or package inventory docs.
5. CLAIM_BOUNDARIES.md exists and contains physical-player software/control boundary.
6. docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md exists.
7. docs map links to the full physical-player doc chain.
8. docs map links to release review docs.
9. docs map links to package refresh/inventory docs.
10. docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md exists.
11. docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md exists.
12. docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md exists.
13. site/index.html exists.
14. site/index.html links to the physical-player docs map or public summary.
15. site/index.html links to integrated simulator/demo docs or release/package docs.
16. Development sequence includes Stages 2–9.
17. Development sequence includes known commits for Stages 2–8.
18. No generated output is tracked or staged.
19. No local Windows workspace paths appear in public docs/site/package metadata.
20. No unsafe affirmative hardware claims appear in public docs/site/package metadata.
21. unsafe_acceptance_count remains 0 if integrated helper/report is available.
22. Public package refresh script exists.
23. Release review script exists.
24. Integrated simulator demo script exists.

The report should include:

- run_name
- base_commit_hint
- site_present
- site_links_present
- readme_entrypoints_present
- docs_map_present
- docs_map_complete
- public_summary_present
- release_review_linked
- package_inventory_linked
- package_refresh_linked
- claim_boundaries_present
- generated_output_tracked
- local_path_leak_found
- unsafe_hardware_claim_found
- unsafe_acceptance_count
- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- real_sensors_required
- real_motors_required
- real_cartridges_required
- real_scans_required
- manufactured_player_claimed
- final_passed
- recommended_next_step

Required claim values:

physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
real_sensors_required = false
real_motors_required = false
real_cartridges_required = false
real_scans_required = false
manufactured_player_claimed = false

final_passed true only if all required public-navigation checks pass and all claim booleans remain false.

================================================================================
02 — PUBLIC NAVIGATION DOC
================================================================================

Create:

docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md

Include:

- purpose
- baseline commit
- what the final Pages/public review checks
- README entry-point checks
- docs map checks
- public summary checks
- site/index.html checks
- release review and package inventory checks
- claim-boundary checks
- generated-output checks
- local-path checks
- what is not claimed
- how to run the final review script
- expected output folder
- next development step

Do not claim hardware exists.

================================================================================
03 — README / DOCS MAP / SITE SYNC
================================================================================

Update README.md only if needed.

Add concise link to:

docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md

Update:

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md

Add link to:

docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md

Update:

site/index.html

only if needed.

Ensure site/index.html has a concise link group for:

- Physical Player Docs Map
- Physical Player Public Summary
- Integrated Simulator Demo
- Release Review
- Public Release Package Inventory or Package Refresh
- Claim Boundaries

Keep wording concise.

Do not make the site claim hardware.

Suggested wording:

The physical-player branch documents and simulates the software/control architecture for a future mechanical/optical AMCF player. It includes deterministic state-machine, fail-closed, reverse/seek, mechanism-profile, integrated-demo, release-review, and package-inventory layers. It does not claim manufactured hardware or physical validation.

================================================================================
04 — DEVELOPMENT SEQUENCE UPDATE
================================================================================

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add Stage 10:

AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1

Purpose:

- final GitHub Pages/public documentation review
- verify README entry points
- verify docs map and public summary
- verify site navigation
- verify release review and package inventory links
- verify generated-output exclusion
- verify local-path scan
- verify unsafe hardware claim scan

Status:

current run, not committed yet

Claim boundary:

- software/control public-docs review only
- no physical hardware validation
- no physical Level 5 claim
- no manufactured physical player claim

Also update Stage 9 from current run to actual pushed commit if not already done:

8f76d7528e4f6399ef719a99f15e1b248ce8e2ff

================================================================================
05 — FINAL PAGES TESTS
================================================================================

Create:

tests/test_public_github_pages_final_review.py

Tests should verify:

1. demo/run_public_github_pages_final_review.py exists
2. docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md exists
3. README links to docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md or docs map links to it
4. docs map links to final review doc
5. site/index.html exists
6. site/index.html links to physical-player docs map or public summary
7. site/index.html links to release review or package inventory
8. final review script can build a report dict
9. final review report final_passed true
10. final review report site_present true
11. final review report site_links_present true
12. final review report generated_output_tracked false
13. final review report local_path_leak_found false
14. final review report unsafe_hardware_claim_found false
15. final review report physical_hardware_claimed false
16. final review report hardware_validation_claimed false
17. final review report physical_level_5_claimed false
18. final review report manufactured_player_claimed false
19. development sequence mentions Stage 10
20. development sequence mentions Stage 9 commit 8f76d75
21. full unittest suite passes

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
06 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile demo/run_public_github_pages_final_review.py
python -m py_compile demo/run_public_release_package_refresh.py
python -m py_compile demo/run_physical_player_release_review.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py
python demo/run_physical_player_release_review.py
python demo/run_public_release_package_refresh.py
python demo/run_public_github_pages_final_review.py

Also run all public/physical-player demos if practical:

python demo/run_physical_player_state_machine_demo.py
python demo/run_physical_player_fail_closed_demo.py
python demo/run_physical_player_reverse_seek_demo.py
python demo/run_physical_player_mechanism_profiles_demo.py
python demo/run_physical_player_simulator_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
07 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md docs site demo tests

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_public_github_pages_final_review.py

Commit message:

git commit -m "Add GitHub Pages final public review"

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- test results
- demo results
- final review output folder
- git status
- git diff --stat

================================================================================
08 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- final Pages review script created yes/no
- final Pages review doc created yes/no
- README updated yes/no
- docs map updated yes/no
- site updated yes/no
- development sequence updated yes/no
- validation commands run
- test results
- integrated simulator demo still passes yes/no
- release review still passes yes/no
- package refresh still passes yes/no
- final Pages review final_passed yes/no
- site present yes/no
- site links present yes/no
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 17 decides

```text id="part17_decision"
Part 17 decides that the next Codex run should be:

AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
```

This run should add:

```text id="part17_adds"
- final GitHub Pages review audit
- final GitHub Pages review script
- final public review doc
- final Pages/public-doc tests
- README/docs map/site link sync if needed
- generated-output scan
- local-path scan
- unsafe hardware claim scan
- development-sequence Stage 10
```

It should build on:

```text id="part17_base"
8f76d7528e4f6399ef719a99f15e1b248ce8e2ff
```

It should not add simulator logic or claim hardware validation.

---

## 5. What Part 18 should cover next

```text id="part18_next"
Part 18 should be:

Codex-Ready Implementation Prompt for AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
```

That next run should create a final closeout/handoff record:

```text id="part18_scope"
- summarize commits from state-machine through final Pages review
- summarize tests and demos
- summarize docs/site/package state
- confirm claim boundaries
- confirm no generated output tracked
- confirm no local path leaks
- produce final public-release handoff doc
- give exact final Git status and push instruction only if committed
```

Part 17 stops here because the GitHub Pages final public review implementation prompt is now defined.
----

Pushed result understood.

Current state:

```text id="current_state_part18"
AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
Base commit: 8f76d7528e4f6399ef719a99f15e1b248ce8e2ff
New commit: 8082f0a1134ea33df330c0508f06cc3ff7130e59
Pushed: yes
Tests: 253 passed
Integrated simulator demo: passed
Release review script: passed
Package refresh script: passed
Final Pages review script: passed
All physical-player demos: passed
site present: yes
site links present: yes
generated output committed/tracked: no
local path leak found: no
unsafe hardware claim found: no
unsafe_acceptance_count: 0
physical hardware claimed: no
hardware validation claimed: no
physical Level 5 claimed: no
```

So Part 18 should now build directly on `8082f0a`.

# AMCF Physical Player Design and Structure Dossier  
## Part 18 — Codex-Ready Implementation Prompt for Public Release Closeout Handoff V1

## 1. Purpose of Part 18

Part 17 completed and pushed:

```text id="part17_done"
AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
```

Commit:

```text id="part17_commit"
8082f0a1134ea33df330c0508f06cc3ff7130e59
```

That run completed the final public GitHub Pages / public documentation review:

```text id="part17_added"
- final Pages review script
- final public review doc
- final Pages review audit
- final Pages review tests
- README/docs map/site link sync
- Stage 10 development-sequence entry
- 253 passing tests
```

Part 18 now defines the closeout/handoff run:

```text id="part18_run"
AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
```

The purpose is to create the final public-release handoff record for the physical-player software/control sequence.

This run should summarize:

```text id="part18_scope"
- commit trail from state-machine through final Pages review
- tests and demos
- docs/site/package state
- claim boundaries
- generated-output policy
- local-path scan
- unsafe hardware claim scan
- final public repo status
- exact handoff instructions
```

This is not a feature run.

This is not a package-build run.

This is the final closeout record so the project has one clear handoff document after the long physical-player sequence.

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part18"
This handoff proves a physical hardware player exists.
```

Correct framing:

```text id="correct_frame_part18"
This is a closeout and handoff for the AMCF physical-player software/control simulator and public documentation sequence.

It records what has been implemented in software, what has been tested, what has been documented, what is publicly linked, and what remains future hardware work.
```

The boundary is:

```text id="part18_boundary"
Public release closeout/handoff: yes.
Physical hardware validation: no.
Manufactured physical player claim: no.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_public_release_closeout_handoff_v1"
You are working on my AMCF project.

Run name:
AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

8082f0a1134ea33df330c0508f06cc3ff7130e59

That commit completed:

AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 253 tests
- integrated simulator demo: PASS
- release review script: PASS
- package refresh script: PASS
- final Pages review script: PASS
- all physical-player demos: PASS
- final Pages review final_passed: yes
- site present: yes
- site links present: yes
- generated output committed/tracked: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count: 0
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no

This run should create a final public-release closeout and handoff record.

Do not add new simulator features.
Do not restart the simulator.
Do not replace the state machine.
Do not alter mechanism profiles.
Do not weaken claim boundaries.
Do not claim hardware validation.
Do not push.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run creates the final handoff record for the physical-player software/control simulator and public documentation sequence.

Correct framing:

- The hardware is not present yet.
- The repo has software-control simulator layers for future hardware alignment.
- The repo has public documentation, Pages navigation, release review, package inventory, and final public review layers.
- This closeout summarizes the public-release state and gives the next maintainer/user a single handoff document.
- The handoff is a software/public-release record, not hardware proof.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim if verified:

- software/control simulator sequence completed
- docs and site navigation completed
- release review completed
- package inventory completed
- final Pages review completed
- tests pass
- public demos pass
- generated output excluded
- no local path leaks
- no unsafe hardware claims
- unsafe_acceptance_count remains 0
- claim boundaries preserved

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

Public framing to preserve:

The physical-player branch is a software/control foundation for future hardware alignment. It can define and test the behaviour that later hardware must obey, but it does not prove manufactured hardware exists.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md
LICENSE
NOTICE if present
PUBLICATION_STATUS.md if present
RELEASE_NOTES.md if present
CHANGELOG.md if present
MANIFEST.md if present
PACKAGE_MANIFEST.md if present
RELEASE_MANIFEST.json if present

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_AUDIT.md
docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md
docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

site/index.html if present

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py
src/amcf_physical_player_integrated_demo_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py
demo/run_physical_player_release_review.py
demo/run_public_release_package_refresh.py
demo/run_public_github_pages_final_review.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
tests/test_physical_player_public_docs_sync.py
tests/test_physical_player_release_review.py
tests/test_public_release_package_refresh.py
tests/test_public_github_pages_final_review.py
tests/test_release_package.py if present
other existing tests

.gitignore
any packaging/build scripts
any existing release/package scripts

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not push.
Do not modify simulator code.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the handoff describes a manufactured player.
Do not claim real optical no-gap switching is proven.
Do not claim real reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not commit generated output folders.
Do not commit generated ZIPs.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_AUDIT.md

Include:

- current git HEAD
- whether 8082f0a or later is present
- repo status before closeout
- closeout-relevant docs found
- closeout-relevant scripts found
- closeout-relevant tests found
- site files found
- claim-boundary files found
- generated output folders found
- known commit trail found
- files to edit
- files to create
- confirmation that this is closeout/handoff only
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — CLOSEOUT HANDOFF SCRIPT
================================================================================

Create:

demo/run_public_release_closeout_handoff.py

This script should inspect the repo and write a deterministic closeout/handoff report.

Use standard library only.

Required output folder:

output/public_release_closeout_handoff/

Required output files:

- closeout_handoff_report.json
- closeout_commit_trail.json
- closeout_validation_summary.json
- closeout_claim_boundary_summary.json
- closeout_docs_site_summary.json
- closeout_generated_output_scan.json
- closeout_local_path_scan.json
- CLOSEOUT_HANDOFF_SUMMARY.md
- NEXT_STEPS.md

Generated output should not be committed.

The script should check:

1. Required public docs exist.
2. Required source modules exist.
3. Required demos exist.
4. Required tests exist.
5. Site exists and links to physical-player/public docs.
6. README links to docs map/public summary/release or package docs.
7. Development sequence includes Stages 2–10.
8. Development sequence includes known pushed commits for Stages 2–10.
9. Closeout handoff doc exists or will be created.
10. Claim boundaries are present.
11. No generated output is tracked or staged.
12. No local Windows workspace paths appear in public docs/site/package metadata.
13. No unsafe affirmative hardware claims appear in public docs/site/package metadata.
14. unsafe_acceptance_count remains 0 if integrated helper/report is available.
15. Release review script exists.
16. Package refresh script exists.
17. Final Pages review script exists.
18. All expected public-review docs exist.

The report should include:

- run_name
- base_commit_hint
- closeout_doc_present
- commit_trail_complete
- required_docs_present
- required_source_present
- required_demos_present
- required_tests_present
- site_present
- site_links_present
- readme_entrypoints_present
- development_sequence_complete
- release_review_present
- package_refresh_present
- final_pages_review_present
- generated_output_tracked
- local_path_leak_found
- unsafe_hardware_claim_found
- unsafe_acceptance_count
- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- real_sensors_required
- real_motors_required
- real_cartridges_required
- real_scans_required
- manufactured_player_claimed
- final_passed
- recommended_next_step

Required claim values:

physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
real_sensors_required = false
real_motors_required = false
real_cartridges_required = false
real_scans_required = false
manufactured_player_claimed = false

final_passed true only if all closeout checks pass and all claim booleans remain false.

================================================================================
02 — FINAL CLOSEOUT HANDOFF DOC
================================================================================

Create:

docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md

This should be the single human-readable closeout document.

Include sections:

1. Purpose
2. Baseline commit
3. Public repo link
4. What has been completed
5. Commit trail
6. Test and demo summary
7. Public docs and site summary
8. Package/release summary
9. Claim-boundary summary
10. Generated-output policy
11. Local-path and unsafe-claim scan summary
12. What is explicitly not claimed
13. What remains future hardware work
14. How to verify the release locally
15. Next recommended step

Commit trail should include:

Stage 2:
AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
f8b6e91e1dfd9b57345ee38ac262635d446f47c8

Stage 3:
AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e

Stage 4:
AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
802042b5395ac860c437188e0d79031d7dd5f591

Stage 5:
AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
01093024f9bbd11d10615a0f526b4440e5f8f41b

Stage 6:
AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
fea00409262dea39d5c9068daac0a206c02d07f5

Stage 7:
AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
c7c2658877f04d40b94b127c6e44fe30d3597a18

Stage 8:
AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
659bd3e74a9e4dd254600558aec6e76309ba596f

Stage 9:
AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
8f76d7528e4f6399ef719a99f15e1b248ce8e2ff

Stage 10:
AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
8082f0a1134ea33df330c0508f06cc3ff7130e59

Stage 11:
AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
current run, not committed yet

Also mention:

Stage 1 model-foundation was not a separate pushed commit in this sequence; early model structures were folded into the state-machine run because no standalone model module existed at that time.

Do not claim hardware exists.

================================================================================
03 — CLOSEOUT DOC MAP / README / SITE SYNC
================================================================================

Update README.md only if needed.

Add concise link to:

docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md

Update:

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md

Add link to:

docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md

Update:

site/index.html

only if needed.

Add a concise link to the closeout handoff doc in the physical-player/public release section.

Do not make the site claim hardware.

Suggested wording:

The closeout handoff records the software/control simulator sequence, public docs, release review, package inventory, final Pages review, claim boundaries, and next steps. It does not claim manufactured hardware or physical validation.

================================================================================
04 — DEVELOPMENT SEQUENCE UPDATE
================================================================================

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add Stage 11:

AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1

Purpose:

- final public-release closeout handoff
- summarize commits, tests, demos, docs, site, package state, claim boundaries, generated-output policy, local-path scan, and unsafe-claim scan

Status:

current run, not committed yet

Claim boundary:

- software/control closeout handoff only
- no physical hardware validation
- no physical Level 5 claim
- no manufactured physical player claim

Also update Stage 10 from current run to actual pushed commit if not already done:

8082f0a1134ea33df330c0508f06cc3ff7130e59

================================================================================
05 — CLOSEOUT TESTS
================================================================================

Create:

tests/test_public_release_closeout_handoff.py

Tests should verify:

1. demo/run_public_release_closeout_handoff.py exists
2. docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md exists
3. README links to closeout handoff doc or docs map links to it
4. docs map links to closeout handoff doc
5. site/index.html links to closeout handoff doc or docs map
6. closeout script can build a report dict
7. closeout report final_passed true
8. closeout report commit_trail_complete true
9. closeout report generated_output_tracked false
10. closeout report local_path_leak_found false
11. closeout report unsafe_hardware_claim_found false
12. closeout report physical_hardware_claimed false
13. closeout report hardware_validation_claimed false
14. closeout report physical_level_5_claimed false
15. closeout report manufactured_player_claimed false
16. closeout handoff doc mentions Stages 2 through 11
17. closeout handoff doc includes commits for Stages 2 through 10
18. development sequence mentions Stage 11
19. development sequence mentions Stage 10 commit 8082f0a
20. full unittest suite passes

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
06 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile demo/run_public_release_closeout_handoff.py
python -m py_compile demo/run_public_github_pages_final_review.py
python -m py_compile demo/run_public_release_package_refresh.py
python -m py_compile demo/run_physical_player_release_review.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py
python demo/run_physical_player_release_review.py
python demo/run_public_release_package_refresh.py
python demo/run_public_github_pages_final_review.py
python demo/run_public_release_closeout_handoff.py

Also run all public/physical-player demos if practical:

python demo/run_physical_player_state_machine_demo.py
python demo/run_physical_player_fail_closed_demo.py
python demo/run_physical_player_reverse_seek_demo.py
python demo/run_physical_player_mechanism_profiles_demo.py
python demo/run_physical_player_simulator_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
07 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md docs site demo tests

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_public_release_closeout_handoff.py

Commit message:

git commit -m "Add public release closeout handoff"

Do not push.

If commit is not appropriate, explain why and report:

- changed files
- test results
- demo results
- closeout output folder
- git status
- git diff --stat

================================================================================
08 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- closeout handoff script created yes/no
- closeout handoff doc created yes/no
- README updated yes/no
- docs map updated yes/no
- site updated yes/no
- development sequence updated yes/no
- validation commands run
- test results
- integrated simulator demo still passes yes/no
- release review still passes yes/no
- package refresh still passes yes/no
- final Pages review still passes yes/no
- closeout handoff final_passed yes/no
- commit trail complete yes/no
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 18 decides

```text id="part18_decision"
Part 18 decides that the next Codex run should be:

AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
```

This run should add:

```text id="part18_adds"
- closeout handoff audit
- closeout handoff script
- final public-release handoff doc
- closeout tests
- README/docs map/site link sync if needed
- generated-output scan
- local-path scan
- unsafe hardware claim scan
- development-sequence Stage 11
- final closeout report
```

It should build on:

```text id="part18_base"
8082f0a1134ea33df330c0508f06cc3ff7130e59
```

It should not add simulator logic or claim hardware validation.

---

## 5. What Part 19 should cover next

```text id="part19_next"
Part 19 should be:

Codex-Ready Implementation Prompt for AMCF_PUBLIC_RELEASE_TAG_PREP_V1
```

That next run should prepare for a possible public release tag:

```text id="part19_scope"
- verify closeout handoff is committed and pushed
- run tests and all public review scripts
- verify repo clean
- prepare suggested tag name
- prepare release notes draft
- verify claim boundaries
- do not create tag unless explicitly instructed
```

Part 18 stops here because the public release closeout handoff implementation prompt is now defined.
-----

Pushed result understood.

Current state:

```text id="current_state_part19"
AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
Base commit: 8082f0a1134ea33df330c0508f06cc3ff7130e59
New commit: 331848fdf10ff18eab0a9426441f0f00e91a8f03
Pushed: yes
Tests: 272 passed
Integrated simulator demo: passed
Release review: passed
Package refresh: passed
Final Pages review: passed
Closeout handoff report: passed
Commit trail complete: yes
generated output committed/tracked: no
local path leak found: no
unsafe hardware claim found: no
unsafe_acceptance_count: 0
physical hardware claimed: no
hardware validation claimed: no
physical Level 5 claimed: no
```

So Part 19 should now build directly on `331848f`.

# AMCF Physical Player Design and Structure Dossier  
## Part 19 — Codex-Ready Implementation Prompt for Public Release Tag Prep V1

## 1. Purpose of Part 19

Part 18 completed and pushed:

```text id="part18_done"
AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
```

Commit:

```text id="part18_commit"
331848fdf10ff18eab0a9426441f0f00e91a8f03
```

That run added the final closeout/handoff layer:

```text id="part18_added"
- closeout handoff script
- closeout handoff doc
- closeout audit
- closeout tests
- README/docs map/site links
- Stage 11 development-sequence entry
- 272 passing tests
```

Part 19 now defines the next Codex run:

```text id="part19_run"
AMCF_PUBLIC_RELEASE_TAG_PREP_V1
```

The purpose is to prepare for a possible public release tag.

This run should **not create a tag**.

It should prepare:

```text id="part19_scope"
- tag-readiness report
- suggested tag name
- release notes draft
- release checklist
- repo cleanliness check
- final test/demo verification
- claim-boundary verification
- generated-output exclusion check
- local-path scan
- unsafe hardware-claim scan
```

This is a release-preparation layer only.

---

## 2. Correct framing

Do not frame this as:

```text id="wrong_frame_part19"
This creates a release proving a physical player exists.
```

Correct framing:

```text id="correct_frame_part19"
This prepares release-tag materials for the AMCF physical-player software/control simulator and public documentation sequence.

It verifies that the repository is tag-ready as a software/control public release, while preserving the boundary that no physical hardware validation or manufactured player is claimed.
```

The boundary is:

```text id="part19_boundary"
Release tag preparation: yes.
Actual tag creation: no, unless explicitly instructed later.
Physical hardware validation: no.
Manufactured physical player claim: no.
```

---

## 3. Copyable Codex prompt

```text id="codex_prompt_amcf_public_release_tag_prep_v1"
You are working on my AMCF project.

Run name:
AMCF_PUBLIC_RELEASE_TAG_PREP_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
<repo-root>

If Codex is already inside the repo root, use the current repo root.

================================================================================
CURRENT BASELINE
================================================================================

This run builds on the pushed commit:

331848fdf10ff18eab0a9426441f0f00e91a8f03

That commit completed:

AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1

Known validation from that run:

- py_compile: PASS
- unittest discover: PASS, 272 tests
- integrated simulator demo: PASS
- release review: PASS
- package refresh: PASS
- final Pages review: PASS
- closeout handoff report: PASS
- commit trail complete: yes
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count: 0
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no

This run should prepare public release tag materials.

Do not create a Git tag.
Do not push.
Do not add new simulator features.
Do not restart the simulator.
Do not replace the state machine.
Do not alter mechanism profiles.
Do not weaken claim boundaries.
Do not claim hardware validation.

================================================================================
CORE FRAMING
================================================================================

AMCF is software-first.

This run prepares release-tag materials for the physical-player software/control simulator and public documentation sequence.

Correct framing:

- The hardware is not present yet.
- The repo has software-control simulator layers for future hardware alignment.
- The repo has public documentation, Pages navigation, release review, package inventory, final Pages review, and closeout handoff.
- This run prepares a tag-readiness report and release notes draft.
- It does not create a tag unless explicitly instructed in a later run.
- It does not claim hardware proof.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim if verified:

- release tag materials prepared
- repo is clean or documented
- tests pass
- public demos pass
- release review passes
- package refresh passes
- final Pages review passes
- closeout handoff passes
- generated output excluded
- no local path leaks
- no unsafe hardware claims
- unsafe_acceptance_count remains 0
- claim boundaries preserved

================================================================================
DESIGN BASELINE TO PRESERVE
================================================================================

Preferred physical-player concept:

compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety.

Preferred simulator default:

mechanism profile:
folded_ab_motor_encoder_baseline

carrier_layout:
folded_indexed_carrier

staging_model:
abstract_ab_staging

actuator_family:
motor_encoder

gate_model:
single_visible_gate_plus_hidden_staging

prefetch_model:
reader_prefetch_ahead

reverse_model:
limited_reverse_buffer

seek_model:
local_buffer_seek_only

safety_model:
fail_closed_required

Public framing to preserve:

The physical-player branch is a software/control foundation for future hardware alignment. It can define and test the behaviour that later hardware must obey, but it does not prove manufactured hardware exists.

================================================================================
EXISTING FILES TO INSPECT FIRST
================================================================================

Inspect first:

README.md
CLAIM_BOUNDARIES.md
LICENSE
NOTICE if present
PUBLICATION_STATUS.md if present
RELEASE_NOTES.md if present
CHANGELOG.md if present
MANIFEST.md if present
PACKAGE_MANIFEST.md if present
RELEASE_MANIFEST.json if present
.gitignore

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md
docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md
docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md

site/index.html if present

src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py
src/amcf_physical_player_integrated_demo_reports.py

demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py
demo/run_physical_player_release_review.py
demo/run_public_release_package_refresh.py
demo/run_public_github_pages_final_review.py
demo/run_public_release_closeout_handoff.py

tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
tests/test_physical_player_public_docs_sync.py
tests/test_physical_player_release_review.py
tests/test_public_release_package_refresh.py
tests/test_public_github_pages_final_review.py
tests/test_public_release_closeout_handoff.py
tests/test_release_package.py if present

any existing release/package/tag scripts
any existing release notes or changelog files

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not run deep tools.
Do not push.
Do not create a Git tag.
Do not create a GitHub release.
Do not modify simulator code.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not claim physical hardware validation.
Do not claim physical Level 5 is complete.
Do not claim the release proves a manufactured player.
Do not claim real optical no-gap switching is proven.
Do not claim real reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not commit generated output folders.
Do not commit generated ZIPs.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PUBLIC_RELEASE_TAG_PREP_AUDIT.md

Include:

- current git HEAD
- whether 331848f or later is present
- repo status before tag prep
- existing tags found if checked
- release notes/changelog files found
- closeout handoff doc found
- final Pages review doc found
- package inventory doc found
- release review docs found
- claim-boundary files found
- generated output folders found
- files to edit
- files to create
- confirmation that this is tag preparation only
- confirmation that no Git tag is being created
- confirmation that no physical hardware validation is being claimed

================================================================================
01 — TAG PREP SCRIPT
================================================================================

Create:

demo/run_public_release_tag_prep.py

This script should inspect the repo and write a deterministic release-tag preparation report.

Use standard library only.

It may inspect existing Git tags with a safe read-only command if practical:

git tag --list

Do not create a tag.

Required output folder:

output/public_release_tag_prep/

Required output files:

- release_tag_prep_report.json
- suggested_tag.json
- release_notes_draft.md
- release_checklist.json
- claim_boundary_scan.json
- local_path_scan.json
- generated_output_scan.json
- RELEASE_TAG_PREP_SUMMARY.md
- NEXT_STEPS.md

Generated output should not be committed.

The script should check:

1. Repo HEAD is readable.
2. Current branch is readable if possible.
3. Repo is clean or expected doc changes are not yet staged.
4. Closeout handoff doc exists.
5. Release review doc exists.
6. Package refresh doc exists.
7. Final Pages review doc exists.
8. Docs map exists.
9. Site index exists.
10. README links to public docs.
11. Development sequence includes Stages 2–11.
12. Known commits for Stages 2–11 are present where available.
13. No generated output is tracked or staged.
14. No local Windows workspace paths appear in public docs/site/package metadata.
15. No unsafe affirmative hardware claims appear in public docs/site/package metadata.
16. unsafe_acceptance_count remains 0 if integrated helper/report is available.
17. Claim boundaries are present.
18. Tag is not created by this script.

The report should include:

- run_name
- base_commit_hint
- current_head
- current_branch
- existing_tags
- suggested_tag_name
- suggested_release_title
- suggested_release_type
- closeout_doc_present
- release_review_present
- package_refresh_present
- final_pages_review_present
- docs_map_present
- site_present
- readme_entrypoints_present
- development_sequence_complete
- generated_output_tracked
- local_path_leak_found
- unsafe_hardware_claim_found
- unsafe_acceptance_count
- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- real_sensors_required
- real_motors_required
- real_cartridges_required
- real_scans_required
- manufactured_player_claimed
- tag_created
- final_passed
- recommended_next_step

Required claim values:

physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
real_sensors_required = false
real_motors_required = false
real_cartridges_required = false
real_scans_required = false
manufactured_player_claimed = false
tag_created = false

final_passed true only if all tag-prep checks pass and no tag was created.

Suggested tag naming:

If there is no existing project tag convention, suggest:

amcf-physical-player-software-control-v1

Also provide an alternate date-style suggestion:

amcf-public-release-2026-10-12

Do not create either tag.

================================================================================
02 — RELEASE NOTES DRAFT DOC
================================================================================

Create:

docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md

Include:

- purpose
- baseline commit
- what tag prep checks
- suggested tag name
- suggested release title
- release notes draft summary
- validation checklist
- claim-boundary checklist
- what is not claimed
- how to run the tag prep script
- expected output folder
- next step

Do not claim hardware exists.

Create:

docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md

This should be a human-readable release-notes draft for a possible later tag.

Include:

1. Proposed title
2. Suggested tag name
3. Baseline commit
4. Summary
5. What changed
6. Physical-player software/control sequence
7. Public documentation and Pages
8. Release/package review
9. Tests and demos
10. Claim boundaries
11. What is not claimed
12. Suggested verification commands
13. Tag creation is not performed in this run

Mention the commit trail:

Stage 2:
f8b6e91e1dfd9b57345ee38ac262635d446f47c8

Stage 3:
4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e

Stage 4:
802042b5395ac860c437188e0d79031d7dd5f591

Stage 5:
01093024f9bbd11d10615a0f526b4440e5f8f41b

Stage 6:
fea00409262dea39d5c9068daac0a206c02d07f5

Stage 7:
c7c2658877f04d40b94b127c6e44fe30d3597a18

Stage 8:
659bd3e74a9e4dd254600558aec6e76309ba596f

Stage 9:
8f76d7528e4f6399ef719a99f15e1b248ce8e2ff

Stage 10:
8082f0a1134ea33df330c0508f06cc3ff7130e59

Stage 11:
331848fdf10ff18eab0a9426441f0f00e91a8f03

Do not claim hardware exists.

================================================================================
03 — RELEASE CHECKLIST DOC
================================================================================

Create:

docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md

Include a checklist:

- repo clean
- latest commit pushed
- tests pass
- integrated simulator demo passes
- release review passes
- package refresh passes
- final Pages review passes
- closeout handoff passes
- generated output untracked
- local path scan passes
- unsafe hardware claim scan passes
- claim boundaries present
- release notes reviewed
- tag name chosen
- explicit human approval to create tag
- tag creation command not run yet
- push tag command not run yet

Include suggested commands only as future manual commands, not executed:

git tag -a amcf-physical-player-software-control-v1 -m "AMCF physical-player software-control public release v1"

git push origin amcf-physical-player-software-control-v1

Clearly state:

Do not run these commands unless explicitly instructed.

================================================================================
04 — README / DOCS MAP / SITE SYNC
================================================================================

Update README.md only if needed.

Add concise link to:

docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md

Update:

docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md

Add links to:

- docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md
- docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md
- docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md

Update:

site/index.html

only if needed.

Add concise link to release tag prep / release notes draft in the public release section.

Do not make the site claim hardware.

================================================================================
05 — DEVELOPMENT SEQUENCE UPDATE
================================================================================

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add Stage 12:

AMCF_PUBLIC_RELEASE_TAG_PREP_V1

Purpose:

- prepare release tag materials
- suggested tag name
- release notes draft
- release checklist
- tag-readiness report
- verify claim boundaries
- verify no generated output tracked
- verify no local path leaks
- verify no unsafe hardware claims

Status:

current run, not committed yet

Claim boundary:

- tag preparation only
- no tag created
- no physical hardware validation
- no physical Level 5 claim
- no manufactured physical player claim

Also update Stage 11 from current run to actual pushed commit if not already done:

331848fdf10ff18eab0a9426441f0f00e91a8f03

================================================================================
06 — TAG PREP TESTS
================================================================================

Create:

tests/test_public_release_tag_prep.py

Tests should verify:

1. demo/run_public_release_tag_prep.py exists
2. docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md exists
3. docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md exists
4. docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md exists
5. README links to tag prep doc or docs map links to it
6. docs map links to tag prep doc
7. docs map links to release notes draft
8. docs map links to tag checklist
9. site/index.html links to tag prep/release notes or docs map
10. tag prep script can build a report dict
11. tag prep report final_passed true
12. tag prep report tag_created false
13. tag prep report generated_output_tracked false
14. tag prep report local_path_leak_found false
15. tag prep report unsafe_hardware_claim_found false
16. tag prep report physical_hardware_claimed false
17. tag prep report hardware_validation_claimed false
18. tag prep report physical_level_5_claimed false
19. tag prep report manufactured_player_claimed false
20. release notes draft includes Stage 11 commit 331848f
21. development sequence mentions Stage 12
22. development sequence mentions Stage 11 commit 331848f
23. full unittest suite passes

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
07 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile demo/run_public_release_tag_prep.py
python -m py_compile demo/run_public_release_closeout_handoff.py
python -m py_compile demo/run_public_github_pages_final_review.py
python -m py_compile demo/run_public_release_package_refresh.py
python -m py_compile demo/run_physical_player_release_review.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py
python demo/run_physical_player_release_review.py
python demo/run_public_release_package_refresh.py
python demo/run_public_github_pages_final_review.py
python demo/run_public_release_closeout_handoff.py
python demo/run_public_release_tag_prep.py

Also run all public/physical-player demos if practical:

python demo/run_physical_player_state_machine_demo.py
python demo/run_physical_player_fail_closed_demo.py
python demo/run_physical_player_reverse_seek_demo.py
python demo/run_physical_player_mechanism_profiles_demo.py
python demo/run_physical_player_simulator_demo.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.
Do not create a tag.

================================================================================
08 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md docs site demo tests

If tests are ignored by .gitignore, force-add only the intended test file:

git add -f tests/test_public_release_tag_prep.py

Commit message:

git commit -m "Prepare public release tag materials"

Do not push.
Do not create a tag.

If commit is not appropriate, explain why and report:

- changed files
- test results
- demo results
- tag prep output folder
- git status
- git diff --stat

================================================================================
09 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- corrected framing preserved yes/no
- files created
- files modified
- tag prep script created yes/no
- tag prep doc created yes/no
- release notes draft created yes/no
- tag checklist created yes/no
- README updated yes/no
- docs map updated yes/no
- site updated yes/no
- development sequence updated yes/no
- validation commands run
- test results
- integrated simulator demo still passes yes/no
- release review still passes yes/no
- package refresh still passes yes/no
- final Pages review still passes yes/no
- closeout handoff still passes yes/no
- tag prep final_passed yes/no
- suggested tag name
- tag created: no
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed
- tag creation command only as a future manual command, clearly marked not run

Expected push command if committed:

git push

Future manual tag command, not run:

git tag -a amcf-physical-player-software-control-v1 -m "AMCF physical-player software-control public release v1"

Future manual tag push command, not run:

git push origin amcf-physical-player-software-control-v1

Do not invent a commit hash.
Do not claim a tag was created.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

## 4. What Part 19 decides

```text id="part19_decision"
Part 19 decides that the next Codex run should be:

AMCF_PUBLIC_RELEASE_TAG_PREP_V1
```

This run should add:

```text id="part19_adds"
- release tag prep audit
- release tag prep script
- tag prep doc
- release notes draft
- release tag checklist
- tag prep tests
- suggested tag name
- future manual tag commands
- README/docs map/site link sync if needed
- generated-output scan
- local-path scan
- unsafe hardware claim scan
- development-sequence Stage 12
```

It should build on:

```text id="part19_base"
331848fdf10ff18eab0a9426441f0f00e91a8f03
```

It should not create a tag, push a tag, add simulator logic, or claim hardware validation.

---

## 5. What Part 20 should cover next

```text id="part20_next"
Part 20 should be one of two paths:

Option A:
AMCF_PUBLIC_RELEASE_TAG_CREATE_V1

Only if you explicitly decide to create the tag.

Option B:
AMCF_PUBLIC_RELEASE_ARCHIVE_FREEZE_V1

If you want one more no-tag archival verification layer before tagging.
```

Recommended next path:

```text id="part20_recommendation"
Use Option A only when you are ready to create a real Git tag.
Until then, stop at Part 19 because tag prep is enough.
```

Part 19 stops here because the public release tag-prep implementation prompt is now defined.
----
