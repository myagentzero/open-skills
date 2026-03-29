---
name: news-summary
description: This skill should be used when the user asks for news updates, daily briefings, or what's happening in the world. Browse current events from trusted international RSS feeds and websites.
---

# News Summary

## Overview

Browse and summarize news from trusted international sources via RSS feeds.

## Required Tools
Use the Browser native tool (implemented in `browser`) to open web pages and RSS feeds. These sites may be blocked by CORS when accessed via `http_request`, so the browser tool is recommended for reliable access.

Primary actions for retrieval:
- `open` to navigate to a URL
- `snapshot` to capture page content for parsing/summarization
- `get_text` for targeted extraction when a selector is known

Install:

```bash
pip install feedparser python-dateutil
```

### Aggregators and websites
Google News (topic feed):
https://news.google.com/rss/search?q=world&hl=en-US&gl=US&ceid=US:en

Google news (technology):
https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en

Ground News:
https://ground.news/

Reuters World:
https://www.reuters.com/

AP Top News:
https://apnews.com/tag/apf-topnews

## RSS Feeds and websites

NPR (US perspective):
https://feeds.npr.org/1001/rss.xml

BBC World news:
https://feeds.bbci.co.uk/news/world/rss.xml

BBC Top stories:
https://feeds.bbci.co.uk/news/rss.xml

BBC Business:
https://feeds.bbci.co.uk/news/business/rss.xml

BBC Technology:
https://feeds.bbci.co.uk/news/technology/rss.xml

## Retrieve A Webpage With Browser Native Tool

Use the tool with an `open` action to load a page:

```json
{
  "action": "open",
  "url": "https://apnews.com/tag/apf-topnews"
}
```

Then capture readable content with `snapshot`:

```json
{
  "action": "snapshot",
  "interactive_only": false,
  "compact": true
}
```

If you need targeted text from HTML pages, use `get_text` with a selector:

```json
{
  "action": "get_text",
  "selector": "main"
}
```

Use the returned content to extract headlines and descriptions before summarizing.

## Workflow

### Text summary
1. Open websites with browser native `open`
2. Optionally supplement with Reuters, NPR, AP News, and other sites
3. Capture page content with `snapshot` or `get_text`
4. Summarize key stories
5. Group by region or topic

## Example Output Format

```
📰 News Summary [date]

🌍 HEADLINES
- [headline 1]
- [headline 2]

💼 BUSINESS
- [headline 1]

💻 TECH
- [headline 1]
```

## Best Practices

- Keep summaries concise (5-8 top stories)
- Prioritize breaking news and major events
- Balance perspectives (Western + Global North)
- Links are okay but only only 1 or 2

## Troubleshooting
- Empty results: some feeds may be unavailable; retry and rotate sources.
- Too many duplicates: increase similarity threshold (e.g., 0.35 -> 0.45).
- Under-grouping: decrease threshold (e.g., 0.35 -> 0.28).
- Rate limiting: fetch feeds sequentially with small delays.
