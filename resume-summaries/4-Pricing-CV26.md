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
