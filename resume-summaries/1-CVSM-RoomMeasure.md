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
