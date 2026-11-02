# Content Management System

**Category:** Web

## Problem

Create a content management system (CMS) like Joomla, Drupal, PHP Nuke etc. Start small. Optional: Allow for the addition of modules/addons.

## Solution

A SQLite `pages` table (slug, title, body, updated) behind a stdlib HTTP server: the public side lists and renders pages, while `/admin` provides create/update/delete forms gated by a token checked on every POST. Page bodies are HTML-escaped and split into paragraphs.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
CMS_TOKEN=secret python3 main.py --port 8001 --db cms.db
python3 main.py --demo
```

## Example

```text
created page: True
updated page: True
bad token status: 403
deleted page status: 404
```
