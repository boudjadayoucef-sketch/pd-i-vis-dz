#!/usr/bin/env python3
"""PD&I Patch 003 — restore the complete PD&I isometric editor V4.8d.

This patch fixes an architectural mistake in the bootstrap: the previous
migration preserved the Guide shell but did not bring the V4.8d isometric
module into the new PD&I application.

The patch downloads the authoritative V4.8d module from the original public
repository, verifies its Git blob SHA, relocates it under src/pdi/isometric,
adapts only its relative imports, and exposes it through the PD&I navigation.

Run from repository root:
    python3 patches/003_restore_pdi_v48d_engine.py
"""

from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import re

ROOT = Path(__file__).resolve().parent if (Path(__file__).resolve().parent / "src").exists() else Path(__file__).resolve().parents[1]
TARGET = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
ADAPTER = ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx"
PDI_APP = ROOT / "src/pdi/app/PdiApp.tsx"

RAW_URL = "https://raw.githubusercontent.com/boudjadayoucef-sketch/PLAN-SONELGAZ-TG-GUIDE/main/src/components/isometrie/IsometrieModule.tsx"
EXPECTED_GIT_BLOB_SHA = "5a3e514a407c06ad22f18226341c829042b9e7cc"
MARKER = "// PD&I PATCH 003 — V4.8d restored"

if MARKER in PDI_APP.read_text(encoding="utf-8"):
    raise SystemExit("ERROR: Patch 003 appears to be already applied; no files changed.")

TARGET.parent.mkdir(parents=True, exist_ok=True)

# Download authoritative V4.8d source.
request = Request(RAW_URL, headers={"User-Agent": "PD-I-migration-patch/003"})
try:
    with urlopen(request, timeout=30) as response:
        source = response.read().decode("utf-8")
except Exception as exc:
    raise SystemExit(
        "ERROR: impossible de récupérer le moteur V4.8d depuis GitHub. "
        f"Vérifiez l'accès réseau puis relancez le patch. Détail: {exc}"
    )

# Verify the exact Git blob content before installing it.
blob_header = f"blob {len(source.encode('utf-8'))}\0".encode("utf-8")
git_blob_sha = hashlib.sha1(blob_header + source.encode("utf-8")).hexdigest()
if git_blob_sha != EXPECTED_GIT_BLOB_SHA:
    raise SystemExit(
        "ERROR: V4.8d integrity check failed. "
        f"Expected {EXPECTED_GIT_BLOB_SHA}, got {git_blob_sha}. No files changed."
    )

# The original module has only two project-relative imports. Relocate them
# without changing the V4.8d implementation itself.
source = source.replace(
    'from "../../lib/firebase"',
    'from "../../../../lib/firebase"',
)
source = source.replace(
    'from "../../assets/pdiLogos"',
    'from "../../../../assets/pdiLogos"',
)

# Add a migration marker without touching the implementation semantics.
source = "// PD&I PATCH 003 — V4.8d restored\n" + source.lstrip("\n")
TARGET.write_text(source, encoding="utf-8")

adapter = '''// PD&I PATCH 003 — V4.8d adapter
import React from "react";
import IsometrieModuleV48d from "./engine/IsometrieModuleV48d";

/**
 * Compatibility boundary for the complete V4.8d editor.
 * The editor is now owned by PD&I and is no longer imported from the Guide.
 */
export default function PdiIsometricEditor() {
  return <IsometrieModuleV48d />;
}
'''
ADAPTER.write_text(adapter, encoding="utf-8")

# Wire the real editor into the existing SaaS navigation.
pdi = PDI_APP.read_text(encoding="utf-8")

import_anchor = 'import { getDefaultEntitlements } from "../saas/entitlements";'
if import_anchor not in pdi:
    raise SystemExit("ERROR: expected Patch 002 import anchor not found in PdiApp.tsx. No App.tsx changes made.")
pdi = pdi.replace(
    import_anchor,
    import_anchor + '\nimport PdiIsometricEditor from "../isometric/PdiIsometricEditor";\n' + MARKER,
    1,
)

section_anchor = 'function SectionContent({ section }: { section: Section }) {\n'
if section_anchor not in pdi:
    section_anchor = '    function SectionContent({ section }: { section: Section }) {\n'
if section_anchor not in pdi:
    raise SystemExit("ERROR: SectionContent anchor not found. No App.tsx changes made.")
pdi = pdi.replace(
    section_anchor,
    section_anchor + '''  if (section === "isometrics") {
    return (
      <div className="-mx-5 -my-8 md:-mx-8">
        <PdiIsometricEditor />
      </div>
    );
  }

''',
    1,
)

PDI_APP.write_text(pdi, encoding="utf-8")

print("PD&I Patch 003 applied successfully.")
print("Restored authoritative PD&I isometric editor V4.8d.")
print(f"Installed: {TARGET.relative_to(ROOT)}")
print(f"Adapter: {ADAPTER.relative_to(ROOT)}")
print("PdiApp now opens the complete V4.8d editor from the Isométries section.")
print("The Guide App is not imported or executed by this editor boundary.")
print("Next: run npm run build and test Isométries before any SaaS UI changes.")
