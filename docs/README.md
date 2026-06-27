# VK Newsletter Bot for Essential Oils

This repository contains a Python script that automates weekly posts to a VKontakte community (or personal wall) about essential oils, alternating between informational and sales-oriented posts to attract leads.

## Project Structure
- `src/` – Python script for generating and publishing posts.
- `data/` – Templates, weekly topics, sources, and posting schedule.
- `logs/` – Log files for each publication attempt.
- `docs/` – Documentation (this file).

## Setup
1. Create a VK standalone app and obtain a `service_token` or `user_token` with `wall`, `groups` permissions.
2. Add the token to `.env`:
   ```
   VK_TOKEN=your_token_here
   GROUP_ID=your_group_id_or_wall_id
   ```
3. Install Python dependencies (if any):
   ```bash
   pip install requests python-dotenv gspread oauth2client   # optional for Google Sheets
   ```
4. Populate `data/sources.md` with recent research links (see `fetch_sources.py` helper if desired).
5. Set the initial topic in `data/weekly_topic.txt` or let the script pick one from sources.
6. Define your posting schedule in `data/schedule.md` (see example).
7. Run the script manually to test:
   ```bash
   python src/post_to_vk.py
   ```
8. Schedule regular runs (e.g., weekly) via cron or Claude's `/loop` command.

## Posting Schedule (example)
- **Week 1 (odd weeks):** Informational post – scientific facts, usage tips.
- **Week 2 (even weeks):** Sales post – product highlight, limited‑time offer, call‑to‑action.
Adjust `data/schedule.md` as needed.

## Logging
Each run creates a log file in `logs/vk_post_YYYY-MM-DD.log` with the request payload and VK API response.

## Extending to Google Sheets
The script includes a placeholder function `update_gsheet()` that can append a row with date, topic, post type, and VK post URL. Fill in your Google Sheets credentials and spreadsheet ID to enable.

## License
Personal use – feel free to adapt.