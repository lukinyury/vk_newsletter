# VK Newsletter Automation

Automated weekly newsletter publishing for essential oils in VKontakte (VK) using Claude Code for content generation and VK API for publishing.

## Overview

This project automates the creation and publishing of weekly posts about essential oils to a VK community or personal wall. It leverages Claude Code (via the `/agent` commands) for researching recent scientific articles, generating post drafts, and optionally publishing them on a schedule via Windows Task Scheduler or cron (WSL).

## Features

- **Research automation**: Use the `explore` agent to fetch recent PubMed articles on essential oils.
- **Content generation**: Use the `general-purpose` agent to draft posts based on collected sources.
- **Verification**: Optionally review generated content with the `verify` agent.
- **Scheduled publishing**: Set up weekly automation via Task Scheduler (Windows) or cron (WSL).
- **Easy configuration**: Store VK token and group ID in `.env`.
- **Extensible**: Adapt templates, add new content formats (video previews, carousels), integrate with Google Sheets or email newsletters.

## Project Structure

```
vk_newsletter/
├─ src/
│   └─ post_to_vk.py          # Main script: generates and publishes posts
├─ data/
│   └─ sources.md             # List of scientific sources (DOIs, annotations)
├─ docs/                      # Additional documentation (optional)
├─ .env                       # Environment variables (VK_TOKEN, GROUP_ID) – **not committed**
├─ .env.example               # Template for environment variables
├─ requirements.txt           # Python dependencies (requests, python-dotenv)
└─ README.md                  # This file
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/lukinyury/vk_newsletter.git
cd vk_newsletter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example environment file and fill in your VK credentials:

```bash
cp .env.example .env
# Edit .env and add your values:
# VK_TOKEN=your_vk_service_token_with_wall_post_permission
# GROUP_ID=your_group_id_without_minus_sign
```

> **Note**: Keep `.env` private and never commit it to the repository.

### 4. (Optional) Prepare sources

Edit `data/sources.md` with a list of recent research articles you want to reference. You can also use the provided research agent to update this file weekly.

### 5. Test the script

Run the script in test mode (comment out the actual VK API call or use your own user ID) to see the generated post:

```bash
python src/post_to_vk.py
```

Check the console output; the generated post will be printed. Verify the content, links, and hashtags.

### 6. Schedule automatic publishing

#### Windows Task Scheduler

1. Open **Task Scheduler**.
2. Create a basic task:
   - Trigger: Weekly, choose day and time.
   - Action: Start a program.
   - Program: `python`
   - Arguments: `C:\full\path\to\vk_newsletter\src\post_to_vk.py`
   - Start in: `C:\full\path\to\vk_newsletter`
3. Ensure the environment variables are accessible (you can create a batch file that sets them before calling Python).

#### WSL + cron

1. Edit your crontab (`crontab -e`).
2. Add a line (example: every Monday at 10:00 AM):

   ```
   0 10 * * 1 /usr/bin/python3 /mnt/c/Users/Юрий/finance/vk_newsletter/src/post_to_vk.py >> /mnt/c/Users/Юрий/finance/vk_newsletter/logs/cron.log 2>&1
   ```

   Adjust paths as needed.

## Usage

### Research step (optional, weekly)

Run the explore agent to fetch recent articles:

```
/agent explore --prompt "Найди 7 последних статей PubMed про эфирные масла (лаванда, мята, эвкалипт) за последние 30 дней, верни список с DOI и короткой аннотацией"
```

Copy the output into `data/sources.md`.

### Generation & publishing

Execute the main script:

```
python src/post_to_vk.py
```

The script will:
- Determine the week parity (odd/even) to alternate between educational and promotional posts.
- Read `data/sources.md` and embed a few citations into the post.
- Render the post using the Jinja2-style template inside `post_to_vk.py`.
- Publish to the VK group defined by `GROUP_ID` using the `VK_TOKEN`.

### Customizing the template

Edit the `template` variable inside `src/post_to_vk.py` or move it to an external file (e.g., `data/template.md`) and load it at runtime.

## How it works

1. **Determine post type** – based on week number (even = educational, odd = promotional).
2. **Load sources** – reads `data/sources.md`.
3. **Generate text** – uses a simple template; for full AI generation, replace the template with a call to the `general-purpose` agent.
4. **Publish** – sends a POST request to `https://api.vk.com/method/wall.post` with parameters `owner_id=-GROUP_ID`, `message=<generated_text>`, `access_token=VK_TOKEN`, `v=5.199`.
5. **Logs** – prints result to console; optionally log to file.

## Requirements

- Python 3.9+
- `requests`
- `python-dotenv`

See `requirements.txt` for exact versions.

## Security

- The `.env` file contains sensitive tokens. It is listed in `.gitignore` to avoid accidental commits.
- Use a VK service token with limited scope (only `wall.post` is needed).
- Regularly rotate your token.

## License

This project is provided for educational purposes. Feel free to adapt and extend it for your own VK automation needs.

## Acknowledgments

- Inspired by the Claude Code course and the Ligа инвесторов community.
- VK API documentation: https://dev.vk.com/method/wall.post