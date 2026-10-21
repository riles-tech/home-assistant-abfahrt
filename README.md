# Abfahrt Transit for Home Assistant

Real-time public transport departures in Home Assistant. 28 European countries, one integration.

## Features

- Real-time departures for bus, subway, tram, train, ferry
- Delays, cancellations, platform info, occupancy
- 28 European countries
- UI-based setup (no YAML needed)
- Configurable polling interval and search radius
- Direct stop queries via stop IDs

## Installation

### HACS (recommended)

1. In HACS, open the menu (three dots) > Custom repositories, add `https://github.com/riles-tech/home-assistant-abfahrt` with type "Integration"
2. Search for "Abfahrt Transit" and install
3. Restart Home Assistant
4. Go to Settings > Integrations > Add Integration > Abfahrt Transit

### Manual

1. Copy `custom_components/abfahrt/` to your HA `custom_components/` directory
2. Restart Home Assistant
3. Go to Settings > Integrations > Add Integration > Abfahrt Transit

## Configuration

Enter your details in the UI:

| Field | Required | Description |
|-------|----------|-------------|
| API Key | Yes | Your Abfahrt API key (get one at [api.abfahrt.now/home-assistant](https://api.abfahrt.now/home-assistant)) |
| Latitude | Yes | Your location (pre-filled from HA) |
| Longitude | Yes | Your location (pre-filled from HA) |
| Radius | No | Search radius in meters (default: 500) |
| Stop IDs | No | Comma-separated stop IDs for direct queries |
| Update interval | No | Polling interval in seconds (default: 180, minimum: 120; the plan allows 750 requests per day) |

## Sensor

The integration creates a `sensor.abfahrt_departures` entity.

**State:** Number of upcoming departures

**Attributes:**

| Attribute | Description |
|-----------|-------------|
| `departures` | Full list of departure objects |
| `stations` | Nearby stations with IDs and distances |
| `region` | Detected transit region |
| `city` | City name |
| `realtime` | Whether real-time data is available |
| `next_line` | Line of the next departure |
| `next_direction` | Direction of the next departure |
| `next_time` | Time of the next departure |
| `next_delay` | Delay in minutes |

## Lovelace Card Example

```yaml
type: markdown
title: Departures
content: >
  {% set deps = state_attr('sensor.abfahrt_departures', 'departures') %}
  {% set icons = {'subway':'🚇','suburban':'🚈','tram':'🚊','bus':'🚌','ferry':'⛴️','regional':'🚆','express':'🚄'} %}
  {% for d in deps[:12] %}
  {{ icons.get(d.mode, '🚏') }} **{{ d.line }}** → {{ d.direction | truncate(25, True) }} · *{{ d.time }}*{% if d.delay and d.delay > 0 %} +{{ d.delay }}min{% endif %}

  {% endfor %}
```

## Finding Stop IDs

1. Set up the integration with a radius-based search
2. Check `sensor.abfahrt_departures` attributes in Developer Tools > States
3. Look at the `stations` attribute for stop IDs
4. Add the desired stop IDs to your integration config

## Coverage

Germany, UK, France, Spain, Netherlands, Italy, Sweden, Norway, Finland, Denmark, Ireland, Austria, Switzerland, Belgium, Czech Republic, Hungary, Portugal, Poland, Romania, Baltics, and more.

Full list: [api.abfahrt.now/home-assistant](https://api.abfahrt.now/home-assistant#coverage)

## API Documentation

[api.abfahrt.now/docs](https://api.abfahrt.now/docs)

## License

MIT
