---
name: vk_newsletter_helper
description: "Helper skill for VK newsletter project: understand structure, start service, make changes, update README, check errors, prepare for publication."
metadata:
  args:
    action:
      type: string
      description: Action to perform (structure, start, change, readme, check, publish)
      default: "structure"
      enum: ["structure", "start", "change", "readme", "check", "publish"]
---

# VK Newsletter Project Helper Skill

This skill helps Claude Code work with the VK newsletter automation repository.

## Usage

Invoke with `/skill vk_newsletter_helper` optionally specifying an action:

- `structure`: Show project structure and key files
- `start`: Attempt to start the service (if applicable)
- `change`: Guide making changes to the codebase
- `readme`: Update README.md with current state
- `check`: Run linting/tests to check for errors
- `publish`: Prepare project for publication (changelog, version bump, etc.)

If no action is provided, defaults to `structure`.

## Implementation Guidance

When invoked, follow these steps based on the selected action:

### structure
1. List the repository root files and directories.
2. Identify key files: README.md, any package.json/requirements.txt, main script, config files.
3. Output a tree-like summary.

### start
1. Check for common startup scripts (npm start, python app.py, etc.).
2. If found, attempt to start the service in the background and report status.
3. If no clear start command, suggest possible commands based on found files.

### change
1. Ask the user what changes they want to make (via clarifying questions).
2. Guide them through making the changes using appropriate tools (Edit, Write, etc.).
3. Confirm changes and suggest next steps.

### readme
1. Read the current README.md.
2. Ask user what updates they want to add (features, usage, etc.).
3. Edit README.md accordingly, preserving existing structure.
4. Show the updated README.

### check
1. Look for linting/test scripts in package.json, requirements.txt, or Makefile.
2. Run those commands and report any errors or warnings.
3. If no scripts, suggest running generic checks (e.g., `npm lint`, `pytest`).

### publish
1. Ensure changes are committed or summarize pending changes.
2. Suggest creating a changelog entry based on recent commits.
3. Recommend version bump (semver) and creating a git tag.
4. Offer to push to remote if configured.

## General Workflow

Regardless of action, always:
- Start by reading the current directory structure.
- Respect user preferences and ask for clarification when ambiguous.
- Use the available tools (Read, Edit, Write, Bash, etc.) to perform tasks.
- Report findings and next steps clearly.
