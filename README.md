# Bencat Digital Newsletter JAS'26 – source package

Interactive HTML newsletter for LT (razor cursor, "slice" buttons, click-to-enlarge photos).
One Python script builds a **single self-contained HTML file** with all photos embedded.

## Folder structure
```
build_newsletter.py      <- all text, numbers, layout (edit here)
extract_from_pptx.py     <- pulls photos out of the PPTX into images/
assets/style.css         <- animations, razor cursor, buttons
assets/script.js         <- slice/open logic, lightbox, slash effect
images/                  <- one file per photo slot (jpg/png)
Bencat_Digital_Newsletter_JAS26.html  <- built output (send this)
```

## Quick start (Python 3 + `pip install pillow python-pptx`)
```
python extract_from_pptx.py "Digital Newsletter JAS'26.pptx"   # fill images/ from slides (only empty slots)
python build_newsletter.py                                      # build the HTML
```
The build prints the list of **missing photos**; those show as dashed placeholders.

## Adding / replacing a photo
Drop a file into `images/` named exactly as the slot key (`.jpg`, `.png` or `.webp`), then rebuild.
Files you put there manually are never overwritten by the extractor (unless `--force`).
New photo in the PPTX? Run the extractor, find it in `images/_raw/sXX_YY.png`, add it to `MAP` in `extract_from_pptx.py`.

| Section | Slot keys |
|---|---|
| Team (slide 2) | ky, minh, xuan, nghi, luan, thuc, angarish, dom, quyen |
| Mắt Thần | matthan_logo, matthan_chat, gsmc_recognition, berlin_walkthrough |
| eDDS for GPO | utility_edds, rccp_whedds |
| BCSSE Soft-service | softservice_chat |
| WISE / VAC / TD | wise_usecases, vac_rtd, td_optimization |
| Quality Alert / PE Base | qa_alert_chat, pebase_timeline |
| Simplify apps | benvoice, benvoice2, mover_apps, mover2, bos_logo, bos_revamp |
| Secure / Anti-fragile | cyber_foundation, cyber_month, prime_alics, octoplant |
| Skills & Benchmark | bootcamp_s2_poster, fy2627_emerging_capability, benchmark_vnps |
| Org Corner | ky_announcement, wages_dashboard, rr_photo, happy_hours |

## Editing content
Open `build_newsletter.py` and search for the section markers:
`# ===== 1. EXEC SUMMARY`, `# ===== 2. 5 IMPACTS`, `# ===== 3. KEY DELIVERABLES`,
`# ===== 4. EMERGING SKILLS`, `# ===== 5. ORG CORNER`, `# ===== 6. WHAT'S NEXT`, `# ===== 7. ONE WINNING DIGITAL TEAM`.
- Landed / Moving lists: `LANDED`, `MOVING`. KPI numbers: `kpi(...)` and `tile(...)` calls.
- Control Tower glidepath: `CT_ROWS` (a cell containing `&#10004;` turns green = live).
- Mắt Thần: `SUPERPOWERS`, `VALIDATION`.
- Yellow "to fill" tags: search for `tbc(`.
- Colors: `# ===== PALETTE`.

## Sending
Interactivity needs a browser. Outlook strips scripts from an email body, so share the HTML
as an **attachment or SharePoint/OneDrive link** with a short teaser in the email.

## Change log
- v5: Exec summary $200M confirmed; Landed/Moving/Watch as slice-to-open tiles; Need attention = 1 (PI/SPS only);
  PE Base moved to Landed; team section moved to bottom (collapsible org chart); 5 Impacts = Foundation left + 2x2 right;
  Cyber DMS healthcheck 100% (+2% IYA); Utility eDDS LIVE (~1 hr/day saved); BCSSE poster, Mắt Thần chat & logo added;
  razor cursor + slash effect + lightbox.
- v6: Shaving effects - every click drops falling hair clippings + foam puff; opening a panel or photo triggers a razor sweep
  (assets/script.js: dropHair / foam / sweep). Scissor icons replaced by razor icon (RAZOR_ICON). All slide photos filled from
  the PPTX (team avatars, GSMC, Berlin, slip ring, WISE, PE Base, apps, cyber, skills, benchmark, Ky announcement now slide 20).
  QA eDDS photo panel removed; WH eDDS + RCCP shown full width.
- Still missing (no photo in PPTX yet): qa_alert_chat, octoplant, wages_dashboard, rr_photo, happy_hours.
- Open items: Landed count (tile says 5, list has 7); results for Quality Alert, BCSSE, PE Base.
