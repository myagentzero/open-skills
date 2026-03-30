---
name: weather-data
version: 1.0.0
author: ZeroClaw
tags: [weather, forecast, open-meteo, wttr, climate]
description: "Get current weather, and forecasts using free Open-Meteo and wttr.in APIs. Use when fetching worldwide weather for a city. For US-specific weather, consider using the weather tool instead."
---

# Weather Data API

## Overview

Get current weather, forecasts, and historical weather data using free APIs. No API keys required.

## Required Tools
Use `http_request` to retrieve weather data from Open-Meteo and wttr.in.

Recommended request defaults:
- Method: `GET`
- Timeout: `10000` ms
- Header: `accept: application/json` (for JSON endpoints)

## Weather data sites

### Get simple weather using wttr.
 `https://wttr.in/PeoriaAZ?format=3&u`
 Response: peoria az: ☀️   +105°F

### Get detailed weather report 
`https://wttr.in/PeoriaAZ?u`

### JSON format
 `https://wttr.in/PeoriaAZ?format=j1&u`
 Response: 
 current_condition[0] | {
  temp_f: .temp_F,
  humidity: .humidity,
  description: .weatherDesc[0].value,
  wind_mph: .windspeedMiles
}


### Get weather by coordinates
`https://wttr.in/40.7128,-74.0060?format=%l:+%C+%t`

## Retrieve weather with http_request

### Open-Meteo current weather (coordinates)

```json
{
   "method": "GET",
   "url": "https://api.open-meteo.com/v1/forecast?latitude=33.5806&longitude=-112.2374&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code&temperature_unit=fahrenheit",
   "headers": {
      "accept": "application/json"
   },
   "timeout_ms": 10000
}
```

Read values from `current`, for example:
- `current.temperature_2m`
- `current.apparent_temperature`
- `current.relative_humidity_2m`
- `current.wind_speed_10m`
- `current.weather_code`

### Open-Meteo daily forecast

```json
{
   "method": "GET",
   "url": "https://api.open-meteo.com/v1/forecast?latitude=33.5806&longitude=-112.2374&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&temperature_unit=fahrenheit&timezone=auto",
   "headers": {
      "accept": "application/json"
   },
   "timeout_ms": 10000
}
```

Read forecast values from the `daily` object arrays (same index per day).

### wttr.in quick current weather (JSON)

```json
{
   "method": "GET",
   "url": "https://wttr.in/PeoriaAZ?format=j1&u",
   "headers": {
      "accept": "application/json"
   },
   "timeout_ms": 10000
}
```

Read values from `current_condition[0]`, for example:
- `temp_F`
- `FeelsLikeF`
- `humidity`
- `windspeedMiles`
- `weatherDesc[0].value`

If the user asks for a plain text one-liner, call wttr.in with `format=3`.

## Output schema

Return weather results in this normalized shape:

```json
{
   "location": "Peoria, AZ",
   "observed_at": "2026-03-20T14:00:00Z",
   "source": "open-meteo",
   "units": "imperial",
   "current": {
      "temp_f": 74,
      "feels_like_f": 72,
      "humidity_pct": 24,
      "wind_mph": 7,
      "condition": "Partly cloudy"
   },
   "forecast": [
      {
         "date": "2026-03-21",
         "temp_max_f": 79,
         "temp_min_f": 58,
         "precip_in": 0.0,
         "condition": "Sunny"
      }
   ]
}
```

Required fields:
- `location`, `source`, `units`, `current`

Optional fields:
- `observed_at`, `forecast`

## Agent prompt

```text
You have access to free weather APIs (Open-Meteo and wttr.in). When you need weather data:

1. For quick weather checks, use wttr.in:
   - Simple: https://wttr.in/{city}?format=3&u
   - JSON: https://wttr.in/{city}?format=j1&u
   - Works with city names or coordinates
   - Use PeoriaAZ for Peoria, AZ or 40.7128,-74.0060 for NYC

2. Weather parameters available:
   - Temperature (current, feels-like, max/min)
   - Humidity, precipitation, wind speed/direction
   - Weather codes (0=clear, 61=rain, 71=snow, 95=thunderstorm)
   - UV index, cloud cover, visibility

3. For current weather and forecasts, use Open-Meteo:
   - Current: https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code
   - Forecast: Add &daily=temperature_2m_max,temperature_2m_min,precipitation_sum
   - Historical: https://archive-api.open-meteo.com/v1/archive


4. Temperature units:
   - Open-Meteo: Add &temperature_unit=fahrenheit (default: celsius)
   - wttr.in: Add &u for imperial units (Fahrenheit, mph)

5. Use the `http_request` tool for all API retrieval:
   - Method: GET
   - Timeout: 10 seconds
   - Prefer JSON endpoints (`accept: application/json`)
   - Parse from `current`/`daily` (Open-Meteo) or `current_condition[0]` (wttr.in)

6. Best practices:
   - Cache weather data for 15-30 minutes
   - Use coordinates for accuracy (get from geocoding)
   - Decode weather codes to human-readable descriptions
   - Set reasonable alert thresholds for monitoring

No API keys required. Unlimited requests within fair use.
```

## Rate limits / Best practices

**wttr.in: 1 Million requests/day** — Community service with fair use and easy to use
**Open-Meteo: 1000 requests/day** — More techncial, but still free and no key required. Use for more detailed data and forecasts.
**Cache weather data** — Weather doesn't change frequently (15-30 min cache)
**Use coordinates** — More accurate than city names
**Set timeouts** — 10-second timeout for weather requests
**Don't poll continuously** — Weather updates hourly, not every second

## Troubleshooting

**Error: "Invalid coordinates"**
- Symptom: API returns error for lat/lon
- Solution: Validate lat ∈ [-90, 90], lon ∈ [-180, 180]

**No data returned:**
- Symptom: API returns empty or null values
- Solution: Check if location has weather station coverage; try nearby coordinates

**Historical data missing:**
- Symptom: Archive API returns no data for date range
- Solution: Open-Meteo archive starts from 1940; check date format is YYYY-MM-DD

**Weather code not recognized:**
- Symptom: Unknown weather code number
- Solution: Refer to WMO weather code standard; codes 0-99 are defined

**wttr.in returns HTML instead of JSON:**
- Symptom: Response is HTML page
- Solution: Ensure you add ?format=j1 to get JSON response

**Temperature unit confusion:**
- Symptom: Unexpected temperature values
- Solution: Open-Meteo defaults to Celsius; add &temperature_unit=fahrenheit if needed
