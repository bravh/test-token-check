# Kitchen App (Windows, "3D OrdX") + CVJ Engine: development summary

## One-line pitch
A Windows desktop kitchen and cabinet designer (Python/PySide6) that reads and writes Cabinet Vision files. It is powered by a clean-room decompiler/compiler for Cabinet Vision's undocumented binary `.cvj` job format.

## Problem and users
- **Users:** cabinet and kitchen manufacturing in Israel, with a Hebrew UI and real customer jobs.
- **Problem:** Cabinet Vision is the production CAD/CAM system, but its native `.cvj` format is closed.
  - Its XML import format (ORDX) loses data: free-form wall shapes, door-frame margins, CAD notes.
  - The goal was to design kitchens outside Cabinet Vision, including from tablet field measurements, and hand Cabinet Vision complete native job files.

## Tech stack
- **Desktop app:**
  - Python and PySide6 (Qt), with a custom OpenGL 3D viewport plus plan and elevation views;
  - SQLite catalog;
  - packaged with PyInstaller as two exes: a designer and a catalog admin.
- **CVJ engine:**
  - pure Python (olefile), with a CLI and a versioned API;
  - its own OLE2/CFB writer using only the standard library, so it can be ported to Kotlin.
- **Data sources:**
  - SQL Server (the Cabinet Vision CV26 catalog database);
  - ORDX XML;
  - Cabinet Vision UCS scripts (JScript);
  - NC/G-code.
- **AI:** a tool-calling `KitchenDesignAgent`, supporting OpenAI/Azure and Anthropic with provider switching at runtime.
- **Other:**
  - pytest and a custom multi-suite test runner;
  - git worktrees;
  - Node (HTML/JS 3D preview);
  - Blender (light baking for a VR showroom export).

## Architecture
- **Desktop app:**
  - scene/job model;
  - plan, elevation and 3D views;
  - catalog database;
  - ORDX and CVJ importers/exporters;
  - an AI layer on a background thread, which updates the UI only through Qt signals.
- **CVJ engine (separate repo), in layers:**
  - **Layer 1:** an MFC `CArchive` object-stream codec.
  - **Layer 2:** per-class codecs: parameters, equations, Construction/Connection streams, CAD scenes.
  - Unknown data is carried losslessly as raw annotated bytes.
  - On top: a geometry and part tree (joints, bores), JSON/preview export, a round-trip checker, and setup-pack tooling.
- **Build pipeline:** reproducible. The engine is staged into the app bundle at an exact git commit.
- **Shared format library:** reused by the Android measuring app (Kotlin port), the PocketCV Android viewer, and a Quest 3 VR showroom exporter.

## Key features
- **ORDX import/export** with a 3D, plan and elevation editor.
  - Measured shaped walls are triangulated with ear-clipping, which handles concave outlines.
  - Shapes round-trip losslessly back to ORDX.
- **Native `.cvj` export/import (ORDX → CVJ migration):**
  - free-form walls, arcs, the full element library, cabinets and accessories, door-frame margins;
  - construction, material and door-style schedules per project, room or cabinet;
  - customer details and template jobs.
- **CAD generation:** writes Cabinet Vision CAD scenes (lines, arcs, polylines, Hebrew notes, dynamic tokens). The donor-based path works in Cabinet Vision.
- **Catalog admin app** for catalog items and CVJ donors.
- **AI design agent:**
  - adds walls and other elements through tool calls;
  - exact arc-wall geometry;
  - validated inputs.
- **Customer setup-pack normalizer** (`cvjengine make-pack`):
  - grafts a customer's materials, construction and doors onto a template, with clash detection;
  - 37 checks.
- **3D preview of manufacturing detail:** bores, shelf-pin holes, routes and cutouts.
- **Side tools for the Cabinet Vision shop:**
  - an NC/G-code → PNG part-preview generator wired into Cabinet Vision's export scripts;
  - a fixed UCS cabinet-trim script for shaped walls;
  - **PDP Studio:** an editor for Raumplan `.pdp` files with ORDX export, 38 tests.

## Hard technical problems solved
- **Reverse-engineered `.cvj`:** an OLE2 container holding MFC `CArchive` serialized object graphs.
  - Decompile → recompile is byte-identical on 143/143 real jobs.
  - Later validation gates: 170/170, then 182/182.
- **Decoded the proprietary Construction stream:**
  - Validated against the vendor's live SQL Server catalog: 52/52 connections and 101/101 schedules match.
  - Joint and bore geometry now comes from each job's own data.
- **Parser bug class:** byte patterns could mimic object references near index multiples of 256 (worst case: 623 objects lost).
  - Fixed with structural validation predicates.
  - The parser now matches an independent reference walk across 22,564 object positions.
- **Engineering method:**
  - A writer must reproduce real reference bytes exactly before it may change content.
  - Anything unproven is refused rather than guessed.
  - Every formula is checked against stored values.
- **Geometry:**
  - root-caused a mirrored-profile bug in a Cabinet Vision script (unstable sort on a tied key);
  - concave wall extrusion;
  - signed-arc rules.
- **Reproducible builds:**
  - the exe build uses `git archive` at an exact commit and refuses dirty trees;
  - it writes provenance metadata;
  - it handles Hebrew filenames and line-ending byte fidelity.

## Testing
- 800+ automated tests (826 passing at last count).
- A 34-suite engine runner.
- Round-trip gates over a real-file corpus, with fixtures pinned by MD5 hash.
- Negative controls that prove a test can fail.
- Tests report "NOT EXAMINED" instead of silently passing when their oracle (SQL Server or Node) is missing.
- Isolated test environments.

## Timeline (2026)
- **Late Aug:**
  - wall shapes and CAD extraction from ORDX;
  - PDP Studio;
  - CVJ parsing/export;
  - AI arc-wall fix.
- **30 Aug – 1 Oct:** cvj-engine decompiler/compiler and the ORDX → CVJ migration, in parallel.
- **Sep:**
  - Construction stream decoded;
  - build hardening;
  - viewer improvements.
- **Oct:**
  - NC preview exe;
  - customer setup-pack normalizer (19 Oct).

## Status
- In active production use as of Oct 2026, with frequent rebuilds.
- **Open items:**
  - adjustable-shelf hole placement;
  - a few unknown format fields;
  - fully from-scratch CAD generation, which is not yet shown to load in Cabinet Vision.

## Suggested resume bullets
1. Built a Windows kitchen/cabinet design app (Python, PySide6, OpenGL, SQLite) that imports and exports Cabinet Vision ORDX and native `.cvj` jobs, with 3D, plan and elevation editing. Shipped as PyInstaller designer and admin executables.
2. Reverse-engineered Cabinet Vision's undocumented binary `.cvj` format (OLE2 + MFC CArchive object graphs) and built a decompiler/compiler that round-trips 143/143 real jobs with byte-identical output, later 182/182.
3. Decoded proprietary streams (construction schedules, connections, CAD scenes) and validated them against the vendor's live SQL Server catalog (52/52 connections, 101/101 schedules). Manufacturing geometry (bores, joints) is now driven from per-job data.
4. Found and fixed a subtle object-reference collision class in the binary parser using configuration sweeps and structural validation, ending silent data loss.
5. Built a multi-provider (OpenAI/Anthropic) tool-calling AI design agent inside the desktop app, with thread-safe Qt integration.
6. Set up rigorous verification: 800+ automated tests, golden-byte round-trip gates, pinned real-world fixtures, negative controls, and reproducible `git archive`-based builds with provenance metadata.
7. Delivered shop-floor tooling around Cabinet Vision: an NC/G-code part-preview generator, a UCS cabinet-trim script fix, and a Raumplan `.pdp` editor. Also built a shared format library reused by Android and VR showroom apps.
