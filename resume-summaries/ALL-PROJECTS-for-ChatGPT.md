# Prompt for ChatGPT

You are a professional resume writer. Below are development summaries of 4 software projects I built (2025–2026), mostly for the kitchen / cabinet manufacturing industry around the Cabinet Vision CAD/CAM software. Using them, write a strong one-page technical resume (plus an optional 2-page version): a short professional summary, a skills section grouped by area (languages, mobile, desktop, data/formats, integrations, tooling, AI-assisted development), and a "Projects / Experience" section with 3–5 achievement bullets per project. Use action verbs and keep the measurable results (test counts, byte-identical round-trips, file sizes, etc.). Don't invent facts not in the summaries.

---

# CVSM / RoomMeasure (Android measuring app): development summary

## Name and pitch
- **Name:** CVSM, also called RoomMeasure (package `com.roommeasure.app`).
- **Pitch:** a Hebrew-first Android tablet and phone app for measuring rooms, walls and openings on site with Bluetooth laser meters. It exports jobs straight into **Cabinet Vision**, the cabinetry CAD/CAM software.
- **Family of apps:**
  - a spin-off door-measuring app, **DoorMeasure**;
  - a companion licence admin app, **CVSM Licenses**.
- **Brand:** Elsop.

## Problem and users
- **Users:** kitchen and cabinet workshops, and door/carpentry contractors in Israel. Their field measurers capture room geometry on site.
- **Problem it solves:** manual measuring, then re-entering the data into Excel and Cabinet Vision.

## Tech stack
- **Android:**
  - Kotlin, Jetpack Compose, Room (SQLite) with migrations, DataStore, Gradle;
  - signed release APKs;
  - right-to-left Hebrew UI, plus English, Russian and Arabic.
- **Hardware:** Leica DISTO X6 / Disto and Bosch GLM 50 C laser meters over Bluetooth.
- **Tooling:**
  - Python `cvj-engine` (a Cabinet Vision file library and CLI);
  - a Python licence tool;
  - an ORDX validator;
  - adb for device QA.
- **Services:**
  - GitHub REST API, used for in-app auto-update from GitHub Releases;
  - a private GitHub repo used as a licence store;
  - SQL Server (the Cabinet Vision CV26 database, examined for a planned catalog sync).

## Architecture
- **RoomMeasure data model:** Project → Room → Walls → elements (doors, windows, cabinets, appliances).
- **Views:** plan, wall elevation, 3D preview, CAD-on-wall layer.
- **Export:**
  - PDF, ZIP and ORDX (Cabinet Vision's XML).
  - Native Cabinet Vision `.cvj`, through Kotlin readers and writers for OLE Compound File containers.
  - The `.cvj` jobs are built from a donor template.
  - Per-project setup templates.
- **DoorMeasure data model:** Project → Floor → Room → DoorOpening (about 45 attributes each), with a status lifecycle and a pricing engine tested against real Excel rows.
- **Licensing (no server):**
  - JSON licence files in a private GitHub repo, written with SHA optimistic locking;
  - bound to the device;
  - a separate entitlement per product (RoomMeasure, PocketCV).
- **Distribution:** an in-app updater installs signed APKs from GitHub Releases over the existing app and keeps user data.
- **Process:** AI-assisted development with Claude Code run as a multi-agent team (app-dev, domain-catalog, cv-bridge, qa-field and designer roles), with spec docs and a mission board.

## Key features
- **Laser measuring with Leica X6 and Bosch:**
  - wall lengths by horizontal projection;
  - exact T-join intersections;
  - elements stay anchored when walls change.
- **Quick Measure:** element size and position from 4 shots.
- **Quick 3D scan:** guided step by step, with Hebrew voice prompts.
- **Laser Contour:** measured points projected onto the wall plane.
- **Floor-datum calibration:** with plausibility checks.
- **Off-plane deviation warnings.**
- **Shaped walls:** vault, cathedral and peninsula silhouettes, exported to Cabinet Vision as shaped walls.
- **3D preview:** miters, real opening cuts and shading, at 60 fps on a tablet.
- **PDF reports:** title blocks, scales, collision-free dimensions and door-swing symbols.
- **Units:** mm/cm and other units, applied across the whole app.
- **CV26 catalog sync:** door, appliance and material names match Cabinet Vision exactly.
- **Per-customer Cabinet Vision setup templates (v5.18.74):** construction methods, materials, drawers and hinges travel into exported jobs. Verified end to end in Cabinet Vision.
- **Direct import of raw Cabinet Vision `.cvj` files (v5.18.75):** converted to setup packs on the device.
- **DoorMeasure:**
  - an 8-step guided door-measuring flow;
  - plan pins per floor;
  - job import/export;
  - XLSX door schedule, bill of quantities and a Hebrew quote PDF;
  - pilot on a hospital door schedule.
- **CVSM Licenses admin app:**
  - create, edit, revoke and approve licences;
  - PIN gate;
  - one-tap 14-day trial licences;
  - multi-product.

## Hard technical problems solved
- **Reverse-engineered Cabinet Vision's binary `.cvj` format and ported the Python engine to Kotlin.**
  - Byte-identical round-trips on 328 real files.
  - The parameter reader was checked against 53 real files (about 5,600 parameters), with zero mismatches.
  - 310 golden and unit tests.
- **Laser geometry:**
  - Found that a global snap lock was silently collapsing heights, and removed it from the laser path.
  - The back-face offset was derived algebraically and unit-tested.
  - Calibration rejects physically impossible floor shots.
- **Release safety:** signing certificates are checked before every update, so user data is never wiped.
- **Build environment:** worked around OneDrive and Hebrew-path Gradle problems.

## Timeline
- **Before Aug 2026:** RoomMeasure already at v4.9 (laser support, ORDX/PDF export, licensing, auto-update).
- **Aug 2026:**
  - DoorMeasure planned and prototyped.
  - v5.0.1 released (Leica X6 fix, quick scan, vaulted walls, 3D/PDF upgrades).
  - Licence admin app built.
- **Late Aug – Sep:**
  - v5.14 – v5.16: units, laser contour, floor datum.
  - Per-product licensing.
- **19 Oct 2026:** v5.18.74 / v5.18.75 released: Cabinet Vision setup templates and raw `.cvj` import.

## Status
- RoomMeasure is in production use on customer devices through the in-app updater. Latest release: v5.18.75.
- DoorMeasure is in development or a field pilot.

## Suggested resume bullets
1. Built and shipped **CVSM/RoomMeasure**, a Kotlin/Jetpack Compose Android app for on-site room measuring. It pairs with Bluetooth laser meters (Leica DISTO X6, Bosch GLM 50 C) and exports production-ready jobs to Cabinet Vision (ORDX and native CVJ). It is distributed to customer tablets through a GitHub-Releases auto-updater.
2. Reverse-engineered Cabinet Vision's binary OLE/CFB `.cvj` job format and ported a Python engine to Kotlin, with byte-identical round-trips on 328 real files and 310 automated tests. This lets customers import their own Cabinet Vision setup files on the device.
3. Designed the laser-measurement geometry: horizontal-projection wall math, T-join anchoring, floor-datum calibration with plausibility checks, and wall-plane projection with deviation warnings. This removed silent height errors found in field testing.
4. Developed a serverless licensing system (GitHub as the store, optimistic locking, device binding, per-product entitlements) and a companion Android admin app with PIN protection and one-tap trials.
5. Led a spin-off door-schedule app for a hospital construction project. Turned a ~45-attribute Excel workflow into a structured domain model with a pricing engine and XLSX/BOM/PDF quote exports.
6. Ran AI-assisted, multi-agent development with Claude Code (specialized agents, spec-driven work, on-device adb QA) and owned release engineering (signing checks, data-preserving upgrades).


---

# PocketCV (Android): development summary

## One-line pitch
An Android app that opens Cabinet Vision (Hexagon) kitchen and furniture job files (`.cvj`) on tablets and phones, with no PC and no Cabinet Vision licence. It shows 3D rooms and cabinets, drawings, reports, cut lists and per-cabinet sheets.

## Problem and users
- **Problem:** Cabinet Vision jobs can normally only be viewed on a licensed Windows PC.
- **Users:** kitchen and furniture manufacturers:
  - installers on site;
  - workshop staff;
  - salespeople in front of customers.
- **Distribution:** sold with licences by Elsop (Israel).

## Tech stack
- **Android host:** Kotlin, Android 7+ (minSdk 24). The UI runs in a WebView loaded through WebViewAssetLoader, with JS bridges.
- **Front end:**
  - three.js r128 for 3D;
  - plain JavaScript (ES2019);
  - a custom SVG drawing renderer;
  - CSS design tokens with light and dark themes.
- **Decoder:** Python (cvj-engine, a separately versioned repo). It runs on the device through Chaquopy (CPython 3.12, and 3.11 for 32-bit builds) and reads OLE compound files with olefile.
- **Networking:**
  - jcifs-ng (SMB2/3);
  - WS-Discovery plus a subnet scan;
  - NetBIOS name lookup.
- **Security:**
  - EncryptedSharedPreferences (AES-256);
  - a device-bound licence checked against a GitHub-hosted store;
  - PBKDF2-HMAC-SHA256 written by hand for Android 7, unit-tested with JUnit against RFC 7914 and the JCE.
- **Build:** Gradle Kotlin DSL. The engine is pinned to a git commit per build, with build-time patch hooks.
- **Tooling:** a Python CSS converter for old WebViews; adb testing on real tablets.

## Architecture
- **On-device pipeline:** `.cvj` → Python engine (via Chaquopy) → scene JSON → JS renderers for the 3D scene, 2D drawings and reports.
- **Offline first:** the network is used only for SMB file shares and the licence check.
- **App/engine contract:** the engine owns the file format and the app owns presentation. App-side fixes to the engine are applied as checked text patches at build time, and the build fails if a patch no longer fits.

## Key features
- **3D viewer:** touch orbit, selection, isolate, hide, X-ray, edges, machining overlays, and an object tree (room / wall / cabinet / part).
- **Per-cabinet dialog:**
  - overview, including the cabinet number;
  - 3D, fronts, parts, drilling, hardware;
  - a sheet with front, side, top and iso views, plus Cabinet Vision's own sheets;
  - print and PDF.
- **Drawings:** Cabinet Vision's own printed pages, generated wall elevations and a plan with CAD overlays, filters, SVG export and printing.
- **Reports:** Cabinet Vision's report designs (cut lists, door lists, hardware lists) run on the device.
- **Projects browser for office PC shares (SMB):** finds PCs on the network, supports guest, anonymous or signed-in access, and shows download progress.
- **Offline use:** "Save to tablet" keeps jobs and their textures on the device.
- **Opening from other apps:** Open with / Share from WhatsApp, Gmail and file managers, with file-type detection from content.
- **Languages:** English, Hebrew, Russian and Arabic, with right-to-left layout.
- **Old devices:** 32-bit builds, Android 7, and fallbacks for 2018-era WebViews.

## Hard technical problems solved
- **Undocumented `.cvj` format:** reverse-engineered nested part trees and older-version record types. This fixed drawers drawn 500 mm out of place; rendered parts went from 688 to 1,034.
- **Conditional quantities:** reads Cabinet Vision's formula flags so the parts Cabinet Vision doesn't build are hidden, as in Cabinet Vision itself.
- **Isometric drawings:** correct hidden-surface ordering (separating-axis per box pair), with shaded faces.
- **SMB on Android:**
  - Windows PC names that don't resolve on Android: the app dials a checked IPv4 address instead, found through NetBIOS, DNS or a cache.
  - Domain controllers refused guest logins; replaced with a true anonymous session.
  - Signing on the share-list channel blocked guest listings; fixed.
  - Downloads read 1 MB per SMB request instead of 64 KB.
- **2018 WebView (Chrome 71):** an automated stylesheet rewrite for old browsers that leaves modern devices unchanged, verified on a real Xiaomi tablet.
- **PBKDF2 on Android 7:** a hand-written implementation, verified against RFC 7914 and the JCE.

## Timeline and status
- **Timeline:**
  - Late Aug 2026: decoder (CVJ engine) work.
  - 22 Sep 2026: the app build starts.
  - Mid-Oct 2026: languages, cabinet numbers and old-device support added.
- **Status:** in active use. Distributed to customers as signed APKs (not on Google Play), and development continues.
- **Measured results:** decodes full kitchen jobs of 4 to 113 MB on the device. Engine changes are regression-checked so earlier jobs decode byte-identically.

## Suggested resume bullets
1. Built **PocketCV**, an Android app (Kotlin, WebView, three.js) that lets kitchen and furniture manufacturers open Cabinet Vision `.cvj` jobs on tablets without a PC or Cabinet Vision licence. It shows 3D models, shop drawings, cut lists and reports, and is distributed to customers under licence.
2. Embedded a Python decoder on Android through **Chaquopy**, in an offline pipeline (`.cvj` → scene JSON → 3D, SVG and report renderers). It handles 4–113 MB jobs on the device, with byte-identical regression checks.
3. Reverse-engineered parts of the undocumented `.cvj` (OLE) format, including nested part trees and conditional-quantity formulas. Rendered parts went from 688 to 1,034, and misplaced drawers were fixed.
4. Built an SMB2/3 network browser for office file shares (jcifs-ng, WS-Discovery, NetBIOS). It handles Android name-resolution failures and anonymous access to domain controllers, and reads 1 MB per request for faster downloads.
5. Built device-bound licensing (EncryptedSharedPreferences, a GitHub-hosted licence store, PBKDF2 verified against RFC 7914) and a Gradle KTS build that pins the engine per commit with build-time patch checks.
6. Localized the interface into 4 languages, including right-to-left Hebrew and Arabic. Added support for old hardware (32-bit, Android 7, 2018 WebViews) through an automated CSS-compatibility rewrite.


---

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


---

# Cabinet Pricer (Pricing for Cabinet Vision / CV26) + related tools: development summary

## One-line pitch
A Windows desktop system that reads a Cabinet Vision project straight from its SQL Server database and prices every item from the shop's own price book: cabinets, doors, drawers, hardware and accessories. It produces a signed, room-by-room Excel quote and can push the job to an ERP.

## Problem and users
- **Users:** kitchen and cabinet manufacturers who design in Cabinet Vision.
- **Problem:** quoting meant re-typing each cabinet's dimensions by hand.
- **Product:** Hebrew UI. Sold under per-team licences by Elsop / CV Advance (cvadvance.net).

## Tech stack
- **Core:**
  - Python;
  - SQL Server via `pyodbc`;
  - Excel via `openpyxl`;
  - XML/JSON price books.
- **Packaging:**
  - PyInstaller executables;
  - Inno Setup installer;
  - custom CPU-bound licensing with a licence generator.
- **ERP:**
  - Odoo (XML-RPC);
  - Monday.com;
  - a generic REST connector;
  - FastAPI mock ERP servers for testing.
- **Later tools:**
  - Qt (CVForge);
  - Priority OData API;
  - SQLite.
- **Website:** Astro on a Wix headless CMS.

## Architecture
1. **Main pricing engine:** UI, Excel exporter, discounts, totals, filters, universal ERP manager.
2. **Catalog / price administrator:** tabs for cabinets, doors, drawers, hardware, accessories and materials.
3. **Quote archive app:** search, open and print past quotes.
4. **Launcher** tying the apps together. On the website they are presented as one 4-stage system.

## Key features
- **Tiered pricing engine:**
  - Cabinets are priced per linear metre of width, with the rate tier chosen by height and depth.
  - Non-standard sizes are detected automatically.
  - Special cabinets get a fixed or per-unit price.
  - Doors are priced per square metre by finish.
  - Drawers are priced by brand and runner.
  - Hardware is priced by length or by unit.
- **Quotes:**
  - per room, in 5 categories, each with a subtotal;
  - line and grand-total discounts, VAT, a signature line;
  - one-click Excel export.
- **Price-book sync:** pulls new door styles, materials and drawer guides from each job. New items are added and existing prices are never overwritten.
- **Universal ERP bridge:**
  - 11 preconfigured ERP profiles, including SAP and Priority;
  - 7+ authentication types (OAuth2, Bearer, API key, SAP/Priority sessions);
  - connection testing;
  - creates customers, leads and jobs.
  - Live with a customer on Odoo and Monday.

## Hard problems solved
- Square-metre pricing for special cabinets.
- Fixes to the width-calculation pipeline.
- Unit vs. length hardware pricing.
- Tax and discounts reaching the ERP correctly.
- Hebrew right-to-left ERP dialogs.
- Licence enforcement inside the compiled exe.
- Dozens of test scripts (discounts, metre pricing, live Odoo integration).

## Related Cabinet Vision (CV26) tools
- **CVForge (Jul 2026):** a Python/Qt CV26 report and quotation designer.
  - Shares the same price books as Cabinet Pricer.
  - SQL-query reports against Cabinet Vision's report database.
  - Column mapping, group subtotals, a safe formula language with autocomplete, Excel and ERP send targets.
  - 24 test suites.
- **CV26 → Priority ERP bridge (Oct 2026):**
  - Python CLI plus a 6-tab manager GUI.
  - Builds the bill of materials from Cabinet Vision data and sends it over the Priority OData API.
  - Material → SKU mapping with unit conversion, a SQLite transfer log, dry-run mode.
  - 119 unit tests.
  - Waiting on the client's credentials before going live.
- **Job-Exporter.exe (Aug–Sep 2026):**
  - Exports CNC/nesting jobs to Excel with custom columns and NC labels.
  - Fixed the part-rotation dimension logic: the old rule was wrong on 42/42 lines; the new rule matches 28/28, checked against machine toolpaths.

## Timeline
- **Jun–Aug 2025:**
  - core pricing engine;
  - ERP (Odoo/Monday);
  - discounts and Excel export;
  - licensing.
- **Jan 2026:** installer and updates.
- **Jul 2026:** CVForge.
- **Aug 2026:**
  - product page live on cvadvance.net;
  - Job-Exporter.
- **Oct 2026:** Priority ERP bridge.

## Status
- Shipped as compiled exes.
- At least one customer runs it live with Odoo/Monday.
- The product page is published.

## Suggested resume bullets
1. Designed and built **Cabinet Pricer**, a Python/Windows quoting system for cabinet manufacturers. It reads Cabinet Vision projects directly from SQL Server and produces room-by-room Excel quotes with discounts, VAT and a signature line, with no manual re-entry.
2. Built a tiered pricing engine:
   - per-linear-metre rates by width, height and depth tiers, with automatic non-standard size detection;
   - square-metre door pricing and separate drawer, hardware and accessory pricing;
   - a price administrator that syncs new catalog items without overwriting prices.
3. Built a configurable ERP integration layer: 11 ERP profiles and 7+ authentication schemes (OAuth2, Bearer, SAP/Priority sessions). Live Odoo (XML-RPC) and Monday.com integrations, tested against FastAPI mock servers.
4. Shipped the product as PyInstaller executables with an Inno Setup installer and a CPU-bound licence system.
5. Extended the product line:
   - a CV26 → Priority ERP bridge (OData BOM transfer, material-to-SKU mapping, dry runs, 119 unit tests);
   - CVForge, a Qt report and quotation designer with a safe formula language.
6. Launched the product's bilingual (Hebrew/English) marketing page on Astro + Wix headless CMS, checking every published claim against the source code.


---

