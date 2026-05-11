---
name: "gws-calendar"
version: "0.2.0"
author: "myagentzero"
description: "Google Workspace Calendar and Tasks via secondbrain CLI. Use when: (1) reading today's or upcoming agenda, (2) creating a calendar event, (3) syncing shared/Outlook calendars, (4) listing open tasks, or (5) marking a task complete."
tags: ["google-calendar", "google-tasks", "productivity", "calendar", "scheduling", "google-workspace"]
---

# GWS Calendar & Tasks

Read and write Google Calendar events and Google Tasks via the secondbrain CLI. Covers agenda retrieval, event creation, calendar sync from shared/Outlook sources, and task management.

## When to use

- When the user asks "what's on my calendar today / this week"
- When the user wants to schedule or add a new event
- When the user wants to sync shared or Outlook calendars into Google Calendar
- When the user asks "what are my open tasks" or "what do I need to do"
- When the user wants to mark a task as done or complete

## Required tools / Setup

- Node.js 18+
- `secondbrain` project cloned and dependencies installed (`npm install`)
- Working directory: secondbrain project root

Auth is handled automatically via cached OAuth2 token. On first run the app will print an authorization URL and prompt for the returned code.

## Skills

### get_agenda
Fetch today's events from the primary calendar.

```bash
# Today only
gws-calendar agenda

# Next N days (max useful value is ~7)
gws-calendar agenda --days 3
```
### create_event
Create a new event on the primary calendar. Times are in Phoenix time (America/Phoenix, always UTC-7).

```bash
# Title, start, end (required)
gws-calendar add-event "Team standup" "2026-05-12 09:00" "2026-05-12 09:30"

# With optional description
gws-calendar add-event "Lunch with Alex" "2026-05-12 12:00" "2026-05-12 13:00" "Discuss Q3 roadmap"
```

Time format must be `"YYYY-MM-DD HH:MM"` in 24-hour Phoenix time. The CLI parses these as `UTC-7` and passes ISO timestamps to the Google Calendar API. Events are created on `calendarId: 'primary'` with `colorId: '8'` (graphite) for visual identification.

### sync_calendar
Pull events from shared Google calendars and external Outlook ICS feeds into the primary calendar. Deduplicates by title + start time, cancels removed events, and respects `skipEvents` config.

```bash
# Sync 1 day ahead (default)
gws-calendar sync

# Sync up to 4 days ahead (hard cap enforced by sync.js)
gws-calendar sync 4
```

Rate limited to 1500ms between Google Calendar API calls. The sync script enforces `MAX_SYNC_DAYS = 4`.

### list_tasks
List all open (incomplete) Google Tasks with their IDs.

```bash
gws-calendar tasks
```

### complete_task
Mark a task as complete by its ID. Get the ID from `list_tasks` output.

```bash
gws-calendar complete <taskId>
```
## Output format

All CLI commands emit markdown to stdout.

**`agenda`:**
```
# Agenda - Mon May 11, 2026

- 09:00–09:30 | Team standup
- 14:00–15:00 | Project review
- All day | Memorial Day
```

**`add-event`:**
```
# Event Created

**Team standup**
2026-05-12 09:00–09:30
```

**`sync`:**
```
# Calendar Sync

Syncing 1 day(s) ahead...
Done.
```

**`tasks`:**
```
# Open Tasks

- [ ] Fix the login bug `abc123def456`
- [ ] Write Q2 review `xyz789ghi012`
```

**`complete`:**
```
# Task Completed

- [x] Fix the login bug
```

Errors are written to stderr with `Error: <message>` and exit code 1.

## Rate limits / Best practices

- `sync` is rate-limited internally (1500ms between calls) — do not run concurrently
- Do not set `--days` above 7 for `agenda`; Google Calendar returns up to 50 events per call
- The scheduler already runs `sync` hourly on weekdays — avoid double-syncing within the same hour
- Tasks API calls are rate-limited to 500ms between requests internally

## Agent prompt

```text
You have gws-calendar capability via the secondbrain CLI.

To read the agenda:        gws-calendar agenda [--days N]
To create an event:        gws-calendar add-event "<title>" "<YYYY-MM-DD HH:MM>" "<YYYY-MM-DD HH:MM>" ["<description>"]
To sync shared calendars:  gws-calendar sync [N]
To list open tasks:        gws-calendar tasks
To complete a task:        gws-calendar complete <taskId>

All times are America/Phoenix (UTC-7, no DST). Parse any user-provided times into
"YYYY-MM-DD HH:MM" format before passing to add-event.

If the user doesn't specify a duration, default to 1 hour.
If the user asks about "today", use `agenda` with no --days flag.
If the user asks about "this week", use `--days 7`.
Always run `tasks` before `complete` if you don't already have the task ID.
```

## Troubleshooting

**`sync` shows no new events:**
- Events outside the sync window (before today or beyond syncDays) are silently skipped

**`complete <taskId>` returns 404:**
- The task ID is case-sensitive; copy it exactly from `tasks` output (the backtick-quoted value)

