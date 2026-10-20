# AMCF Device Profile Layer

## Purpose

Device profiles bind the three physical software corridors to a selected
provider without changing the AMCF software-control protocol:

- `pc_to_printer`: carrier or printer profile;
- `reader_to_pc`: reader or scanner profile;
- `pc_to_player`: player-control profile.

Profiles describe the backend, transport, capabilities, configuration values,
and safety contract. They do not claim that a physical device is present.

## Default Profile

The built-in profile bundle uses:

- `file` for a hash-checked carrier artifact;
- `folder` for captured-section recovery;
- `loopback` for the player-control protocol.

An editable example is provided at
`profiles/amcf_device_profiles.example.json`.

Validate and run the default bundle with:

```text
amcf device-profiles --project-root . --output output/device_profile_validation
```

Validate a custom bundle with:

```text
amcf device-profiles --project-root . --profile profiles/amcf_device_profiles.example.json --output output/device_profile_validation
```

The command validates the schema and then runs the selected provider adapters.
It writes the normalized bundle, validation report, provider discovery report,
feedback, and a summary. A successful software profile has no hardware
connection and keeps physical transition authorization disabled.

## Hardware Profiles

A hardware profile may select `windows-spooler`, `windows-wia`, or `serial`.
Such a profile must set `hardware_requested: true`, and the command must also
receive `--enable-hardware`:

```text
amcf device-profiles --project-root . --profile <profile.json> --output output/device_profile_validation --enable-hardware
```

Both gates are required. A profile cannot silently open a device. Missing
drivers, missing names or ports, failed probes, invalid replies, and hash
mismatches remain rejected and fail closed.

The profile layer deliberately does not infer device-specific settings. The
actual printer model, scanner/WIA profile, serial protocol, media calibration,
and player timing contract must be selected and reviewed before hardware is
operated. Physical validation and physical Level 5 remain unclaimed.
