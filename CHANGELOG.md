# Changelog
All notable changes to this project are documented here. This file follows a simplified
["Keep a Changelog"](https://keepachangelog.com/en/1.1.0/) style with Semantic Versioning.

## [Unreleased]
- (planned) CI workflow to validate JSON schema and lint
- (planned) CLI flags for rate limiting and user-agent override


### Changed
- Updated repo bundle and notes to reflect the removal.
- Removed the images-only download buttons from the index and list views; documentation now points to the helper script/API instead.

## [0.3.1] - 2025-09-16

Conversation-driven, incremental commits that reflect our UI work on the reddit-image-scrapper. Each commit includes files and intent.

1. feat(list/grid): render images in responsive cards
   - files: `templates/list.html`
   - purpose: Match the index page's masonry-like grid so the list view feels consistent.
   - notes: Introduced `.grid`, `.card`, `.imgwrap`, `.content`, `.title` styles and rewired the loop to output `<article.card>`.

2. feat(list/filter): add filter input similar to index
   - files: `templates/list.html`
   - purpose: Quickly narrow visible items when browsing many results.
   - notes: Full-width search bar added under header actions; JS hides non-matching cards by title.

3. style(index): unify header actions + tidy spacing
   - files: `templates/index.html`
   - purpose: Make the top section cleaner with a subtle "List View"/"Download JSON" action area.
   - notes: Light button styling, softened shadows, consistent container padding.

4. fix(encoding): replace odd placeholder and separators
   - files: `templates/index.html`, `templates/list.html`
   - purpose: Some environments showed replacement characters. Ensure clean text.
   - how to reproduce: Open the grid or list view on Windows/Edge and observe "A" characters around score/comments, or the search placeholder showing "author?".
   - resolution: Normalized placeholders to HTML entities (`&hellip;`, `&middot;`, `&#9650;`) and added a defensive JS normalizer for existing DOM text.
   - manual fix guidance: If custom templates still show the artifact, ensure the file encoding is UTF-8 and replace the characters with the entities above. Reload the page (Ctrl+F5) after edits to flush cached HTML.

5. chore(changelog): expand narrative to mirror conversation
   - files: `CHANGELOG.md`
   - purpose: Make the development trail explicit for reviewers.

## [0.3.2] - 2025-09-16

1. docs(readme): beginner-proof setup and shutdown guide
   - files: `README.md`
   - intent: Provide zero-experience users with copy-paste commands, explain what to expect in Command Prompt, and document required folder structure.
   - highlights:
     - Added explicit notes about copying commands, verifying Python installation, and keeping core files (`display.py`, `templates/`, `output/`, etc.) together.
     - Expanded Windows instructions with deactivate steps and output verification.
     - Added housekeeping tips (API check, cleaning `output/`, backups) and an FAQ covering common questions (Reddit account, storage location, large page counts, empty results).

2. chore(changelog): document README enhancements
   - files: `CHANGELOG.md`
   - intent: Capture documentation work so future contributors see the guidance improvements and underlying rationale.

## [0.3.0] - 2025-09-16

Human-friendly commit log documenting the UI improvements and their intent. Each commit lists the concrete files touched and the reasoning.

1. feat(ui/index): polish header and cards for friendlier look
   - files: `templates/index.html`
   - why: Make the landing grid feel modern and clean without adding dependencies.
   - changes:
     - Added subtle shadows and hover-lift on `.card` for depth.
     - Tightened container padding and consistent `max-width`.
     - Styled the header link as a button for better affordance.
     - Normalized search placeholder to "Filter visible cards by title or author...".
     - Added a small runtime sanitation to replace stray encoding artifacts in the metadata line.

2. chore(ui/list): header/title/back-link normalization
   - files: `templates/list.html`
   - why: The page title and back label showed replacement characters in some environments.
   - changes:
     - Script sets document title to `Images - <filename>` using a safe en dash.
     - Back link label normalized to "← Back to grid".

3. feat(list): add filter bar like index page
   - files: `templates/list.html`
   - why: Enable quick client-side filtering when browsing many images.
   - changes:
     - Added full-width search input with rounded corners under the header.
     - Implemented client-side filter that hides items whose title does not match the query.

4. refactor(list): render images in the same card grid as index
   - files: `templates/list.html`
   - why: Provide visual consistency between the list view and the landing page.
   - changes:
     - Introduced `.grid`, `.card`, `.imgwrap`, `.content`, and `.title` styles mirroring index.
     - Switched markup to an `<article.card>` per item with fixed aspect-ratio image area.
     - Image opens in a new tab for quick inspection.
     - Updated filter logic to target `.card` elements via `data-title`.

5. style(list): minor spacing and shadow alignment
   - files: `templates/list.html`
   - why: Match index spacing and achieve a cohesive feel.
   - changes:
     - Unified gaps/margins and added a light shadow to images for depth.

## [0.2.1] - 2025-09-15

Incremental backend/UI commits based on early feedback while wiring the viewer.

1. feat(api): images-only JSON download endpoint
   - files: `display.py`, `filter_images.py`
   - purpose: One-click export of images-only data from latest or chosen file via `/download-images-json`.
   - notes: Reused `filter_images.filter_posts`; added safe fallbacks and proper error handling.

2. feat(view): background scraping trigger + clamped pages
   - files: `display.py`
   - purpose: Start scraping from the browser without blocking the server; avoid huge requests.
   - notes: Start a daemon thread, clamp pages to 1-50, and handle both `scrape(pages)` and `scrape(num_pages=pages)` signatures.
   - manual fix guidance: If you forked `RedditScraper` and renamed the argument, update the `run_job()` call accordingly or keep the dual-call pattern to avoid `TypeError: scrape() got an unexpected keyword`.

3. refactor(view): normalize loaded posts
   - files: `display.py`
   - purpose: Ensure all templates have a `title` even if the JSON uses `post_title`.
   - notes: Added `_normalize_posts()` and `latest_json_path()` helpers.

4. fix(structure): relocate app scripts from `src/` to project root
   - files: `display.py`, `scraper.py`, `filter_images.py`
   - why: Running `python display.py` from the repository root failed because the modules lived under `src/`, breaking imports (`ModuleNotFoundError: No module named 'scraper'`).
   - resolved: Moved the three scripts to the top-level `reddit-image-scrapper/` folder, updated references, and verified that Flask auto-reload and CLI execution work without tweaking `PYTHONPATH`.
   - tip: If you keep a `src/` layout, either add it to `PYTHONPATH` or convert the directory into a package (`__init__.py`) and update imports accordingly.

## [0.1.0] - 2025-09-14
### Added
- **Repository scaffold**
  - Project layout with `src/`, `templates/`, `output/`.
  - `.gitignore`, `requirements.txt`, `LICENSE`, and this `CHANGELOG.md`.
  - Sample data at `output/sample_output.json` so reviewers can test without scraping.

## [0.2.0] - 2025-09-15
- **Scraper (`src/scraper.py`)**
  - Fetch posts from a chosen subreddit.
  - Pagination support across multiple pages.
  - Persist results as JSON (including fields like title, image URL, and post URL when available).
- **Filter (`src/filter_images.py`)**
  - Reduce any scraped JSON to an images-only list: `(title, image_url)`.
  - Basic duplicate elimination.
- **Viewer (`src/display.py`)**
  - Flask app to inspect results locally:
    - `/` - show latest file (with images if present).
    - `/list` - images-only view for a selected or latest file.
    - `/api/posts` - serve JSON for quick programmatic checks.
    - `/download-images-json` - export images-only JSON from the latest or chosen file.
    - `/scrape` - trigger a background scrape from the browser form.
  - Minimal HTML templates: `templates/index.html`, `templates/list.html`.
- **Docs & publishing helpers**
  - README instructions to install, run, and understand the repo.
  - A push command guide with meaningful, incremental commits.

### Development narrative (step-by-step)
1. **Initialize & hygiene** - Created `.gitignore`, pinned dependencies in `requirements.txt`, drafted README goals.
2. **Core scraper** - Implemented a paginator and extracted post records into JSON.
3. **Image focus** - Wrote `filter_images.py` to keep only `(title, image_url)` and to remove duplicates.
4. **Display layer** - Built a tiny Flask app with `index` and `list` pages plus an API and one-click JSON export.
5. **Demonstration data** - Added `output/sample_output.json` to enable immediate review without network calls.
6. **Licensing & logs** - Added MIT license and began this changelog.
7. **Repository prep** - Wrote a sequence of meaningful commits and instructions for pushing to GitHub.
