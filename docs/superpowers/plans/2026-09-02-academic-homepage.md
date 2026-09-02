# Ruijing Xu Academic Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a concise GitHub Pages academic homepage for Ruijing Xu using the approved Jon Barron-inspired layout and Ruijing's supplied materials.

**Architecture:** The site is a dependency-free static page composed of one semantic HTML document, one stylesheet, a portrait, and a downloadable CV. A Python standard-library test validates required content, external links, local assets, accessibility text, and removal of copied personal content.

**Tech Stack:** HTML5, CSS3, Python 3 standard library, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-09-02-academic-homepage-design.md`

## Global Constraints

- Keep the site dependency-free and compatible with GitHub Pages.
- Preserve the reference site's narrow single-page academic layout and circular portrait treatment.
- Do not copy Jon Barron's personal media, publications, CNAME, or metadata.
- Publish no empty or fabricated links.
- Keep `.venv/` untracked.

---

### Task 1: Homepage content and assets

**Files:**
- Create: `.gitignore`
- Create: `tests/test_site.py`
- Create: `index.html`
- Create: `stylesheet.css`
- Create: `images/RuijingXu.jpg`
- Create: `data/RuijingXu-CV.pdf`
- Modify: `_config.yml`

**Interfaces:**
- Consumes: the approved copy in the design spec, `/Users/raexu/Downloads/IMG_0165.jpg`, and `/Users/raexu/Library/Mobile Documents/com~apple~CloudDocs/Downloads/NUS EE Ruijing Xu.pdf`
- Produces: a complete static homepage whose local assets resolve from `index.html`

- [ ] **Step 1: Create the isolated Python environment and failing site contract test**

Create `.venv` with `python3 -m venv .venv`, add `.venv/` to `.gitignore`, and create `tests/test_site.py` with tests that parse `index.html`, require Ruijing's name, approved About and Research themes, Email/GitHub/LinkedIn/CV links, image alt text, and local asset existence. The test must also reject `Jon Barron`, `jonbarron@gmail.com`, and copied project titles.

- [ ] **Step 2: Run the test and confirm the missing homepage fails**

Run: `.venv/bin/python -m unittest tests/test_site.py -v`

Expected: FAIL because `index.html` does not exist.

- [ ] **Step 3: Implement the minimal static homepage**

Create `index.html` with a header containing the user-approved About copy, the supplied portrait, and `Email / CV / GitHub / LinkedIn` links. Add a Research introduction and three concise entries: visuo-tactile manipulation, long-horizon cloth folding, and edge-AI heart-sound diagnosis. Create `stylesheet.css` using the reference layout's typography, 800-pixel content width, link behavior, circular portrait, and a responsive mobile breakpoint. Copy the supplied portrait and CV to their specified local asset paths. Update `_config.yml` with Ruijing's title and research description.

- [ ] **Step 4: Run the site contract test**

Run: `.venv/bin/python -m unittest tests/test_site.py -v`

Expected: all tests PASS.

- [ ] **Step 5: Commit the working homepage**

Run: `git add .gitignore tests/test_site.py index.html stylesheet.css images/RuijingXu.jpg data/RuijingXu-CV.pdf _config.yml && git commit -m "feat: build Ruijing Xu academic homepage"`

---

### Task 2: Attribution, responsive inspection, and release readiness

**Files:**
- Modify: `README.md`
- Modify: `index.html` only if inspection finds a visible or accessibility defect
- Modify: `stylesheet.css` only if inspection finds an overflow, crop, spacing, or legibility defect

**Interfaces:**
- Consumes: the passing homepage from Task 1
- Produces: an attributed, visually checked site ready for GitHub Pages publication

- [ ] **Step 1: Add concise source attribution and maintenance notes**

Update `README.md` to identify the repository as Ruijing Xu's academic homepage, link to `https://github.com/jonbarron/jonbarron.github.io`, acknowledge that the layout is adapted for personal use, and document that content is edited in `index.html` while images and documents live in `images/` and `data/`.

- [ ] **Step 2: Serve and inspect desktop and mobile layouts**

Run: `.venv/bin/python -m http.server 8000 --bind 127.0.0.1`

Inspect `http://127.0.0.1:8000/` at approximately 1440x900 and 390x844. Confirm the portrait crop is natural, links are readable and tappable, the research list has no horizontal overflow, and no content is clipped.

- [ ] **Step 3: Re-run automated verification**

Run: `.venv/bin/python -m unittest tests/test_site.py -v`

Run: `rg -n -i "Jon Barron|jonbarron@gmail.com|JonBarron" --glob '!README.md' --glob '!docs/**' .`

Expected: tests PASS and the prohibited-content search returns no matches.

- [ ] **Step 4: Commit release-ready documentation and visual fixes**

Run: `git add README.md index.html stylesheet.css && git commit -m "docs: attribute homepage layout and finalize presentation"`

- [ ] **Step 5: Push and verify GitHub Pages**

Run: `git push origin main`, then open `https://ruijingxu.github.io/` and confirm the deployed title, portrait, links, CV download, and responsive presentation match the local site.

