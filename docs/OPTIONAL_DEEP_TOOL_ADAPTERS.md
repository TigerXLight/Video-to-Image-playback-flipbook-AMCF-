# Optional Deep Tool Adapters

The AMCF clean core package does not bundle SAM2, SAMURAI, CoTracker, AOT, Cutie, DEVA, RAFT, XMem, TAPNet, Track-Anything, copied third-party repositories, model checkpoints, or deep-tool weights.

SAM2/SAMURAI/CoTracker work may exist in local research runs, but those local runs are not part of this clean GitHub core package.

If CoTracker or other non-commercial tooling is included later, the non-commercial boundary must remain visible. Such integrations should be described as source-available non-commercial, non-commercial research software, open code under non-commercial terms, or other licence-specific research integrations as appropriate, not as strict OSI open source.

AGPL or/copyleft-heavy tooling should not be copied into the AMCF core package unless those licence effects are explicitly accepted. When possible, keep the core package independent and reimplement general mechanisms rather than bundling restricted repositories.

Optional deep adapters are future work. The AMCF core package remains runnable without deep tools.
