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
