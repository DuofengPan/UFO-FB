# Robot data layout

Each robot's description, motion files and motion YAML live together. Paths in
YAML are relative to the repository root. Run scripts from that root.

- `humanoidverse/data/robots/g1/mjcf/`: G1 29-DoF model and meshes.
- `humanoidverse/data/robots/g1/config/`: robot spec, LaFAN manifest and examples.
- `humanoidverse/data/robots/g1/motions/lafan/`: G1 LaFAN full and 10-second training PKLs.
- `humanoidverse/data/robots/astro_p2/mjcf/` and `meshes/`: Astro P2 model and meshes.
- `humanoidverse/data/robots/astro_p2/config/`: robot spec, baseline and high dynamic manifests.
- `humanoidverse/data/robots/astro_p2/motions/lafan/`: Astro LaFAN full and training PKLs.
- `humanoidverse/data/robots/astro_p2/motions/high_dynamic/`: the 20 kungfu + four backflip sources,
  converted data, hashes and rebuild instructions.

The large G1 and Astro LaFAN PKLs are local, ignored by Git and downloadable
from their existing Hugging Face datasets with:

```bash
bash scripts/download_data.sh g1_lafan
bash scripts/download_data.sh astro_lafan
```

The current server's G1 files were copied from `/data/workspace/UFO` after
checking the same SHA256 values as the downloader. The older repository retains
its copies. The high dynamic set is versioned in this repository and has not
been uploaded to Hugging Face. Existing run folders retain their original
provenance; new runs use the grouped paths.
