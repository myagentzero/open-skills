---
name: news-summary
version: 1.1.0
author: myagentzero
tags: [news, briefing, rss, current-events, world]
description: Use when asked for news updates, daily briefings, current events, or what's happening in the world. 
---

# News Summary

## Overview

Browse and summarize from international news sources.

## Required Tools
Use the Browser native tool `browser` to open web pages. These sites may be blocked by CORS when accessed via `http_request`, so the browser tool is recommended for reliable access.

### Web search news tool
You can now get news via `web_search_tool` using searxng search with the news category.
For example use query=world & categories=news

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

## Workflow

### Text summary
1. Open websites with browser native `open`
2. Optionally supplement with Reuters, NPR, AP News, and other sites
3. Capture page content with `snapshot` or `get_text`
4. Summarize key stories
5. Group by region or topic

## Example Output Format

📰 News Summary [date]

🌍 HEADLINES
- [headline 1]
- [headline 2]

💼 BUSINESS
- [headline 1]

💻 TECH
- [headline 1]


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
- If site consistently fails to load, update the `news-summary` skill to remove it.
- If a better news source is discovered, add it to the skill with instructions on how to use it.
